import chess


class Evaluator:

    def __init__(self):
        self.simulation_finished = False


    def evaluate(self, board, color):
        winner = board.outcome().winner
        if winner is None:
            return 0
        if winner == color:
            return 1
            
        return -1

    def init_simulation(self):
        pass

    def iterate(self, board):
        self.simulation_finished = board.is_game_over() == True
    


class StockfishEvaluator(Evaluator):

    CLAMP_VALUE=3000

    def __init__(self, depth, timeout):
        self._max_depth = depth
        self._timeout = timeout
        self._engine = chess.engine.SimpleEngine.popen_uci('stockfish')
        self._curr_depth = 0
    
    def evaluate(self, board, color):
        if board.is_game_over():
            return super(StockfishEvaluator, self).evaluate(board, color)

        value = self._engine.analyse(
                board,
                chess.engine.Limit(time=self._timeout)
            )['score'].pov(color).score(mate_score=3000)

        cv = StockfishEvaluator.CLAMP_VALUE
        value = min(cv, max(value, -cv))
        _normalize(value,
                   x_min=-cv,
                   x_max=cv,
                   range_=(-1, 1))

        return value

    def init_simulation(self):
        self._curr_depth = 0
    
    def iterate(self, board):
        self.depth += 1
        self.simulation_finished = board.is_game_over() or self._curr_depth >= self._max_depth


def _normalize(x, x_min=0, x_max=1, range_=(0, 1)):
    a, b = range_
    return (b-a) * ((x - x_min) / (x_max - x_min)) + a