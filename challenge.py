import random
import math
import pickle
from typing import Dict
import chess
import chess.pgn
import chess.engine

from mcts_player import MCTSPlayer
from human_player import HumanPlayer


def play_contender(player_1,
                   player_2,
                   max_moves=512,
                   time_per_move=0.001,
                   record_game=True,
                   save_dir=None,
                   game_id=None,
                   verbose=True,
                   callback=None):

    board = chess.Board()
    game = chess.pgn.Game()
    moves = []

    white, black = (player_1, player_2) if random.uniform(0, 1) >= 0.5 else (player_2, player_1)
    white.set_color('White')
    black.set_color('Black')

    game.headers["Event"] = f"Game {game_id}"
    game.headers["Site"] = "Virtual"
    game.headers["White"] = white.id['name']
    game.headers["Black"] = black.id['name']

    for i in range(max_moves//2):
        player = white if board.turn else black

        m = player.play(board)

        if verbose:
            print(board.san(m))

        board.san_and_push(m)
        moves.append(m)

        if callback:
            callback(board)

        if board.is_game_over():
            break

    player_1.quit()
    player_2.quit()
    if record_game:
        game.add_line(moves)

        with open(f"{save_dir}/game_{game_id}.pgn", "w", encoding="utf-8") as f:
            exporter = chess.pgn.FileExporter(f)
            game.accept(exporter)

        with open(f"{save_dir}/match_stats_{game_id}.pkl", "wb") as f:
            dict_ = {
                'white': {
                    'num_samples': white.num_samples,
                    'depth': white.depth,
                    'stockfish': white.stockfish
                },
                'black': {
                    'num_samples': black.num_samples,
                    'depth': black.depth,
                    'stockfish': black.stockfish
                },
                'winner': str(board.outcome().winner).lower() if board.outcome().winner is not None else "Draw",
                'moves': i
            }
            pickle.dump(dict_, f, protocol=pickle.HIGHEST_PROTOCOL)


def MCTSvsMCTS(p1: Dict = {'num_samples': 100000, 'depth': 20, 'c': math.sqrt(2), 'stockfish': True},
               p2: Dict = {'num_samples': 1000, 'depth': -1, 'c': math.sqrt(2), 'stockfish': False}
               ):

    p1_string = f"{p1['num_samples']}_{p1['depth']}_{p1['c']:.4f}_{'T' if p1['stockfish'] else 'F'}"
    p2_string = f"{p2['num_samples']}_{p2['depth']}_{p2['c']:.4f}_{'T' if p2['stockfish'] else 'F'}"

    p1 = MCTSPlayer(p1['num_samples'], p1['depth'], p1['c'], p1['stockfish'])
    p2 = MCTSPlayer(p2['num_samples'], p2['depth'], p2['c'], p2['stockfish'])

    play_contender(p1,
                   p2,
                   save_dir='./games',
                   game_id=f"{p1_string}_{p2_string}",
                   verbose=True,
                   time_per_move=1e-10)

    return 0


def MCTSvsHuman():

    stockfish = chess.engine.SimpleEngine.popen_uci('stockfish')

    p1 = MCTSPlayer(num_samples=1000, stockfish=stockfish)
    p2 = HumanPlayer()

    play_contender(p1,
                   p2,
                   save_dir='.',
                   game_id='test',
                   verbose=True,
                   time_per_move=1e-10)


if __name__ == "__main__":
    MCTSvsMCTS()
