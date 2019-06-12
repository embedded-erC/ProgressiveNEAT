import random
import time
from Applications.Tetris.tetris import Tetris
from Source.main import NEATSession
from Source.constants import get_config

from multiprocessing import Process, Pipe


def play_game(child_conn, _standardized_block_queue):
    population = child_conn.recv()

    for individual in population:
        tetris_game = Tetris(block_queue=_standardized_block_queue[:])
        game_over, board_state = tetris_game.do_frame(None)

        while not game_over:
            output_vector = individual.frame(board_state)
            strongest_signal = output_vector.index(max(output_vector))
            game_over, board_state = tetris_game.do_frame(strongest_signal)
        individual.fitness = tetris_game.score

    child_conn.send(population)


if __name__ == '__main__':

    xor_config = get_config("tetris_config")
    session = NEATSession(200, 5, xor_config)

    for generation in range(800):

        standardized_block_queue = [1] * 10 + [0, 0] + [random.choice(range(5)) for i in range(100)]

        start = time.time()
        population = session.get_individuals()

        step = int(len(population) / 4)  # Split the population into thirds and run the evaluations in parallel
        first = population[:step]
        second = population[step: 2 * step]
        third = population[2 * step:3 * step]
        fourth = population[3 * step:]
        split_population = [first, second, third, fourth]

        parent_conn, child_conn = Pipe()
        parent_conn2, child_conn2 = Pipe()
        parent_conn3, child_conn3 = Pipe()
        parent_conn4, child_conn4 = Pipe()

        p = Process(target=play_game, args=(child_conn, standardized_block_queue[:]))
        p2 = Process(target=play_game, args=(child_conn2, standardized_block_queue[:]))
        p3 = Process(target=play_game, args=(child_conn3, standardized_block_queue[:]))
        p4 = Process(target=play_game, args=(child_conn4, standardized_block_queue[:]))

        p.start()
        p2.start()
        p3.start()
        p4.start()

        parent_conn.send(first)
        parent_conn2.send(second)
        parent_conn3.send(third)
        parent_conn4.send(fourth)

        population_1 = parent_conn.recv()
        population_2 = parent_conn2.recv()
        population_3 = parent_conn3.recv()
        population_4 = parent_conn4.recv()

        p.join()
        p2.join()
        p3.join()
        p4.join()

        population = population_1 + population_2 + population_3 + population_4

        print("Generation: {0}".format(generation), time.time() - start)

        session.collect_individuals(population)
        session.advance_generation()

        time.sleep(5)

    session.show_stats()


