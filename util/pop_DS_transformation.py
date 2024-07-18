import pandas as pd

pd.set_option('display.max_columns', None)  # use only to console print pandas DF
#pd.set_option('display.max_rows', None)
pd.set_option("display.precision", 3)

def sum_by_value(x, y):
    result = (x + abs(y)) + 1
    return result

# pop_df = pd.read_csv('../data/datasets/tree_1_population_1.csv')
pop_df = pd.read_csv('../src/data_generator/datasets/tree_1_population_2.csv')
pop_df = pop_df.drop('id', axis=1)
# selected_df = AD_df[['AD (bimax)','AD (-1)']][AD_df.tree_height == 4]
print(pop_df.describe())
min = pop_df.min().min()
max = pop_df.max().max()

df_normalized = pop_df.apply(sum_by_value, args=(min,), axis=1)
print(df_normalized)

