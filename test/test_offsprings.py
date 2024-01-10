from spike.life.individuals import __calculate_off_springs
from spike.life.cells import Cell, Gene, GeneType
import pytest

def test_calculate_offsprings():
    c1 = Cell([])
    c1.genes[GeneType.GENDER_FLUIDITY] = Gene(GeneType.GENDER_FLUIDITY,1)
    c1.genes[GeneType.PRONE_TO_MULTIPLE_OFFSPRINGS] = Gene(GeneType.PRONE_TO_MULTIPLE_OFFSPRINGS,1)
    
    c2 = Cell([])
    c2.genes[GeneType.GENDER_FLUIDITY] = Gene(GeneType.GENDER_FLUIDITY,0)
    c2.genes[GeneType.PRONE_TO_MULTIPLE_OFFSPRINGS] = Gene(GeneType.PRONE_TO_MULTIPLE_OFFSPRINGS,1)   
     
    number = __calculate_off_springs(c1, c2)
    print(">>> Number", number)
    assert number == 0
