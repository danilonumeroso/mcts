import math
import chess
import chess.engine
import random
import pdb
from copy import deepcopy

MAX_DEPTH = 20
CLAMP_VALUE = 3000

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


def mcts(root, num_samples, stockfish):
    for _ in range(num_samples):
        color = root.board.turn
        root.n += 1
        node = selection(root)
        node = expansion(node)
        node, value = simulation(node, color,
                                 stockfish=stockfish, depth=10)  # , depth, stockfish, color)
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


def simulation(node, color, stockfish=None, depth=10):

    if not node.board.is_game_over():
        node = random.choice(node.children)
        node.n += 1

        while not node.board.is_game_over() and depth > 0:
            m = random.choice(list(node.board.legal_moves))
            node.board.push(m)
            depth -= 1

        if stockfish is not None and not node.board.is_game_over():
            value = stockfish.analyse(
                node.board,
                chess.engine.Limit(time=1e-10)
            )['score'].pov(color).score(mate_score=3000)

            value = min(CLAMP_VALUE, max(value, -CLAMP_VALUE))
            normalize(value,
                      x_min=-CLAMP_VALUE,
                      x_max=CLAMP_VALUE,
                      range_=(-1, 1))
            return node, value

    if node.board.outcome().winner is None:
        return node, 0

    if node.board.outcome().winner == color:
        return node, 1

    return node, -1


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


def normalize(x, x_min=0, x_max=1, range_=(0, 1)):
    a, b = range_
    return (b-a) * ((x - x_min) / (x_max - x_min)) + a

# root = Node()
# root.board = chess.Board()

# mcts(root=root,
#      num_samples=25,
#      stockfish=None)
