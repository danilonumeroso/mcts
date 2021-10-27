import itertools
import math

from challenge import MCTSvsMCTS


NUM_SAMPLES = [50, 100, 500]
C = [math.sqrt(2), 2, math.sqrt(8), 4]
DEPTH_STOCKFISH = [(20, True), (40, True), (-1, False)]


remotes = []
for ns1, c1, ds1 in itertools.product(NUM_SAMPLES, C, DEPTH_STOCKFISH):
    for ns2, c2, ds2 in itertools.product(NUM_SAMPLES, C, DEPTH_STOCKFISH):

        if ns1 == ns2 and ds1[0] == ds2[0]:
            continue

        p1_dict = {'num_samples': ns1, 'depth': ds1[0], 'c': c1, 'stockfish': ds1[1]}
        p2_dict = {'num_samples': ns2, 'depth': ds2[0], 'c': c2, 'stockfish': ds2[1]}

        MCTSvsMCTS(p1_dict, p2_dict)
