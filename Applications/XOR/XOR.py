from Source.main import NEATSession
from Source.constants import get_config
import random


def evaluate_task(_individual):

    inputs = {
        'neither': [0, 0],
        'left': [1, 0],
        'right': [0, 1],
        'both': [1, 1]
    }

    options = list(inputs.keys())
    random.shuffle(options)
    for choice in options:
        inputs[choice] = individual.evaluate(inputs[choice])[0]

    squared_performance = ((1 - inputs['neither']) + inputs['left'] + inputs['right'] + (1 - inputs['both'])) ** 2
    _individual.fitness = squared_performance


if __name__ == '__main__':

    target_fitness = 14

    xor_config = get_config("XOR_config")
    session = NEATSession(2, 1, xor_config)

    for generation in range(10000):
        population = session.get_individuals()
        for individual in population:
            evaluate_task(individual)
        session.collect_individuals(population)
        session.advance_generation()

        print(session.current_champion.fitness, "Number of species: {0}".format(len(session.species)))
        if session.current_champion.fitness > target_fitness:
            print("Success on generation {0}".format(generation))
            session.show_stats(session.current_champion)
            break
