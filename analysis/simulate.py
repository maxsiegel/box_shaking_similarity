import pandas as pd
import seaborn as sns
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

n_kids = 10
n_trials = 8

def success_fun(disc, age):
    return 1 / (1 + np.exp(-age * disc / 3))

ages = np.arange(3, 7, 1)
disc_values = np.linspace(.5, 2, n_trials)



def simulate_parameters(n_kids, n_trials):

    data = pd.DataFrame({'kid': [],
                         'age': [],
                         'outcome': [],
                         'disc': [],
                         'prob_success': []})

    for age in ages:
        for kid in range(n_kids):
            for trial in range(n_trials):
                disc = disc_values[trial]
                prob_success = success_fun(disc, age)
                outcome = np.random.binomial(1, prob_success)

                # apparently we have to do it this way since data.append was removed
                data.loc[len(data.index)] = [kid, age, outcome, disc, prob_success]


    sns.barplot(x='age', y='outcome', data=data)
    plt.show()
    model = sm.formula.ols('outcome ~ age', data=data).fit()
    p = model.pvalues.age
    return p

p = simulate_parameters(10, 8)
