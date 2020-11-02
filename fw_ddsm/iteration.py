from fw_ddsm.community import *
from fw_ddsm.aggregator import *


class Iteration:

    def __init__(self):
        self.scheduling_method = ""
        self.pricing_method = ""
        self.num_households = 0
        self.num_iteration = 0
        self.num_intervals = 0

        self.community = Community()
        self.aggregator = Aggregator()
        self.data_folder = "test_data/"

    def new(self, algorithm, num_households,
            file_task_power=file_demand_list, max_demand_multiplier=maxium_demand_multiplier,
            file_normalised_pricing_table=file_pricing_table, file_preferred_demand_profile=file_pdp,
            num_tasks_dependent=no_tasks_dependent,
            full_flex_task_min=no_full_flex_tasks_min, full_flex_task_max=0,
            semi_flex_task_min=no_semi_flex_tasks_min, semi_flex_task_max=0,
            fixed_task_min=no_fixed_tasks_min, fixed_task_max=0,
            inconvenience_cost_weight=care_f_weight, max_care_factor=care_f_max,
            data_folder=None):
        self.scheduling_method = algorithm[k2_before_fw]
        self.pricing_method = algorithm[k2_after_fw]

        self.num_households = num_households

        if data_folder is not None:
            self.data_folder = data_folder if data_folder.endswith("/") else data_folder + "/"

        # 1. generate new households, trackers and a pricing table
        self.community.new(num_households=self.num_households,
                           scheduling_method=self.scheduling_method,
                           file_preferred_demand_profile_path=file_preferred_demand_profile,
                           file_demand_list_path=file_task_power,
                           write_to_file_path=self.data_folder,
                           max_demand_multiplier=max_demand_multiplier,
                           num_tasks_dependent=num_tasks_dependent,
                           full_flex_task_min=full_flex_task_min, full_flex_task_max=full_flex_task_max,
                           semi_flex_task_min=semi_flex_task_min, semi_flex_task_max=semi_flex_task_max,
                           fixed_task_min=fixed_task_min, fixed_task_max=fixed_task_max,
                           inconvenience_cost_weight=inconvenience_cost_weight, max_care_factor=max_care_factor)

        self.aggregator.new(normalised_pricing_table_csv=file_normalised_pricing_table,
                            aggregate_preferred_demand_profile=self.community.preferred_demand_profile,
                            pricing_method=self.pricing_method, write_to_file_path=self.data_folder)

        print("Households and the aggregator are created. ")

    def read_data(self, algorithm, read_from_folder="test2"):
        self.scheduling_method = algorithm[k2_before_fw]
        self.pricing_method = algorithm[k2_after_fw]
        self.community = Community()
        self.community.read(read_from_folder=read_from_folder, scheduling_method=self.scheduling_method)
        self.aggregator = Aggregator()
        self.aggregator.read(read_from_folder=read_from_folder, pricing_method=self.pricing_method)

        print("Households and the aggregator are read. ")

    def begin_iteration(self, algorithm):
        scheduling_method = self.scheduling_method
        pricing_method = self.pricing_method

        # aggregator, k = 0
        aggregator_demand_profile = self.aggregator.aggregator_tracker.data[pricing_method][k0_demand][0]
        prices, consumption_cost, inconvenience, step, new_aggregate_demand_profile, time_pricing \
            = self.aggregator.pricing(num_iteration=0,
                                      aggregate_demand_profile=aggregator_demand_profile,
                                      aggregate_inconvenience=0)

        num_iteration = 1
        while step > 0:
            aggregate_demand_profile, total_inconvenience, time_scheduling_iteration \
                = self.community.schedule(num_iteration=num_iteration, prices=prices,
                                          scheduling_method=scheduling_method)
            prices, consumption_cost, inconvenience, step, new_aggregate_demand_profile, time_pricing \
                = self.aggregator.pricing(num_iteration=num_iteration,
                                          aggregate_demand_profile=aggregate_demand_profile,
                                          aggregate_inconvenience=total_inconvenience)
            num_iteration += 1

        print(f"Converged in {num_iteration - 1}")
        self.aggregator.compute_start_time_probabilities(pricing_method)

    def finalise_schedules(self, algorithm):
        scheduling_method = algorithm[k2_before_fw]
        pricing_method = algorithm[k2_after_fw]

        start_time_probability_distribution = self.aggregator.start_time_probability
        final_aggregate_demand_profile, final_total_inconvenience \
            = self.community.decide_final_schedules(scheduling_method=scheduling_method,
                                                    probability_distribution=start_time_probability_distribution)

        final_prices, final_consumption_cost = self.aggregator.__prices_and_cost(final_aggregate_demand_profile)
        self.aggregator.update(num_iteration=None, final=True, pricing_method=pricing_method,
                               demands=final_aggregate_demand_profile, prices=final_prices,
                               consumption_cost=final_consumption_cost, inconvenience_cost=final_total_inconvenience)

        print(self.aggregator.aggregator[pricing_method][k0_final][k0_demand])
        print(final_prices)
        print(f"Preferred cost is {self.aggregator.aggregator[pricing_method][k0_cost][0]}, "
              f"PAR is {self.aggregator.aggregator[pricing_method][k0_par][0]}")
        print(f"Final cost is {final_consumption_cost}, "
              f"PAR is {self.aggregator.aggregator[pricing_method][k0_final][k0_par]} and "
              f"inconvenience is {final_total_inconvenience}.")

        return final_aggregate_demand_profile, final_total_inconvenience
