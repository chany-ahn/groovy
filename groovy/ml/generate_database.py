import os
import shutil
import pickle
from itertools import product
from contextlib import suppress
from multiprocessing import Pool
import sys; sys.path.insert(0, "../..")

import numpy as np

import groovy.pde

# Create directory to store all the data
folder = 'bigger_database'
with suppress(FileNotFoundError):
    shutil.rmtree(folder)
os.mkdir(folder)

# Create a parameter grid
size = 12
ru_grid = np.linspace(0.7, 0.9, size)
rv_grid = np.linspace(0.1, 0.3, size)
f_grid  = np.linspace(0.034, 0.046, size)
k_grid  = np.linspace(0.061, 0.065, size)

# Run all the simulations
frame_t0 = groovy.pde.initialframe((100, 100), conctype='clump')
combinations = list(product([frame_t0], ru_grid, rv_grid, f_grid, k_grid))

# Create the function
def make_data(frame_t0, ru, rv, f, k):
    time_array = groovy.pde.evolve(frame_t0, ru, rv, f, k, boundary='wrap')
    final_frame = time_array[:,:,-1,:]

    # Pickle the results
    with open(f"{folder}/{ru}_{rv}_{f}_{k}.pkl", 'wb') as f:
        pickle.dump(final_frame, f)

# Multiprocess
with Pool(10) as p:
    p.starmap(make_data, combinations)

