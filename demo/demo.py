from src.BipartyNodeDT import TreeNode
from src.SimulationsAG import BipartyDT
import src.ConsolePrint as ConsolePrint
NaN = float('nan')

if __name__ == "__main__":
    # define the tree
    root = TreeNode("n0", "")
    n2 = TreeNode("n2", "Low red meat consumption is necessary for a healthy diet.")
    n3 = TreeNode("n3", "It is really difficult to change diet.")
    n4 = TreeNode("n4", "I really like the taste of meat.")
    n5 = TreeNode("n5", "Think about the benefits of reducing red meat.")
    n6 = TreeNode("n6", "Try to reduce red meat slowly.")
    n7 = TreeNode("n7", "White meat can be an alternative.")
    n8 = TreeNode("n8", "Fish is a tasty alternative to meat.")
    n5.set_utility_opponent(2)
    n5.set_utility_proponent(7)
    n6.set_utility_opponent(5)
    n6.set_utility_proponent(5)
    n7.set_utility_opponent(3)
    n7.set_utility_proponent(7)
    n8.set_utility_opponent(6)
    n8.set_utility_proponent(6)

    # array of policies to be applied
    policies = [[0, 'agg'], [0.5, 'SMD'], [0.9, 'DON']]

    # Creazione albero
    root.add_child(n2)
    n2.set_children([n3, n4])
    n3.set_children([n5, n6])
    n4.set_children([n7, n8])

    # incapsulamento albero
    bdt = BipartyDT()
    bdt.root = root
    # dict tree l'ho fatta in quanto semplifica il codice di certe funzioni
    bdt.dict_tree = {0: root, 1: n2, 2: n3, 3: n4, 4: n5, 5: n6, 6: n7, 7: n8}

    # operazioni di decision theory sull'albero
    bdt.root.compute_chance_decision(is_decision_node=True, height=0, dict_tree={})
    #bdt.root.compute_chance_decision(is_decision_node=False, height=0, dict_tree={})
    bdt.root.propagate_utility("bimaximax", -1, '')
    ConsolePrint.print_tree(root, 'bimaximax', -1, show_type_node=False)

    for p in policies:  #
        root.propagate_utility("aggregated", p[0], p[1])
        ConsolePrint.print_tree(root, 'aggregated', p, show_type_node=False)

key = bdt.root.dict_tree
print(key.keys())
height = bdt.root.dict_tree[3]
print(bdt.root.get_tree_height())