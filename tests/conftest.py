import pytest
import Source.NEAT.genome as genome
import Source.NEAT.species as species
import Source.NEAT.individual as individual


@pytest.fixture
def genome_simple_shuffle():
    c1 = genome.ConnectionGene(1, 3, 0.5, innov_num=5)
    c2 = genome.ConnectionGene(2, 3, 0.5, innov_num=6)
    c3 = genome.ConnectionGene(1, 4, 0.1, innov_num=7)
    c4 = genome.ConnectionGene(4, 3, 0.8, innov_num=8)
    c5 = genome.ConnectionGene(9, 3, 0.25, innov_num=10)
    c6 = genome.ConnectionGene(4, 9, 0.333, innov_num=11)
    c7 = genome.ConnectionGene(2, 12, 0.22, innov_num=13)
    c8 = genome.ConnectionGene(12, 4, 0.22, innov_num=14)
    c9 = genome.ConnectionGene(1, 15, 0.1, innov_num=16)
    c10 = genome.ConnectionGene(15, 3, 0.1, innov_num=17)

    n1 = genome.NodeGene(node_type='input', innov_num=1)
    n2 = genome.NodeGene(node_type='input', innov_num=2)
    n3 = genome.NodeGene(node_type='output', innov_num=3)
    n4 = genome.NodeGene(innov_num=4)
    n5 = genome.NodeGene(innov_num=9)
    n6 = genome.NodeGene(innov_num=12)
    n7 = genome.NodeGene(innov_num=15)

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

    g1 = genome.Genome()

    g1.node_genes = nodes
    g1.connection_genes = connections

    return g1


@pytest.fixture()
def genome_four_nodes():
    c1 = genome.ConnectionGene(1, 3, 0.1, innov_num=5)
    c2 = genome.ConnectionGene(2, 3, 0.25, innov_num=6)
    c3 = genome.ConnectionGene(1, 4, 0.1, innov_num=7)
    c4 = genome.ConnectionGene(4, 3, -0.6, innov_num=8)

    n1 = genome.NodeGene(node_type='input', innov_num=1)
    n2 = genome.NodeGene(node_type='input', innov_num=2)
    n3 = genome.NodeGene(node_type='output', innov_num=3)
    n4 = genome.NodeGene(innov_num=4)

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

    g1 = genome.Genome()

    g1.node_genes = nodes
    g1.connection_genes = connections

    return g1


@pytest.fixture()
def genome_five_nodes():
    c1 = genome.ConnectionGene(1, 3, 0.6, innov_num=5)
    c2 = genome.ConnectionGene(2, 3, 0.75, innov_num=6)
    c3 = genome.ConnectionGene(1, 4, 0.6, innov_num=7)
    c4 = genome.ConnectionGene(4, 3, -0.1, innov_num=8)
    c5 = genome.ConnectionGene(1, 9, 0.1, innov_num=10)
    c6 = genome.ConnectionGene(9, 3, 0.1, innov_num=11)

    n1 = genome.NodeGene(node_type='input', innov_num=1)
    n2 = genome.NodeGene(node_type='input', innov_num=2)
    n3 = genome.NodeGene(node_type='output', innov_num=3)
    n4 = genome.NodeGene(innov_num=4)
    n5 = genome.NodeGene(innov_num=9)

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

    g1 = genome.Genome()

    g1.node_genes = nodes
    g1.connection_genes = connections

    return g1


@pytest.fixture()
def species_five_members():
    i1 = individual.Individual("Mock Genome")
    i2 = individual.Individual("Mock Genome")
    i3 = individual.Individual("Mock Genome")
    i4 = individual.Individual("Mock Genome")
    i5 = individual.Individual("Mock Genome")

    i1.fitness = 10
    i2.fitness = 20
    i3.fitness = 40
    i4.fitness = 80
    i5.fitness = 0

    s1 = species.Species(1, i1)
    s1.members = [i1, i2, i3, i4, i5]
    return s1


@pytest.fixture()
def species_six_members():
    i1 = individual.Individual("Mock Genome")
    i2 = individual.Individual("Mock Genome")
    i3 = individual.Individual("Mock Genome")
    i4 = individual.Individual("Mock Genome")
    i5 = individual.Individual("Mock Genome")
    i6 = individual.Individual("Mock Genome")

    i1.fitness = 10
    i2.fitness = 20
    i3.fitness = 40
    i4.fitness = 80
    i5.fitness = 0
    i6.fitness = -30.0

    s1 = species.Species(1, i1)
    s1.members = [i1, i2, i3, i4, i5, i6]
    return s1
