import chess
import numpy as np
from copy import deepcopy

from mcts import StateRepresentation

STOCKFISH_PATH = '/home/danilo/workspace/mcts/stockfish'


class ChessState(StateRepresentation):

    def __init__(self, board, action):
        self.board = board
        self.action = action

    def get_feasible_actions(self):
        return list(self.board.legal_moves)

    def apply_action(self, action, copy=True):
        if copy:
            board_copy = deepcopy(self.board)
            board_copy.push(action)
            return ChessState(board_copy, action)
        else:
            self.board.push(action)
            self.action = action
            return self

    def is_terminal(self):
        return self.board.is_game_over()


class BoardEvaluator:
    def __init__(self, color, stockfish=False, timeout=1e-10) -> None:
        self.color = color
        if stockfish:
            self.stockfish = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
            self.timeout = timeout
        else:
            self.stockfish = None

    def __call__(self, state):
        if state.is_terminal():
            winner = state.board.outcome().winner
            if winner is None:
                return 0
            if winner == self.color:
                return 1

            return -1
        else:
            value = self.stockfish.analyse(
                state.board,
                chess.engine.Limit(time=self.timeout)
            )['score'].pov(self.color).score(mate_score=3000)

            return np.sign(value)


def board_eval_fn(color, stockfish=False, timeout=None):
    return BoardEvaluator(color, stockfish, timeout)
