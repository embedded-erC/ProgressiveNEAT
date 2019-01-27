"""
Module-level docstring stub
"""


def test_sort_ascending_fitness(species_six_members):
    assert species_six_members.members[4].fitness < species_six_members.members[3].fitness
    species_six_members._sort_ascending_fitness()
    assert species_six_members.members[0].fitness < species_six_members.members[1].fitness
    assert species_six_members.members[1].fitness < species_six_members.members[2].fitness
    assert species_six_members.members[2].fitness < species_six_members.members[3].fitness
    assert species_six_members.members[3].fitness < species_six_members.members[4].fitness
    assert species_six_members.members[4].fitness < species_six_members.members[5].fitness


def test_save_champion(species_five_members, species_six_members):

    species_five_members._sort_ascending_fitness()
    species_six_members._sort_ascending_fitness()

    species_five_members._save_champion()
    species_six_members._save_champion()

    assert species_five_members.champion is None
    assert species_six_members.champion is not None


def test_incrementing_species_id(species_six_members, species_five_members):
    assert species_six_members.id < species_five_members.id


def test_sum_adjusted_fitnesses(species_five_members, species_six_members):
    species_five_members._sum_adjusted_fitnesses()
    species_six_members._sum_adjusted_fitnesses()

    assert species_five_members.adjusted_fitness_sum == 30
    assert species_six_members.adjusted_fitness_sum == 20
