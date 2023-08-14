"""
Make classification experiments
"""
#from keras.wrappers.scikit_learn import KerasRegressor

from src.SimulationsPO import BipartyDT
from DT_simulation import Simulations
import multiprocessing
#from sklearn.neural_network import MLPRegressor
#from multiprocessing import Process
#import os
import numpy as np
import getopt, sys
from sklearn.datasets import make_blobs
#import matplotlib.pyplot as plt
#from sklearn.cluster import KMeans
#from sklearn.model_selection import train_test_split
#from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVR
#from sklearn.tree import DecisionTreeClassifier
#from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingRegressor
# from utils import plot_mae
from functools import partial
from custom_regressors import MeanRegressor, RandomRegressor, ClusterRegressor, CRFRegressor, MLP_Model
#import math
import random
#import json
#import pdb
#from sklearn.multioutput import MultiOutputRegressor
#from sklearn.metrics import mean_absolute_error, accuracy_score, fowlkes_mallows_score
#from sklearn.model_selection import KFold
import pandas as pd
import logging
import time
#from PlotResults import PlotResults
n_samples = 2000
seed = 0

def multiprocessing_simulations(simulation_setting_dict, tree_population_ids, seed=1):
    results = {"Tree id": [], "Tree height": [], "Tree leaves": [], "Sample id": [], "Cluster score": [], "Min Lickert value": [], "Max Lickert value": [],
    "Sample clusters": [], "Model": [], "Accuracy": [], "Accuracy std": [], "Mae Prop": [],
    "Mae Prop std": [], "Mae Opp": [], "Mae Opp std": [], "Mean arg distance": [], "Mean arg distance std": []}


    #mae_node_id = {model[0]: {'mae_cv': [], 'std_mae_cv': []} for model in  simulation_setting_dict['models']}
    #mae_Q_proponent = {model[0]: {'mae_cv': [], 'std_mae_cv': []} for model in  simulation_setting_dict['models']}
    #mae_Q_opponent = {model[0]: {'mae_cv': [], 'std_mae_cv': []} for model in  simulation_setting_dict['models']}
    #mean_args_distance = {model[0]: {'mae_cv': [], 'std_mae_cv': []} for model in  simulation_setting_dict['models']}

    tree_id= tree_population_ids[0]
    sample_id = tree_population_ids[1]
    simulation = tree_population_ids[2]
    height = tree_population_ids[3]
    leaves, leaf_names = simulation.get_leaves()


    #for sample_id in range(simulation_setting_dict['number_population_samples']):
    # Random data generation
    #random.seed(seed)
    num_clusters = random.choice(simulation_setting_dict['clusters'])
    # print(f'num_clusters {num_clusters}')
    # random.seed(seed)
    center_box_width = random.choice(simulation_setting_dict['center_box_width'])
    print(f'center_box_width {center_box_width}')
    # random.seed(seed)
    #num_clusters = 4
    #center_box_width = 2
    radius = 0
    box_init = center_box_width - radius
    box_end = center_box_width + radius

    # box_init = 2
    # box_end = 11

    # if box_init <= 0:
    #     box_init = 2
    #     # box_end+= 1
    # if box_end >= 13:
    #     box_end = 12

    box_init = 3
    box_end = 9

    X, y = make_blobs(n_samples=n_samples, centers=num_clusters, n_features=len(leaves), shuffle=True, cluster_std=0.5, center_box=(box_init,box_end))
    X = np.rint(X)

    min_value = np.min(X)
    max_value = np.max(X)
    print(min_value)
    print(max_value)
    synth_data_df = pd.DataFrame(X, columns=leaf_names)
    synth_data_df.insert(0, 'id', y, allow_duplicates=True)
    # print(synth_data_df)
    synth_data_df.to_csv(f"datasets/tree_{tree_id}_population_{sample_id}.csv", index=False)
    X = synth_data_df.values

    # Check cluster difficulty

    return results


if __name__ == '__main__':
    # Keep all but the first
    argument_list = sys.argv[1:]

    try:
        arguments, values = getopt.getopt(argument_list, "p:", ["parallel"])
    except getopt.error as err:
        # Output error, and return with an error code
        print(str(err))
        sys.exit(2)

    for opt, arg in arguments:
        if opt == '-p':
            use_pool_multiproc = True if arg == 'True' else False
            sklearn_jobs = 1 if arg == 'True' else -1

    sklearn_jobs = 1
    use_pool_multiproc = False
    # ML models for utility learning
    models = [('SuppVecMachTuned', SVR(C=0.5, gamma='auto'), {'estimator__gamma': ['scale', 'auto'], 'estimator__C': [0.1, 1, 10],'estimator__kernel': ['rbf']}),
    ('ClusterRegressor', ClusterRegressor(num_clusters=[4, 6, 8, 10]), {}),('MeanRegressor', MeanRegressor(), {}),
	            ('RandomRegressor', RandomRegressor(), {}), ('SuppVecMach', SVR(), {'estimator__gamma': ['scale', 'auto'], 'estimator__C': [0.1, 1, 10],'estimator__kernel': ['rbf']})]

    # models = [('ClusterRegressor', ClusterRegressor(num_clusters=[4, 6, 8, 10]), {}),
    # ('CRFRegressor', CRFRegressor(num_clusters_list=[4, 6, 8, 10]), {}),
    # ('MeanRegressor', MeanRegressor(), {}),
    # ('RandomRegressor', RandomRegressor(), {}),
    # ('SuppVecMach', SVR(), {'estimator__gamma': ['scale', 'auto'], 'estimator__C': [0.1, 1, 10],'estimator__kernel': ['rbf']})]
    #models = [('CRFRegressor', CRFRegressor(num_clusters_list=[4, 6, 8, 10]), {}),
    #('MeanRegressor', MeanRegressor(), {}), ('RandomRegressor', RandomRegressor(), {})]
    # simulation settings
    JOBS = multiprocessing.cpu_count()
    debug_mode = False
    RESULTS_PATH = 'results'
    simulation_setting_dict = {'height_simulated_trees': [4], 'sklearn_jobs': sklearn_jobs,
    'branching_factors': [2, 3, 4], 'models': models, 'debug_mode': debug_mode,
    'clusters': [4,6,8,10], 'center_box_width': [5, 7, 9]}
    tree_number = 10
    number_population_samples = 10
    info_level = logging.DEBUG if debug_mode else logging.INFO
    logging.basicConfig(filename='results/simulation_experiments.log', filemode='w', format=f'%(asctime)s-%(levelname)s-%(message)s', datefmt='%d-%b-%y %H:%M:%S', level=info_level)


    create_tree = False
    tree_population_ids_list = []

    if create_tree:
        #  Trees ids generation

        logging.info("Trees and population ids generation")
        tree_population_ids_list = []
        for tree_id in range(tree_number):
            simulation_ = Simulations()
            height_ = random.choice(simulation_setting_dict['height_simulated_trees'])
            simulation_.generate_random_tree(height_, simulation_setting_dict['branching_factors'])
            simulation_.random_utilities(agent='prop')
            simulation_.root.compute_chance_decision(True)
            simulation_.to_csv(f"data_new/DT/tree_{tree_id}.csv")
            for sample_id in range(number_population_samples):
                tree_population_ids_list.append((tree_id, sample_id, simulation_, height_))

    else:  # instead of creating a tree, load a given tree
        for tree_id in range(tree_number):
            # load tree
            bdt = BipartyDT()
            bdt.load_tree(tree_id, folder='../data/DT')
            print(bdt.get_tree_height())
            # create object
            # append tree information
            for sample_id in range(number_population_samples):
                tree_population_ids_list.append((tree_id, sample_id, bdt, bdt.get_tree_height()))

    print(tree_population_ids_list)
    final_results = []

    # population generation
    start_time = time.time()
    if use_pool_multiproc:
        pool = multiprocessing.Pool(processes=JOBS)
        func = partial(multiprocessing_simulations, simulation_setting_dict)
        final_results = pool.map(func, tree_population_ids_list)
        pool.close()
    else:
        for el in tree_population_ids_list:
            final_results.append(multiprocessing_simulations(simulation_setting_dict, el))
    print(f"Simulations took {(time.time() - start_time)/3600.} hours")
    print('2')

    # results = final_results[0].copy()
    # for id in range(1, len(final_results)):
    #     for k in results.keys():
    #         results[k] += final_results[id][k]
    #
    # results_df = pd.DataFrame.from_dict(results)
    # plot_res = PlotResults(results_df, RESULTS_PATH)
    # plot_res.plot_single_trees()
    # plot_res.plot_aggregate_results('Tree leaves')
    # plot_res.plot_aggregate_results('Sample clusters')
    # plot_res.plot_aggregate_results('Cluster score')
    # plot_res.plot_aggregate_results_evidence_perc()
    # results_df.to_csv(os.path.join(RESULTS_PATH, 'results.csv'), index=False)