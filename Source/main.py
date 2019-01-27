"""
    Module-level docstring start
"""


import Source.NEAT.functions as functions


def sort_into_species(_individuals):


    # Maintain an ordered list of species
    # After fitness evaluations are complete, choose a representative (at random per species among it's members)
    # Iterate through the individuals:
        # If they return True from compare_genome_compat() then add them to the species.members field (or the method for this)
        # If we run to the end of the list, found a new species with that individual as the representative.
    functions.compare_genome_compatibility()
    pass


if __name__ == "__main__":
    """
    Algorithm Flow:
        - Spin all this off in a separate thread so I can control it from the outside?
        0. Load configuration data
        1. Generate initial population

        2. Enter Algorithm main loop:
            3. Evaluate each network against the goal (play the game, try the XOR, whatever)
                -Will probably have to split this into multiprocess/multithread to have a chance.
                -This will populate the individuals with their fitness scores
            4. Update Species
                -Calculate and set stats (top performer, generations existed, etc)
                -Choose representatives from among members
                -Sort individuals into species
            5. Gather data report from the visualization module (includes saving any individuals for later inspection)
            6. Mutate (?? Mate first ??)
            7. Mate (?? Mutate first ??)
            8. Build genome topologies in prep for step (3) again.      
    """

import os
user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
print(user_paths)
