import numpy as np
import pandas as pd
from seeds import known_seeds
from utils import save_solution, load_solution, load_problem_data
from evaluation import evaluation_function, get_actual_demand


def get_my_solution(d):
    fleet = pd.DataFrame()
    pricing_strategy = pd.DataFrame()

    print(d)

    filtered_demand = d[d['server_generation'] == 'CPU.S1']  # Filter for CPU.S1
    filtered_demand = filtered_demand.set_index('time_step')['high']  # Set time_step as index and select the 'high' column

    print(filtered_demand)
    print(type(filtered_demand))

    for index, row in filtered_demand.iterrows():
        print(index, row)

    return fleet, pricing_strategy


seeds = known_seeds()
demand = pd.read_csv('./data/demand.csv')


# GET SOLUTIONS
for seed in seeds:
    # SET THE RANDOM SEED
    np.random.seed(seed)

    # GET THE DEMAND
    actual_demand = get_actual_demand(demand)

    # CALL YOUR APPROACH HERE
    fleet, pricing_strategy = get_my_solution(actual_demand)

    # SAVE YOUR SOLUTION
    save_solution(fleet, pricing_strategy, f'./output/{seed}.json')

    break


# EVALUATE SOLUTIONS
for seed in seeds:
    # SET THE RANDOM SEED
    np.random.seed(seed)

    # LOAD SOLUTION
    fleet, pricing_strategy = load_solution(f'./output/{seed}.json')

    # LOAD PROBLEM DATA
    demand, datacenters, servers, selling_prices, elasticity = load_problem_data()

    # EVALUATE THE SOLUTION
    score = evaluation_function(fleet,
                                pricing_strategy,
                                demand,
                                datacenters,
                                servers,
                                selling_prices,
                                elasticity,
                                seed=seed)

    print(f'Solution score: {score}')

    break
