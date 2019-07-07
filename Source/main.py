"""
    Module-level docstring start
"""

import random
import Source.NEAT.species as species
import Source.Persistence.persistence as persistence
import Source.Visualization.visualization as visualization
from Source.constants import get_config
from Source.NEAT.functions import Functions


class NEATSession(object):
    def __init__(self, inputs, outputs, _config=None):
        super().__init__()

        self.config = get_config() if not _config else _config
        self.functions = Functions(config=self.config)
        self.persistence = persistence.Persistence(self.config)

        self.generation = 0
        self.population = self._get_initial_population(inputs, outputs)
        self.current_unused_innov = self.population[0].genome.get_greatest_innov() + 1
        self.session_stats = visualization.Visualization()
        self.current_champion = None

        # TESTING:
        self.all_innovs = dict()

        first_species = species.Species(self.generation, self.population[0], config=self.config)
        self.species = {first_species.id: first_species}

        for individual in self.population[1:]:
            self.species[first_species.id].add_member(individual)

    def _get_initial_population(self, _inputs, _outputs):
        if self.config['kLoad_saved_genomes']:
            return self.persistence.load_genomes()
        else:
            return [self.functions.create_initial_individual(_inputs, _outputs) for individual in range(self.config['kPop_size'])]

    def _choose_species_representatives(self):
        for specie in self.species.values():
            specie.choose_representative()

    def _eliminate_extinct_species(self):  # TODO: TEST ME
        extinct_species_keys = [specie.id for specie in self.species.values() if
                                specie.extinction_generation]
        for specie in extinct_species_keys:
            dead_one = self.species.pop(specie)
            print("EXTINCTION!!! ", dead_one.adjusted_fitness_sum, dead_one.peak_fitness, dead_one.generations_existed,
                  dead_one.rank)

    def _interspecies_mate(self):
        hybrid_offspring = []
        if len(self.species) >= 2:
            for num_hybrid_offspring in range(round(self.config['kInterspecies_rate'] * self.config['kPop_size'])):
                species1, species2 = random.sample(list(self.species.values()), 2)
                hybrid_offspring.append(
                    species1.mate(random.choice(species1.members), random.choice(species2.members)))
        return hybrid_offspring

    def _mate_and_gather_offspring(self):
        total_population_fitness = sum([specie.adjusted_fitness_sum for specie in self.species.values()])
        hybrid_offspring = self._interspecies_mate()
        for specie in self.species.values():
            num_offspring = round((specie.adjusted_fitness_sum / total_population_fitness) * self.config['kPop_size'])
            num_offspring = max(5, num_offspring)
            specie.select_offspring(num_offspring)  # Refreshes each species' members with new offspring
        for hybrid in hybrid_offspring:
            lucky_specie = random.choice(list(self.species.values()))
            lucky_specie.add_member(hybrid)

    def _gather_visualization_data(self):
        fitness_scores = []
        self.session_stats.set_generation(self.generation)
        for specie in self.species.values():
            self.session_stats.gather_species_generational_stats(specie.id, specie.report_stats())
            [fitness_scores.append(member.fitness) for member in specie.members]
        self.session_stats.gather_overall_generational_stats({'overall peak fitness': self.current_champion.fitness,
                                                              'current champion': self.current_champion,
                                                              'fitness scores': fitness_scores})

    def _mutate_species(self, _innovs_this_generation):
        for specie in self.species.values():
            self.current_unused_innov = specie.mutate(_innovs_this_generation, self.current_unused_innov)

    def _rank_speices(self):  # TODO: TEST ME
        species_peak_fitnesses = [(specie.peak_fitness, specie.id) for specie in self.species.values()]
        for enum_species_fitness in enumerate(sorted(species_peak_fitnesses, reverse=True), start=1):
            # enum_species_fitness looks like:  (enum_num, (peak_fitness, species.id))
            # So enum_species_fitness[1][1]] gives you the species ID
            self.species[enum_species_fitness[1][1]].rank = enum_species_fitness[0]

    def _set_overall_peak_fitness(self):
        if not self.current_champion:
            self.current_champion = self.species[1].members[-1]

        for specie in self.species.values():
            if specie.members[-1].fitness > self.current_champion.fitness:
                self.current_champion = specie.members[-1]

    def _update_all_species(self):
        for specie in self.species.values():
            specie.update_species()

    def get_individuals(self):
        """
        When individuals are given to the outside manager, strip them from their species associations.
        Reassign them when they return.
        :return:
        """
        self.population = []
        for specie in self.species.values():
            self.population.extend(specie.get_members())
            specie.clear_members(_keep_representative=False)
        return self.population

    def collect_individuals(self, _population):
        """
        The individuals have returned from fitness evaluations. Place them back into their species.
        :param _population:
        :return:
        """
        for _individual in _population:
            self.species[_individual.assigned_specie].add_member(_individual)

    def advance_generation(self):
        """
        Main NEAT speciation/mutation/mating loop. To be called after all individuals have assigned fitness scores
        :return:
        """
        self.generation += 1

        # TODO: TESTING
        # innovs_this_generation = dict()

        self._update_all_species()
        self._eliminate_extinct_species()
        self._set_overall_peak_fitness()
        self._gather_visualization_data()
        self._rank_speices()
        self._choose_species_representatives()
        self.functions.sort_into_species(self.species, self.population, self.generation)
        self._mutate_species(self.all_innovs)
        self._mate_and_gather_offspring()

        # TODO: Move all this to functions and have no methods that are not required for the external interface
        # TODO: Get tests in place for all of those functions.

    def show_stats(self, winner=None):
        self.session_stats.graph_stats(winner)


if __name__ == "__main__":
    """
    Algorithm Flow:
        - Spin all this off in a separate thread so I can control it from the outside?
        0. Load configuration data
        1. Generate initial population

        2. Enter Algorithm main loop:
        
            Will need to define an interface for outside apps to use these network objects. I think I'll have to
            send out Individuals (which means they will need extra, supporting methods) as the unit to be manipulated
            by the outside code. The client code will use the individuals for frames (inputting an array that is sent
            to the input nodes and getting out an array from the output nodes), then also populate the individual with
            it's performance measure after the run. It will get a bolus of individuals (size depending on how parallel 
            we can run client code), which it will return to the main network module for generational advancement.
        
        
                -Get a list of all individuals (excluding representatives) for sorting into species
                    -Add to a list from all Species: Species.get_members()
                -Clear out all members of the species excluding representatives
                    -For all species: Species.clear_members()
            3. Evaluate each network against the goal (play the game, try the XOR, whatever)  
                
                -TODO: Write the algorithm (with charts) for network evaluation
                
                -Will probably have to split this into multiprocess/multithread to have a chance.
                -This will populate the individuals with their fitness scores
            4. Update and Repopulate Species
                -Calculate and set stats (top performer, generations existed, etc)
                    -For all species: Species.update_species()
                -Gather data report from the visualization module (inc. saving any individuals for later inspection)
                    -Visualization.set_generation() with the current generation 
                    -For all species: visualization.gather_generational_stats(species.id, species.report_stats())

                -Sort individuals into species
                    -functions.sort_into_species(species_list, individuals_list, current_generation)
                -Choose representatives from among members
                    -For all species: Species.choose_representative()
            5. Reproduce
                
                -Mutate
                    -Track this generation's innovations!
                    -Eliminate lowest performers per species (select reproducers)
                    -kConn_mut_rate to mutate connections. If this happens:
                        -kWeight_adjusted_rate per connection to perturb uniformly
                        -1.0 - kWeight_adjusted_rate for new, random connection weight
                    -kNode_new_rate chance to add a node.
                    -kConn_new_rate to add a new connection w/ a random weight
                    
                -Mate
                    -Assign number of new offspring per species, proportional to adjusted fitness
                        -Rounded up. Total before rounding will be kPop_size
                        -New species get at least 5 slots
                    -Champions are used for mating
                    -kMutation_only_rate chance that an offspring slot will be from mutation only. 
                    -kInterspecies_rate chance that an offspring slot will be from interspecies mating
                    -Choose pairs to mate
                -Gather offspring
                    -return a list that includes champions and all mated and mutated genomes in new individuals (where not copied)
                    
                        
            6. Build genome topologies in prep for step (3) again.      
                
    """
