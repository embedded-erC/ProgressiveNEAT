"""
    Module-level docstring start
"""

import os


def sort_into_species(_individuals):

    # Maintain an ordered list of species
    # After fitness evaluations are complete, choose a representative (at random per species among it's members)
    # Iterate through the individuals:
        # If they return True from compare_genome_compat() then add them to the species.members field (or the method for this)
        # If we run to the end of the list, found a new species with that individual as the representative.

    # functions.compare_genome_compatibility()
    pass


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
                
                # TODO: When evaluating through the network, if a node has only itself or zero inbound connections,
                # TODO: send out a pulse of 0.0 to all outbound connections to prevent network lock.       
                
                Here add to assemble_topology to add the outbound connection wts to a new NodeGene param, 
                outbound_weights. outbound_weights will be multiplied by the activation pulse strength, then zipped
                with the outbound_connections to notify the next series of nodes. 
                
                Also thinking I can order all nodes in a genome by layer, then simply iterate though them all from
                lowest to highest layer (put them in an ordered dict?), notifying all outbound nodes of inbound
                connection pulses. Will have to handle recursion and island cases here.
                
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
                -Mutate (Mate first?!)
                -Mate (Mutate first?!)
            6. Build genome topologies in prep for step (3) again.      
                
    """

user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
print(user_paths)
