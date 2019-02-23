"""
Module-leve docstring stub
"""


class NEATConfigBase(object):
    def __init__(self, config):
        super().__init__()
        self.config = config

        # General
        self.kPop_size = config['kPop_size']
        self.kSigmoid_power = config['kSigmoid_power']
        self.kBias_node = config['kBias_node']

        # Speciation
        self.kCompat_threshold = config['kCompat_threshold']
        self.kExtinction_generation = config['kExtinction_generation']
        self.kCoeff_excess = config['kCoeff_excess']
        self.kCoeff_disjoint = config['kCoeff_disjoint']
        self.kCoeff_wt_diff = config['kCoeff_wt_diff']
        self.kGene_threshold = config['kGene_threshold']
        self.kReproduction_pct = config['kReproduction_pct']
        self.kMin_new_species_size = config['kMin_new_species_size']

        # Mutation
        self.kConn_mut_rate = config['kConn_mut_rate']
        self.kMax_conn_change = config['kMax_conn_change']
        self.kWeight_adjusted_rate = config['kWeight_adjusted_rate']
        self.kRandom_weight_rate = config['kRandom_weight_rate']
        self.kNew_conn_rate = config['kNew_conn_rate']
        self.kNew_node_rate = config['kNew_node_rate']

        # Mating
        self.kConn_still_disabled_rate = config['kConn_still_disabled_rate']
        self.kMutation_only_rate = config['kMutation_only_rate']
        self.kInterspecies_rate = config['kInterspecies_rate']
