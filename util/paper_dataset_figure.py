import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#sns.set(style="whitegrid")
plt.figure(figsize=(6.5, 6.5))

for tree_id in range(1):
    prop_ds = pd.read_csv(f'../data_generator/datasets_paper/tree_{tree_id}_proponent.csv')
    opp_ds  = pd.read_csv(f'../data_generator/datasets_paper/tree_{tree_id}_opponent.csv')
    prop = prop_ds.values[:50]
    opp = opp_ds.values[:50]
    print('tree:', tree_id)

    #stack = np.stack((prop,opp)).T

    # for value in stack:
    #     plt.scatter(value[:, 0], value[:, 1], color='#4660AC')
    for i,j in enumerate(prop):
        for k in range(len(j)):
            if ((prop[i,k] <= 4) & (opp[i,k] >= 8)) or ((prop[i,k] >= 8) & (opp[i,k] < 4)):
                plt.scatter(prop[i,k], opp[i,k], color='red')
            else:
                plt.scatter(prop[i, k], opp[i, k], color='blue')

    plt.xlabel('Proponent utility', fontsize=20)
    plt.ylabel('Opponent utility', fontsize=20)
    plt.yticks(fontsize=20)
    plt.xticks(np.arange(0, 12, step=2),fontsize=20)
    # plt.xlabel('Proponent utility')
    # plt.ylabel('Opponent utility')
    # plt.axis('equal')

plt.savefig('UB_ds.pdf')
plt.show()

# data_folder = "data_generator"
    # folder_name = 'datasets_paper' #'datasets'
    #
    # folders = os.path.join(data_folder, folder_name)
    # # load the dataset to print the scatter plot
    # dataset_path = os.path.join(folders, f"donadelloDS")
    # dataset = pd.read_csv(dataset_path)
    #
    #
    # sns.set(style="whitegrid")
    # plt.figure(figsize=(6, 5))
    #
    # for tree_id in range(10):
    #     tree_df = dataset.loc[dataset['tree_id'] == tree_id]
    #     tree_df = tree_df.dropna(axis=1)
    #     prop_df = tree_df.loc[tree_df['utility_type'] == 'proponent']
    #     prop_df = prop_df.drop(['tree_id', 'sample_id', 'utility_type'], axis=1)
    #     opp_df = tree_df.loc[tree_df['utility_type'] == 'opponent']
    #     opp_df = opp_df.drop(['tree_id', 'sample_id', 'utility_type'], axis=1)
    #
    #     prop = prop_df.values
    #     opp = opp_df.values
    #
    #     stack = np.stack((prop,opp)).T
    #     for value in stack:
    #         plt.scatter(value[:, 0], value[:, 1], color='#4660AC')
    #
    #     plt.xlabel('Proponent utility')
    #     plt.ylabel('Opponent utility')
    #     plt.axis('equal')

    # plt.show()


