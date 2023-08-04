import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set(style="whitegrid")
plt.figure(figsize=(6, 5))

for tree_id in range(10):
    prop_ds = pd.read_csv(f'../data_generator/datasets_paper/tree_{tree_id}_proponent.csv')
    opp_ds  = pd.read_csv(f'../data_generator/datasets_paper/tree_{tree_id}_opponent.csv')
    prop = prop_ds.values
    opp = opp_ds.values
    stack = np.stack((prop,opp)).T
    for value in stack:
        plt.scatter(value[:, 0], value[:, 1], color='#4660AC')

    plt.xlabel('Proponent utility')
    plt.ylabel('Opponent utility')
    plt.axis('equal')

plt.savefig('UB_ds.pdf')
plt.show()
