from typing import Dict
import chess
import chess.engine
import numpy as np
from evaluator import Evaluator, StockfishEvaluator

from mcts import mcts, Node


class MCTSPlayer:

    def __init__(self, num_samples: int = 100, eval_type: str = 'naive', eval_args: Dict = {}):
        self.num_samples = num_samples
        
        if eval_type == 'naive':
            self.evaluator = Evaluator()
        if eval_type == 'stockfish':
            self.evaluator = StockfishEvaluator(depth=eval_args['depth'], timout=eval_args['timeout'])

        self.id = {
            'name': 'MCTS'
        }

    def play(self, board: chess.Board) -> chess.engine.PlayResult:
        root = Node()
        root.board = board

        mcts(root=root,
             num_samples=self.num_samples,
             evaluator=self.evaluator)

        move_idx = np.argmax([x.value for x in root.children])

        legal_moves = list(board.legal_moves)
        return chess.engine.PlayResult(move=legal_moves[move_idx],
                                       ponder=None)

    def quit(self):
        pass
