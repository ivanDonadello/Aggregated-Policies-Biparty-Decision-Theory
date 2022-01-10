import pdb
from src.BipartyNodeDT import TreeNode
from src.SimulationsAG import BipartyDT
import settings
import os

if __name__ == "__main__":
    for tree_id in settings.num_trees:
        bdt = BipartyDT()
        bdt.from_csv(os.path.join(settings.tree_folder, f"tree_{tree_id}"))
        bdt.root.compute_chance_decision(is_decision_node=True, height=0)
        tree_leaves = bdt.get_leaves()
        tree_number_leaves = len(tree_leaves)
        tree_height = tree_leaves[0].height
        for population_id in settings.num_populations:


            # Parte 1: lo scaling
            # carica il file delle utilità di popolazione (usa sempre os.path.join)
            # puoi usare np.genfromtxt per caricare il file in una tabella oppure anche pandas
            # trova il minimo escludendo la colonna degli id e la prima riga
            # somma alla tabella caricata (escludendo la colonna degli id e la prima riga) il minimo trovato sopra + 1

            # Parte 2: il bottom up
            # per ogni sample nella tabella caricata
                # metti nell'albero le corrispondenti utilità della popolazione
                # va implementata una nuova funzione in SimulationsAG che puoi chiamare set_util_opp(sample)
                for policy in settings.policies:
                    bdt.propagate_utility(policy[0], policy[1])
                    # salvare le Q (opp e prop alla root) per ogni sample in una tabella risultati con le seguenti colonne:
                    # sample_id, tree_id, tree_height, tree_number_leaves, population_id, policy, root_Q_opp, root_Q_prop


            # Parte 3: plot tramite heatmap della tabella dei risultati
            # da fare, forse meglio creare una classe dedicata in un file a parte dentro src
