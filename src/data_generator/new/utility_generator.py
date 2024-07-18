import pandas as pd

from src.SimulationsPO import BipartyDT
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
n_population = 1
n_tree = 10
n_samples = 1000
mean_prop = 6
mean_opp = 6
std_x = 0.2
std_y = 2
sx, sy = 1, 1
rotation = 0.75 # 0.25 #
type_of_distribution = 1  # 0 = normal / 1 = uniform
max_value = 12
min_value = 0
uniform_x_min = 5; uniform_x_max = 7
uniform_y_min = 0; uniform_y_max = 12

save = True
random_sample_data = False
cut_outliers = 1  # 0 = False  1 = True
rint = 1  # 0 = False  1 = True


def sum_by_value(x, y):
    result = (x + abs(y)) + 1
    return result


def utility_gen(tree_population_ids):
    tree_id = tree_population_ids[0]
    sample_id = tree_population_ids[1]
    simulation = tree_population_ids[2]
    height = tree_population_ids[3]
    leaves, leaves_names = simulation.get_leaves()
    n_leaves = len(leaves)
    print(f'n of leaves: {n_leaves} ')
    print(leaves_names)

    # set the seed as the tree_id number
    np.random.seed(tree_id)

    data = []
    for i in range(n_samples):
        if type_of_distribution == 0:
            x = np.random.normal(mean_prop, std_x, n_leaves)
            y = np.random.normal(mean_opp, std_y, n_leaves)
        else:
            x = np.random.uniform(uniform_x_min,uniform_x_max, n_leaves)
            y = np.random.uniform(uniform_y_min,uniform_y_max, n_leaves)

        X = np.vstack((x, y)).T

        # Scaling matrix
        Scale = np.array([[sx, 0], [0, sy]])

        # Rotation matrix
        theta = rotation * np.pi
        c, s = np.cos(theta), np.sin(theta)
        Rot = np.array([[c, -s], [s, c]])

        # Transformation matrix
        T = Scale.dot(Rot)

        # Apply transformation matrix to X
        Y = X.dot(T)

        if rint:
            Y = np.rint(Y)

        # if cut_outliers:
        #     x_original = Y[:, 0]
        #     y_original = Y[:, 1]
        #     indices = np.where((y_original > min_value) & (y_original < max_value) & (x_original > min_value) & (
        #                 x_original < max_value))
        #     Y = np.vstack((x_original[indices], y_original[indices])).T

        data.append(Y)

    data = np.asarray(data)
    normalized_data = []
    min_prop = data[:, :, 0].min().min()
    min_opp = data[:, :, 1].min().min()

    for val in data:
        prop = sum_by_value(val[:, 0], min_prop)
        opp = sum_by_value(val[:, 1], min_opp)
        normalized_data.append(np.vstack((prop, opp)).T)

    normalized_data = np.asarray(normalized_data)
    prop_values = normalized_data[:, :, 0]
    opp_values = normalized_data[:, :, 1]
    # print('norm data')
    # print(normalized_data)
    # print(f'proponent: {prop_values}')
    # print(f'proponent: {opp_values}')
    samples_id_values = np.arange(n_samples).astype(int)
    prop_dataset = pd.DataFrame(prop_values, columns=leaves_names)
    prop_dataset.insert(0, 'utility_type', 'proponent')
    prop_dataset.insert(0, 'sample_id', samples_id_values)
    prop_dataset.insert(0, 'tree_id', tree_id)

    opp_dataset = pd.DataFrame(opp_values, columns=leaves_names)
    opp_dataset.insert(0, 'utility_type', 'opponent')
    opp_dataset.insert(0, 'sample_id', samples_id_values)
    opp_dataset.insert(0, 'tree_id', tree_id)

    concat_df = pd.concat([prop_dataset, opp_dataset], axis=0, ignore_index=True)

    return normalized_data, X, concat_df


def run():
    tree_population_ids_list = []

    for tree_id in range(n_tree):
        # load tree
        bdt = BipartyDT()
        bdt.load_tree(tree_id, folder='../../data/DT')
        #print(bdt.get_tree_height())
        # create object
        # append tree information
        for sample_id in range(n_population):
            tree_population_ids_list.append((tree_id, sample_id, bdt, bdt.get_tree_height()))

    print('pop ids = ',tree_population_ids_list)

    final_data = []
    final_original_data = []
    dataframes = []
    for el in tree_population_ids_list:
        a, b, dataframe = utility_gen(el)
        final_data.append(a)
        final_original_data.append(b)
        dataframes.append(dataframe)

    for data in final_original_data:
        plt.scatter(data[:, 0], data[:, 1])
        plt.title('Original Data')
        plt.axis('equal')
    plt.show()

    #print(final_data[0][0])
    for data in final_data:
        plt.scatter(data[:, :, 0], data[:, :, 1])
        plt.title('Transformed Data')
        plt.axis('equal')
    plt.show()

    if save:
        # prop_dataset.to_csv(f"../datasets_paper/tree_{tree_id}_proponent.csv", index=False)
        # opp_dataset.to_csv(f"../datasets_paper/tree_{tree_id}_opponent.csv", index=False)
        first_columns = ['tree_id', 'sample_id', 'utility_type']
        orderer_columns = np.arange(start=6, stop=171, dtype=int).astype(str)

        reorder_columns = np.concatenate((first_columns,orderer_columns))
        print(reorder_columns)
        concat_dataframes = pd.concat(dataframes, axis=0, ignore_index=True)
        concat_dataframes = concat_dataframes.reindex(columns=reorder_columns)
        concat_dataframes.to_csv(f"donadello2023UNB", index=False)

# main
if __name__ == "__main__":
    run()
