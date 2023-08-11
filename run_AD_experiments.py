import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# print("opp" in "Q_opp")

policy_df = pd.read_csv('results/csv_policy_experiments.csv')
#policy_df = pd.read_csv('results/csv_policy_experiments_last_paper.csv')
df_columns = policy_df.columns

value_to_find = ['AD', 'Q_prop', 'Q_opp']

for value in value_to_find:
    ad_columns = []

    for column in df_columns:
        if value in column:
            ad_columns.append(column)

    ad_columns.append('tree_height')

    df0 = policy_df[ad_columns].groupby('tree_height')
    print('-------------------------')
    print(f'------- {value} --------')
    df1 = df0.mean()
    df1 = df1.round(3)
    # print(df1.columns)
    new_col = []
    for col in df1.columns:
        new_col.append(re.search(r'\((.*?)\)', col).group(1).replace("_", " "))

    df1.columns = new_col
    df1 = df1.astype('string')
    # use the following line to change comma to dot for overleaf paper
    # df1 = df1.apply(lambda x: x.str.replace('.', ','))
    print(df1.T)


data_folder = "data_generator"
folder_name = 'datasets_paper' #'datasets'

folders = os.path.join(data_folder, folder_name)
# load the dataset to print the scatter plot
dataset_path = os.path.join(folders, f"donadelloDS")
dataset = pd.read_csv(dataset_path)


sns.set(style="whitegrid")
plt.figure(figsize=(6, 5))

for tree_id in range(10):
    tree_df = dataset.loc[dataset['tree_id'] == tree_id]
    tree_df = tree_df.dropna(axis=1)
    prop_df = tree_df.loc[tree_df['utility_type'] == 'proponent']
    prop_df = prop_df.drop(['tree_id', 'sample_id', 'utility_type'], axis=1)
    opp_df = tree_df.loc[tree_df['utility_type'] == 'opponent']
    opp_df = opp_df.drop(['tree_id', 'sample_id', 'utility_type'], axis=1)

    prop = prop_df.values
    opp = opp_df.values

    stack = np.stack((prop,opp)).T
    for value in stack:
        plt.scatter(value[:, 0], value[:, 1], color='#4660AC')

    plt.xlabel('Proponent utility')
    plt.ylabel('Opponent utility')
    plt.axis('equal')

plt.show()