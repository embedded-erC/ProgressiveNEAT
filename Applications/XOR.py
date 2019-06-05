from Source.main import NEATSession
from Source.constants import get_config


def evaluate_task(_individual):
    neither = _individual.evaluate([0, 0])[0]
    left = _individual.evaluate([1, 0])[0]
    right = _individual.evaluate([0, 1])[0]
    both = _individual.evaluate([1, 1])[0]

    squared_performance = ((1 - neither) + left + right + (1 - both)) ** 2
    _individual.fitness = squared_performance
    return squared_performance


if __name__ == '__main__':

    target_fitness = 15.9995
    best_fitness = 0

    xor_config = get_config("XOR_config")
    session = NEATSession(2, 1, xor_config)

    for generation in range(10000):
        population = session.get_individuals()
        for individual in population:
            performance = evaluate_task(individual)
            if performance > best_fitness:
                best_fitness = performance
        session.collect_individuals(population)
        session.advance_generation()

        print(best_fitness, "Number of species: {0}".format(len(session.species)))
        if best_fitness > target_fitness:
            print("Success on generation {0}".format(generation))
            session.show_stats()
            break
