import pickle

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import zscore

with open('dists_no_mod_power.pkl', 'rb') as f:
    x = pickle.load(f)


# m = np.mean(list(y.values()))
# s = np.std(list(y.values()))

# dists = {key: (float(val) - m) / s for key, val in y.items()}
# dists2 = dict(zip(dists.keys(), zscore(list(dists.values()))))
dists = dict(zip(x.keys(), abs(zscore(list(x.values())))))
dists = dict(reversed(sorted(x.items(), key = lambda x: x[1])))

x = list(dists.keys())
x = [e[0] + " v " + e[1] for e in x]
y = list(dists.values())

f = plt.figure(figsize=(35, 35))

plt.barh(x, y, tick_label=x)

plt.savefig('no_mod_power.png')
plt.show()
