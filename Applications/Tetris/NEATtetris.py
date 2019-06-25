import random
import time
from Applications.Tetris.tetris import Tetris
from Source.main import NEATSession
from Source.constants import get_config

import gc

from multiprocessing import Process, Pipe

# TODO: Size testing code from SO:

import sys
from numbers import Number
from collections import Set, Mapping, deque

zero_depth_bases = (str, bytes, Number, range, bytearray)
iteritems = 'items'


def getsize(obj_0):
    """Recursively iterate to sum size of object & members."""
    _seen_ids = set()

    def inner(obj):
        obj_id = id(obj)
        if obj_id in _seen_ids:
            return 0
        _seen_ids.add(obj_id)
        size = sys.getsizeof(obj)
        if isinstance(obj, zero_depth_bases):
            pass # bypass remaining control flow and return
        elif isinstance(obj, (tuple, list, Set, deque)):
            size += sum(inner(i) for i in obj)
        elif isinstance(obj, Mapping) or hasattr(obj, iteritems):
            size += sum(inner(k) + inner(v) for k, v in getattr(obj, iteritems)())
        # Check for custom object instances - may subclass above too
        if hasattr(obj, '__dict__'):
            size += inner(vars(obj))
        if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
            size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
        return size
    return inner(obj_0)

# TODO: END


class ParallelTetrisPlayer(object):
    def __init__(self, _child_conn):
        super().__init__()
        self.proc = Process(target=self.play_game)
        self.child_conn = _child_conn

    def start(self):
        self.proc.start()

    def play_game(self):
        while True:
            sub_population = None
            block_queue = None
            tetris_game = None
            game_over = None
            board_state = None

            time.sleep(3)

            sub_population, block_queue = self.child_conn.recv()
            if sub_population == "stop":
                break

            for individual in sub_population:
                tetris_game = Tetris(block_queue=block_queue[:])
                game_over, board_state = tetris_game.do_frame(None)

                while not game_over:
                    output_vector = individual.frame(board_state)
                    strongest_signal = output_vector.index(max(output_vector))
                    game_over, board_state = tetris_game.do_frame(strongest_signal)
                individual.fitness = tetris_game.score

            self.child_conn.send(sub_population)

        print("Ending Process")


if __name__ == '__main__':

    xor_config = get_config("tetris_config")
    session = NEATSession(200, 5, xor_config)

    parent_conn, child_conn = Pipe()
    parent_conn2, child_conn2 = Pipe()
    parent_conn3, child_conn3 = Pipe()
    parent_conn4, child_conn4 = Pipe()

    p = ParallelTetrisPlayer(child_conn)
    p2 = ParallelTetrisPlayer(child_conn2)
    p3 = ParallelTetrisPlayer(child_conn3)
    p4 = ParallelTetrisPlayer(child_conn4)

    p.start()
    p2.start()
    p3.start()
    p4.start()

    for generation in range(200):
        population, population_1, population_2, population_3, population_4 = None, None, None, None, None

        gc.collect()
        time.sleep(1)

        standardized_block_queue = [1] * 10 + [0, 0] + [random.choice(range(5)) for i in range(100)]

        start = time.time()
        population = session.get_individuals()

        step = int(len(population) / 4)  # Split the population into thirds and run the evaluations in parallel

        parent_conn.send((population[:step], standardized_block_queue))
        parent_conn2.send((population[step: 2 * step], standardized_block_queue))
        parent_conn3.send((population[2 * step:3 * step], standardized_block_queue))
        parent_conn4.send((population[3 * step:], standardized_block_queue))

        population_1 = parent_conn.recv()
        population_2 = parent_conn2.recv()
        population_3 = parent_conn3.recv()
        population_4 = parent_conn4.recv()

        population = population_1 + population_2 + population_3 + population_4

        av_fit = sum([individual.fitness for individual in population])/len(population)

        # print("Gen: {0}, average fitness: {1}. Generation Time: {2}".format(generation, av_fit, time.time() - start))

        session.collect_individuals(population)
        session.advance_generation()

        # TODO: SIZE TESTING
        print("Total Size: {0}, ID: {1}, num con genes: {2}, num node genes: {3}, size of genome: {4} ".format(
            getsize(population[0]),
                    population[0].id,
                    len(population[0].genome.connection_genes),
                    len(population[0].genome.node_genes),
                    getsize(population[0].genome)))
        # TODO: END

    parent_conn.send(("stop", []))
    parent_conn2.send(("stop", []))
    parent_conn3.send(("stop", []))
    parent_conn4.send(("stop", []))

    session.show_stats()


