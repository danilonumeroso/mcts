import chess
from copy import deepcopy

from mcts import StateRepresentation


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


def board_eval_fn(color, stockfish=False, timeout=None):
    if not stockfish:
        def _eval_fn(state):
            winner = state.board.outcome().winner
            if winner is None:
                return 0
            if winner == color:
                return 1

            return -1
    else:
        CLAMP_VALUE = 3000
        engine = chess.engine.SimpleEngine.popen_uci('stockfish')
        
        def _eval_fn(state):
            if state.is_terminal():
                winner = state.board.outcome().winner
                if winner is None:
                    return 0
                if winner == color:
                    return 1

                return -1
            
            else:
                value = engine.analyse(
                    state.board,
                    chess.engine.Limit(time=timeout)
                )['score'].pov(color).score(mate_score=3000)

                cv = CLAMP_VALUE
                value = min(cv, max(value, -cv))
                
                return _normalize(value, x_min=-cv, x_max=cv, range_=(-1, 1))
        
    return _eval_fn
    

def _normalize(x, x_min=0, x_max=1, range_=(0, 1)):
    a, b = range_
    return (b-a) * ((x - x_min) / (x_max - x_min)) + a