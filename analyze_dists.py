import pickle
import numpy as np
import matplotlib.pyplot as plt

with open('dists.pkl', 'rb') as f:
    x = pickle.load(f)

y = dict(reversed(sorted(x.items(), key = lambda x: x[1])))

m = np.mean(list(y.values()))
s = np.std(list(y.values()))

dists = {key: (float(val) - m) / s for key, val in y.items()}
