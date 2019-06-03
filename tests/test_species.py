"""
Module-level docstring stub
"""
from Source.NEAT.individual import Individual
from Source.NEAT.species import Species
from Source.constants import get_config


def test_sort_ascending_fitness(species_six_members):
    assert species_six_members.members[4].fitness < species_six_members.members[3].fitness
    species_six_members._sort_fitness_ascending()
    assert species_six_members.members[0].fitness < species_six_members.members[1].fitness
    assert species_six_members.members[1].fitness < species_six_members.members[2].fitness
    assert species_six_members.members[2].fitness < species_six_members.members[3].fitness
    assert species_six_members.members[3].fitness < species_six_members.members[4].fitness
    assert species_six_members.members[4].fitness < species_six_members.members[5].fitness


def test_save_champion(species_five_members, species_six_members):

    species_five_members._sort_fitness_ascending()
    species_six_members._sort_fitness_ascending()

    species_five_members._save_champion()
    species_six_members._save_champion()

    assert species_five_members.champion is None
    assert species_six_members.champion is not None
    assert species_six_members.champion is not species_six_members.members[-1]  # We want a copy, not a reference.


def test_incrementing_species_id(species_six_members, species_five_members):
    assert species_six_members.id < species_five_members.id


def test_sum_adjusted_fitnesses(species_five_members, species_six_members):
    species_five_members._sum_adjusted_fitness()
    species_six_members._sum_adjusted_fitness()

    assert species_five_members.adjusted_fitness_sum == 30
    assert species_six_members.adjusted_fitness_sum == 20


def test_update_generations_and_fitness_peak(species_six_members):
    assert species_six_members.peak_fitness == 0
    assert species_six_members.generations_existed == 0
    assert species_six_members.num_generations_at_peak == 0
    assert species_six_members.extinction_generation is None

    species_six_members._sort_fitness_ascending()
    species_six_members._update_generations_and_fitness_peak()

    assert species_six_members.peak_fitness > 0
    assert species_six_members.generations_existed == 1
    assert species_six_members.num_generations_at_peak == 1
    assert species_six_members.extinction_generation is None

    for i in range(9):
        species_six_members._update_generations_and_fitness_peak()

    assert species_six_members.peak_fitness > 0
    assert species_six_members.generations_existed == 10
    assert species_six_members.num_generations_at_peak == 10
    assert species_six_members.extinction_generation is None

    species_six_members.members[-1].fitness = 999999
    species_six_members._update_generations_and_fitness_peak()

    assert species_six_members.peak_fitness == 999999
    assert species_six_members.generations_existed == 11
    assert species_six_members.num_generations_at_peak == 1
    assert species_six_members.extinction_generation is None

    for i in range(89):
        species_six_members._update_generations_and_fitness_peak()

    assert species_six_members.peak_fitness > 0
    assert species_six_members.generations_existed == 100
    assert species_six_members.num_generations_at_peak == 90
    assert species_six_members.extinction_generation == species_six_members.kExtinction_generation + 10  # b/c we set a new fitness record @ generation 10


def test_choose_representative(species_six_members):

    species_six_members.representative = "Mock Representative"
    assert species_six_members.representative == "Mock Representative"

    species_six_members.choose_representative()

    assert isinstance(species_six_members.representative, Individual)


def test_get_members(species_six_members):
    species_six_members.choose_representative()
    assert len(species_six_members.get_members(_include_representative=False)) == 5
    assert len(species_six_members.get_members()) == 6


def test_clear_members(species_five_members, species_six_members):
    assert len(species_five_members.members) == 5
    assert len(species_six_members.members) == 6

    species_five_members.clear_members()
    species_six_members.clear_members(_keep_representative=False)

    assert len(species_five_members.members) == 1
    assert len(species_six_members.members) == 0


def test_report_stats(species_six_members):

    species_six_members.update_species()
    stats_dict = species_six_members.report_stats()

    assert stats_dict["size"] == 6
    assert stats_dict["species fitness"] == 120
    assert isinstance(stats_dict["peak individual"], Individual)
    assert stats_dict["peak individual"] is not species_six_members.members[-1]  # ensure it's not a reference
    assert stats_dict["extinction generation"] is None


def test_add_member(species_six_members, genome_basic):

    new_member = Individual(genome_basic, config=get_config())

    assert new_member.assigned_specie is None
    assert len(species_six_members.members) == 6
    species_six_members.add_member(new_member)

    assert new_member.assigned_specie == species_six_members.id
    assert len(species_six_members.members) == 7


def test_eliminate_lowest_performers(species_six_members):
    assert len(species_six_members.members) == 6
    species_six_members._eliminate_lowest_performers()
    assert len(species_six_members.members) == 4
    assert species_six_members.members[0].fitness == 10
    assert species_six_members.members[3].fitness == 80


def test_mate(genome_four_nodes, genome_five_nodes):
    i1 = Individual(genome_four_nodes, config=get_config())
    i2 = Individual(genome_five_nodes, config=get_config())

    i1.fitness = 10
    i2.fitness = 5

    species_object = Species(0, i1, config=get_config())
    offspring = species_object.mate(i1, i2)
    assert offspring.genome.get_genome_size() == i1.genome.get_genome_size()
    for innov_num in range(1, 9):
        assert innov_num in offspring.genome.get_all_gene_ids()


def test_mate_inverted_fitness(genome_four_nodes, genome_five_nodes):
    i1 = Individual(genome_four_nodes, config=get_config())
    i2 = Individual(genome_five_nodes, config=get_config())

    i1.fitness = 5
    i2.fitness = 10

    species_object = Species(0, i1, config=get_config())
    offspring = species_object.mate(i1, i2)
    assert offspring.genome.get_genome_size() == i2.genome.get_genome_size()
    for innov_num in range(1, 12):
        assert innov_num in offspring.genome.get_all_gene_ids()


def test_select_one_offspring(species_one_member):
    num_assigned_offspring = 10
    species_one_member.select_offspring(num_assigned_offspring)
    assert len(species_one_member.members) == species_one_member.kMin_new_species_size
    assert len([individual for individual in species_one_member.members if individual.fitness]) == 5


def test_select_offspring_no_champion(species_five_members, genome_five_nodes):
    num_assigned_offspring = 10
    for individual in species_five_members.members:
        # Replace the mock genomes with actual genomes
        individual.genome = genome_five_nodes
    species_five_members.update_species()

    species_five_members.select_offspring(num_assigned_offspring)
    assert len(species_five_members.members) == num_assigned_offspring
    assert len([individual for individual in species_five_members.members if individual.fitness]) == 2


def test_select_offspring_with_champion(species_six_members, genome_five_nodes):
    num_assigned_offspring = 10
    for individual in species_six_members.members:
        # Replace the mock genomes with actual genomes
        individual.genome = genome_five_nodes
    species_six_members.update_species()

    species_six_members.select_offspring(num_assigned_offspring)
    assert len(species_six_members.members) == num_assigned_offspring
    assert len([individual for individual in species_six_members.members if individual.fitness]) == 3
    assert species_six_members.champion in species_six_members.members
