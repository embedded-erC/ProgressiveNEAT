from Applications.Tetris.tetris import Tetris
from Source.main import NEATSession
from Source.constants import get_config

if __name__ == '__main__':

    xor_config = get_config("tetris_config")
    session = NEATSession(200, 5, xor_config)

    for generation in range(10000):
        population = session.get_individuals()

        # Insert multiprocessing here...
        for individual in population:

            tetris_game = Tetris(block_queue=[1] * 20)
            game_over, board_state = tetris_game.do_frame(None)

            while not game_over:
                output_vector = individual.evaluate([0] * 200)
                # Do some processing on the output_vector to choose which input to select
                game_over, board_state = tetris_game.do_frame(None)
            individual.fitness = tetris_game.score

        print("The next generation...")

        session.collect_individuals(population)
        session.advance_generation()
