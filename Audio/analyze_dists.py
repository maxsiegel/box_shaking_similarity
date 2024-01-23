import os
import pickle
from itertools import combinations
from os.path import join

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import loadmat
from scipy.spatial.distance import mahalanobis
from scipy.stats import zscore

# with open('dists_no_mod_power.pkl', 'rb') as f:
#     x = pickle.load(f)

to_compare = ['env_mean',
              'env_var',
              'env_skew',
              'env_C',
              'mod_power'
              ]

stat_folder = 'stats'

design = []                     # n x p matrix of sounds x features
sound_feats = {}
for file_name in os.listdir(stat_folder):

    stats_mat = loadmat(join(stat_folder, file_name))

    current_sound_feats = np.array([])
    for i, stat in enumerate(to_compare):
        # this is necessary because I saved matfiles with differing variable names
        val = list(stats_mat.keys())[-1]
        # weird arrays so seems like i have to do it this way
        current_sound_feats = np.hstack((current_sound_feats, stats_mat[val][0][0][i].flatten()))

    design.append(current_sound_feats)
    sound_feats[file_name.strip('.mat')] = current_sound_feats



cov = np.cov(np.array(design).T)
inv_cov = np.linalg.inv(cov)

dists = {}

pairs = combinations(sound_feats, 2)
for x, y in pairs:
    dists[x, y] = mahalanobis(sound_feats[x], sound_feats[y], inv_cov)

# m = np.mean(list(y.values()))
# s = np.std(list(y.values()))
# """
# dists = dict(zip(x.keys(), abs(zscore(list(x.values())))))
dists = {k: dists[k] for k in dists if not np.isnan(dists[k])}
dists = dict(reversed(sorted(dists.items(), key = lambda x: x[1])))


x = list(dists.keys())
x = [e[0] + " v " + e[1] for e in x]
y = list(dists.values())

f = plt.figure(figsize=(35, 35))

plt.barh(x, y, tick_label=x)

plt.savefig('mahalanobis.png')
plt.show()
# """
