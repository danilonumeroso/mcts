import math
import chess
import chess.engine
import random
import pdb
from copy import deepcopy


class Node:

    def __init__(self):
        self.ucb = 100
        self.value = 0
        self.children = []
        self.parent = None
        self.board = None
        self.n = 0

    def is_leaf(self):
        return not self.children


def mcts(root, num_samples, stockfish, depth):
    for _ in range(num_samples):
        color = root.board.turn
        root.n += 1
        node = selection(root)
        node = expansion(node)
        node, value = simulation(node, color, stockfish=stockfish, depth=depth)
        backpropagation(node, value)
        # pdb.set_trace()


def selection(root):
    if root.is_leaf():
        return root

    max_children = []
    max_ucb = float('-inf')
    for i, node in enumerate(root.children):
        if node.ucb > max_ucb:
            max_children = [node]
            max_ucb = node.ucb
        elif node.ucb == max_ucb:
            max_children.append(node)

    child = random.choice(max_children)
    child.n += 1

    return selection(child)


def expansion(node):

    for move in node.board.legal_moves:
        child = Node()
        child.parent = node

        board = deepcopy(node.board)
        board.push(move)
        child.board = board

        node.children.append(child)

    return node


def simulation(node, color, evaluator):

    if not node.board.is_game_over():
        node = random.choice(node.children)
        node.n += 1

        evaluator.init_simulation()
        while evaluator.simulation_finished():
            m = random.choice(list(node.board.legal_moves))
            node.board.push(m)
            evaluator.iterate(node.board)

    return node, evaluator.evaluate(node.board, color)


# def simulation(node, depth, evaluator, color):

#     for _ in depth:
#         m = random.choice(list(node.board.legal_moves))
#         node.board.push(m)

#     return evaluator.analyse(node.board, limit=chess.engine.Limit(time=1))['score'].pov(color)


def backpropagation(node, value):

    while node.parent is not None:
        node.value += value
        node.ucb = ucb(node)
        node = node.parent

    node.value += value


def ucb(node):
    return node.value / node.n + math.sqrt(2) * math.sqrt(math.log2(node.parent.n) / node.n)

# root = Node()
# root.board = chess.Board()

# mcts(root=root,
#      num_samples=25,
#      stockfish=None)
