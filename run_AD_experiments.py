import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")
# pd.set_option('display.max_columns', None)  # use only to console print pandas DF
# pd.set_option('display.max_rows', None)
print("opp" in "Q_opp")
policy_df = pd.read_csv('results/csv_policy_experiments.csv')
#policy_df = pd.read_csv('results/csv_policy_experiments_last_paper.csv')
df_columns = policy_df.columns

value_to_find = ['AD', 'Q_prop', 'Q_opp']

for value in value_to_find:
    ad_columns = []
    #print(df_columns)

    for column in df_columns:
        if value in column:
            ad_columns.append(column)

    ad_columns.append('tree_height')
    #print(ad_columns)

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
    #df1.apply(lambda x: x.str.replace('.', ','))
    df1 = df1.astype('string')
    # use the following line to change comma to dot for overleaf paper
    df1 = df1.apply(lambda x: x.str.replace('.', ','))
    print(df1.T)

plt.figure(figsize=(6, 5))

for tree_id in range(10):
    prop_ds = pd.read_csv(f'../data_generator/datasets_paper/tree_{tree_id}_proponent.csv')
    opp_ds  = pd.read_csv(f'../data_generator/datasets_paper/tree_{tree_id}_opponent.csv')
    prop = prop_ds.values
    opp = opp_ds.values
    stack = np.stack((prop,opp)).T
    for value in stack:
        plt.scatter(value[:, 0], value[:, 1], color='#4660AC')

    plt.xlabel('Proponent utility')
    plt.ylabel('Opponent utility')
    plt.axis('equal')

plt.show()



#
# x = False
#
# if x:
#     df0 = policy_df[ad_columns].groupby('tree_height')
#
#     print('-------------------------')
#     df1 = df0.mean()
#     print(df1.T.columns)
#     df2 = df0.std()
#     df3 = pd.merge(df1,df2,left_index = True , right_index =True, suffixes=['_mean','_std'])
#     df3 = df3.T
#     df3 = df3.reindex(index=df3.index.sort_values())
#     print('df3')
#     print(df3)
#     # df3 = pd.concat([df1,df2], axis='columns')
#     # df3.columns = ['mean', 'std']
#     # print(df3)
#     df1.T.to_csv('data/AD_results/AD_mean.csv', encoding='utf-8', index=True)
#     df2.T.to_csv('data/AD_results/AD_std.csv', encoding='utf-8', index=True)
#     df3.to_csv('data/AD_results/normal_AD_both.csv', encoding='utf-8', index=True)
#
# else:
#     df0 = policy_df[ad_columns].groupby('tree_height')
#     print('-------------------------')
#     df1 = df0.mean()
#     print(df1.T)


#
# df3.to_csv('AD_mean_std.csv', encoding='utf-8', index=True)






# ad_mean = []
# ad_std = []
# for ad in ad_columns:
#     ad_mean.append(policy_df[ad].mean())
#     ad_std.append(policy_df[ad].std())
#
# #ad_columns.insert(0,'Type')
# idx = ['mean', 'std']
# #result df = pd.DataFrame()
# print(ad_mean)
# print(ad_std)