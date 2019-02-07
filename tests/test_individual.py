"""
Module docstring stub
"""

import Source.NEAT.individual as individual


def test_network_evaluation(genome_recursive_two_outputs):

    i1 = individual.Individual(genome_recursive_two_outputs)
    genome_recursive_two_outputs.assemble_topology()

    output = i1.evaluate([1.0, -1.0])
    assert len(output) == 2
    assert output[0] == 0.5
    assert 0.7 <= output[1] <= 0.8

    output = i1.evaluate([1.0, -1.0])
    assert len(output) == 2
    assert output[0] == 0.5
    assert output[1] > 0.9  # Same inputs but output #2 changed means recursive node kicked in

    output = i1.evaluate([-1.0, 1.0])
    assert len(output) == 2
    assert output[0] == 0.5
    assert output[1] > 0.9

    output = i1.evaluate([1.0, 1.0])
    assert len(output) == 2
    assert output[0] > 0.99
    assert output[1] < 0.01


def test_network_evaluation_isolated_node(genome_recursive_two_outputs):

    # Isolate the recursive node
    genome_recursive_two_outputs.connection_genes[12].enabled = False

    i1 = individual.Individual(genome_recursive_two_outputs)
    genome_recursive_two_outputs.assemble_topology()

    output = i1.evaluate([1.0, -1.0])
    assert len(output) == 2
    assert output[0] == 0.5
    assert 0.7 <= output[1] <= 0.8

    output_2 = i1.evaluate([1.0, -1.0])
    output_3 = i1.evaluate([-1.0, 1.0])

    assert output == output_2 == output_3
