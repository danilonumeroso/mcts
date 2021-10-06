from typing import Dict
import chess
import chess.engine
import numpy as np

from mcts import monte_carlo_tree_search
from chess_logic import board_eval_fn, ChessState


class MCTSPlayer:

    def __init__(self,
                 num_samples,
                 depth,
                 stockfish
                 ):
        self.num_samples = num_samples
        self.depth = depth
        self.stockfish = stockfish
        self.eval_fn = None
        
        self.id = {
            'name': f"{num_samples}_{depth}_{'T' if stockfish else 'F'}"
        }

    def play(self, board: chess.Board) -> chess.engine.PlayResult:
        root_state = ChessState(board, None)

        move = monte_carlo_tree_search(state=root_state,
                                       num_samples=self.num_samples,
                                       sim_depth=self.depth,
                                       evaluate_fn=self.eval_fn)

        return move

    def quit(self):
        if self.stockfish:
            self.eval_fn.stockfish.quit()
    
    def set_color(self, color):
        self.eval_fn = board_eval_fn(color, self.stockfish, timeout=0.0001)