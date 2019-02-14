"""
    Module-level docstring start
"""

import os


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
                -Get a list of all individuals (excluding representatives) for sorting into species
                    -Add to a list from all Species: Species.get_members()
                -Clear out all members of the species excluding representatives
                    -For all species: Species.clear_members()
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

user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
print(user_paths)
