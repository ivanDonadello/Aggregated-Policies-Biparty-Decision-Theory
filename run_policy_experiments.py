from src.SimulationsPO import BipartyDT
import os
import pandas as pd
from argparse import ArgumentParser


def sum_by_value(x, y):
    result = (x + abs(y)) + 1
    return result


if __name__ == "__main__":
    parser = ArgumentParser()
    # parser.add_argument('--ds', default='don2022_new', help='input dataset')  # donadello2023UNB don2022
    parser.add_argument('--ds', default='don2022b', help='input dataset')  # donadello2023UNB don2022

    args = parser.parse_args()
    dataset_name = args.ds
    print(f'Running experiments using {dataset_name} dataset')

    bdt = BipartyDT()
    data_folder = "data"
    folder_name = 'datasets_paper'

    folders = os.path.join(data_folder, folder_name)
    # load the whole dataset
    dataset_path = os.path.join(folders, dataset_name)
    donadelloDS = pd.read_csv(dataset_path)

    p_values = [[-2, 'agg'],[-1, 'agg'],[0, 'agg'],[1, 'agg'],[2, 'agg'],[0.1, 'SMD'],[0.3, 'SMD'],
                [0.5, 'SMD'],[0.7, 'SMD'],[0.9, 'SMD'],[-1, 'std']]

    pd.set_option('display.max_rows', None)

    # tree_height
    # ============== SETTING UP THE FIRST COLUMNS OF THE FINAL DATASET ==============
    sim_ds_columns = ['Tree_id', 'Population_id', 'Sample_id', 'tree_height', 'APU (bimax)', 'AOU (bimax)', 'AAD (bimax)']
    for p in p_values:
        sim_ds_columns.append(f'APU ({p[1]}_{p[0]})')
        sim_ds_columns.append(f'AOU ({p[1]}_{p[0]})')
        sim_ds_columns.append(f'AAD ({p[1]}_{p[0]})')

    sim_data = []  # vector/matrix used to append and store raw data (rows) to then construct the pandas DF

    for tree_id in range(10):
        # ============== LOAD TREE and COMPUTE CHANCE/DECISION NODES ==============
        bdt.load_tree(tree_id, fixed_first_node=True, type_first_node='Decision')

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

            # ============== UPDATE UTILITIES ==============
            utility_count = len(prop_df) # to change to the whole DS >> len(df_normalized)
            for row in range(utility_count):  # len(df_normalized)):  # to change to the whole DS >> len(df_normalized)
                bdt.reset_utilities()
                prop_values = prop_df.iloc[row]
                opp_values = opp_df.iloc[row]
                for i in range(len(columns)):
                    bdt.dict_tree[columns[i]].set_utility_proponent(prop_values[i])
                    bdt.dict_tree[columns[i]].set_utility_opponent(opp_values[i])

                # ============== PROPAGATE UTILITY ==============
                bdt.root.propagate_utility("bimaximax", -1, '')

                # ============== (RE)CREATE ROW OF VALUES ==============
                row_result = [tree_id, tree_pop, row, bdt.root.get_tree_height()]
                # ============== APPEND VALUES FOR GIVEN POLICY ==============
                row_result.append(bdt.root.Q_proponent)
                row_result.append(bdt.root.Q_opponent)
                row_result.append(bdt.root.get_AD())

                for p in p_values:  #
                    bdt.root.propagate_utility(policy="aggregated", p=p[0], v=p[1])
                    row_result.append(bdt.root.Q_proponent)
                    row_result.append(bdt.root.Q_opponent)
                    row_result.append(bdt.root.get_AD())

                sim_data.append(row_result)
                # print('prop', bdt.root.Q_proponent)
                # print('opp', bdt.root.Q_opponent)
                # print(row_result)

    sim_ds = pd.DataFrame(data=sim_data,columns=sim_ds_columns)
    sim_ds.to_csv(f'results/policies_experiments_{dataset_name}.csv', encoding='utf-8', index=False)
