from typing import List
from spike.life.individuals import OriginalIndividual, BornIndividual
from spike.life.cells import Cell, Gene, GeneType
from spike.life.traits import Trait
import pytest

def test_individual_creation_as_dead():
    ind1 = OriginalIndividual(1, [])
    assert ind1.energy == 0.0
    assert ind1.total_alive_cycles == 0
    assert ind1.total_dead_cycles == 0
    assert ind1.energy == 0
    assert ind1.alive == False


def test_original_individual_energy_as_zero_at_creation():
    genes = [
        Gene(GeneType.GENDER_FLUIDITY, 0),
        Gene(GeneType.MOVEMENT, 0),
        Gene(GeneType.SIGHT, 0),
        Gene(GeneType.IDENTIFICATION, 0),
        Gene(GeneType.ABILITY_TO_REPRODUCE, 0),
        Gene(GeneType.DEFENSE, 0),
        Gene(GeneType.ATTACK, 0),
        Gene(GeneType.COMMUNICATION, 0),
        Gene(GeneType.SCAVENGING, 0),
        Gene(GeneType.ENERGY_EFFICIENCY, 0),
        Gene(GeneType.PRONE_TO_MULTIPLE_OFFSPRINGS, 0),
    ]
    cell = Cell(genes)
    cells = [cell]
    ind = OriginalIndividual(1, cells)
    assert ind.energy == 0
    assert ind.alive == False
    assert ind.get_stronger_traits() == None


def test_original_individual_generational_attributes():
    genes = [
        Gene(GeneType.ATTACK, 0.3),
        Gene(GeneType.COMMUNICATION, 0.9),
    ]
    cell = Cell(genes)
    cells = [cell]
    ind = OriginalIndividual(1, cells)
    assert ind.generation == (0, 0)
    assert ind.parents == (None, None)
    assert ind.grand_parents() == ((None, None), (None, None))


def test_individual_energy_as_average_at_creation():
    genes = [
        Gene(GeneType.GENDER_FLUIDITY, 0.5),
        Gene(GeneType.MOVEMENT, 0.5),
        Gene(GeneType.SIGHT, 0.5),
        Gene(GeneType.IDENTIFICATION, 0.5),
        Gene(GeneType.ABILITY_TO_REPRODUCE, 0.5),
        Gene(GeneType.DEFENSE, 0.5),
        Gene(GeneType.ATTACK, 0.5),
        Gene(GeneType.COMMUNICATION, 0.5),
        Gene(GeneType.SCAVENGING, 0.5),
        Gene(GeneType.ENERGY_EFFICIENCY, 0.5),
        Gene(GeneType.PRONE_TO_MULTIPLE_OFFSPRINGS, 0.5),
    ]
    cell = Cell(genes)
    cells = [cell]
    ind = OriginalIndividual(1, cells)

    assert ind.energy == 0.5
    assert ind.alive == True

    traits = ind.get_stronger_traits()
    gene_value, gene_types = traits

    assert len(gene_types) == 10


def test_individual_one_stronger_trait():
    genes = [
        Gene(GeneType.ATTACK, 0.6),
        Gene(GeneType.COMMUNICATION, 0.4),
        Gene(GeneType.DEFENSE, 0.5),
        Gene(GeneType.ENERGY_EFFICIENCY, 0.5),
        Gene(GeneType.GENDER_FLUIDITY, 0.6),
        Gene(GeneType.IDENTIFICATION, 0.9),
        Gene(GeneType.MOVEMENT, 0.6),
        Gene(GeneType.SCAVENGING, 0.4),
        Gene(GeneType.SIGHT, 0.5),
    ]
    cell = Cell(genes)
    cells = [cell]
    ind = OriginalIndividual(1, cells)

    traits = ind.get_stronger_traits()
    gene_value, gene_types = traits

    assert gene_value == 0.9
    assert len(gene_types) == 1

    assert gene_types == [
        GeneType.IDENTIFICATION,
    ]


def test_original_individual_generation_both_should_be_zero():
    genes1 = [
        Gene(GeneType.ATTACK, 0.6),
    ]
    cell1 = Cell(genes1)
    cells1 = [cell1]
    ind1 = OriginalIndividual(1, cells1)

    genes2 = [
        Gene(GeneType.ATTACK, 0.6),
    ]
    cell2 = Cell(genes2)
    cells2 = [cell2]
    ind2 = OriginalIndividual(1, cells2)

    assert (0, 0) == ind1.generation
    assert (0, 0) == ind2.generation

def test_reproduction_should_not_reproduce():
    genes1 = [
        Gene(GeneType.SEX, 0.6),
    ]
    cell1 = Cell(genes1)
    cells1 = [cell1]
    ind1 = OriginalIndividual(1, cells1)

    genes2 = [
        Gene(GeneType.ATTACK, 0.6),
    ]
    cell2 = Cell(genes2)
    cells2 = [cell2]
    ind2 = OriginalIndividual(1, cells2)
    
    off_spring: List[BornIndividual] = ind1.reproduce(ind2)
    assert len(off_spring) == 1
    
def test_born_individual_generation_both_should_be_different():
    genes1 = [
        Gene(GeneType.ATTACK, 0.6),
    ]
    cell1 = Cell(genes1)
    cells1 = [cell1]
    ind1 = OriginalIndividual(1, cells1)

    genes2 = [
        Gene(GeneType.ATTACK, 0.6),
    ]
    cell2 = Cell(genes2)
    cells2 = [cell2]
    ind2 = OriginalIndividual(1, cells2)

# TODO FInish it
    # ind3 = BornIndividual(1,parents=(ind1,ind2))
    # assert (1,1) == ind3.generation
