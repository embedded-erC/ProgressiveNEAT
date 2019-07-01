"""
Module-level docstring stub
"""


def test_species_generational_stats(visualization_instance, species_six_members, species_five_members):

    visualization_instance.set_generation(0)

    for species in [species_five_members, species_six_members]:
        visualization_instance.gather_species_generational_stats(species.id, species.report_stats())

    visualization_instance.set_generation(1)

    for species in [species_five_members, species_six_members]:
        visualization_instance.gather_species_generational_stats(species.id, species.report_stats())

    assert len(visualization_instance.species_generational_stats) == 2
    assert visualization_instance.species_generational_stats[0][species_six_members.id]["size"] == 6
    assert visualization_instance.species_generational_stats[0][species_five_members.id]["size"] == 5
    assert visualization_instance.species_generational_stats[1][species_six_members.id]["size"] == 6
    assert visualization_instance.species_generational_stats[1][species_five_members.id]["size"] == 5

    assert visualization_instance.species_generational_stats[0][species_six_members.id]["average connections"] == 1
    assert visualization_instance.species_generational_stats[0][species_six_members.id]["average nodes"] == 2
