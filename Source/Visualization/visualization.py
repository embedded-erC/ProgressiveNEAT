"""
Module level docstring stub
"""


class Visualization(object):
    """
    Class level docstring stub
    -Species tracking:
        -Species creation and extinction events will be shown
        -The size of each species will be reported every generation
        -The total fitness (sum of the adjusted fitnesses for each species member) of the species each generation will be tracked
        -The max fitness of the best individual in that species for that generation will be recorded
        -The topology of the best individual for that species for each generation will be visible

    -Topology visualization:
        -Topology should be derivable from an individual's genome
        -Zones for nodes should be defined as Inputs on the left or bottom, outputs on the right or top, and hidden in between
        -Innovation numbers will be visible for nodes and connections
        -Weights will be visible on connections

    -General Statistics:
        -Total number of individuals spawned will be tracked
        -Current innovation number by generation will be tracked
        -Total number of node evaluations will be recorded by generation
        -A list of all fitnesses for that generation will be saved for optional statistical analysis
        -The number of hidden nodes will be recorded per generation
        -The number of total connections will be recorded per generation
        -The number of disabled connections will be recorded per generation

    -Real-time visualization a-la MarIO for a given ANN?!
        -Future requirement

    Generational data structure:
        Dict:
            Keys = generations
            Values = Species-containing dicts

        Species-containing dicts:
            Keys = Species IDs
            Values = Species Stats

        Species Stats dicts:
            Keys/values = <defined in gather_generational_stats() interface>

        If, for example, you wanted to know the size of species #5 on generation 81, you would request:
            self.generational_stats[81][5]["size"]
    """

    def __init__(self):
        super().__init__()
        self.current_generation = 0
        self.generational_stats = dict()

    def set_generation(self, _generation):
        self.current_generation = _generation
        self.generational_stats[_generation] = dict()

    def gather_generational_stats(self, _species_id, _stats_dict):
        """
        This will interface with Species report_stats() methods.
        Species.report_stats() will return a dict containing the following fields as text dictionary keys:
            1. "size" - the number of individuals in that species in that generation
            2. "species fitness" - the sum total of each individual's performance measure
            3. "peak individual" - full copy of the best performing individual that generation
            4. "extinction generation" - None if an active species, else the generation that it died out
        :return:
        """
        self.generational_stats[self.current_generation].update({_species_id: _stats_dict})
