from src.SimulationsPO import BipartyDT
import os
import pandas as pd
import random
import re
import numpy as np
from argparse import ArgumentParser

def sum_by_value(x, y):
    result = (x + abs(y)) + 1
    return result


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--ds', default='don2022', help='input dataset')
    args = parser.parse_args()
    dataset_name = args.ds

    # dataset_name = 'don2022b'  # datasets are in: /data/datasets_paper
    print(f'>> Running policy propagation experiments using [{dataset_name}] dataset')

    bdt = BipartyDT()
    data_folder = "data"
    folder_name = 'datasets_paper'

    folders = os.path.join(data_folder, folder_name)
    # load the whole dataset
    dataset_path = os.path.join(folders, dataset_name)
    donadelloDS = pd.read_csv(dataset_path)

    p_values = [[-2, 'agg'],[-1, 'agg'],[0, 'agg'],[1, 'agg'],[2, 'agg'],[0.1, 'SMD'],
                [0.5, 'SMD'],[0.9, 'SMD'],[-1, 'std']]

    pd.set_option('display.max_rows', None)

    # tree_height
    # ============== SETTING UP THE FIRST COLUMNS OF THE FINAL DATASET ==============
    propagate_data_columns = ['Tree_id', 'Population_id', 'Sample_id', 'tree_height', 'APU (bimax)', 'AOU (bimax)', 'AAD (bimax)']
    for p in p_values:
        propagate_data_columns.append(f'APU ({p[1]}_{p[0]})')
        propagate_data_columns.append(f'AOU ({p[1]}_{p[0]})')
        propagate_data_columns.append(f'AAD ({p[1]}_{p[0]})')

    propagate_data = []

    for tree_id in range(10):
        # ============== LOAD TREE and COMPUTE CHANCE/DECISION NODES ==============
        bdt.load_tree(tree_id, fixed_first_node=True, type_first_node='Decision')

        for tree_pop in range(1):
            # ============== LOAD POPULATION ==============
            tree_df = donadelloDS.loc[donadelloDS['tree_id'] == tree_id]
            tree_df = tree_df.dropna(axis=1)
            prop_df = tree_df.loc[tree_df['utility_type'] == 'proponent']
            prop_df = prop_df.drop(['tree_id', 'sample_id', 'utility_type'], axis=1)
            opp_df = tree_df.loc[tree_df['utility_type'] == 'opponent']
            opp_df = opp_df.drop(['tree_id', 'sample_id', 'utility_type'], axis=1)

            columns = prop_df.columns

            min_prop = prop_df.min().min()
            min_opp = opp_df.min().min()
            max_prop = prop_df.max().max()
            max_opp = opp_df.max().max()

            print('Tree > id: {} | min_prop: {} | max_prop: {} | min_opp: {} | max_opp {}'
                  .format(tree_id, min_prop, max_prop, min_opp, max_opp))

            # ============== UPDATE UTILITIES ==============
            utility_count = len(prop_df)
            for row in range(utility_count):
                bdt.reset_utilities()
                prop_values = prop_df.iloc[row]
                opp_values = opp_df.iloc[row]
                for i in range(len(columns)):
                    bdt.dict_tree[columns[i]].set_utility_proponent(prop_values[i])
                    bdt.dict_tree[columns[i]].set_utility_opponent(opp_values[i])

                # ============== PROPAGATE UTILITY ==============
                bdt.root.propagate_utility("bimaximax", -1, '')

                # ============== (RE)CREATE ROW OF VALUES ==============
                row_result = [tree_id, tree_pop, row, bdt.root.get_tree_height()]
                # ============== APPEND VALUES FOR GIVEN POLICY ==============
                row_result.append(bdt.root.Q_proponent)
                row_result.append(bdt.root.Q_opponent)
                row_result.append(bdt.root.get_AD())

                for p in p_values:  #
                    bdt.root.propagate_utility(policy="aggregated", p=p[0], v=p[1])
                    row_result.append(bdt.root.Q_proponent)
                    row_result.append(bdt.root.Q_opponent)
                    row_result.append(bdt.root.get_AD())

                propagate_data.append(row_result)

    propagate_dataset = pd.DataFrame(data=propagate_data, columns=propagate_data_columns)
    # propagate_dataset.to_csv(f'results/policies_experiments_{dataset_name}.csv', encoding='utf-8', index=False)

    # ------------- Acceptance rate experiments -----------------

    print(f'\n>> Including the Acceptance Rate results in the dataset')
    # propagate_dataset = pd.read_csv(f'results/policies_experiments_{dataset_name}.csv')
    df_columns = propagate_dataset.columns

    seed_value = 1
    random.seed(seed_value)
    # Generate a list of 1000 random integers between 1 and 10
    # mean_Clusters = [random.randint(1, 10) for _ in range(1000)]

    # Generate a list of size N (size of the dataset) with random distribution of 3, 5, and 7 values
    rows_dataset = len(propagate_dataset)
    mean_Clusters = random.choices([3, 5, 7], k=rows_dataset)
    mean_cluster_columns_values = []

    for i in range(1):
        mean_cluster_columns_values.extend(mean_Clusters)

    # print(mean_cluster_columns_values)
    # policy_df.insert(4,'mean_cluster', mean_cluster_columns_values)

    propagate_dataset['mean_cluster'] = mean_cluster_columns_values

    # Creating the new column 'th'
    propagate_dataset['th'] = np.random.normal(propagate_dataset['mean_cluster'], 1)

    columns = propagate_dataset.columns
    opponent_columns_names = []
    for column in columns:
        if 'AOU ' in column:
            opponent_columns_names.append(column)

    for i in opponent_columns_names:
        # Create the 'accepted' column based on the condition 'AOU' >= 'th'
        column_name = 'accept' + re.sub('[AOU]', '', i)
        propagate_dataset[column_name] = np.where(propagate_dataset[i] >= propagate_dataset['th'], 1, 0)

    # Display the updated DataFrame

    # Reordering columns
    propagate_dataset = propagate_dataset[['Tree_id', 'Population_id', 'Sample_id', 'tree_height', 'mean_cluster', 'th',
                           'APU (bimax)', 'AOU (bimax)', 'AAD (bimax)', 'accept (bimax)',
                           'APU (agg_-2)', 'AOU (agg_-2)', 'AAD (agg_-2)', 'accept (agg_-2)',
                           'APU (agg_-1)', 'AOU (agg_-1)', 'AAD (agg_-1)', 'accept (agg_-1)',
                           'APU (agg_0)', 'AOU (agg_0)', 'AAD (agg_0)', 'accept (agg_0)',
                           'APU (agg_1)', 'AOU (agg_1)', 'AAD (agg_1)', 'accept (agg_1)',
                           'APU (agg_2)', 'AOU (agg_2)', 'AAD (agg_2)', 'accept (agg_2)',
                           'APU (SMD_0.1)', 'AOU (SMD_0.1)', 'AAD (SMD_0.1)', 'accept (SMD_0.1)',
                           'APU (SMD_0.5)', 'AOU (SMD_0.5)', 'AAD (SMD_0.5)', 'accept (SMD_0.5)',
                           'APU (SMD_0.9)', 'AOU (SMD_0.9)', 'AAD (SMD_0.9)', 'accept (SMD_0.9)',
                           'APU (std_-1)', 'AOU (std_-1)', 'AAD (std_-1)', 'accept (std_-1)']]

    propagate_dataset.to_csv(f'results/policies_experiments_{dataset_name}.csv', index=False)


    # ------------- Metrics results -----------------

    print(f'\n>> Printing the result metrics using [{dataset_name}] dataset')

    # policy_df = pd.read_csv(f'results/policies_experiments_{dataset_name}.csv')
    df_columns = propagate_dataset.columns

    metrics = ['AAD', 'APU', 'AOU', 'accept']
    mean_values = [3, 5, 7]

    for value in metrics:
        ad_columns = []

        for column in df_columns:
            if value in column:
                ad_columns.append(column)

        ad_columns.append('tree_height')

        if value == 'accept':
            for mean in mean_values:
                df_cluster = propagate_dataset.loc[propagate_dataset['mean_cluster'] == mean]
                df0 = df_cluster[ad_columns].groupby('tree_height')
                print('-------------------------')
                print(f'------- {value} with mean:{mean} --------')
                df1 = df0.mean()
                df1 = df1.round(3)
                new_col = []
                for col in df1.columns:
                    new_col.append(re.search(r'\((.*?)\)', col).group(1).replace("_", " "))

                df1.columns = new_col
                df1 = df1.astype('string')
                print(df1.T)
                df1.T.to_csv(f'results/metrics_{value}_mean{mean}_{dataset_name}.csv', encoding='utf-8')

        else:
            df0 = propagate_dataset[ad_columns].groupby('tree_height')
            print('-------------------------')
            print(f'------- {value} --------')
            df1 = df0.mean()
            df1 = df1.round(3)
            new_col = []
            for col in df1.columns:
                new_col.append(re.search(r'\((.*?)\)', col).group(1).replace("_", " "))

            df1.columns = new_col
            df1 = df1.astype('string')
            print(df1.T)
            df1.T.to_csv(f'results/metrics_{value}_{dataset_name}.csv', encoding='utf-8')