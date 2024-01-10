import uuid
import random
import math
import spike.life.actions as actions
from abc import ABC, abstractmethod
from typing import override

from spike.life.cells import Cell, Gene, GeneType

MAX_LIFE_IN_CYCLES: int = 100
MAX_ENERGY_PER_INDIVIDUAL = 1  # 0 Individual is dead, 1 is maxPedro2008@@01
MIN_VALUE_TO_ABILITY_TO_REPRODUCE = 0.2
MAX_VALUE_TO_ABILITY__TO_REPRODUCE = 0.7
MIN_ENERGY_LEVEL_TO_REPRODUCE = 0.15
MIN_GENRE_FLUIDITY_DISTANCE_FOR_REPRODUCTION = 0.8

class Individual(ABC):
    def __init__(self, group, cells: [Cell]):
        self.parents = (None, None)
        self.generation = (0, 0)

        self.cells = cells
        self.group = group
        self.unique_id = uuid.uuid4()
        self.total_alive_cycles = 0
        self.total_dead_cycles = 0

        self.energy = self.calculate_initial_energy()
        self.alive = self.energy > 0
        self.__initialize_traits()

    @abstractmethod
    def grand_parents(self):
        pass

    def __initialize_traits(self):
        pass

    def calculate_initial_energy(self):
        energy = 0
        for cell in self.cells:
            energy += self.calculate_cell_energy(cell)
        return energy

    def calculate_cell_energy(self, cell):
        values = [
            gene.gene_value
            for gene in cell.genes.values()
            if gene.count_to_energy == True
        ]
        return sum(values) / len(values)

    def get_stronger_traits(self):
        """
        Returns None if cell is not alive, otherwise returns alist with:
        1 or more genes (cannot be empty) whose value is the huighest
        compared with all the others.
        """
        if not self.alive:
            return None

        all_genes = [
            gene for cell in self.cells for gene in cell.genes.values()]
        some_genes = [gene for gene in all_genes if gene.gene_type !=
                      GeneType.GENDER_FLUIDITY]
        highest_value = max(gene.gene_value for gene in some_genes)
        return (
            highest_value,
            [gene.gene_type for gene in some_genes if gene.gene_value == highest_value],
        )

    def update_individual(self):
        self.update_traits()
        for cell in self.cells:
            self.update_cell(cell)

    def update_traits(self):
        # AGE
        self.update_alive_status()

    def update_alive_status(self):
        pass

    def update_cell(self, cell: Cell):
        for gene in cell.genes:
            self.update_gene(gene)

    def update_gene(self):
        self.update_energy_level()
        self.update_ability_to_reproduce()
        self.update_chances_of_twins()

    def update_energy_level(self):
        pass

    def update_ability_to_reproduce(self):
        pass

    def update_chances_of_twins():
        pass
    
    def __str__(self):
        return f"Ind:{self.unique_id}.Alive:[{self.alive}]"


class OriginalIndividual(Individual):
    def __init__(self, group, cells: [Cell]):
        super().__init__(group, cells)

    @override
    def __initialize_traits(self):
        pass

    def grand_parents(self):
        return ((None, None), (None, None))


class BornIndividual(Individual):
    def __init__(self, group, parents=(None, None)):
        super().__init__(group, self.merge_parent_genes(parents[0], parents[1]))

        super().parents = parents
        p1 = 0 if not self.parents[0].generation else self.parents[0].generation + 1
        p2 = 0 if not self.parents[1].generation else self.parents[1].generation + 1
        super().generation = (p1, p2)

    def grand_parents():
        pass


def __merge_parent_genes(p1: Individual, p2: Individual):
    pass


def __select_cell_pair(p1: [Cell], p2: [Cell]):
    # ABILITY_TO_REPRODUCE is what should be considered. Anything else should be used to update the value, including energy
    for cell1 in p1:
        gene1 = cell1.genes[GeneType.ABILITY_TO_REPRODUCE]
        if not __able_to_reproduce(gene1.gene_value):
            continue

        for cell2 in p2:
            gene2 = cell2.genes[GeneType.ABILITY_TO_REPRODUCE]
            if not __able_to_reproduce(gene2.gene_value):
                continue

            if not __gender_compatibility(
                cell1.genes[GeneType.GENDER_FLUIDITY],
                cell2.genes[GeneType.GENDER_FLUIDITY],
            ):
                continue

            return (cell1, cell2)

    return (None, None)

def sigmoid(x, a=0, b=0):
    """
    Sigmoid function with adjustable parameters
    """
    return 1 / (1 + math.exp(-a * (x - b)))

def __gender_compatibility(fc1: Gene, fc2: Gene):
    combined_fluidity = fc1.gene_value + fc2.gene_value
    sigmoid_factor = sigmoid(combined_fluidity, 30, 0)
    return True if sigmoid_factor >= MIN_GENRE_FLUIDITY_DISTANCE_FOR_REPRODUCTION else False


def __able_to_reproduce(value):
    return (
        value >= MIN_VALUE_TO_ABILITY_TO_REPRODUCE
        and value <= MAX_VALUE_TO_ABILITY__TO_REPRODUCE
    )


def __calculate_off_springs(cell1: Cell, cell2: Cell, random_function=random.random):
    return None

def reproduce(p1: Individual, p2: Individual):

    cell1, cell2 = __select_cell_pair(p1.cells, p2.cells)
    if cell1 is None or cell2 is None:
        return None

    num_of_offsprings = __calculate_off_springs(cell1, cell2)
    
    # Determine number of offspring (exponential distribution)
    BASE_TWINS_PROBABILITY = 0.25  # Adjust as needed
    probability_multiple = BASE_TWINS_PROBABILITY * math.exp(-random.random())
    num_offspring = 1  # Default single offspring
    if random.random() < probability_multiple:
        num_offspring += random.randint(1, 3)  # Add 1-3 more offspring

    # Create offspring objects with independent genes
    offspring_list = []
    for _ in range(num_offspring):
        offspring_genes = {}
        for gene_id in self.genes.keys():
            # Choose parent for the gene
            parent = self if random.random() < 0.5 else p2
            offspring_gene_value = parent.genes[gene_id]

            # Apply regular mutation logic
            # ... (existing mutation logic based on age, health, etc.)

            # Introduce chance for defective gene
            if random.random() < P_DEFECT:
                offspring_gene_value = (
                    0  # Replace with your definition of defective value
                )

            offspring_genes[gene_id] = offspring_gene_value

        offspring_obj = Cell(offspring_genes, self.age_policy)
        offspring_list.append(offspring_obj)

    return offspring_list  # Return list of offspring objects
