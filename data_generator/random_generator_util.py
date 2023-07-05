"""
Make classification experiments
"""


from src.SimulationsPO import BipartyDT
from DT_simulation import Simulations
import multiprocessing
import numpy as np
import getopt, sys
from sklearn.datasets import make_blobs
from sklearn.svm import SVR
from functools import partial
from custom_regressors import MeanRegressor, RandomRegressor, ClusterRegressor, CRFRegressor, MLP_Model
from numpy import random
import pandas as pd
import logging
import time
#from PlotResults import PlotResults
n_samples = 2000
seed = 0

def multiprocessing_simulations(tree_population_ids):

    tree_id= tree_population_ids[0]
    sample_id = tree_population_ids[1]
    simulation = tree_population_ids[2]
    height = tree_population_ids[3]
    leaves, leaf_names = simulation.get_leaves()
    #for sample_id in range(simulation_setting_dict['number_population_samples']):
    print('leaves = ',len(leaves))
    # rng = np.random.default_rng()
    # X = rng.integers(low=1,high=12,size=(n_samples,len(leaves)))

    sigma = 1
    mu = 6
    #X = sigma * np.random.randn(n_samples, len(leaves)) + mu
    X = []
    for i in range(n_samples):
        rnd = random.uniform(low=1, high=11, size=len(leaves))
        rnd = np.rint(rnd)
        X.append(rnd)

    min_value = np.min(X)
    max_value = np.max(X)
    # print(min_value)
    # print(max_value)
    synth_data_df = pd.DataFrame(X, columns=leaf_names)
    synth_data_df.insert(0, 'id', 0, allow_duplicates=True)
    # print(synth_data_df)
    synth_data_df.to_csv(f"datasets_random/tree_{tree_id}_population_{sample_id}.csv", index=False)


if __name__ == '__main__':
    # Keep all but the first

    sklearn_jobs = 1
    use_pool_multiproc = False
    # ML models for utility learning
    tree_number = 10
    number_population_samples = 10
    create_tree = False
    tree_population_ids_list = []

    for tree_id in range(tree_number):
        # load tree
        bdt = BipartyDT()
        bdt.load_tree(tree_id, folder='../data/DT')
        #print(bdt.get_tree_height())
        # create object
        # append tree information
        for sample_id in range(number_population_samples):
            tree_population_ids_list.append((tree_id, sample_id, bdt, bdt.get_tree_height()))

    print('pop ids = ',tree_population_ids_list)
    final_results = []

    for el in tree_population_ids_list:
        final_results.append(multiprocessing_simulations(el))

