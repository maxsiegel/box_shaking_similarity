import os
import subprocess as sp
from itertools import combinations
from multiprocessing import Pool
from os.path import join

import numpy as np


def convert_16bit_to_float(wav):
    assert wav.dtype == 'int16', 'needs a numpy array of int16s'
    wav = wav / float(np.iinfo(wav.dtype).max)
    return wav

def get_texture_stat_distance(wav1, wav2, fname):
    # try:

    err = 'dbstop if error'
    # err = ''
    path = os.getcwd()
    matlab_call = f"cd('{path}'); {err}; pairwise_compare_stats('{wav1}', '{wav2}', '{fname}')"
    call = ['matlab',
            '-singleCompThread',
            '-nodesktop',
            '-nojvm',
            '-sd', get_base_path(),
            '-r',
            matlab_call.format(wav1=wav1,
                                                                           wav2=wav2,
                                                                           fname=fname)]

    print(' '.join(call))
    sp.check_call(call)

    with open(fname, 'r') as f:
        val = float(f.readline())

    try:
        os.unlink(fname)
    except:
        print("removing temp file " + fname + " didn't work")

    return wav1, wav2, val

def texture_features_similarity(sound1, sound2, sr=44100):
    return get_texture_stat_distance(sound1, sound2, 'tempor')

def get_base_path():
    """
    Returns the directory of the source file, usually wherever this package is placed.
    """
    return os.path.dirname(os.path.realpath(__file__))
def get_base_path():
    return  '/Users/maxs/object_sounds_discriminability/Stims-Vivian-V3-UpDown'

def extract_num(fn):
    fn = str(fn)
    return fn.split('/')[-1][:-4]

def main():

    # files = [join(get_base_path(), f) for f in os.listdir(get_base_path()) if f.endswith('m4a')]
    stim_dir = '/Users/maxs/object_sounds_discriminability/Stims-Vivian-V3-UpDown'
    files = [join(stim_dir, f) for f in os.listdir(stim_dir) if f.endswith('wav')]
    pairs = list(combinations(files, 2))

    todo = []
    dists = {}

    for i, j in pairs:
        x = i, j, "temp_" + extract_num(i) + '_' + extract_num(j)
        todo.append(x)



    with Pool(8) as p:
        out = p.starmap(get_texture_stat_distance, todo)

    # from itertools import starmap
    # out = starmap(get_texture_stat_distance, todo)
    # print(todo[0])
    # import pdb; pdb.set_trace()

    dists = {(extract_num(i), extract_num(j)): k for i, j, k in out}

    import pickle
    with open('dists.pkl', 'wb') as f:
        pickle.dump(dists, f)


if __name__ == '__main__':
    main()
