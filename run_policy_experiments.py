from src.SimulationsPO import BipartyDT
import settings
import os
import pandas as pd


def sum_by_value(x, y):
    return (x + abs(y)) + 1


bdt = BipartyDT()
NaN = float('nan')

p_values = [[-1, '-1'], [0, '0'], [1, '1'], [2, '2'], [3, '3']]  # , [NaN, 'mean/std'],[NaN, 'mean/stdev']]

# pd.set_option('display.max_columns', None)  # use only to console print pandas DF
# pd.set_option('display.max_rows', None)

# tree_height
# ============== SETTING UP THE FIRST COLUMNS OF THE FINAL DATASET ==============
sim_ds_columns = ['Tree_id', 'Population_id', 'Sample_id', 'tree_height', 'Q_prop (bimax)', 'Q_opp (bimax)', 'AD (bimax)']
for p in p_values:
    sim_ds_columns.append(f'Q_prop ({p[1]})')
    sim_ds_columns.append(f'Q_opp ({p[1]})')
    sim_ds_columns.append(f'AD ({p[1]})')

print(sim_ds_columns)
sim_data = []  # vector/matrix used to append and store raw data (rows) to then construct the pandas DF

for tree_id in range(10):

    # ============== LOAD TREE and COMPUTE CHANCE/DECISION NODES ==============
    bdt.load_tree(tree_id)

    for tree_pop in range(10):
        # ============== LOAD POPULATION ==============
        path_pop = os.path.join(settings.population_folder, f"tree_{tree_id}_population_{tree_pop}.csv")
        ds_population = pd.read_csv(path_pop)
        ds_population = ds_population.drop('id', axis=1)
        ds_population = ds_population.drop(index=0)
        columns = ds_population.columns.values

        min_val = ds_population.min().min()
        print('Tree > id: {} | pop: {} | min_val: {}'.format(tree_id, tree_pop, min_val))

        df_normalized = ds_population.apply(sum_by_value, axis=1, args=(min_val,))

        # ============== UPDATE UTILITIES ==============
        for col in range(5):  # len(df_normalized)):  # to change to the whole DS >> len(df_normalized)
            bdt.reset_opponent_utilities()
            columns_values = df_normalized.iloc[col]
            for i in range(len(columns)):
                bdt.dict_tree[columns[i]].set_utility_opponent(columns_values[i])

            # ============== PROPAGATE UTILITY ==============
            bdt.root.propagate_utility("bimaximax", -1, '')
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
