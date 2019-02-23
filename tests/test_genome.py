"""
Module docstring stub
"""
from Source.constants import *
from Source.NEAT.genome import NodeGene, ConnectionGene


def test_assemble_topology(genome_simple_shuffle):

    assert genome_simple_shuffle.node_genes[1].layer == 1
    assert genome_simple_shuffle.node_genes[2].layer == 1
    assert genome_simple_shuffle.node_genes[3].layer == -1
    assert genome_simple_shuffle.node_genes[4].layer == -1
    assert genome_simple_shuffle.node_genes[9].layer == -1
    assert genome_simple_shuffle.node_genes[12].layer == -1
    assert genome_simple_shuffle.node_genes[15].layer == -1

    assert genome_simple_shuffle.node_genes[1].inbound_connections == []
    assert genome_simple_shuffle.node_genes[2].inbound_connections == []
    assert genome_simple_shuffle.node_genes[3].inbound_connections == []
    assert genome_simple_shuffle.node_genes[4].inbound_connections == []
    assert genome_simple_shuffle.node_genes[9].inbound_connections == []
    assert genome_simple_shuffle.node_genes[12].inbound_connections == []
    assert genome_simple_shuffle.node_genes[15].inbound_connections == []

    assert genome_simple_shuffle.node_genes[1].outbound_connections == []
    assert genome_simple_shuffle.node_genes[2].outbound_connections == []
    assert genome_simple_shuffle.node_genes[3].outbound_connections == []
    assert genome_simple_shuffle.node_genes[4].outbound_connections == []
    assert genome_simple_shuffle.node_genes[9].outbound_connections == []
    assert genome_simple_shuffle.node_genes[12].outbound_connections == []
    assert genome_simple_shuffle.node_genes[15].outbound_connections == []

    # Fill out the inbound/outbound connections and layer information for the nodes
    genome_simple_shuffle.assemble_topology()

    assert genome_simple_shuffle.node_genes[1].layer == 1
    assert genome_simple_shuffle.node_genes[2].layer == 1
    assert genome_simple_shuffle.node_genes[3].layer == 5
    assert genome_simple_shuffle.node_genes[4].layer == 3
    assert genome_simple_shuffle.node_genes[9].layer == 4
    assert genome_simple_shuffle.node_genes[12].layer == 2
    assert genome_simple_shuffle.node_genes[15].layer == 2

    assert sorted(genome_simple_shuffle.node_genes[1].inbound_connections) == []
    assert sorted(genome_simple_shuffle.node_genes[2].inbound_connections) == []
    assert sorted(genome_simple_shuffle.node_genes[3].inbound_connections) == [1, 2, 4, 9, 15]
    assert sorted(genome_simple_shuffle.node_genes[4].inbound_connections) == [1, 12]
    assert sorted(genome_simple_shuffle.node_genes[9].inbound_connections) == [4]
    assert sorted(genome_simple_shuffle.node_genes[12].inbound_connections) == [2]
    assert sorted(genome_simple_shuffle.node_genes[15].inbound_connections) == [1]

    assert sorted(genome_simple_shuffle.node_genes[1].outbound_connections) == [3, 4, 15]
    assert sorted(genome_simple_shuffle.node_genes[2].outbound_connections) == [3, 12]
    assert sorted(genome_simple_shuffle.node_genes[3].outbound_connections) == []
    assert sorted(genome_simple_shuffle.node_genes[4].outbound_connections) == [3, 9]
    assert sorted(genome_simple_shuffle.node_genes[9].outbound_connections) == [3]
    assert sorted(genome_simple_shuffle.node_genes[12].outbound_connections) == [4]
    assert sorted(genome_simple_shuffle.node_genes[15].outbound_connections) == [3]

    assert list(zip(genome_simple_shuffle.node_genes[1].outbound_connections,
                    genome_simple_shuffle.node_genes[1].outbound_weights)) == [(3, 0.5), (4, 0.1), (15, 0.1)]


def test_assembly_with_recursion(genome_four_nodes_recursive):

    genome_four_nodes_recursive.assemble_topology()

    assert genome_four_nodes_recursive.node_genes[1].layer == 1
    assert genome_four_nodes_recursive.node_genes[2].layer == 1
    assert genome_four_nodes_recursive.node_genes[3].layer == 3
    assert genome_four_nodes_recursive.node_genes[4].layer == 2

    assert sorted(genome_four_nodes_recursive.node_genes[1].inbound_connections) == []
    assert sorted(genome_four_nodes_recursive.node_genes[2].inbound_connections) == []
    assert sorted(genome_four_nodes_recursive.node_genes[3].inbound_connections) == [1, 2, 4]
    assert sorted(genome_four_nodes_recursive.node_genes[4].inbound_connections) == [1, 4]

    assert sorted(genome_four_nodes_recursive.node_genes[1].outbound_connections) == [3, 4]
    assert sorted(genome_four_nodes_recursive.node_genes[2].outbound_connections) == [3]
    assert sorted(genome_four_nodes_recursive.node_genes[3].outbound_connections) == []
    assert sorted(genome_four_nodes_recursive.node_genes[4].outbound_connections) == [3, 4]


def test_get_genome_size(genome_simple_shuffle):
    assert genome_simple_shuffle.get_genome_size() == 17


def test_get_greatest_innov(genome_simple_shuffle):
    assert genome_simple_shuffle.get_greatest_innov() == 17


def test_get_all_gene_ids(genome_simple_shuffle):
    assert genome_simple_shuffle.get_all_gene_ids() == list(range(1, 18))


def test_set_output_layer(genome_two_outputs):
    assert genome_two_outputs.node_genes[1].layer == 1
    assert genome_two_outputs.node_genes[2].layer == 1
    assert genome_two_outputs.node_genes[3].layer == -1
    assert genome_two_outputs.node_genes[4].layer == -1
    assert genome_two_outputs.node_genes[9].layer == -1

    genome_two_outputs.assemble_topology()

    assert genome_two_outputs.node_genes[1].layer == 1
    assert genome_two_outputs.node_genes[2].layer == 1
    assert genome_two_outputs.node_genes[3].layer == 3
    assert genome_two_outputs.node_genes[4].layer == 3
    assert genome_two_outputs.node_genes[9].layer == 2


def test_sort_nodes_by_layer(genome_simple_shuffle):

    assert list(genome_simple_shuffle.node_genes) == [1, 2, 3, 4, 9, 12, 15]

    genome_simple_shuffle.assemble_topology()

    assert list(genome_simple_shuffle.node_genes) == [1, 2, 12, 15, 4, 9, 3]  # Sort order by layer

    previous_layer = 0
    for gene in genome_simple_shuffle.node_genes.values():
        assert gene.layer >= previous_layer
        previous_layer = gene.layer


def test_isolated_node(genome_isolated_recursive):

    assert genome_isolated_recursive.node_genes[4].is_isolated is False
    genome_isolated_recursive.assemble_topology()

    assert genome_isolated_recursive.node_genes[1].is_isolated is False
    assert genome_isolated_recursive.node_genes[2].is_isolated is False
    assert genome_isolated_recursive.node_genes[3].is_isolated is False
    assert genome_isolated_recursive.node_genes[4].is_isolated is True


def test_isolated_output_node(genome_isolated_output_node):
    assert genome_isolated_output_node.node_genes[4].is_isolated is False
    genome_isolated_output_node.assemble_topology()

    assert genome_isolated_output_node.node_genes[1].is_isolated is False
    assert genome_isolated_output_node.node_genes[2].is_isolated is False
    assert genome_isolated_output_node.node_genes[3].is_isolated is False
    assert genome_isolated_output_node.node_genes[4].is_isolated is True


def test_mutate_connections(genome_simple_shuffle):
    matched = 0
    for i in range(1000):
        pre_mutate = [conn.conn_weight for conn in genome_simple_shuffle.connection_genes.values()]
        genome_simple_shuffle.mutate_connections()
        post_mutate = [conn.conn_weight for conn in genome_simple_shuffle.connection_genes.values()]
        for pre, post in zip(pre_mutate, post_mutate):
            if pre != post and abs(pre - post) < genome_simple_shuffle.kMax_conn_change:
                matched += 1
    assert 9000 < matched < 9400


def test_add_brand_new_node(genome_four_nodes):

    # Simulate node that hasn't been created this generation
    old_largest_innov = genome_four_nodes.get_greatest_innov()
    nodes_this_generation = dict()
    genome_four_nodes.add_node(nodes_this_generation, old_largest_innov + 1)
    assert old_largest_innov + 3 == genome_four_nodes.get_greatest_innov()
    assert isinstance(genome_four_nodes.node_genes[old_largest_innov + 1], NodeGene)
    assert isinstance(genome_four_nodes.connection_genes[old_largest_innov + 2], ConnectionGene)
    assert isinstance(genome_four_nodes.connection_genes[old_largest_innov + 3], ConnectionGene)

    disabled_test = [conn for conn in genome_four_nodes.connection_genes.values() if conn.enabled is False]
    assert len(disabled_test) == 1
    assert len(nodes_this_generation) == 3


def test_add_already_innovated_node(genome_four_nodes_recursive):

    # Simulate node that has already been created this generation
    old_next_largest_innov = genome_four_nodes_recursive.get_greatest_innov() + 1
    old_genome_size = genome_four_nodes_recursive.get_genome_size()
    simulated_nodes = dict()
    for conn_gene in genome_four_nodes_recursive.connection_genes.values():
        simulated_nodes[conn_gene.innov_num] = old_next_largest_innov
    old_simulated_nodes_keys = simulated_nodes.keys()

    # Try to add a new node that should have already been created:
    new_next_largest_innov = genome_four_nodes_recursive.add_node(simulated_nodes, old_next_largest_innov)
    assert new_next_largest_innov == old_next_largest_innov
    assert old_simulated_nodes_keys == simulated_nodes.keys()
    assert genome_four_nodes_recursive.get_genome_size() == old_genome_size + 3


def test_find_eligible_connections(genome_six_nodes):
    genome_six_nodes.assemble_topology()
    eligible_connections = genome_six_nodes._find_eligible_connections()
    assert (2, 9) in eligible_connections
    assert (2, 12) in eligible_connections
    assert (2, 4) in eligible_connections
    assert (9, 9) in eligible_connections
    assert (9, 12) in eligible_connections
    assert (9, 4) in eligible_connections
    assert (12, 9) in eligible_connections
    assert (12, 12) in eligible_connections
    assert (12, 3) in eligible_connections
    assert (4, 4) in eligible_connections
    assert (4, 9) not in eligible_connections
    assert (1, 1) not in eligible_connections
    assert (1, 2) not in eligible_connections
    assert (3, 1) not in eligible_connections
    assert (1, 3) not in eligible_connections


def test_add_brand_new_connection(genome_four_nodes):
    innovs_this_generation = dict()  # TODO: Align this with what we did in the test above after the merge
    old_next_largest_innov = genome_four_nodes.get_greatest_innov() + 1
    old_genome_size = genome_four_nodes.get_genome_size()
    genome_four_nodes.assemble_topology()
    new_next_largest_innov = genome_four_nodes.add_connection(innovs_this_generation, old_next_largest_innov)

    assert new_next_largest_innov == old_next_largest_innov + 1
    assert len(innovs_this_generation) == 1
    assert old_next_largest_innov in innovs_this_generation.values()
    assert genome_four_nodes.get_genome_size() == old_genome_size + 1


def test_add_already_innovated_connection(genome_four_nodes):
    innovs_this_generation = {(2, 4): 9, (4, 4): 9}
    old_next_largest_innov = genome_four_nodes.get_greatest_innov() + 1
    old_genome_size = genome_four_nodes.get_genome_size()
    genome_four_nodes.assemble_topology()
    new_next_largest_innov = genome_four_nodes.add_connection(innovs_this_generation, old_next_largest_innov)

    assert new_next_largest_innov == old_next_largest_innov
    assert len(innovs_this_generation) == 2
    assert new_next_largest_innov + 1 not in innovs_this_generation.values()
    assert genome_four_nodes.get_genome_size() == old_genome_size + 1
