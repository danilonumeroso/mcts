import chess
import chess.engine
import numpy as np

from mcts import mcts, Node


class MCTSPlayer:

    def __init__(self, num_samples=100, stockfish=None):
        self.num_samples = num_samples
        self.stockfish = stockfish
        self.id = {
            'name': 'MCTS'
        }

    def play(self, board: chess.Board, limit=None) -> chess.engine.PlayResult:
        root = Node()
        root.board = board

        mcts(root=root,
             num_samples=self.num_samples,
             stockfish=self.stockfish)

        move_idx = np.argmax([x.value for x in root.children])

        legal_moves = list(board.legal_moves)
        return chess.engine.PlayResult(move=legal_moves[move_idx],
                                       ponder=None)

    def quit(self):
        pass
