"""
    Module-level docstring start
"""

import os
import Source.NEAT.genome as genome
import Source.NEAT.species as species
import Source.Visualization.visualization as visualization
from Source.constants import get_config
from Source.NEAT.functions import Functions


class NEATSession(object):
    def __init__(self, inputs, outputs):
        super().__init__()

        self.config = get_config()
        self.functions = Functions(config=self.config)

        self.generation = 0
        self.population = [self.functions.create_initial_individual(inputs, outputs) for individual in range(self.config['kPop_size'])]
        self.species = [species.Species(self.generation, self.population[0], config=self.config)]  # TODO: Make this a dict w/ species ID as the key?
        self.current_unused_innov = self.population[0].genome.get_greatest_innov() + 1
        self.session_stats = visualization.Visualization()

        for individual in self.population[1:]:
            self.species[0].add_member(individual)

    def _choose_species_representatives(self):
        for specie in self.species:
            specie.choose_representative()

    def _gather_offspring(self):
        total_population_fitness = sum([specie.adjusted_fitness_sum for specie in self.species])


    def _gather_visualization_data(self):
        self.session_stats.set_generation(self.generation)
        for specie in self.species:
            self.session_stats.gather_generational_stats(specie.id, specie.report_stats())

    def _mutate_species(self, _innovs_this_generation):
        for specie in self.species:
            self.current_unused_innov = specie.mutate(_innovs_this_generation, self.current_unused_innov)

    def _update_all_species(self):
        for specie in self.species:
            specie.update_species()

    def get_individuals(self):
        self.population = []
        [self.population.extend(specie.get_members()) for specie in self.species]
        return self.population

    def collect_individuals(self, _population):
        self.population = _population

    def advance_generation(self):
        """
        Main NEAT speciation/mutation/mating loop. To be called after all individuals have assigned fitness scores
        :return:
        """
        self.generation += 1
        innovs_this_generation = dict()

        self._update_all_species()
        self._gather_visualization_data()
        self.functions.sort_into_species(self.species, self.population, self.generation)
        self._choose_species_representatives()
        self._mutate_species(innovs_this_generation)

        # TODO: Ok, slight problem here. When i send out the individuals they are removed from their species association
        # TODO: What needs to happen is: Sort_into_species needs to include code to assign a species # to each individual.
        # TODO: When individuals are sent out, species get their members cleared - including the representative
        # TODO: When individuals return with their fitness scores they are placed BACK into their species
        # TODO: Everything in advance_generation proceeds as normal.



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
import random

user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
print(user_paths)
test = NEATSession(2, 2)
test_men = test.get_individuals()
print(len(test_men), len(test.population), len(test.species[0].members))
for man in test_men:
    man.fitness = random.random() * 10000
test.advance_generation()

