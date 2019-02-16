"""
Module level docstirng stub
"""

import random
import Source.NEAT.genome as genome
from Source.NEAT.individual import Individual
from Source.NEAT.species import Species
from Source.constants import *


def _calc_excess_disjoint_genes(_genome_one, _genome_two):
    genome_one_genes = _genome_one.get_all_gene_ids()
    genome_two_genes = _genome_two.get_all_gene_ids()

    genome_one_max_innov = _genome_one.get_greatest_innov()
    genome_two_max_innov = _genome_two.get_greatest_innov()

    num_excess_genes = 0
    num_disjoint_genes = 0

    for gene in genome_one_genes:
        if gene not in genome_two_genes:
            if gene > genome_two_max_innov:
                num_excess_genes += 1
            else:
                num_disjoint_genes += 1

    for gene in genome_two_genes:
        if gene not in genome_one_genes:
            if gene > genome_one_max_innov:
                num_excess_genes += 1
            else:
                num_disjoint_genes += 1

    return num_excess_genes, num_disjoint_genes


def _calc_avg_wt_difference(_genome_one, _genome_two):
    num_matching_connections = 0
    total_conn_weight_diff = 0

    for conn_gene in _genome_one.connection_genes:
        if conn_gene in _genome_two.connection_genes:
            num_matching_connections += 1
            total_conn_weight_diff += abs(_genome_one.connection_genes[conn_gene].conn_weight -
                                          _genome_two.connection_genes[conn_gene].conn_weight)
    return total_conn_weight_diff / num_matching_connections


def compare_genome_compatibility(_genome_one, _genome_two):
    """
    cdist = c1(Excess / N) + c2(Disjoint / N) + c3 * AvgWtDiffMatching

    :param _genome_one:
    :param _genome_two:
    :return:
    True if cdist is less than kCompat_threshold, else False
    """

    highest_num_genes = max(_genome_one.get_genome_size(), _genome_two.get_genome_size())
    highest_num_genes = 1 if highest_num_genes < kGene_threshold else highest_num_genes

    num_excess_genes, num_disjoint_genes = _calc_excess_disjoint_genes(_genome_one, _genome_two)
    avg_wt_diff = _calc_avg_wt_difference(_genome_one, _genome_two)

    return kCompat_threshold > (kCoeff_excess * (num_excess_genes / highest_num_genes) +
                                kCoeff_disjoint * (num_disjoint_genes / highest_num_genes) +
                                kCoeff_wt_diff * avg_wt_diff)


def create_initial_individual(_inputs, _outputs):
    _inputs += 1 if kBias_node else 0

    first_genome = genome.Genome()
    innov_num = 1

    for input_node in range(_inputs):
        first_genome.node_genes[innov_num] = genome.NodeGene(node_type='input', innov_num=innov_num)
        innov_num += 1
    for output_node in range(_outputs):
        first_genome.node_genes[innov_num] = genome.NodeGene(node_type='output', innov_num=innov_num)
        innov_num += 1

    for in_node in first_genome.node_genes.values():
        if in_node.node_type == 'input':
            for out_node in first_genome.node_genes.values():
                if out_node.node_type == 'output':
                    first_genome.connection_genes[innov_num] = genome.ConnectionGene(in_node.innov_num,
                                                                                     out_node.innov_num,
                                                                                     random.gauss(0, 1),
                                                                                     innov_num=innov_num)
                    innov_num += 1
    return Individual(first_genome)


def sort_into_species(all_species, _individuals, _current_generation):
    """
    *Note this function may append to the list passed as all_species
    :param all_species:
    :param _individuals:
    :param _current_generation:
    :return:
    """

    for individual in _individuals:
        found_species_match = False
        for single_species in all_species.values():
            if compare_genome_compatibility(single_species.get_representative_genome(), individual.genome):
                single_species.add_member(individual)
                found_species_match = True
                break
        if not found_species_match:
            new_species = Species(_current_generation, individual)
            all_species[new_species.id] = new_species
