import pytest
import Source.NEAT.genome as genome
import Source.NEAT.species as species
import Source.NEAT.functions as functions
import Source.NEAT.individual as individual
import Source.Visualization.visualization as visualization
from Source.constants import get_config


@pytest.fixture
def genome_simple_shuffle():
    c1 = genome.ConnectionGene(1, 3, 0.5, innov_num=5, config=get_config())
    c2 = genome.ConnectionGene(2, 3, 0.5, innov_num=6, config=get_config())
    c3 = genome.ConnectionGene(1, 4, 0.1, innov_num=7, config=get_config())
    c4 = genome.ConnectionGene(4, 3, 0.8, innov_num=8, config=get_config())
    c5 = genome.ConnectionGene(9, 3, 0.25, innov_num=10, config=get_config())
    c6 = genome.ConnectionGene(4, 9, 0.333, innov_num=11, config=get_config())
    c7 = genome.ConnectionGene(2, 12, 0.22, innov_num=13, config=get_config())
    c8 = genome.ConnectionGene(12, 4, 0.22, innov_num=14, config=get_config())
    c9 = genome.ConnectionGene(1, 15, 0.1, innov_num=16, config=get_config())
    c10 = genome.ConnectionGene(15, 3, 0.1, innov_num=17, config=get_config())

    n1 = genome.NodeGene(node_type='input', innov_num=1, config=get_config())
    n2 = genome.NodeGene(node_type='input', innov_num=2, config=get_config())
    n3 = genome.NodeGene(node_type='output', innov_num=3, config=get_config())
    n4 = genome.NodeGene(innov_num=4, config=get_config())
    n5 = genome.NodeGene(innov_num=9, config=get_config())
    n6 = genome.NodeGene(innov_num=12, config=get_config())
    n7 = genome.NodeGene(innov_num=15, config=get_config())

    connections = {
        c1.innov_num: c1,
        c2.innov_num: c2,
        c3.innov_num: c3,
        c4.innov_num: c4,
        c5.innov_num: c5,
        c6.innov_num: c6,
        c7.innov_num: c7,
        c8.innov_num: c8,
        c9.innov_num: c9,
        c10.innov_num: c10
    }

    nodes = {
        n1.innov_num: n1,
        n2.innov_num: n2,
        n3.innov_num: n3,
        n4.innov_num: n4,
        n5.innov_num: n5,
        n6.innov_num: n6,
        n7.innov_num: n7
    }

    g1 = genome.Genome(config=get_config())

    g1.node_genes = nodes
    g1.connection_genes = connections

    return g1


@pytest.fixture()
def genome_four_nodes():
    c1 = genome.ConnectionGene(1, 3, 0.1, innov_num=5, config=get_config())
    c2 = genome.ConnectionGene(2, 3, 0.25, innov_num=6, config=get_config())
    c3 = genome.ConnectionGene(1, 4, 0.1, innov_num=7, config=get_config())
    c4 = genome.ConnectionGene(4, 3, -0.6, innov_num=8, config=get_config())

    n1 = genome.NodeGene(node_type='input', innov_num=1, config=get_config())
    n2 = genome.NodeGene(node_type='input', innov_num=2, config=get_config())
    n3 = genome.NodeGene(node_type='output', innov_num=3, config=get_config())
    n4 = genome.NodeGene(innov_num=4, config=get_config())

    connections = {
        c1.innov_num: c1,
        c2.innov_num: c2,
        c3.innov_num: c3,
        c4.innov_num: c4,
    }

    nodes = {
        n1.innov_num: n1,
        n2.innov_num: n2,
        n3.innov_num: n3,
        n4.innov_num: n4,
    }

    g1 = genome.Genome(config=get_config())

    g1.node_genes = nodes
    g1.connection_genes = connections

    return g1


@pytest.fixture()
def genome_four_nodes_recursive():
    c1 = genome.ConnectionGene(1, 3, 0.1, innov_num=5, config=get_config())
    c2 = genome.ConnectionGene(2, 3, 0.25, innov_num=6, config=get_config())
    c3 = genome.ConnectionGene(1, 4, 0.1, innov_num=7, config=get_config())
    c4 = genome.ConnectionGene(4, 3, -0.6, innov_num=8, config=get_config())
    c5 = genome.ConnectionGene(4, 4, 0.25, innov_num=9, config=get_config())  # Recursive connection

    n1 = genome.NodeGene(node_type='input', innov_num=1, config=get_config())
    n2 = genome.NodeGene(node_type='input', innov_num=2, config=get_config())
    n3 = genome.NodeGene(node_type='output', innov_num=3, config=get_config())
    n4 = genome.NodeGene(innov_num=4, config=get_config())

    connections = {
        c1.innov_num: c1,
        c2.innov_num: c2,
        c3.innov_num: c3,
        c4.innov_num: c4,
        c5.innov_num: c5
    }

    nodes = {
        n1.innov_num: n1,
        n2.innov_num: n2,
        n3.innov_num: n3,
        n4.innov_num: n4,
    }

    g1 = genome.Genome(config=get_config())

    g1.node_genes = nodes
    g1.connection_genes = connections

    return g1


@pytest.fixture()
def genome_isolated_recursive():
    c1 = genome.ConnectionGene(1, 3, 0.1, innov_num=5, config=get_config())
    c2 = genome.ConnectionGene(2, 3, 0.25, innov_num=6, config=get_config())
    c3 = genome.ConnectionGene(1, 4, 0.1, innov_num=7, config=get_config())
    c4 = genome.ConnectionGene(4, 3, -0.6, innov_num=8, config=get_config())
    c5 = genome.ConnectionGene(4, 4, 0.25, innov_num=9, config=get_config())  # Recursive connection

    n1 = genome.NodeGene(node_type='input', innov_num=1, config=get_config())
    n2 = genome.NodeGene(node_type='input', innov_num=2, config=get_config())
    n3 = genome.NodeGene(node_type='output', innov_num=3, config=get_config())
    n4 = genome.NodeGene(innov_num=4, config=get_config())

    c3.enabled = False  # Isolate node 4

    connections = {
        c1.innov_num: c1,
        c2.innov_num: c2,
        c3.innov_num: c3,
        c4.innov_num: c4,
        c5.innov_num: c5
    }

    nodes = {
        n1.innov_num: n1,
        n2.innov_num: n2,
        n3.innov_num: n3,
        n4.innov_num: n4,
    }

    g1 = genome.Genome(config=get_config())

    g1.node_genes = nodes
    g1.connection_genes = connections

    return g1


@pytest.fixture()
def genome_isolated_output_node():
    c1 = genome.ConnectionGene(1, 3, 0.1, innov_num=5, config=get_config())
    c2 = genome.ConnectionGene(2, 3, 0.25, innov_num=6, config=get_config())
    c3 = genome.ConnectionGene(1, 4, 0.1, innov_num=7, config=get_config())
    c4 = genome.ConnectionGene(2, 4, -0.6, innov_num=8, config=get_config())

    n1 = genome.NodeGene(node_type='input', innov_num=1, config=get_config())
    n2 = genome.NodeGene(node_type='input', innov_num=2, config=get_config())
    n3 = genome.NodeGene(node_type='output', innov_num=3, config=get_config())
    n4 = genome.NodeGene(node_type='output', innov_num=4, config=get_config())

    # Isolate output node 4
    c3.enabled = False
    c4.enabled = False

    connections = {
        c1.innov_num: c1,
        c2.innov_num: c2,
        c3.innov_num: c3,
        c4.innov_num: c4
    }

    nodes = {
        n1.innov_num: n1,
        n2.innov_num: n2,
        n3.innov_num: n3,
        n4.innov_num: n4,
    }

    g1 = genome.Genome(config=get_config())

    g1.node_genes = nodes
    g1.connection_genes = connections

    return g1


@pytest.fixture()
def genome_five_nodes():
    c1 = genome.ConnectionGene(1, 3, 0.6, innov_num=5, config=get_config())
    c2 = genome.ConnectionGene(2, 3, 0.75, innov_num=6, config=get_config())
    c3 = genome.ConnectionGene(1, 4, 0.6, innov_num=7, config=get_config())
    c4 = genome.ConnectionGene(4, 3, -0.1, innov_num=8, config=get_config())
    c5 = genome.ConnectionGene(1, 9, 0.1, innov_num=10, config=get_config())
    c6 = genome.ConnectionGene(9, 3, 0.1, innov_num=11, config=get_config())

    n1 = genome.NodeGene(node_type='input', innov_num=1, config=get_config())
    n2 = genome.NodeGene(node_type='input', innov_num=2, config=get_config())
    n3 = genome.NodeGene(node_type='output', innov_num=3, config=get_config())
    n4 = genome.NodeGene(innov_num=4, config=get_config())
    n5 = genome.NodeGene(innov_num=9, config=get_config())

    connections = {
        c1.innov_num: c1,
        c2.innov_num: c2,
        c3.innov_num: c3,
        c4.innov_num: c4,
        c5.innov_num: c5,
        c6.innov_num: c6,
    }

    nodes = {
        n1.innov_num: n1,
        n2.innov_num: n2,
        n3.innov_num: n3,
        n4.innov_num: n4,
        n5.innov_num: n5
    }

    g1 = genome.Genome(config=get_config())

    g1.node_genes = nodes
    g1.connection_genes = connections

    return g1


@pytest.fixture()
def genome_six_nodes():
    c1 = genome.ConnectionGene(1, 3, 0.6, innov_num=5, config=get_config())
    c2 = genome.ConnectionGene(2, 3, 0.75, innov_num=6, config=get_config())
    c3 = genome.ConnectionGene(1, 4, 0.6, innov_num=7, config=get_config())
    c4 = genome.ConnectionGene(4, 3, -0.1, innov_num=8, config=get_config())
    c5 = genome.ConnectionGene(1, 9, 0.1, innov_num=10, config=get_config())
    c6 = genome.ConnectionGene(9, 3, 0.1, innov_num=11, config=get_config())
    c7 = genome.ConnectionGene(1, 12, 0.3, innov_num=13, config=get_config())
    c8 = genome.ConnectionGene(12, 4, 0.1, innov_num=14, config=get_config())

    n1 = genome.NodeGene(node_type='input', innov_num=1, config=get_config())
    n2 = genome.NodeGene(node_type='input', innov_num=2, config=get_config())
    n3 = genome.NodeGene(node_type='output', innov_num=3, config=get_config())
    n4 = genome.NodeGene(innov_num=4, config=get_config())
    n5 = genome.NodeGene(innov_num=9, config=get_config())
    n6 = genome.NodeGene(innov_num=12, config=get_config())

    connections = {
        c1.innov_num: c1,
        c2.innov_num: c2,
        c3.innov_num: c3,
        c4.innov_num: c4,
        c5.innov_num: c5,
        c6.innov_num: c6,
        c7.innov_num: c7,
        c8.innov_num: c8
    }

    nodes = {
        n1.innov_num: n1,
        n2.innov_num: n2,
        n3.innov_num: n3,
        n4.innov_num: n4,
        n5.innov_num: n5,
        n6.innov_num: n6
    }

    g1 = genome.Genome(config=get_config())

    g1.node_genes = nodes
    g1.connection_genes = connections

    return g1


@pytest.fixture()
def genome_two_outputs():
    c1 = genome.ConnectionGene(1, 3, 0.6, innov_num=5, config=get_config())
    c2 = genome.ConnectionGene(2, 3, 0.75, innov_num=6, config=get_config())
    c3 = genome.ConnectionGene(1, 4, 0.6, innov_num=7, config=get_config())
    c4 = genome.ConnectionGene(2, 4, 0.1, innov_num=8, config=get_config())
    c5 = genome.ConnectionGene(1, 9, 0.1, innov_num=10, config=get_config())
    c6 = genome.ConnectionGene(9, 3, 0.3, innov_num=11, config=get_config())

    n1 = genome.NodeGene(node_type='input', innov_num=1, config=get_config())
    n2 = genome.NodeGene(node_type='input', innov_num=2, config=get_config())
    n3 = genome.NodeGene(node_type='output', innov_num=3, config=get_config())
    n4 = genome.NodeGene(node_type='output', innov_num=4, config=get_config())
    n5 = genome.NodeGene(innov_num=9, config=get_config())

    connections = {
        c1.innov_num: c1,
        c2.innov_num: c2,
        c3.innov_num: c3,
        c4.innov_num: c4,
        c5.innov_num: c5,
        c6.innov_num: c6
    }

    nodes = {
        n1.innov_num: n1,
        n2.innov_num: n2,
        n3.innov_num: n3,
        n4.innov_num: n4,
        n5.innov_num: n5
    }

    g1 = genome.Genome(config=get_config())

    g1.node_genes = nodes
    g1.connection_genes = connections

    return g1


@pytest.fixture()
def genome_recursive_two_outputs():
    c1 = genome.ConnectionGene(1, 3, 1.0, innov_num=5, config=get_config())
    c2 = genome.ConnectionGene(2, 3, 1.0, innov_num=6, config=get_config())
    c3 = genome.ConnectionGene(1, 4, -1.0, innov_num=7, config=get_config())
    c4 = genome.ConnectionGene(2, 4, -1.0, innov_num=8, config=get_config())
    c5 = genome.ConnectionGene(1, 9, 0.0, innov_num=10, config=get_config())
    c6 = genome.ConnectionGene(9, 4, 0.5, innov_num=11, config=get_config())
    c7 = genome.ConnectionGene(9, 9, 1.0, innov_num=12, config=get_config())

    n1 = genome.NodeGene(node_type='input', innov_num=1, config=get_config())
    n2 = genome.NodeGene(node_type='input', innov_num=2, config=get_config())
    n3 = genome.NodeGene(node_type='output', innov_num=3, config=get_config())
    n4 = genome.NodeGene(node_type='output', innov_num=4, config=get_config())
    n5 = genome.NodeGene(innov_num=9, config=get_config())

    connections = {
        c1.innov_num: c1,
        c2.innov_num: c2,
        c3.innov_num: c3,
        c4.innov_num: c4,
        c5.innov_num: c5,
        c6.innov_num: c6,
        c7.innov_num: c7
    }

    nodes = {
        n1.innov_num: n1,
        n2.innov_num: n2,
        n3.innov_num: n3,
        n4.innov_num: n4,
        n5.innov_num: n5
    }

    g1 = genome.Genome(config=get_config())

    g1.node_genes = nodes
    g1.connection_genes = connections

    return g1


@pytest.fixture()
def species_one_member():
    i1 = individual.Individual("Mock Genome", config=get_config())
    i1.fitness = 1

    s1 = species.Species(0, i1, config=get_config())
    s1.members = [i1]
    return s1


@pytest.fixture()
def species_five_members():
    i1 = individual.Individual("Mock Genome", config=get_config())
    i2 = individual.Individual("Mock Genome", config=get_config())
    i3 = individual.Individual("Mock Genome", config=get_config())
    i4 = individual.Individual("Mock Genome", config=get_config())
    i5 = individual.Individual("Mock Genome", config=get_config())

    i1.fitness = 10
    i2.fitness = 15
    i3.fitness = 40
    i4.fitness = 80
    i5.fitness = 5

    s1 = species.Species(0, i1, config=get_config())
    s1.members = [i1, i2, i3, i4, i5]
    return s1


@pytest.fixture()
def species_six_members():
    i1 = individual.Individual("Mock Genome", config=get_config())
    i2 = individual.Individual("Mock Genome", config=get_config())
    i3 = individual.Individual("Mock Genome", config=get_config())
    i4 = individual.Individual("Mock Genome", config=get_config())
    i5 = individual.Individual("Mock Genome", config=get_config())
    i6 = individual.Individual("Mock Genome", config=get_config())

    i1.fitness = 10
    i2.fitness = 15
    i3.fitness = 40
    i4.fitness = 80
    i5.fitness = 5
    i6.fitness = -30.0

    s1 = species.Species(0, i1, config=get_config())
    s1.members = [i1, i2, i3, i4, i5, i6]
    return s1


@pytest.fixture()
def visualization_instance():
    v1 = visualization.Visualization()
    return v1


@pytest.fixture()
def functions_object():
    f1 = functions.Functions(config=get_config())
    return f1
