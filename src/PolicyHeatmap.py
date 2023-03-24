import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
import pandas as pd
#import Levenshtein as leven
#threshhold = 50

ds = pd.read_csv('../csv_policy_experiments.csv')
column_list = ds.columns
value_to_compare = 'Q_'

axis_values = []

for item in column_list:
    if item.find(value_to_compare) == 0:
        axis_values.append(item)

# create a list pair with the 2 p values: (Q_prop (bimax), Q_opp (bimax))
paired_axis_values = list(zip(axis_values,axis_values[1:]))[::2]

for pair in paired_axis_values:
    col1 = pair[0]
    col2 = pair[1]
    fig_name = col1[col1.find("(") + 1:col1.find(")")]

    bimax_ds = ds[[col1, col2]]
    df = bimax_ds # bimax_ds.groupby([col1, col2]).size()

    df = pd.crosstab(df[col1],df[col2]).replace(0,np.nan).\
         stack().reset_index().rename(columns={0:'Frequency'})

    df2 = df.drop_duplicates().pivot_table(index=col1, columns=col2, values='Frequency', sort=False)
    ax = sns.heatmap(df2, cmap='coolwarm', square=True, linewidth=0.5, xticklabels=True, yticklabels=True, center=1, vmin= 0, vmax=60,
                annot=True, annot_kws={"size": 7})
    ax.invert_yaxis()
    #plt.show()
    ax.get_figure().savefig(f'../data/heatmap/fig_{fig_name}.png')