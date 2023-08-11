from src.SimulationsPO import BipartyDT
import src.ConsolePrint as ConsolePrint
import os
import pandas as pd

# select the tree
tree_id = 1
# select the population
population_id = 0
# select the row for the given populationDS
row_id = 1
# select the policies
p_values = [[-1, 'agg'], [0.5, 'SMD']]

data_folder = "../data"
folder_name = 'datasets_paper' #'datasets'
dataset_name = 'donadello2023unbalanced'

# load tree
bdt = BipartyDT()
bdt.load_tree(tree_id)


folders = os.path.join(data_folder, folder_name)
# load proponent dataset
dataset_path = os.path.join(folders, dataset_name)
donadelloDS = pd.read_csv(dataset_path)
tree_df = donadelloDS.loc[donadelloDS['tree_id'] == tree_id]
tree_df = tree_df.dropna(axis=1)

# bdt.preproc_dataset(tree_id,population_id)
#print(df_selected.loc[:5])
prop_df = tree_df.loc[tree_df['utility_type'] == 'proponent']
prop_df = prop_df.drop(['tree_id', 'sample_id', 'utility_type'], axis=1)
opp_df = tree_df.loc[tree_df['utility_type'] == 'opponent']
opp_df = opp_df.drop(['tree_id', 'sample_id', 'utility_type'], axis=1)

columns = prop_df.columns

prop_values = prop_df.iloc[row_id]
opp_values = opp_df.iloc[row_id]

for i in range(len(columns)):
    bdt.dict_tree[columns[i]].set_utility_proponent(prop_values[i])
    bdt.dict_tree[columns[i]].set_utility_opponent(opp_values[i])


# summarized results list
result = [f'{"prop"},{"opp"} > {"policie"}']
# propagate utilities
bdt.root.propagate_utility("bimaximax", -1, '')
ConsolePrint.print_tree(bdt.root, 'bimaximax', -1, show_type_node=True)
# append first result
result.append(f'{bdt.root.Q_proponent},{bdt.root.Q_opponent}  > bimax')

for p in p_values:  #
    bdt.root.propagate_utility("aggregated", p[0], p[1])
    result.append(f'{bdt.root.Q_proponent},{bdt.root.Q_opponent} > {p}')
    ConsolePrint.print_tree(bdt.root, 'aggregated', p, show_type_node=True)

print("Summarized Results:")
for i in result:
    print(i)

print('Height',bdt.root.get_tree_height())