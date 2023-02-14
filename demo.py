import pdb
from src.BipartyNodeDT import TreeNode
from src.SimulationsAG import BipartyDT
import src.ConsolePrint as ConsolePrint


if __name__ == "__main__":
    root = TreeNode("n0", "")
    n2 = TreeNode("n2", "Low red meat consumption is necessary for a healthy diet.")
    n3 = TreeNode("n3", "It is really difficult to change diet.")
    n4 = TreeNode("n4", "I really like the taste of meat.")
    n5 = TreeNode("n5", "Think about the benefits of reducing red meat.")
    n6 = TreeNode("n6", "Try to reduce red meat slowly.")
    n7 = TreeNode("n7", "White meat can be an alternative.")
    n8 = TreeNode("n8", "Fish is a tasty alternative to meat.")
    n5.set_utility_opponent(3)
    n5.set_utility_proponent(9)
    n6.set_utility_opponent(4)
    n6.set_utility_proponent(6)
    n7.set_utility_opponent(1)
    n7.set_utility_proponent(2)
    n8.set_utility_opponent(2)
    n8.set_utility_proponent(4)

    # Creazione albero
    root.add_child(n2)
    n2.set_children([n4, n3])
    n3.set_children([n5, n6])
    n4.set_children([n7, n8])

    # incapsulamento albero
    bdt = BipartyDT()
    bdt.root = root
    # dict tree l'ho fatta in quanto semplifica il codice di certe funzioni
    bdt.dict_tree = {0: root, 1: n2, 2: n3, 3: n4, 4: n5, 5: n6, 6: n7, 7: n8}

    # operazioni di decision theory sull'albero
    # ---- IMPORTANT -----
    # the dict_tree below is not the same as defined in line 35 (bdt.dict_tree).
    # Is a different dict to calculate the matrix and print it in the console
    bdt.root.compute_chance_decision(is_decision_node=True, height=0, dict_tree={})
    bdt.root.propagate_utility("bimaximax", -1)
    ConsolePrint.print_tree(root, 'bimaximax', -1)

    p_values = [[0, 'geometric'], [-1, 'hm'], [1], [2], [3, 'cubic'], [100, 'prod'], [101, 'mean/std'],
                [102, 'mean/stdev']]

    for p in p_values:    #
        root.propagate_utility("aggregated", p[0])
        ConsolePrint.print_tree(root, 'aggregated', p)



    # printing
    #bdt.to_pdf("prova")
