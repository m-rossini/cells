import random
from enum import Enum
from typing import List

from spike.life.parameters import MAX_RANDOM_GENE_VALUE, MIN_RANDOM_GENE_VALUE


class GeneType(Enum):
    """
    Gene types. When creating a gene one has to assign a type to it.
    Besides the type, there is a value associated with it in the range from 0 to 1,
        with 0 meaning lack of that ability and 1 total mastership of it.
    When that is high (near 1) it implies less energy to perform tasks requiring that geneds/traits
    All these traits are the peak an individual can have. From a certain age forward they will start
        to be less effective. How their values decrease can be spcified by a policy (to be implemented)
    """
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self,
                 seq,
                 count_to_energy=True,
                 affect_male_level=1,
                 affect_female_level=1):
        self.seq = seq
        self.count_to_energy = count_to_energy

    SEX = 0, False, 1, 1 
    # My Gender fludity how far (0) or close(1) to my sex
    GENDER_FLUIDITY = 1, False, 1, 1
    MOVEMENT = 2, True, 1, 1  # How fast I can move around
    SIGHT = 3, True, 1, 1  # How far I can perceive something
    # How far I can identify something (this is different for perceiving)
    IDENTIFICATION = 4, True, 1, 1
    ABILITY_TO_REPRODUCE = 5, True, 1, 1  # How good I am reproducing
    DEFENSE = 6, True, 1, 1  # How good I am defending
    ATTACK = 7, True, 1, 0.1  # How good I am attacking
    COMMUNICATION = 8, True, 0.9, 1  # How goo I am communicating
    SCAVENGING = 9, True, 1, 1  # How good I am to look and find resources
    ENERGY_EFFICIENCY = 10, True, 1, 1  # How efficient I am in using energy
    PRONE_TO_MULTIPLE_OFFSPRINGS = 11, True, 0, 1


gene_type_values = {member for member in GeneType}


class Gene:
    def __init__(self, gene_type: GeneType, gene_value: int = -1):
        self.gene_type = gene_type

        if gene_value >= 0 and gene_value <= 1:
            self.gene_value = gene_value
        else:
            self.gene_value = random.uniform(
                MIN_RANDOM_GENE_VALUE, MAX_RANDOM_GENE_VALUE)

    def __str__(self):
        return f"Type:<{self.gene_type} : {self.gene_value}>"

    def __repr__(self):
        return self.__str__()


class Cell:
    def __init__(self, genes: List[Gene]):
        self.genes = genes
        passed = {gene.gene_type for gene in genes}
        missing = gene_type_values - passed
        for gene_type in missing:
            self.genes.append(Gene(gene_type))

        self.genes = {gene.gene_type: gene for gene in genes}
        self.energy = self.__calculate_energy()

    def update_energy_level(self):
        self.energy = self.__calculate_energy()

    def __calculate_energy(self):
        values = [
            gene.gene_value
            for gene in self.genes.values()
            if gene.gene_type.count_to_energy == True
        ]
        return sum(values) / len(values)

    def __str__(self):
        return f"Genes:<{self.genes}>"

    def __repr__(self):
        return self.__str__()
