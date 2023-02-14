from src.BipartyNodeDT import TreeNode
from src.SimulationsAG import BipartyDT
import src.ConsolePrint as ConsolePrint

if __name__ == "__main__":

    root = TreeNode("n0", "")
    n4 = TreeNode("n4", "I really like the taste of meat.")
    n7 = TreeNode("n7", "White meat can be an alternative.")
    n8 = TreeNode("n8", "Fish is a tasty alternative to meat.")

    # leaf1 = [5, 5]
    # leaf2 = [3, 7]
    leaf1 = [7, 3]
    leaf2 = [3, 2]

    n7.set_utility_opponent(leaf1[0])
    n7.set_utility_proponent(leaf1[1])
    n8.set_utility_opponent(leaf2[0])
    n8.set_utility_proponent(leaf2[1])

    # n7.set_utility_opponent(8)
    # n7.set_utility_proponent(1)
    # n8.set_utility_opponent(7)
    # n8.set_utility_proponent(8)

    # Creazione albero
    root.add_child(n4)
    n4.set_children([n7, n8])
    root.compute_chance_decision(is_decision_node=True, height=0, dict_tree={})

    root.propagate_utility("bimaximax", -1)

    ConsolePrint.print_tree(root, 'bimaximax', -1)

    p_values = [[0, 'geometric'], [-1, 'hm'], [1], [2], [3, 'cubic'], [100, 'prod'], [101, 'mean/std'],
                [102, 'mean/stdev']]

    for p in p_values:  #
        root.propagate_utility("aggregated", p[0])
        ConsolePrint.print_tree(root, 'aggregated', p)

