from multiprocessing import freeze_support
import sys
from fw_ddsm.iteration import *
from fw_ddsm.output import *
from pandas import DataFrame

algorithms = dict()
algorithms[m_minizinc] = dict()
algorithms[m_minizinc][m_before_fw] = m_minizinc
algorithms[m_minizinc][m_after_fw] = f"{m_minizinc}_fw"
algorithms[m_ogsa] = dict()
algorithms[m_ogsa][m_before_fw] = m_ogsa
algorithms[m_ogsa][m_after_fw] = f"{m_ogsa}_fw"

# penalty_weight_range = [0, 5, 50, 500, 5000, 50000]
# num_tasks_dependent_range = [0, 3, 5]
num_households_range = [20]
penalty_weight_range = [1]
num_tasks_dependent_range = [2]
num_full_flex_tasks = 5
num_semi_flex_tasks = 0
num_fixed_tasks = 0
num_samples = 5
num_repeat = 1
name_exp = "test_monarch"
id_job = 2
cpus_nums = cpu_count()


def main(num_households, num_tasks_dependent, penalty_weight, num_cpus=None, experiment_name=None, job_id=0):
    experiment_tracker = dict()
    num_experiment = -1
    out = Output(output_root_folder="results", output_parent_folder=experiment_name)

    print("----------------------------------------")
    print(f"{num_households} households, "
          f"{num_tasks_dependent} dependent tasks, "
          f"{num_full_flex_tasks} fully flexible tasks, "
          f"{num_semi_flex_tasks} semi-flexible tasks, "
          f"{num_fixed_tasks} fixed tasks, "
          f"{penalty_weight} penalty weight. ")
    print("----------------------------------------")

    new_iteration = Iteration()
    output_folder, output_parent_folder, this_date_time \
        = out.new_output_folder(num_households=num_households,
                                num_dependent_tasks=num_tasks_dependent,
                                num_full_flex_task_min=num_full_flex_tasks,
                                num_semi_flex_task_min=num_semi_flex_tasks,
                                inconvenience_cost_weight=penalty_weight,
                                folder_id=job_id)
    plots_demand_layout = []
    plots_demand_finalised_layout = []
    new_data = True
    for alg in algorithms.values():
        num_experiment += 1
        experiment_tracker[num_experiment] = dict()
        experiment_tracker[num_experiment][k_households_no] = num_households
        experiment_tracker[num_experiment][k_penalty_weight] = penalty_weight
        experiment_tracker[num_experiment][k_dependent_tasks_no] = num_tasks_dependent
        experiment_tracker[num_experiment][h_tasks_no_ff_min] = num_full_flex_tasks
        experiment_tracker[num_experiment][h_tasks_no_sf_min] = num_semi_flex_tasks
        experiment_tracker[num_experiment][h_tasks_no_fixed_min] = num_fixed_tasks
        experiment_tracker[num_experiment][m_algorithm] = alg[m_after_fw]
        experiment_tracker[num_experiment]["id"] = job_id

        # 1. iteration data
        if new_data:
            preferred_demand_profile, prices = \
                new_iteration.new(algorithm=alg, num_households=num_households,
                                  max_demand_multiplier=maxium_demand_multiplier,
                                  num_tasks_dependent=num_tasks_dependent,
                                  full_flex_task_min=num_full_flex_tasks, full_flex_task_max=0,
                                  semi_flex_task_min=num_semi_flex_tasks, semi_flex_task_max=0,
                                  fixed_task_min=num_fixed_tasks, fixed_task_max=0,
                                  inconvenience_cost_weight=penalty_weight,
                                  max_care_factor=care_f_max,
                                  data_folder=output_parent_folder,
                                  date_time=this_date_time)
            new_data = False
        else:
            preferred_demand_profile, prices = \
                new_iteration.read(algorithm=alg, inconvenience_cost_weight=penalty_weight,
                                   num_dependent_tasks=num_tasks_dependent,
                                   read_from_folder=output_parent_folder,
                                   date_time=this_date_time)

        # 2. iteration begins
        start_time_probability = new_iteration.begin_iteration(starting_prices=prices, num_cpus=num_cpus)

        # 3. finalising schedules
        new_iteration.finalise_schedules(num_samples=num_samples,
                                         start_time_probability=start_time_probability)

        # 4. preparing plots and writing results to CSVs
        plots_demand, plots_demand_finalised, overview_dict \
            = out.save_to_output_folder(algorithm=alg,
                                        aggregator_tracker=new_iteration.aggregator.tracker,
                                        aggregator_final=new_iteration.aggregator.final,
                                        community_tracker=new_iteration.community.tracker,
                                        community_final=new_iteration.community.final)
        plots_demand_layout.append(plots_demand)
        plots_demand_finalised_layout.append(plots_demand_finalised)
        experiment_tracker[num_experiment].update(overview_dict)

    # 6. drawing all plots
    output_file(f"{output_folder}{this_date_time}_plots.html")
    tab1 = Panel(child=layout(plots_demand_layout), title="FW-DDSM results")
    tab2 = Panel(child=layout(plots_demand_finalised_layout), title="Actual schedules")
    save(Tabs(tabs=[tab2, tab1]))

    # 5. writing experiment overview
    DataFrame.from_dict(experiment_tracker).transpose() \
        .to_csv(r"{}{}_overview.csv".format(output_parent_folder, this_date_time))
    with open(f"{out.output_parent_folder}data/{this_date_time}_{file_experiment_pkl}",
              'wb+') as f:
        pickle.dump(experiment_tracker, f, pickle.HIGHEST_PROTOCOL)
    print("----------------------------------------")

    print("----------------------------------------")
    print("Experiment is finished. ")
    print(experiment_tracker)


if __name__ == '__main__':
    freeze_support()
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        arg = int(arg)
        if i == 1:
            id_job = arg
        elif i == 2:
            cpus_nums = arg
        elif i == 3:
            num_households_range = [arg]
        elif i == 4:
            penalty_weight_range = [arg]
        elif i == 5:
            num_tasks_dependent_range = [arg]
        print(f"Argument {i:>6}: {arg}")

    for h in num_households_range:
        for w in penalty_weight_range:
            for dt in num_tasks_dependent_range:
                main(num_households=h,
                     num_tasks_dependent=dt,
                     penalty_weight=w,
                     experiment_name=name_exp,
                     num_cpus=cpus_nums,
                     job_id=id_job)
