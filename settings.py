import os

num_trees = 10
num_populations = 10
tree_folder = os.path.join("data", "DT")
population_folder = os.path.join("data", "datasets")
policies = [("bimaximax", -1), ("aggregated", -1), ("aggregated", 0), ("aggregated", 1)]