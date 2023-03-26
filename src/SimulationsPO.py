import settings
from src.BipartyNodeDT import TreeNode
import csv
import re
from graphviz import Digraph
from typing import Dict, Type
import ast
import os

# Class that is used to run Simulations for POlicy/POpulation experiments

class BipartyDT:
    """
    Class for simulating a dialogue
    """
    def __init__(self):
        self.dict_tree: Dict[str, TreeNode] = None
        self.dict_children = {}
        self.root: TreeNode = None
        self.node_results = []
        self.user_model = {}
        self.extra_data = {}

    def reset_opponent_utilities(self):
        for _, node in self.dict_tree.items():
            node.Q_opponent = -1
            node.Q_proponent = -1
            node.Q_aggregated = -1
            node.utility_opponent = -1

    def reset_results(self):
        self.node_results = []

    # def get_leaves(self):
    #     leaf_list = []
    #     leaf_names_list = []
    #     for _, node in self.dict_tree.items():
    #         if node.isLeaf():
    #             leaf_list.append(node)
    #             leaf_names_list.append(node.id)
    #     return leaf_list, leaf_names_list

    def from_csv(self, filename):
        self.dict_tree = {}
        self.dict_children = {}
        self.root = None
        id = "Node_id"
        type = "Type"
        children_ids = "Children_ids"
        utility_p = "Utility_proponent"
        utility_o = "Utility_opponent"

        with open(filename) as f:
            reader = csv.DictReader(f)  # , delimiter='\t')
            for row in reader:
                tmp_node = TreeNode(row[id], row[type])
                tmp_node.set_utility_proponent(int(row[utility_p]))
                tmp_node.set_utility_opponent(int(row[utility_o]))
                self.dict_tree[row[id]] = tmp_node
                self.dict_children[row[id]] = ast.literal_eval(row[children_ids])

        for i in self.dict_children:
            children = self.dict_children[i]
            if len(children) > 0:
                for child in children:
                    self.dict_tree[i].add_child(self.dict_tree[child])

        self.root = self.dict_tree['0']

    def load_tree(self, tree_id):
        self.from_csv(os.path.join(settings.tree_folder, f"tree_{tree_id}.csv"))
        self.root.compute_chance_decision(is_decision_node=True, height=0, dict_tree={})
        #self.dict_tree = self.root.dict_tree





