"""
Module level docstring stub
"""


import Source.NEAT.individual as individual
import Source.NEAT.species as species
from Source.constants import get_config


def test_compare_genome_compatibility(functions_object, genome_four_nodes, genome_five_nodes):
    assert functions_object.compare_genome_compatibility(genome_four_nodes, genome_five_nodes) is False
    assert functions_object.compare_genome_compatibility(genome_five_nodes, genome_five_nodes) is True


def test_calc_excess_disjoint_genes(functions_object, genome_four_nodes, genome_five_nodes):
    assert functions_object._calc_excess_disjoint_genes(genome_four_nodes, genome_five_nodes) == (3, 0)


def test_calc_avg_wt_difference(functions_object, genome_four_nodes, genome_five_nodes):
    assert functions_object._calc_avg_wt_difference(genome_four_nodes, genome_five_nodes) == 0.5
    assert functions_object._calc_avg_wt_difference(genome_five_nodes, genome_four_nodes) == 0.5


def test_sort_into_species(functions_object, genome_four_nodes, genome_six_nodes):
    i_four_1 = individual.Individual(genome_four_nodes, config=get_config())
    i_four_2 = individual.Individual(genome_four_nodes, config=get_config())
    i_four_3 = individual.Individual(genome_four_nodes, config=get_config())

    i_six_1 = individual.Individual(genome_six_nodes, config=get_config())
    i_six_2 = individual.Individual(genome_six_nodes, config=get_config())

    s1 = species.Species(0, i_four_1, config=get_config())

    individuals = [i_four_1, i_four_2, i_four_3, i_six_1, i_six_2]
    all_species = {s1.id: s1}

    functions_object.sort_into_species(all_species, individuals, 1)

    assert len(all_species) == 2
    assert all_species[2].generation_created == 1
    assert all_species[2].representative is i_six_1
    assert len(all_species[1].members) == 4
    assert len(all_species[2].members) == 2


def test_create_initial_individual(functions_object):

    # Note this test assumes bias nodes are set to 'no' in the testing config
    i1 = functions_object.create_initial_individual(2, 2)
    i2 = functions_object.create_initial_individual(10, 10)

    i1_conn_gene_set = set()
    i2_conn_gene_set = set()

    assert i1.genome.get_greatest_innov() == 8
    assert len(i1.genome.node_genes) == 4
    assert len([node for node in i1.genome.node_genes.values() if node.node_type == 'input']) == 2
    assert len([node for node in i1.genome.node_genes.values() if node.node_type == 'output']) == 2
    assert len(i1.genome.connection_genes) == 4
    # Show all connections are unique:
    [i1_conn_gene_set.add((conn.in_node, conn.out_node)) for conn in i1.genome.connection_genes.values()]
    assert len(i1_conn_gene_set) == 4

    assert i2.genome.get_greatest_innov() == 120
    assert len(i2.genome.node_genes) == 20
    assert len([node for node in i2.genome.node_genes.values() if node.node_type == 'input']) == 10
    assert len([node for node in i2.genome.node_genes.values() if node.node_type == 'output']) == 10
    assert len(i2.genome.connection_genes) == 100
    # Show all connections are unique:
    [i2_conn_gene_set.add((conn.in_node, conn.out_node)) for conn in i2.genome.connection_genes.values()]
    assert len(i2_conn_gene_set) == 100
