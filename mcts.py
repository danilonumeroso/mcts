import random
import math
from copy import deepcopy
import numpy as np


def monte_carlo_tree_search(state, num_samples, sim_depth, evaluate_fn):
    root = Node(state, None)
    for _ in range(num_samples):
        leaf = _selection(root)
        if not leaf.state.is_terminal():
            _expansion(leaf)
            leaf = random.choice(leaf.children)
            leaf.n += 1

            terminal_state = _simulation(leaf.state, sim_depth)
        else:
            terminal_state = leaf.state

        _backpropagation(leaf, evaluate_fn(terminal_state))
    best_child = np.argmax([x.value for x in root.children])
    
    return best_child.state.action
    

        
def _selection(root):
    if root.is_leaf():
        return root

    max_children = []
    max_ucb = float('-inf')
    curr_node = root
    curr_node.n += 1
    while not curr_node.is_leaf():

        for node in root.children:
            if node.ucb > max_ucb:
                max_children = [node]
                max_ucb = node.ucb
            elif node.ucb == max_ucb:
                max_children.append(node)
        curr_node = random.choice(max_children)
        curr_node.n += 1

    return curr_node


def _expansion(node):
    for action in node.state.feasible_actions():
        next_state = node.state.apply_action(action)
        child = Node(next_state, node)
        node.children.append(child)


def _simulation(state, sim_depth):
    state = deepcopy(state)
    depth = 0
    while (sim_depth == -1 or depth < sim_depth) and not state.is_terminal():
        action = random.choice(state.get_feasible_actions)
        state = state.apply_action(action, copy=False)
        depth += 1
    
    return state


def _backpropagation(leaf, value):
    curr_node = leaf
    while curr_node.parent is not None:
        curr_node.value += value
        curr_node.ucb = ucb(curr_node)
        curr_node = curr_node.parent

    curr_node.value += value


def ucb(node):
    return node.value / node.n + math.sqrt(2) * math.sqrt(math.log2(node.parent.n) / node.n)


class Node:

    def __init__(self, state, parent):
        self.parent = parent
        self.children = []

        self.state = state

        self.value = 0
        self.ucb = 100

    def is_leaf(self):
        return not self.children


class StateRepresentation:

    def __init__(self, state):
        self._state = state
    
    def get_feasible_actions(self):
        pass

    def apply_action(self, action, copy=True):
        pass

    def is_terminal(self):
        pass