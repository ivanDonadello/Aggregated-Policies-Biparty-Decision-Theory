import pandas as pd
from scipy.stats import wilcoxon
#pd.set_option('display.max_columns', None)  # use only to console print pandas DF
#pd.set_option('display.max_rows', None)

table = []
size = 120

col1 = 'AD (bimax)'
col2 = 'Q_prop (bimax)'
col3 = 'Q_opp (bimax)'

dataset = pd.read_csv('../results/csv_policy_experiments.csv')
dataset = dataset.loc[dataset['tree_height'] == 6]
#dataset = dataset.loc[:size]
dataset = dataset.sample(size, random_state=1)

#print(dataset.head())
#print(dataset.loc[:,[col1,col2,col3]])
# selected_df = AD_df[['AD (bimax)','AD (-1)']] # original

policy = 'SMD_0.5'
policy = 'agg_-1'

col1 = 'AD (bimax)'
col2 = f'AD ({policy})'
#print(dataset.loc[:20,[col1,col2]])

#res = wilcoxon(x=selected_df.iloc[:20,0].values, y=selected_df.iloc[:20,1].values, method='auto')
res = wilcoxon(x=dataset.loc[:,col1].values, y=dataset.loc[:,col2].values, method='auto')
print(res)
table.append([res.pvalue,res.statistic])

# ----------------------------------------------
col1 = 'Q_prop (bimax)'
col2 = f'Q_prop ({policy})'
res = wilcoxon(x=dataset.loc[:,col1].values, y=dataset.loc[:,col2].values, method='auto')

table.append([res.pvalue,res.statistic])

# ---------------------------------------------
col1 = 'Q_opp (bimax)'
col2 = f'Q_opp ({policy})'
res = wilcoxon(x=dataset.loc[:,col1].values, y=dataset.loc[:,col2].values, method='auto')

table.append([res.pvalue,res.statistic])

#print(dataset.loc[:20,[col1,col2]])

# ---- dataframe creation ------------
columns = ['p_value', 'statistic']
index = ['AD','Q_prop', 'Q_opp']

result_df = pd.DataFrame(table, columns=columns, index=index)
#result_df = result_df.round(5)
print('')
print("Null hypothesis test for: Bimax vs p-1")
print(result_df.round(11))



