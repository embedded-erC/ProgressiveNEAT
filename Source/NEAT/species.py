"""
    Module-level docstring start
"""

import copy
import random
from Source.NEAT.genome import Genome
from Source.NEAT.individual import Individual
from Source.NEAT.NEATConfigBase import NEATConfigBase


class Species(NEATConfigBase):
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
            13. Define a get_representative_genome function for species sorting
            14. Define a choose_representative function that randomly selects an individual for species sorting comparisons
            15. Define an Update Species function <THAT DOES WHAT>
            16. Define a clear_members function <THAT DOES WHAT>
            17. Define a report_stats method that transfers generational stats data to the visualization library
            18. Define an add_member function for sorting individuals into species
        Data Reporting/Visualization Responsibilities:
            1. Track the generation the species was created in
            2. Track the generation the species went extinct
            3. Track/Save the top individual (not just its genome) of the species each generation
    """
    id = 0

    def __init__(self, generation_created, representative, **kwargs):
        super().__init__(**kwargs)

        # Data reporting fields:
        Species.id += 1
        self.id = Species.id
        self.generation_created = generation_created
        self.extinction_generation = None
        self.champion = None
        self.rank = 0

        representative.assigned_specie = self.id
        self.members = [representative]  # Should never be empty!
        self.representative = representative  # This will be an instance of the Individual class. Must not be None
        self.adjusted_fitness_sum = 0
        self.generations_existed = 0
        self.peak_fitness = 0
        self.num_generations_at_peak = 0

    def _eliminate_lowest_performers(self):
        self._sort_fitness_ascending()
        self.members = self.members[round(len(self.members) * (1 - self.kReproduction_pct)):]

    def _save_champion(self):
        self.champion = copy.deepcopy(self.members[-1]) if len(self.members) > 5 else None

    def _sort_fitness_ascending(self):
        self.members.sort(key=lambda individual: individual.fitness)

    def _sum_adjusted_fitness(self):
        """
        sum([(individual.fitness / len(self.members)) for individual in self.members])
        :return:
        """
        self.adjusted_fitness_sum = sum([(individual.fitness / len(self.members)) for individual in self.members])

    def _update_generations_and_fitness_peak(self):
        """

        :return:
        """
        self.generations_existed += 1
        if self.members[-1].fitness > self.peak_fitness:
            self.peak_fitness = self.members[-1].fitness
            self.num_generations_at_peak = 1
        else:
            self.num_generations_at_peak += 1
        if self.num_generations_at_peak >= self.kExtinction_generation and not self.extinction_generation and self.rank > 5:
            self.extinction_generation = self.generation_created + self.generations_existed

    def add_member(self, _new_individual):
        _new_individual.assigned_specie = self.id
        self.members.append(_new_individual)

    def select_offspring(self, _num_assigned_offspring):
        """
        Thinking this can work as follows:
        1. Based on this species' relative fitness, it will be assigned a number of offspring
        2. It will first copy over the number required by mutation only
        3. It will then fill the rest with offspring from random pairs of mated genomes
        :return:
        """
        all_offspring = []
        if len(self.members) == 1:
            for ii in range(self.kMin_new_species_size):
                all_offspring.append(copy.deepcopy(self.members[0]))
        else:
            if self.champion:
                all_offspring.append(self.champion)
            random.shuffle(self.members)
            all_offspring += self.members[:round(self.kMutation_only_rate * _num_assigned_offspring)]
            while len(all_offspring) < _num_assigned_offspring:
                parents = random.sample(self.members, k=2)
                all_offspring.append(self.mate(parents[0], parents[1]))

        self.clear_members(_keep_representative=False)
        [self.add_member(offspring) for offspring in all_offspring]

    def mate(self, _mother, _father):
        """
        This might take other genomes as arguments and be static. That way I could just use the Species class
        for intraspecies mating

        This should return an new individual which will go into the pool of individuals that will be ready to run
        the next sequence of attempts at the goal.
        :param _mother:
        :param _father:
        :return:
        """
        offspring_genome = Genome(config=self.config)
        if _father.fitness > _mother.fitness:
            # Mother always has the higher fitness
            _mother, _father = _father, _mother

        for node_gene_id in _mother.genome.node_genes:
            if node_gene_id in _father.genome.node_genes:
                offspring_genome.node_genes[node_gene_id] = copy.deepcopy(
                    random.choice([_mother.genome.node_genes[node_gene_id],
                                   _father.genome.node_genes[node_gene_id]]))
            else:
                offspring_genome.node_genes[node_gene_id] = copy.deepcopy(_mother.genome.node_genes[node_gene_id])

        for conn_gene_id in _mother.genome.connection_genes:
            if conn_gene_id in _father.genome.connection_genes:
                new_conn = copy.deepcopy(
                    random.choice([_mother.genome.connection_genes[conn_gene_id],
                                   _father.genome.connection_genes[conn_gene_id]]))
                if (_mother.genome.connection_genes[conn_gene_id].enabled is False or
                    _father.genome.connection_genes[conn_gene_id] is False) and \
                        random.random() < self.kConn_still_disabled_rate:
                    new_conn.enabled = False
                else:
                    new_conn.enabled = True
                offspring_genome.connection_genes[conn_gene_id] = new_conn
                # TODO: TEST DISABLED RATE
            else:
                offspring_genome.connection_genes[conn_gene_id] = copy.deepcopy(
                    _mother.genome.connection_genes[conn_gene_id])
        return Individual(offspring_genome, self.kBias_node)

    def mutate(self, innovs_this_generation, current_unused_innov):
        self._eliminate_lowest_performers()
        for individual in self.members:
            if random.random() < self.kConn_mut_rate:
                individual.genome.mutate_connections()
            if random.random() < self.kNew_node_rate:
                current_unused_innov = individual.genome.add_node(innovs_this_generation, current_unused_innov)
            if random.random() < self.kNew_conn_rate:
                current_unused_innov = individual.genome.add_connection(innovs_this_generation, current_unused_innov)
            individual.genome.assemble_topology()
        return current_unused_innov

    def choose_representative(self):
        self.representative = random.choice(self.members)

    def clear_members(self, _keep_representative=True):
        self.members = [self.representative] if _keep_representative else []

    def get_representative_genome(self):
        return self.representative.genome

    def get_members(self, _include_representative=True):
        if _include_representative:
            return self.members
        else:
            return [individual for individual in self.members if individual != self.representative]

    def report_stats(self):
        """
        This method will interface with the Visualization.gather_generational_stats() method.

        :return: stats dictionary
        """
        self._sort_fitness_ascending()  # So we don't rely on function calling order outside of this class

        stats = dict()
        stats["size"] = len(self.members)
        stats["species fitness"] = self.adjusted_fitness_sum * len(self.members)
        stats['peak fitness'] = self.peak_fitness
        stats["peak individual"] = copy.deepcopy(self.members[-1])
        stats["extinction generation"] = self.extinction_generation
        stats["average connections"] = sum([len(member.genome.connection_genes) for member in self.members]) / len(self.members)
        stats["average nodes"] = sum([len(member.genome.node_genes) for member in self.members]) / len(self.members)
        return stats

    def update_species(self):
        """
        This function is called after all the individuals are evaluated against the performance task and before mating.
        :return:
        """
        self._sort_fitness_ascending()
        self._save_champion()
        self._sum_adjusted_fitness()
        self._update_generations_and_fitness_peak()
