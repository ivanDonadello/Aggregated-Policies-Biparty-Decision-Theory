import pandas as pd
import numpy as np
from src.SimulationsPO import BipartyDT


def sum_by_value(x, y):
    result = (x + abs(y)) + 1
    return result


n_population = 1
n_tree = 10
n_samples = 100
samples_id_values = np.arange(n_samples).astype(int)

dataframes = []
for tree_id in range(n_tree):
    bdt = BipartyDT()
    bdt.load_tree(tree_id)
    leaves, leaves_names = bdt.get_leaves()
    tree_prop_utilities = []
    for leaf in leaves:
        tree_prop_utilities.append(leaf.utility_proponent)

    # because the proponent values is static (from the DT dataset), we have to duplicate the data to achieve n_samples
    prop_values = []
    for i in range(n_samples):
        prop_values.append(tree_prop_utilities)

    for population_id in range(n_population):
        opp_dataset = pd.read_csv(f'datasets/tree_{tree_id}_population_{population_id}.csv')
        opp_dataset = opp_dataset.drop(columns='id')
        opp_dataset = opp_dataset.iloc[:n_samples]

        # normalization if needed
        min_val = opp_dataset.min().min()
        if min_val < 0:
            opp_dataset = opp_dataset.apply(sum_by_value, args=(min_val,), axis=1)

        # new columns for organization purposes
        opp_dataset.insert(0, 'utility_type', 'opponent')
        opp_dataset.insert(0, 'sample_id', samples_id_values)
        opp_dataset.insert(0, 'tree_id', tree_id)

        # proponent values
        prop_dataset = pd.DataFrame(prop_values, columns=leaves_names)
        prop_dataset.insert(0, 'utility_type', 'proponent')
        prop_dataset.insert(0, 'sample_id', samples_id_values)
        prop_dataset.insert(0, 'tree_id', tree_id)

        concat_df = pd.concat([prop_dataset, opp_dataset], axis=0, ignore_index=True)

        dataframes.append(concat_df)

first_columns = ['tree_id', 'sample_id', 'utility_type']
orderer_columns = np.arange(start=6, stop=171, dtype=int).astype(str)
reorder_columns = np.concatenate((first_columns,orderer_columns))
# print(reorder_columns)

concat_dataframes = pd.concat(dataframes, axis=0, ignore_index=True)
concat_dataframes = concat_dataframes.reindex(columns=reorder_columns)
# print(concat_dataframes)
concat_dataframes.to_csv(f"../data/datasets_paper/donadello2022balanced", index=False)