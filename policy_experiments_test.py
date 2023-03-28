from src.SimulationsPO import BipartyDT
import src.ConsolePrint as ConsolePrint

tree_id = 2
population_id = 1
row_id = 0
p_values = [[-1, '-1'], [0, '0'], [1, '1'], [2, '2'], [3, '3']]  # , [NaN, 'mean/std'],[NaN, 'mean/stdev']]

bdt = BipartyDT()
bdt.load_tree(tree_id)
print(bdt.root.dict_tree)
ConsolePrint.print_tree(bdt.root, 'bimaximax', -1)

bdt.preproc_dataset(tree_id,population_id)
bdt.set_utilities(row_id)

bdt.root.propagate_utility("bimaximax", -1, '')
ConsolePrint.print_tree(bdt.root, 'bimaximax', -1)

for p in p_values:  #
    bdt.root.propagate_utility("aggregated", p[0], p[1])
    ConsolePrint.print_tree(bdt.root, 'aggregated', p, show_id=True)