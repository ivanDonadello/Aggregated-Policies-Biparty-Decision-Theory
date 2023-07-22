from src.SimulationsPO import BipartyDT
import src.ConsolePrint as ConsolePrint
import os
import pandas as pd

# select the tree
tree_id = 1
# select the population
population_id = 0
# select the row for the given populationDS
row_id = 0
# select the policies
p_values = [[-1, '-1'], [0.5, 'SMD']]

data_folder = "../data_generator"
folder_name = 'datasets_paper' #'datasets'

# load tree
bdt = BipartyDT()
bdt.load_tree(tree_id)

pop_folder = os.path.join(data_folder, folder_name)
# load proponent dataset
path_pop = os.path.join(pop_folder, f"tree_{tree_id}_proponent.csv")
df_proponent = pd.read_csv(path_pop)
# load opponent dataset
path_pop = os.path.join(pop_folder, f"tree_{tree_id}_opponent.csv")
df_opponent = pd.read_csv(path_pop)
columns = df_opponent.columns.values
# bdt.preproc_dataset(tree_id,population_id)
prop_values = df_proponent.iloc[row_id]
opp_values = df_opponent.iloc[row_id]

for i in range(len(columns)):
    bdt.dict_tree[columns[i]].set_utility_proponent(prop_values[i])
    bdt.dict_tree[columns[i]].set_utility_opponent(opp_values[i])


# summarized results list
result = [f'{"prop"},{"opp"} > {"policie"}']
# propagate utilities
bdt.root.propagate_utility("bimaximax", -1, '')
ConsolePrint.print_tree(bdt.root, 'bimaximax', -1)
# append first result
result.append(f'{bdt.root.Q_proponent},{bdt.root.Q_opponent}  > bimax')

for p in p_values:  #
    bdt.root.propagate_utility("aggregated", p[0], p[1])
    result.append(f'{bdt.root.Q_proponent},{bdt.root.Q_opponent} > {p}')
    ConsolePrint.print_tree(bdt.root, 'aggregated', p, show_id=False)

print("Summarized Results:")
for i in result:
    print(i)