import random
import time
from Applications.Tetris.tetris import Tetris
from Source.main import NEATSession
from Source.constants import get_config
from multiprocessing import Process, Pipe


class ParallelTetrisPlayer(object):
    def __init__(self, _child_conn):
        super().__init__()
        self.proc = Process(target=self.play_game)
        self.child_conn = _child_conn

    def start(self):
        self.proc.start()

    def play_game(self):
        while True:

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

    for generation in range(5):

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

        print("Gen: {0}, average fitness: {1}. Generation Time: {2}".format(generation, av_fit, time.time() - start))

        session.collect_individuals(population)
        session.advance_generation()

    parent_conn.send(("stop", []))
    parent_conn2.send(("stop", []))
    parent_conn3.send(("stop", []))
    parent_conn4.send(("stop", []))

    session.show_stats()

"""
Next-step changes:
1. I wonder if I can tweak the mutation rate based on median score progression. 
2. More detailed stats. Median, percentiles, etc.
3. Save the visualization data out to disk every generation
4. A viewer application that can work with the stored data and display only what is wanted. 
5. Change the way species extinction works? Change it to median, or first st. dev. not progressing AND it's in the bottom half
     of all species in rank? Something that avoids (relatively) good species getting killed off. 
6. Num generations to run as a param
7. Save the current best performer in the NEAT session for later viewing. Maybe store 1 per generation?
8. Fix the network graphing issue with different layers having the same y_pos for nodes. 
9. Find a way to visually represent the connection weights on the network graphs
"""

