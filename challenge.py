import random
import fire
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
                   verbose=False,
                   callback=None):

    board = chess.Board()
    game = chess.pgn.Game()
    moves = []

    white, black = (player_1, player_2) if random.uniform(0, 1) >= 0.5 else (player_2, player_1)

    game.headers["Event"] = f"Game {game_id}"
    game.headers["Site"] = "Virtual"
    game.headers["White"] = white.id['name']
    game.headers["Black"] = black.id['name']

    for i in range(max_moves//2):
        player = white if board.turn else black

        m = player.play(board, chess.engine.Limit(time=time_per_move)).move

        if verbose:
            print(board.san(m))

        board.san_and_push(m)
        moves.append(m)

        if callback:
            callback(board)

        if board.is_game_over():
            break

    if record_game:
        game.add_line(moves)

        with open(f"{save_dir}/game_{game_id}.pgn", "w", encoding="utf-8") as f:
            exporter = chess.pgn.FileExporter(f)
            game.accept(exporter)

    player_1.quit()
    player_2.quit()


def MCTSvsMCTS():

    stockfish = chess.engine.SimpleEngine.popen_uci('stockfish')

    p1 = MCTSPlayer(num_samples=100, stockfish=stockfish)
    p2 = MCTSPlayer(num_samples=50, stockfish=stockfish)

    play_contender(p1,
                   p2,
                   save_dir='.',
                   game_id='test',
                   verbose=True,
                   time_per_move=1e-10)


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
    fire.Fire(MCTSvsHuman)
