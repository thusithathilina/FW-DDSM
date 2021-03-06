# time related parameters
no_intervals = 144
no_periods = 48
no_intervals_periods = int(no_intervals / no_periods)
time_out = 10

# household related parameters
# new_households = True
create_new_households = False
no_households = 10
no_full_flex_tasks_min = 5
no_full_flex_tasks_max = 8
no_semi_flex_tasks_min = 0
no_semi_flex_tasks_max = 0
no_fixed_tasks_min = 0
no_tasks_dependent = 2
maxium_demand_multiplier = no_full_flex_tasks_min + no_semi_flex_tasks_min + no_fixed_tasks_min
care_f_max = 10
care_f_weight = 1

# pricing related parameters
pricing_table_weight = 1
# cost_function_type = "linear"
cost_function_type = "piece-wise"


# solver related parameters
variable_selection = "smallest"
value_choice = "indomain_min"
model_type = "pre"
solver_type = "cp"
solver_name = "gecode"

# external file related parameters
parent_folder = ""
file_cp_pre = parent_folder + 'data/Household-cp-pre.mzn'
file_cp_ini = parent_folder + 'data/Household-cp.mzn'
file_pricing_table = parent_folder + 'data/pricing_table_0.csv'
file_household_area_folder = parent_folder + 'data/'
file_pdp = parent_folder + 'data/probability.csv'
file_demand_list = parent_folder + 'data/demands_list.csv'
result_folder = parent_folder + "results/"
file_community_pkl = "community.pkl"
file_community_meta_pkl = "community_aggregate.pkl"
file_aggregator_pkl = "aggregator.pkl"
file_pricing_table_pkl = "pricing_table.pkl"
file_experiment_pkl = "experiment.pkl"

# summary related parameters
k_area = "area"
k_penalty_weight = "penalty_weight"
k_households_no = "no_households"
k_tasks_no = "no_tasks"
k_cost_type = "cost_function_type"
k_iteration_no = "no_iterations"
k_dependent_tasks_no = "no_dependent_tasks"

# household dictionary keys
h_key = "key"
h_psts = "preferred_starts"
h_ests = "earliest_starts"
h_lfs = "latest_finishes"
h_durs = "durations"
h_powers = "powers"
h_cfs = "care_factors"
h_max_cf = "maximum_care_factor"
h_no_precs = "no_precedences"
h_precs = "precedents"
h_succ_delay = "succeeding_delays"
h_demand_limit = "maximum_demand"
h_incon_weight = "inconvenience_cost_weight"
h_tasks_no_ff_min = "no_fully_flexible_tasks_min"
h_tasks_no_ff_max = "no_fully_flexible_tasks_max"
h_tasks_no_sf_min = "no_semi_flexible_tasks_min"
h_tasks_no_sf_max = "no_semi_flexible_tasks_max"
h_tasks_no_fixed_min = "no_fixed_tasks_min"
h_tasks_no_fixed_max = "no_fixed_tasks_max"

# demand related parameters
k_household_key = "key"
s_starts = "start_times"
s_demand = "demands"
s_demand_max = "max_demand"
s_demand_max_init = "init_max_demand"
s_demand_reduction = "demand_reduction"
s_demand_total = "total_demand"
s_par = "PAR"
s_par_init = "init_PAR"
s_final = "final"
s_penalty = "inconvenient"
s_obj = "objective"

# step size
p_step = "step_size"

# pricing related parameters
p_cost = "cost"
p_cost_reduction = "cost_reduction"
p_prices = "prices"
p_price_levels = "price_levels"
p_demand_table = "demand_levels"

# run time related
t_time = "run_time"
t_scheduling = "rescheduling_time"
t_pricing = "pricing_time"
t_average = "average_run_time"

# k1_interval = "interval"
# k1_period = "period"
m_algorithm = "algorithm"
m_minizinc = "minizinc"
m_ogsa = "ogsa"
m_before_fw = "scheduling"
m_after_fw = "pricing"

# tracking-related
k_tracker = "tracker"
k_others = "others"
algorithms = dict()
algorithms[m_minizinc] = dict()
algorithms[m_minizinc][m_before_fw] = m_minizinc
algorithms[m_minizinc][m_after_fw] = f"{m_minizinc}_fw"
algorithms[m_ogsa] = dict()
algorithms[m_ogsa][m_before_fw] = m_ogsa
algorithms[m_ogsa][m_after_fw] = f"{m_ogsa}_fw"

algorithm_full_names = dict()
algorithm_full_names[algorithms[m_minizinc][m_before_fw]] = "MiniZinc model with data preprocessing"
algorithm_full_names[algorithms[m_minizinc][m_after_fw]] = "FW-DDSM with MiniZinc model and data preprocessing"
algorithm_full_names[algorithms[m_ogsa][m_before_fw]] = "OGSA"
algorithm_full_names[algorithms[m_ogsa][m_after_fw]] = "FW-DDSM with OGSA"




