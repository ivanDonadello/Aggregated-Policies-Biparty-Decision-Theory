import numpy as np

from src.SimulationsPO import BipartyDT
import settings
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import src.ConsolePrint as ConsolePrint

utility_count = 5

def sum_by_value(x, y):
    result = (x + abs(y)) + 1
    return result



bdt = BipartyDT()
NaN = float('nan')

p_values = [[-1, '-1'], [0, '0'], [1, '1'], [2, '2'], [3, '3']]  # , [NaN, 'mean/std'],[NaN, 'mean/stdev']]

#pd.set_option('display.max_columns', None)  # use only to console print pandas DF
pd.set_option('display.max_rows', None)

# tree_height
# ============== SETTING UP THE FIRST COLUMNS OF THE FINAL DATASET ==============
sim_ds_columns = ['Tree_id', 'Population_id', 'Sample_id', 'tree_height', 'Q_prop (bimax)', 'Q_opp (bimax)', 'AD (bimax)']
for p in p_values:
    sim_ds_columns.append(f'Q_prop ({p[1]})')
    sim_ds_columns.append(f'Q_opp ({p[1]})')
    sim_ds_columns.append(f'AD ({p[1]})')

print(sim_ds_columns)
sim_data = []  # vector/matrix used to append and store raw data (rows) to then construct the pandas DF

for tree_id in range(1):

    # ============== LOAD TREE and COMPUTE CHANCE/DECISION NODES ==============
    bdt.load_tree(tree_id)
    # ConsolePrint.print_tree(bdt.root, 'bimaximax', -1)

    for tree_pop in range(1):
        # ============== LOAD POPULATION ==============
        path_pop = os.path.join(settings.population_folder, f"tree_{tree_id}_population_{tree_pop}.csv")
        df_population = pd.read_csv(path_pop)
        df_population = df_population.drop('id', axis=1)
        df_population = df_population.drop(index=0)
        columns = df_population.columns.values

        min_val = df_population.min()

        print('Tree > id: {} | pop: {} | min_val: {}'.format(tree_id, tree_pop, min_val))

        df_normalized = df_population.apply(sum_by_value, args=(min_val,), axis=1)
        # df_normalized = df_population.copy()
        # scaler = MinMaxScaler(feature_range=(1, 11))
        # df_normalized.iloc[:, :] = scaler.fit_transform(df_normalized.iloc[:,:].to_numpy()) #df_normalized.iloc[:, 0:-1].apply(lambda x: (x - x.mean()) / x.std(), axis=0)
        # df_normalized = np.around(df_normalized[columns])

        # print(df_population[:20])
        # print(df_normalized[:20])
        # ============== UPDATE UTILITIES ==============
        utility_count = 1# len(df_normalized) # to change to the whole DS >> len(df_normalized)
        for col in range(utility_count):  # len(df_normalized)):  # to change to the whole DS >> len(df_normalized)
            bdt.reset_opponent_utilities()
            columns_values = df_normalized.iloc[col]
            for i in range(len(columns)):
                bdt.dict_tree[columns[i]].set_utility_opponent(columns_values[i])

            # ============== PROPAGATE UTILITY ==============
            bdt.root.propagate_utility("bimaximax", -1, '')
            # ConsolePrint.print_tree(bdt.root, 'bimaximax', -1)
            # ============== (RE)CREATE ROW OF VALUES ==============
            row_result = [tree_id, tree_pop, col, bdt.root.get_tree_height()]
            # ============== APPEND VALUES FOR GIVEN POLICY ==============
            row_result.append(bdt.root.Q_proponent)
            row_result.append(bdt.root.Q_opponent)
            row_result.append(bdt.root.get_AD())

            for p in p_values:  #
                bdt.root.propagate_utility("aggregated", p[0], p[1])
                row_result.append(bdt.root.Q_proponent)
                row_result.append(bdt.root.Q_opponent)
                row_result.append(bdt.root.get_AD())

            sim_data.append(row_result)

sim_ds = pd.DataFrame(data=sim_data,columns=sim_ds_columns)
sim_ds.to_csv('csv_policy_experiments.csv', encoding='utf-8', index=False)
