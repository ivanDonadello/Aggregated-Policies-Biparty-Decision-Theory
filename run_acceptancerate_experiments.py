import pandas as pd
import random
import re
import numpy as np
from argparse import ArgumentParser

if __name__ == "__main__":
    # Read dataset
    parser = ArgumentParser()
    #parser.add_argument('--ds', default='don2022NoOPT', help='input dataset') # donadello2023UNB  don2022NoOPT
    parser.add_argument('--ds', default='don2022OPT_new', help='input dataset')
    args = parser.parse_args()
    dataset_name = args.ds
    print(f'Running experiments using {dataset_name} dataset')
    policy_df = pd.read_csv(f'results/policies_experiments_{dataset_name}.csv')
    df_columns = policy_df.columns

    seed_value = 1
    random.seed(seed_value)
    # Generate a list of 1000 random integers between 1 and 10
    #mean_Clusters = [random.randint(1, 10) for _ in range(1000)]

    # Generate a list of size N (size of the dataset) with random distribution of 3, 5, and 7 values
    rows_dataset = len(policy_df)
    mean_Clusters = random.choices([3, 5, 7], k=rows_dataset)
    mean_cluster_columns_values = []

    for i in range(1):
        mean_cluster_columns_values.extend(mean_Clusters)

    #print(mean_cluster_columns_values)
    #policy_df.insert(4,'mean_cluster', mean_cluster_columns_values)

    policy_df['mean_cluster'] = mean_cluster_columns_values

    # Creating the new column 'th'
    policy_df['th'] = np.random.normal(policy_df['mean_cluster'], 1)

    columns = policy_df.columns
    opponent_columns_names = []
    for column in columns:
        if 'AOU ' in column:
            opponent_columns_names.append(column)

    for i in opponent_columns_names:
        # Create the 'accepted' column based on the condition 'AOU' >= 'th'
        column_name = 'accept' + re.sub('[AOU]', '', i)
        policy_df[column_name] = np.where(policy_df[i] >= policy_df['th'], 1, 0)

    # Display the updated DataFrame

    # Reordering columns
    policy_df = policy_df[['Tree_id', 'Population_id', 'Sample_id', 'tree_height','mean_cluster', 'th',
           'APU (bimax)', 'AOU (bimax)', 'AAD (bimax)', 'accept (bimax)',
           'APU (agg_-2)', 'AOU (agg_-2)', 'AAD (agg_-2)', 'accept (agg_-2)',
           'APU (agg_-1)', 'AOU (agg_-1)', 'AAD (agg_-1)', 'accept (agg_-1)',
           'APU (agg_0)', 'AOU (agg_0)', 'AAD (agg_0)', 'accept (agg_0)',
           'APU (agg_1)', 'AOU (agg_1)', 'AAD (agg_1)', 'accept (agg_1)',
           'APU (agg_2)', 'AOU (agg_2)', 'AAD (agg_2)', 'accept (agg_2)',
           'APU (SMD_0.1)', 'AOU (SMD_0.1)', 'AAD (SMD_0.1)', 'accept (SMD_0.1)',
           'APU (SMD_0.3)', 'AOU (SMD_0.3)', 'AAD (SMD_0.3)', 'accept (SMD_0.3)',
           'APU (SMD_0.5)', 'AOU (SMD_0.5)', 'AAD (SMD_0.5)', 'accept (SMD_0.5)',
           'APU (SMD_0.7)', 'AOU (SMD_0.7)', 'AAD (SMD_0.7)', 'accept (SMD_0.7)',
           'APU (SMD_0.9)', 'AOU (SMD_0.9)', 'AAD (SMD_0.9)', 'accept (SMD_0.9)',
           'APU (std_-1)', 'AOU (std_-1)', 'AAD (std_-1)', 'accept (std_-1)']]

    print()
    print(policy_df.iloc[:10,2:9])

    policy_df.to_csv(f'results/policies_experiments_{dataset_name}.csv', index=False)