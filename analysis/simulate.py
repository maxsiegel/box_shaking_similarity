import pandas as pd
import numpy as np
import statsmodels.api as sm

def success_fun(disc, age):
    return 1 / (1 + np.exp(-age * disc / 3))

def simulate_parameters(n_kids, n_trials, ages, disc_values):
    data_list = []
    for age in ages:
        for kid in range(n_kids):
            for trial in range(n_trials):
                disc = disc_values[trial]
                prob_success = success_fun(disc, age)
                outcome = np.random.binomial(1, prob_success)
                data_list.append([kid, age, outcome, disc, prob_success])

    data = pd.DataFrame(data_list, columns=['kid', 'age', 'outcome', 'disc', 'prob_success'])
    model = sm.formula.ols('outcome ~ age', data=data).fit()
    p = model.pvalues.age
    return p

def find_parameters(n_simulations, n_kids_range, n_trials_range):
    ages = np.arange(3, 7, 9)
    disc_values = np.linspace(.5, 2, max(n_trials_range))  # Set to the max of n_trials_range
    successful_configs = []

    for n_kids in n_kids_range:
        for n_trials in n_trials_range:
            successful_simulations = 0
            for _ in range(n_simulations):
                p_value = simulate_parameters(n_kids, n_trials, ages, disc_values[:n_trials])
                if p_value < 0.05:
                    successful_simulations += 1

            success_rate = successful_simulations / n_simulations
            if success_rate >= 0.95:
                successful_configs.append((n_kids, n_trials))

    return successful_configs

# Define the ranges for n_kids


# Set the number of simulations, kids, and trials here
# n_simulations = 100  # Number of simulations to run
# n_kids = 10  # Number of kids
# n_trials = 8  # Number of trials

# # Run the simulation loop
# is_successful = find_parameters(n_simulations, n_kids, n_trials)
# print(f"Success in achieving p-value < 0.05 in 95% of simulations: {is_successful}")


n_simulations = 100 # Number of simulations to run for each configuration
n_kids_range = range(5, 16, 2) # For example, kids from 5 to 15, stepping by 2
n_trials_range = range(4, 12, 2) # For example, trials from 4 to 12, stepping by 2

successful_configs = find_parameters(n_simulations, n_kids_range, n_trials_range)
for config in successful_configs:
    print(f"Successful configuration: n_kids = {config[0]}, n_trials = {config[1]}")
