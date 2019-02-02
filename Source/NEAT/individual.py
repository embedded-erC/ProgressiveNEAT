"""
    Module-level docstring start
"""


class Individual(object):
    """
        Class Docstring

        NEAT Responsibilities:
            1. Maintain a Genome
            2. Track their fitness each generation
        Data Reporting/Visualization Responsibilities:
            1. Increment and track their global number (Increment on construction, don't copy or rebuild the individuals)
    """
    num_created = 0

    def __init__(self, genome):
        super().__init__()
        Individual.num_created += 1
        self.id = Individual.num_created
        self.genome = genome
        self.fitness = 0

    def evaluate(self, inputs):
        """
        In
        :param inputs:
        :return:
        """
