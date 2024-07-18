import pandas as pd
import re
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--ds', default='don2022', help='input dataset')
    #parser.add_argument('--ds', default='don2022NoOPT', help='input dataset')
    #parser.add_argument('--ds', default='donOPT_new', help='input dataset')

    args = parser.parse_args()
    dataset_name = args.ds
    print(f'Running experiments using {dataset_name} dataset')

    policy_df = pd.read_csv(f'results/2policies_experiments_{dataset_name}_new.csv')
    df_columns = policy_df.columns

    metrics = ['AAD', 'APU', 'AOU', 'accept']
    mean_values = [3, 5, 7]
    #dataset_name = 'don2022'

    for value in metrics:
        ad_columns = []

        for column in df_columns:
            if value in column:
                ad_columns.append(column)

        ad_columns.append('tree_height')

        if value == 'accept':
            for mean in mean_values:
                df_cluster = policy_df.loc[policy_df['mean_cluster'] == mean]
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
                #df1.T.to_csv(f'results/metrics_{value}_mean{mean}_{dataset_name}.csv', encoding='utf-8')

        else:
            df0 = policy_df[ad_columns].groupby('tree_height')
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
            #df1.T.to_csv(f'results/metrics_{value}_{dataset_name}.csv', encoding='utf-8')