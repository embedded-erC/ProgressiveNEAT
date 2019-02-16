"""
Module level docstring stub
"""

import Source.NEAT.functions as functions
import Source.NEAT.individual as individual
import Source.NEAT.species as species


def test_compare_genome_compatibility(genome_four_nodes, genome_five_nodes):
    assert functions.compare_genome_compatibility(genome_four_nodes, genome_five_nodes) is False
    assert functions.compare_genome_compatibility(genome_five_nodes, genome_five_nodes) is True


def test_calc_excess_disjoint_genes(genome_four_nodes, genome_five_nodes):
    assert functions._calc_excess_disjoint_genes(genome_four_nodes, genome_five_nodes) == (3, 0)


def test_calc_avg_wt_difference(genome_four_nodes, genome_five_nodes):
    assert functions._calc_avg_wt_difference(genome_four_nodes, genome_five_nodes) == 0.5
    assert functions._calc_avg_wt_difference(genome_five_nodes, genome_four_nodes) == 0.5


def test_sort_into_species(genome_four_nodes, genome_six_nodes):
    i_four_1 = individual.Individual(genome_four_nodes)
    i_four_2 = individual.Individual(genome_four_nodes)
    i_four_3 = individual.Individual(genome_four_nodes)

    i_six_1 = individual.Individual(genome_six_nodes)
    i_six_2 = individual.Individual(genome_six_nodes)

    s1 = species.Species(0, i_four_1)

    individuals = [i_four_1, i_four_2, i_four_3, i_six_1, i_six_2]
    all_species = [s1]

    functions.sort_into_species(all_species, individuals, 1)

    assert len(all_species) == 2
    assert all_species[1].generation_created == 1
    assert all_species[1].representative is i_six_1
    assert len(all_species[0].members) == 4
    assert len(all_species[1].members) == 2


def test_create_initial_individual():

    # Note this test assumes bias nodes are set to 'no' in the testing config
    i1 = functions.create_initial_individual(2, 2)
    i2 = functions.create_initial_individual(10, 10)

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
