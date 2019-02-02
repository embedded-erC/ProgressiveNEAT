"""
    Module level docstring stub

    ...so the idea here is to load an .ini style config file that will specify the parameters of the NEAT session
    to be run. The config parser layer will take the text file, process it, and output some module-level constants
    to be used across the rest of the NEAT space

    # Config fields:
    # With the exception of the Visualization section, all fields are mandatory. No defaults are provided
    [General]
    population size = 150
    transfer function power = -4.9

    [Speciation]
    # compatibility_distance = c1(Excess_genes / Num_genes) + c2(Disjoint_genes / Num_genes) + c3 * AvgWtDiffMatching
    # AvgWtDiffMatching is the average wt difference for all matching genes between the genomes, including disabled genes
    c1 = 1.0
    c2 = 1.0
    c3 = 0.4
    gene counting threshold = 20
    compatibility threshold = 3.0
    extinction generation = 15

    [Mutation]
    # Chances in pct / 100. So 0.8 is an 80% chance of occurrence
    connection mutation chance = 0.8
    uniform weight change chance = 0.9
    random new weight chance = 0.1
    new node chance = 0.03
    new connection chance = 0.05

    [Mating]
    gene disabled if disabled in a parent chance = 0.75
    percent offspring from mutation only = 0.25
    interspeces mating rate = 0.01

    [Visualization]

"""

import configparser

config = configparser.ConfigParser()
config.read('/home/erc/PycharmProjects/ProgressiveNEAT/config')

try:

    # General
    kPop_size = int(config['General']['population size'])
    kSigmoid_power = float(config['General']['transfer function power'])

    # Speciation
    kCompat_threshold = float(config['Speciation']['compatibility threshold'])
    kExtinction_generation = int(config['Speciation']['extinction generation'])
    kCoeff_excess = float(config['Speciation']['c1'])
    kCoeff_disjoint = float(config['Speciation']['c2'])
    kCoeff_wt_diff = float(config['Speciation']['c3'])
    kGene_threshold = int(config['Speciation']['gene counting threshold'])

    # Mutation
    kConn_mut_rate = float(config['Mutation']['connection mutation chance'])
    kWeight_adjusted_rate = float(config['Mutation']['uniform weight change chance'])
    kRandom_weight_rate = float(config['Mutation']['random new weight chance'])
    kConn_new_rate = float(config['Mutation']['new connection chance'])
    kNode_new_rate = float(config['Mutation']['new node chance'])

    # Mating
    kConn_still_disabled_rate = float(config['Mating']['gene disabled if disabled in a parent chance'])
    kMutation_only_rate = float(config['Mating']['percent offspring from mutation only'])
    kInterspecies_rate = float(config['Mating']['interspecies mating rate'])

except (ValueError, KeyError) as err:
    print("Invalid Parameters! Check your NEAT config settings. Aborting.")
    quit(err)

# TODO: Also get some tests up for the config
