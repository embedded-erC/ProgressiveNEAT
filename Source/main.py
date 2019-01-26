"""
    Module-level docstring start
"""

# TODO: REMOVE THIS INTO PART OF THE TESTING MODULE
import Source.NEAT.genome as genome
# TODO

import Source.NEAT.functions as functions


def sort_into_species(_individuals):
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
            4. Sort the individuals into their species
            5. Gather data report from the visualization module (includes saving any individuals for later inspection)
            6. Mutate (?? Mate first ??)
            7. Mate (?? Mutate first ??)
            8. Build genome topologies in prep for step (3) again.      
    """

import os
user_paths = os.environ['PYTHONPATH'].split(os.pathsep)
print(user_paths)