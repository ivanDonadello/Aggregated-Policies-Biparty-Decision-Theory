from src.SimulationsPO import BipartyDT
import src.ConsolePrint as ConsolePrint

# select the tree
tree_id = 2
# select the population
population_id = 5
# select the row for the given populationDS
row_id = 0
# select the policies
p_values = [[-1, '-1'], [0.5, 'SMD']]

# load tree
bdt = BipartyDT()
bdt.load_tree(tree_id)
bdt.preproc_dataset(tree_id,population_id)
bdt.set_utilities(row_id)

# summarized results list
result = [f'{"opp"},{"prop"} > {"policie"}']
# propagate utilities
bdt.root.propagate_utility("bimaximax", -1, '')
ConsolePrint.print_tree(bdt.root, 'bimaximax', -1)
# append first result
result.append(f'{bdt.root.Q_opponent}, {bdt.root.Q_proponent} > bimax')

for p in p_values:  #
    bdt.root.propagate_utility("aggregated", p[0], p[1])
    result.append(f'{bdt.root.Q_opponent}, {bdt.root.Q_proponent} > {p}')
    ConsolePrint.print_tree(bdt.root, 'aggregated', p, show_id=False)

print("Summarized Results:")
for i in result:
    print(i)