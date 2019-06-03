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
    bias node = yes

    [Speciation]
    # compatibility_distance = c1(Excess_genes / Num_genes) + c2(Disjoint_genes / Num_genes) + c3 * AvgWtDiffMatching
    # AvgWtDiffMatching is the average wt difference for all matching genes between the genomes, including disabled genes
    c1 = 1.0
    c2 = 1.0
    c3 = 0.4
    gene counting threshold = 20
    compatibility threshold = 3.0
    extinction generation = 15
    minimum new species size = 4

    # Take this percentage of the best performers as the basis for the next generation
    percentage allowed to reproduce = 0.75

    [Mutation]
    # Chances in pct / 100. So 0.8 is an 80% chance of occurrence
    connection mutation chance = 0.8
    max connection change = 0.3
    uniform weight change chance = 0.9
    # random new weight chance = 1.0 - uniform weight change chance
    new node chance = 0.03
    new connection chance = 0.05

    [Mating]
    gene disabled if disabled in a parent chance = 0.75
    percent offspring from mutation only = 0.25
    interspeces mating rate = 0.01

    [Visualization]

"""

import os
import configparser


def get_config(_config_name=''):

    config = configparser.ConfigParser()
    config_name = _config_name if _config_name else "pytest_config"
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, config_name))

    config.read(config_path)
    config_dict = dict()

    try:
        # General
        config_dict['kPop_size'] = int(config['General']['population size'])
        config_dict['kSigmoid_power'] = float(config['General']['transfer function power'])
        config_dict['kBias_node'] = config['General'].getboolean('bias node')

        # Speciation
        config_dict['kCompat_threshold'] = float(config['Speciation']['compatibility threshold'])
        config_dict['kExtinction_generation'] = int(config['Speciation']['extinction generation'])
        config_dict['kCoeff_excess'] = float(config['Speciation']['c1'])
        config_dict['kCoeff_disjoint'] = float(config['Speciation']['c2'])
        config_dict['kCoeff_wt_diff'] = float(config['Speciation']['c3'])
        config_dict['kGene_threshold'] = int(config['Speciation']['gene counting threshold'])
        config_dict['kReproduction_pct'] = float(config['Speciation']['percentage allowed to reproduce'])
        config_dict['kMin_new_species_size'] = int(config['Speciation']['minimum new species size'])

        # Mutation
        config_dict['kConn_mut_rate'] = float(config['Mutation']['connection mutation chance'])
        config_dict['kMax_conn_change'] = float(config['Mutation']['max connection change'])  # TODO: What should this range be?
        config_dict['kWeight_adjusted_rate'] = float(config['Mutation']['uniform weight change chance'])
        config_dict['kRandom_weight_rate'] = 1 - config_dict['kWeight_adjusted_rate']
        config_dict['kNew_conn_rate'] = float(config['Mutation']['new connection chance'])
        config_dict['kNew_node_rate'] = float(config['Mutation']['new node chance'])

        # Mating
        config_dict['kConn_still_disabled_rate'] = float(config['Mating']['gene disabled if disabled in a parent chance'])
        config_dict['kMutation_only_rate'] = float(config['Mating']['percent offspring from mutation only'])
        config_dict['kInterspecies_rate'] = float(config['Mating']['interspecies mating rate'])

    except (ValueError, KeyError) as err:
        print("Invalid Parameters! Check your NEAT config settings. Aborting.")
        quit(err)

    return config_dict
    # TODO: Also get some tests up for the config
