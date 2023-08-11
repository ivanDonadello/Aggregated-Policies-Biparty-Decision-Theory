import numpy as np

from src.SimulationsPO import BipartyDT
import settings
import os
import pandas as pd
#from sklearn.preprocessing import MinMaxScaler
#import src.ConsolePrint as ConsolePrint

#utility_count = 5

def sum_by_value(x, y):
    result = (x + abs(y)) + 1
    return result

bdt = BipartyDT()
NaN = float('nan')

data_folder = "data_generator"
folder_name = 'datasets_paper' #'datasets'

folders = os.path.join(data_folder, folder_name)
# load the whole dataset
dataset_path = os.path.join(folders, f"donadelloDS")
donadelloDS = pd.read_csv(dataset_path)


#p_values = [[0, 'SMD'],[1, 'SMD'],[0, 'DON'],[0.1, 'DON'],[0.2, 'DON'],[0.3, 'DON'],[0.4, 'DON'],[0.5, 'DON'],[0.6, 'DON'],[0.7, 'DON'],[0.8, 'DON'],[1, 'DON']]
#p_values = [[-1, 'agg'],[0, 'agg'],[1, 'agg'],[0.1, 'SMD'],[0.2, 'SMD'],[0.3, 'SMD'],[0.4, 'SMD'],[0.5, 'SMD'],[0.6, 'SMD'],[0.7, 'SMD'],[0.8, 'SMD'],[0.9, 'SMD'],[0.9, 'DON']]

p_values = [[-2, 'agg'],[-1, 'agg'],[0, 'agg'],[1, 'agg'],[2, 'agg'],[0, 'SMD'],[0.1, 'SMD'],[0.2, 'SMD'],[0.3, 'SMD'],
          [0.4, 'SMD'], [0.5, 'SMD'],[0.6, 'SMD'],[0.7, 'SMD'],[0.8, 'SMD'],[0.9, 'SMD'],[1, 'SMD'],[-1, 'std']]

#p_values = [[-2, 'agg']]



#pd.set_option('display.max_columns', None)  # use only to console print pandas DF
pd.set_option('display.max_rows', None)

# tree_height
# ============== SETTING UP THE FIRST COLUMNS OF THE FINAL DATASET ==============
sim_ds_columns = ['Tree_id', 'Population_id', 'Sample_id', 'tree_height', 'Q_prop (bimax)', 'Q_opp (bimax)', 'AD (bimax)']
for p in p_values:
    sim_ds_columns.append(f'Q_prop ({p[1]}_{p[0]})')
    sim_ds_columns.append(f'Q_opp ({p[1]}_{p[0]})')
    sim_ds_columns.append(f'AD ({p[1]}_{p[0]})')
    #sim_ds_columns.append(f'AVG ({p[1]})')

print(sim_ds_columns)
sim_data = []  # vector/matrix used to append and store raw data (rows) to then construct the pandas DF

for tree_id in range(10):
    #tree_id = 1
    # ============== LOAD TREE and COMPUTE CHANCE/DECISION NODES ==============
    #tree_folder = os.path.join("data_generator", "data_new/DT")
    bdt.load_tree(tree_id, fixed_first_node=True, type_first_node='Decision')
    # ConsolePrint.print_tree(bdt.root, 'bimaximax', -1)

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

        # print(df_population[:20])
        # print(df_normalized[:20])
        # print('-------------------------------------------------------------')
        # ============== UPDATE UTILITIES ==============
        utility_count =  len(prop_df) # to change to the whole DS >> len(df_normalized)
        for row in range(utility_count):  # len(df_normalized)):  # to change to the whole DS >> len(df_normalized)
            bdt.reset_utilities()
            prop_values = prop_df.iloc[row]
            opp_values = opp_df.iloc[row]
            for i in range(len(columns)):
                bdt.dict_tree[columns[i]].set_utility_proponent(prop_values[i])
                bdt.dict_tree[columns[i]].set_utility_opponent(opp_values[i])

            # ============== PROPAGATE UTILITY ==============
            bdt.root.propagate_utility("bimaximax", -1, '')
            # ConsolePrint.print_tree(bdt.root, 'bimaximax', -1)
            # ============== (RE)CREATE ROW OF VALUES ==============
            row_result = [tree_id, tree_pop, row, bdt.root.get_tree_height()]
            # ============== APPEND VALUES FOR GIVEN POLICY ==============
            row_result.append(bdt.root.Q_proponent)
            row_result.append(bdt.root.Q_opponent)
            row_result.append(bdt.root.get_AD())
            #row_result.append(bdt.root.get_AVG())

            for p in p_values:  #
                bdt.root.propagate_utility(policy="aggregated", p=p[0], v=p[1])
                row_result.append(bdt.root.Q_proponent)
                row_result.append(bdt.root.Q_opponent)
                row_result.append(bdt.root.get_AD())
                #row_result.append(bdt.root.get_AVG())

            sim_data.append(row_result)

sim_ds = pd.DataFrame(data=sim_data,columns=sim_ds_columns)
sim_ds.to_csv('results/csv_policy_experiments.csv', encoding='utf-8', index=False)
