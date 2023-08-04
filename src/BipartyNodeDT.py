from __future__ import annotations
import statistics
#import pdb
from operator import attrgetter
import random
from typing import List, Type
import numpy as np


def load_samples(filename: str) -> None:
    samples = np.genfromtxt(filename, delimiter=',', names=True, dtype=None)
    return samples


class TreeNode:
    delta = 1.0

    def __init__(self, _id, text) -> None:
        self.dict_tree = None
        self.labelling: TreeNode = None
        self.text: str = text
        self.height: int = -1
        self.id: str = _id
        self.children: list = []
        self.utility_proponent: int = -1
        self.utility_opponent: int = -1
        self.Q_proponent: int = -1
        self.Q_opponent: int = -1
        self.Q_aggregated: int = -1
        self.is_decision: bool = False # if it is a chance or decision node
        self.location = 0

    def set_utility_proponent(self, value: int) -> None:
        self.utility_proponent = value

    def add_child(self, node: TreeNode) -> None:
        assert isinstance(node, TreeNode)
        self.children.append(node)

    def set_children(self, children: List[TreeNode]) -> None:
        self.children = children

    def set_utility_opponent(self, utility_opponent: int) -> None:
        self.utility_opponent = utility_opponent

    def __str__(self) -> str:
        node_type = "Decision" if self.is_decision is True else "Chance"
        base_str = f"{node_type} node {self.id} - {self.height}:\n{self.text}\n[{self.Q_proponent}, {self.Q_opponent}, " \
                   f"{self.Q_aggregated:.2f}]"
        # for child in self.children:
        #  base_str += f"\n\t{child.id}: {child.text}"
        return base_str

    def compute_chance_decision(self, is_decision_node: bool, height: int, dict_tree) -> None:
        self.is_decision = is_decision_node
        self.height = height
        child_type = False if is_decision_node is True else True
        height += 1
        try:
            dict_tree[self.height].append(self)
        except:
            dict_tree[self.height] = [self]

        for child in self.children:
            if child.isLeaf():
                child_type = False
            child.compute_chance_decision(child_type, height, dict_tree)

        if self.id == 'n0' or self.id == '0':
            self.dict_tree = dict_tree

    def isLeaf(self) -> bool:
        return True if len(self.children) == 0 else False

    def AMax(self, policy: str) -> List[TreeNode]:
        """
        torna i figli del nodo con maxima utilita
        :return:
        """
        output_list = []
        tmp_list = self.children

        if self.is_decision:
            if policy == 'bimaximax':
                key = attrgetter('Q_proponent', 'id')
            else:
                key = attrgetter('Q_aggregated', 'id')
        else:
            key = attrgetter('Q_opponent', 'id')

        tmp_list.sort(key=key, reverse=False)
        max_util_node = tmp_list[-1]
        output_list.append(max_util_node)
        for i in range(0, len(tmp_list) - 1):
            if self.is_decision:
                # if max_util_node.Q_proponent == tmp_list[i].Q_proponent:
                #     output_list.append(tmp_list[i])
                if policy == 'bimaximax':
                    if max_util_node.Q_proponent == tmp_list[i].Q_proponent:
                        output_list.append(tmp_list[i])
                else:
                    if max_util_node.Q_aggregated == tmp_list[i].Q_aggregated:
                        output_list.append(tmp_list[i])

            else:
                if max_util_node.Q_opponent == tmp_list[i].Q_opponent:
                    output_list.append(tmp_list[i])
        return output_list

    def print_post_order(self) -> None:
        for n in self.children:
            n.print_post_order()
        print(self)

    def propagate_utility(self, policy: str, p: float = 0, v: str = 'prod') -> None:
        #print(f'p = {p} | v = {v}')
        for child in self.children:
            child.propagate_utility(policy=policy, p=p, v=v)
        if policy == 'bimaximax':
            if self.isLeaf():  # the node is a leaf
                self.Q_proponent = self.utility_proponent
                self.Q_opponent = self.utility_opponent
            else:
                max_utility_child = self.choose_child(policy)
                self.Q_proponent = self.delta * max_utility_child.Q_proponent
                self.Q_opponent = self.delta * max_utility_child.Q_opponent
            if self.is_decision:
                self.labelling = max_utility_child
        elif policy == 'aggregated':
            if self.isLeaf():  # the node is a leaf

                if v == 'SMD':
                    q_prop = self.utility_proponent
                    q_opp = self.utility_opponent
                    w = p
                    score = ((1 - w) * (q_prop + q_opp)) - (w * abs(q_prop - q_opp))
                    self.Q_aggregated = score

                if v == 'DON':
                    U = [self.utility_proponent,self.utility_opponent]
                    w = p
                    score = (w * np.linalg.norm(U, ord=1) ** 2) - ((1 - w) * np.linalg.norm(U, ord=1))
                    self.Q_aggregated = score

                elif v == 'std':
                    up = self.utility_proponent
                    uo = self.utility_opponent
                    score = np.mean([up, uo]) / (statistics.stdev([up, uo]) + 1)
                    self.Q_aggregated = score

                elif v == 'agg':
                    if p == 0:
                        self.Q_aggregated = np.sqrt(self.utility_proponent * self.utility_opponent)
                    else:
                        self.Q_aggregated = ((1 / 2) * (self.utility_proponent ** p + self.utility_opponent ** p)) ** (1 / p)

                self.Q_proponent = self.utility_proponent
                self.Q_opponent = self.utility_opponent
            else:
                max_utility_child = self.choose_child(policy)
                self.Q_proponent = self.delta * max_utility_child.Q_proponent
                self.Q_opponent = self.delta * max_utility_child.Q_opponent
                self.Q_aggregated = self.delta * max_utility_child.Q_aggregated
            if self.is_decision:
                self.labelling = max_utility_child
        else:
            print(f"Policy {policy} not implemented.")

    def choose_child(self, policy: str, pick_first: bool = False) -> TreeNode:
        """
        torna un figlio a casa del nodo con massima/minima utilita
        :return:
        """
        output_list = self.AMax(policy)

        if pick_first:
            return output_list[0]
        else:
            return random.choice(output_list)

    def get_tree_height(self):
        return list(self.dict_tree.keys())[-1]

    def get_AD(self):
        return abs((self.Q_proponent - self.Q_opponent))

    def get_AVG(self):
        return abs((self.Q_proponent + self.Q_opponent) / 2)
