import array as arr
import random

from enum import Enum
from typing import List

MIN_RANDOM_GENE_VALUE = 0.3
MAX_RANDOM_GENE_VALUE = 0.65
MIN_VALUE_FOR_AFFECTING_GENDER_FLUIDITY = 0.8
# MAX_LIMIT_FOR_MALE = 0.1
# MIN_LIMIT_FOR_FEMALE = 0.9

class GeneType(Enum):
    """
    Gene types. When creating a gene one has to assign a type to it.
    Besides the type, there is a value associated with it in the range from 0 to 1,
        with 0 meaning lack of that ability and 1 total mastership of it.
    When that is high (near 1) it implies less energy to perform tasks requiring that geneds/traits
    All these traits are the peak an individual can have. From a certain age forward they will start
        to be less effective. How their values decrease can be spcified by a policy (to be implemented)
    """

    GENDER_FLUIDITY = 1  # My Gender. 0-0.1 is male, 0.9-1 is female
    MOVEMENT = 2  # How fast I can move around
    SIGHT = 3  # How far I can perceive something
    # How far I can identify something (this is different for perceiving)
    IDENTIFICATION = 4
    ABILITY_TO_REPRODUCE = 5  # How good I am reproducing
    DEFENSE = 6  # How good I am defending
    ATTACK = 7  # How good I am attacking
    COMMUNICATION = 8  # How goo I am communicating
    SCAVENGING = 9  # How good I am to look and find resources
    ENERGY_EFFICIENCY = 10  # How efficient I am in using energy
    PRONE_TO_MULTIPLE_OFFSPRINGS = 11

gene_type_values = {member for member in GeneType}

class Gene:
    def __init__(self, gene_type: GeneType, gene_value: int = -1):
        self.gene_type = gene_type
        self.count_to_energy = True
        self.affect_gender_fluidity = -1
        
        if gene_type == GeneType.PRONE_TO_MULTIPLE_OFFSPRINGS:
            self.count_to_energy = False
            self.affect_gender_fluidity = MIN_VALUE_FOR_AFFECTING_GENDER_FLUIDITY
            self.gene_value = random.uniform(0,1)            
        if gene_type == GeneType.ABILITY_TO_REPRODUCE:
            self.gene_value = 0
            self.count_to_energy = False
        elif gene_type == GeneType.GENDER_FLUIDITY:
            self.gene_value = self.fix_gene_value_for_gender(gene_value)
            self.count_to_energy = False
        elif gene_value >= 0 and gene_value <= 1:
            self.gene_value = gene_value
        else:
            self.gene_value = random.uniform(
                MIN_RANDOM_GENE_VALUE, MAX_RANDOM_GENE_VALUE
            )

    def fix_gene_value_for_gender(self, value):
        return value

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

    def __str__(self):
        return f"Genes:<{self.genes}>"

    def __repr__(self):
        return self.__str__()
