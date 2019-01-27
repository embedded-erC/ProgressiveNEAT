"""
Module docstring stub
"""


def test_assemble_topology(genome_simple_shuffle):

    # TODO: Add in recursive node connection checks to make sure this test code doesn't fail.

    assert genome_simple_shuffle.node_genes[1].layer == 1
    assert genome_simple_shuffle.node_genes[2].layer == 1
    assert genome_simple_shuffle.node_genes[3].layer is None
    assert genome_simple_shuffle.node_genes[4].layer is None
    assert genome_simple_shuffle.node_genes[9].layer is None
    assert genome_simple_shuffle.node_genes[12].layer is None
    assert genome_simple_shuffle.node_genes[15].layer is None

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


def test_get_genome_size(genome_simple_shuffle):
    assert genome_simple_shuffle.get_genome_size() == 17


def test_get_greatest_innov(genome_simple_shuffle):
    assert genome_simple_shuffle.get_greatest_innov() == 17


def test_get_all_gene_ids(genome_simple_shuffle):
    assert genome_simple_shuffle.get_all_gene_ids() == list(range(1, 18))
