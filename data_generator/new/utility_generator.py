import pandas as pd

from src.SimulationsPO import BipartyDT
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
n_population = 1

n_tree = 10
n_samples = 100
mean_prop = 6
mean_opp = 6
std_x = 0.4
std_y = 2
sx, sy = 1, 1
rotation = 0.25
type_of_distribution = 1  # 0 = normal / 1 = uniform
percentage_more = 1.4
max_value = 11
min_value = 0
uniform_x_min = 4; uniform_x_max = 6
uniform_y_min = 0; uniform_y_max = 13

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
    leaves, leaf_names = simulation.get_leaves()
    n_leaves = len(leaves)
    n_data_to_gen = int(n_leaves * n_samples * percentage_more)
    print(f'n of leaves: {n_leaves} | data needed: {n_leaves * n_samples} | data generated: {n_data_to_gen} ')
    print(leaf_names)

    if type_of_distribution == 0:
        x = np.random.normal(mean_prop, std_x, n_data_to_gen)
        y = np.random.normal(mean_opp, std_y, n_data_to_gen)
    else:
        x = np.random.uniform(uniform_x_min,uniform_x_max, n_data_to_gen)
        y = np.random.uniform(uniform_y_min,uniform_y_max, n_data_to_gen)

    X = np.vstack((x, y)).T

    # Scaling matrix
    Scale = np.array([[sx, 0], [0, sy]])
    # Apply scaling matrix to X
    Y = X.dot(Scale)

    # Rotation matrix
    theta = rotation * np.pi
    c, s = np.cos(theta), np.sin(theta)
    Rot = np.array([[c, -s], [s, c]])

    # Transformation matrix
    #T = Scale.dot(Rot)

    # Apply transformation matrix to X
    # Y = X.dot(T)
    mean_x, mean_y = np.mean(Y, axis=0)
    Y = np.dot(Y - np.array([mean_x, mean_y]), Rot.T) + np.array([mean_x, mean_y])
    print(Y.shape)

    if rint:
        Y = np.rint(Y)

    if cut_outliers:
        x_original = Y[:, 0]
        y_original = Y[:, 1]
        indices = np.where((y_original > min_value) & (y_original < max_value) & (x_original > min_value) & (x_original < max_value))
        Y = np.vstack((x_original[indices], y_original[indices])).T

    data = Y

    dataset_leaves = []
    for i in range(n_samples):
        if random_sample_data:
            # Randomly sample n_leaves values from the original array
            # leaves_values = np.random.choice(data, size=n_leaves, replace=False)
            x_leaves = np.random.choice(data[:, 0], size=n_leaves, replace=False)
            print(x_leaves)
            # Get the indices of the selected values in the original array
            x_selected_indices = np.where(np.isin(data[:, 0], x_leaves))
            print(x_selected_indices, x_selected_indices[0])
            leaves_values = data[x_selected_indices]
            print(leaves_values)
            data = np.delete(data, (x_selected_indices[0],x_selected_indices[0]))



        else:
            # sample n_leaves values from the original array
            leaves_values = data[:n_leaves]
            # Remove the first n_leaves values from the original array
            data = data[n_leaves:]

        dataset_leaves.append(leaves_values)

    dataset_leaves = np.asarray(dataset_leaves)
    prop_values = dataset_leaves[:, :, 0]
    opp_values = dataset_leaves[:, :, 1]
    prop_dataset = pd.DataFrame(prop_values,columns=leaf_names)
    opp_dataset = pd.DataFrame(opp_values, columns=leaf_names)

    if save:
        prop_dataset.to_csv(f"../datasets_paper/tree_{tree_id}_proponent.csv", index=False)
        opp_dataset.to_csv(f"../datasets_paper/tree_{tree_id}_opponent.csv", index=False)

    return data, X


def run():
    tree_population_ids_list = []

    for tree_id in range(n_tree):
        # load tree
        bdt = BipartyDT()
        bdt.load_tree(tree_id, folder='../data/DT')
        #print(bdt.get_tree_height())
        # create object
        # append tree information
        for sample_id in range(n_population):
            tree_population_ids_list.append((tree_id, sample_id, bdt, bdt.get_tree_height()))

    print('pop ids = ',tree_population_ids_list)

    final_data = []
    final_original_data = []
    for el in tree_population_ids_list:
        final_data.append(utility_gen(el)[0])
        final_original_data.append(utility_gen(el)[1])

    for data in final_original_data:
        plt.scatter(data[:, 0], data[:, 1])
        plt.title('Original Data')
        plt.axis('equal')
    plt.show()

    for data in final_data:
        plt.scatter(data[:, 0], data[:, 1])
        plt.title('Transformed Data')
        plt.axis('equal')
    plt.show()


# main
if __name__ == "__main__":
    run()
