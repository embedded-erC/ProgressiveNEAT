"""
Module level docstring stub
"""
import Source.NEAT.functions as functions


def test_compare_genome_compatibility(genome_four_nodes, genome_five_nodes):
    assert functions.compare_genome_compatibility(genome_four_nodes, genome_five_nodes) is False
    assert functions.compare_genome_compatibility(genome_five_nodes, genome_five_nodes) is True


def test_calc_excess_disjoint_genes(genome_four_nodes, genome_five_nodes):
    assert functions._calc_excess_disjoint_genes(genome_four_nodes, genome_five_nodes) == (3, 0)


def test_calc_avg_wt_difference(genome_four_nodes, genome_five_nodes):
    assert functions._calc_avg_wt_difference(genome_four_nodes, genome_five_nodes) == 0.5
    assert functions._calc_avg_wt_difference(genome_five_nodes, genome_four_nodes) == 0.5
