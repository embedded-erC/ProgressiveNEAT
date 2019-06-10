import random
import time
from Applications.Tetris.tetris import Tetris
from Source.main import NEATSession
from Source.constants import get_config


if __name__ == '__main__':

    xor_config = get_config("tetris_config")
    session = NEATSession(200, 5, xor_config)

    for generation in range(100):

        start = time.time()

        population = session.get_individuals()

        standardized_block_queue = [1] * 15 + [random.randrange(0, 5) for i in range(500)]

        # Insert multiprocessing here...
        for individual in population:

            tetris_game = Tetris(block_queue=standardized_block_queue[:])
            game_over, board_state = tetris_game.do_frame(None)

            while not game_over:
                output_vector = individual.frame(board_state)
                strongest_signal = output_vector.index(max(output_vector))
                game_over, board_state = tetris_game.do_frame(strongest_signal)
            individual.fitness = tetris_game.score

        print("Generation: {0}".format(generation), time.time() - start)

        session.collect_individuals(population)
        session.advance_generation()

    session.show_stats()
