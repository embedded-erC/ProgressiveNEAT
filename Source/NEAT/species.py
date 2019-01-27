"""
    Module-level docstring start
"""

import Source.constants as consts


class Species(object):
    """
        Class Docstring

        NEAT Responsibilities:
            1. Maintain a list of individuals in the species
            2. Track a representative individual for comparison at reproduction time
            3. Be founded with at least one member
            4. Have a mechanism to set the adjusted fitness for its members  - Do we need this? Does it matter?
            6. Track the sum of the adjusted fitness for its members
            7. Have a mechanism to determine which individuals can reproduce and which will die off (and which will be copied, if any)
            8. Have a mechanism for mating its individuals
            9. Maintain a peak fitness score
            10. Maintain number of generations existed
            11. Maintain number of generations that peak fitness score has not improved
            12. Maintain a species ID
            13. Define a get_representative function for species sorting
        Data Reporting/Visualization Responsibilities:
            1. Track the generation the species was created in
            2. Track the generation the species went extinct
            3. Track/Save the top individual (not just its genome) of the species each generation
    """
    id = 0

    def __init__(self, generation_created, representative):
        super().__init__()

        # Data reporting fields:
        Species.id += 1
        self.id = Species.id
        self.generation_created = generation_created
        self.extinction_generation = 0
        self.champion = None

        self.members = []  # Should never be empty!
        self.representative = representative  # This will be an instance of the Individual class. Must not be None
        self.adjusted_fitness_sum = 0
        self.generations_existed = 0
        self.peak_fitness = 0
        self.num_generations_at_peak = 0

    def _sort_ascending_fitness(self):
        self.members.sort(key=lambda individual: individual.fitness)

    def _save_champion(self):
        self.champion = self.members[-1] if len(self.members) > 5 else None

    def _sum_adjusted_fitnesses(self):
        """
        sum([(individual.fitness / len(self.members)) for individual in self.members])
        :return:
        """
        self.adjusted_fitness_sum = sum([(individual.fitness / len(self.members)) for individual in self.members])

    def select_offspring(self):
        pass

    def mate(self):
        """
        This might take other genomes as arguments and be static. That way I could just use the Species class
        for intraspecies mating

        This should return an new individual which will go into the pool of individuals that will be ready to run
        the next sequence of attempts at the goal.
        :return:
        """
        pass

    def get_representative(self):
        return self.representative.genome

    def update_species(self):
        """
        -Species creation and extinction events will be shown
        -The size of each species will be reported every generation
        -The total fitness (sum of the adjusted fitnesses for each species member) of the species each generation will be tracked
        -The max fitness of the best individual in that species for that generation will be recorded
        -The topology of the best individual for that species for each generation will be visible

        This function is called after all the individuals are evaluated against the performance task and before mating.
        :return:
        """
        self._sort_ascending_fitness()
        self._save_champion()
        self._sum_adjusted_fitnesses()
        # TODO: tally generational changes (new function, most likely)
