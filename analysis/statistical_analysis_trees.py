import ast
import pandas as pd
import numpy as np

def calculate_tree_metrics(csv_file):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Calculate tree depth
    def calculate_tree_depth(node_id):
        children_ids = ast.literal_eval(df.loc[df['Node_id'] == node_id, 'Children_ids'].values[0])
        if children_ids:
            return max(calculate_tree_depth(int(child_id)) for child_id in children_ids) + 1
        return 1

    root_id = df.loc[df['Type'] == 'root', 'Node_id'].values[0]
    depth = calculate_tree_depth(root_id) - 1

    # Calculate tree length (number of nodes)
    length = len(df)

    # Calculate tree width (number of leaf nodes)
    width = len(df.loc[df['Children_ids'] == '[]'])

    # Calculate average branching factor
    total_branching_factor = np.sum(df['Children_ids'].apply(lambda x: len(ast.literal_eval(x))))
    average_branching_factor = total_branching_factor / (length - width)

    # Calculate number of branches
    num_branches = np.sum(df['Children_ids'].apply(lambda x: len(ast.literal_eval(x))))

    # Calculate maximum branching factor
    max_branching_factor = np.max(df['Children_ids'].apply(lambda x: len(ast.literal_eval(x))))

    # Calculate node type count
    node_type_count = df['Type'].value_counts().to_dict()

    # Return the calculated metrics
    return {
        'Tree height': depth,
        'Tree Length': length,
        'Tree Width': width,
        'Average Branching Factor': average_branching_factor,
        'Maximum Branching Factor': max_branching_factor,
        #'Node Type Count': node_type_count
    }

pd.set_option('display.max_columns', None)  # use only to console print pandas DF
pd.set_option('display.max_rows', None)

dict_metrics = {}
for i in range(10):
    #print(f'Tree {i}')
    file_path = f'../data/DT/tree_{i}.csv'
    metrics = calculate_tree_metrics(file_path)
    dict_metrics[i] = metrics
    #print(metrics)

df_metrics = pd.DataFrame(dict_metrics)
sorted_df = df_metrics.sort_values(df_metrics.first_valid_index(),axis=1).astype('int')
print(df_metrics.astype('int'))
print()
print(sorted_df)

sorted_df.T.to_csv('trees_metrics.csv')







