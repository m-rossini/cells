import uuid
import random
import math
import spike.life.parameters as parameter

from itertools import accumulate

from spike.life.traits import Trait
from abc import ABC, abstractmethod
from typing import override

from spike.life.cells import Cell, Gene, GeneType


class Individual(ABC):
    def __init__(self, group, cells: [Cell]):
        self.parents = (None, None)
        self.generation = (0, 0)

        self.cells = cells
        self.group = group
        self.unique_id = uuid.uuid4()
        self.total_alive_cycles = 0
        self.total_dead_cycles = 0

        self.energy = self.__calculate_individual_energy_level()
        self.alive = self.energy > 0

        self.total_previous_offspring = 0

    @abstractmethod
    def grand_parents(self):
        pass

    def __calculate_individual_energy_level(self):
        energy = 0
        for cell in self.cells:
            energy += cell.energy
        return energy

    def get_stronger_traits(self):
        """
        Returns None if cell is not alive, otherwise returns a list with:
        1 or more genes (cannot be empty) whose value is the highest
        compared with all the others.
        """
        if not self.alive:
            return None

        all_genes = [
            gene for cell in self.cells for gene in cell.genes.values()]
        some_genes = [gene for gene in all_genes if gene.gene_type.count_to_energy == True] 
        highest_value = max(gene.gene_value for gene in some_genes)
        return (
            highest_value,
            [gene.gene_type for gene in some_genes if gene.gene_value == highest_value],
        )

    def update_individual(self):
        for cell in self.cells:
            self.__update_gene(cell)
            self.__update_cell(cell)
            self.__update_traits(cell)
            self.__update_individual()

    def __update_gene(self, cell):
        self.__update_ability_to_reproduce(cell)
        self.__update_chances_of_multiples(cell)

    def __update_ability_to_reproduce(self, cell):
        pass

    def __update_chances_of_multiples(self, cell):
        pass

    def __update_cell(self, cell: Cell):
        cell.update_energy_level()

    def __update_traits(self, cell: Cell):
        self.__update_alive_status(cell)
        self.__increase_age()
        self.__update_fertitlity(cell)

    def __increase_age(self):
        if self.alive:
            self.total_alive_cycles += 1
        else:
            self.total_dead_cycles += 1

    def __update_alive_status(self, cell):
        pass

    def __update_fertitlity(self, cell: Cell):
        pass

    def __update_individual(self,):
        self.__calculate_individual_energy_level()


    def reproduce(self, other_individual):
        off_spring = self.__merge_parent_genes(other_individual)
        print(">>>type of", type(off_spring))
        self.total_previous_offspring += len(off_spring)
        return []
    
    def __merge_parent_genes(self, p2: 'Individual'):
        cell1, cell2 = self.__select_cell_pair(self.cells, p2.cells)
        if cell1 is None or cell2 is None:
            return []

        num_of_offsprings = self.__calculate_off_springs(
            (self, cell1), (p2, cell2))

        chances_of_identical = 0
        return self.__create_off_springs(num_of_offsprings, chances_of_identical, p2)

    def __create_off_springs(self, num_of_offsprings, chances_of_identical, p2):
        results = []
        for _ in range(num_of_offsprings):
            results.append()
        print(">>>results", type(results), results)
        return results
    
    def __calculate_off_springs(self, ind1, ind2):
        i1: Individual
        i2: Individual
        cell1 : Cell
        cell2 : Cell
        i1, cell1 = ind1
        i2, cell2 = ind2

        c1 = cell1.genes[GeneType.SEX]
        c2 = cell2.genes[GeneType.SEX]
        ind: Individual
        cell: Cell
        ind, cell = (i1, cell1) if c1 > c2 else (i2, cell2)
        if cell.genes[GeneType.SEX] <= 0.5:
            return 0

        assert sum(parameter.OFFSPRING_COUNT_CHANCES) == 1
        assert len(parameter.OFFSPRING_COUNT_CHANCES) == 5

        fertility = cell.traits[Trait.FERTILITY]
        proneness = cell.genes[GeneType.PRONE_TO_MULTIPLE_OFFSPRINGS].gene_value
        base_offspring = fertility**2 + \
            (proneness * len(parameter.MIN_FERTILITY_FOR_REPRODUCTION))
        age_factor = min(1, ind.age / parameter.MAX_POSSIBLE_AGE)
        previous_offspring_factor = 1 / (1 + ind.total_previous_offspring)
        adjusted_offspring = base_offspring * age_factor * previous_offspring_factor
        
        target_offspring = min(max(0, adjusted_offspring), len(
            parameter.MIN_FERTILITY_FOR_REPRODUCTION))

        # Try different values for fluctuation, also experiment with addition or multiplication
        random_fluctuation = random.uniform(-0.4, 0.4)
        offspring_count = target_offspring + random_fluctuation
        offspring_count = int(offspring_count)
        offspring_count = max(
            0, min(len(parameter.MIN_FERTILITY_FOR_REPRODUCTION), offspring_count))

        # Create indices up to the calculated count
        weighted_indices = range(offspring_count + 1)
        final_offspring_count = random.choices(
            weighted_indices, weights=parameter.OFFSPRING_COUNT_CHANCES[:offspring_count + 1], k=1)[0]

        return final_offspring_count

    def __select_cell_pair(self, p1: [Cell], p2: [Cell]):
        # ABILITY_TO_REPRODUCE is what should be considered. Anything else should be used to update the value, including energy
        for cell1 in p1:
            gene1 = cell1.genes[GeneType.ABILITY_TO_REPRODUCE]
            if not able_to_reproduce(gene1.gene_value, cell1.traits.get(Trait.FERTILITY)):
                continue

            for cell2 in p2:
                gene2 = cell2.genes[GeneType.ABILITY_TO_REPRODUCE]
                if not able_to_reproduce(gene2.gene_value, cell2.traits.get(Trait.FERTILITY)):
                    continue

                if not __fluidity_compatibility(
                    cell1.genes[GeneType.GENDER_FLUIDITY],
                    cell2.genes[GeneType.GENDER_FLUIDITY],
                ):
                    continue

                if not __sex_compatibility(
                    cell1.genes[GeneType.SEX],
                    cell2.genes[GeneType.SEX],
                ):
                    continue
                
                return (cell1, cell2)

        return (None, None)

    def __str__(self):
        return f"Ind:{self.unique_id}.Alive:[{self.alive}]"


class OriginalIndividual(Individual):
    def __init__(self, group, cells: [Cell]):
        super().__init__(group, cells)

    def grand_parents(self):
        return ((None, None), (None, None))


class BornIndividual(Individual):
    def __init__(self, group, parents=(None, None)):
        super().__init__(group, self.__merge_parent_genes(
            parents[0], parents[1]))

        super().parents = parents
        p1 = 0 if not self.parents[0].generation else self.parents[0].generation + 1
        p2 = 0 if not self.parents[1].generation else self.parents[1].generation + 1
        super().generation = (p1, p2)

    def grand_parents():
        pass


def __fluidity_compatibility(fc1: Gene, fc2: Gene):
    combined_fluidity = abs(fc1.gene_value - fc2.gene_value)
    return True if combined_fluidity >= parameter.MIN_GENRE_FLUIDITY_DISTANCE_FOR_REPRODUCTION else False

def __sex_compatibility(fc1: Gene, fc2: Gene):
    sex_distance = abs(fc1.gene_value - fc2.gene_value)
    return True if sex_distance >= parameter.MIN_SEX_DISTANCE_FOR_REPRODUCTION else False

def able_to_reproduce(ability_to_reproduce, fertility_level):
    return (
        (ability_to_reproduce is not None and fertility_level is not None) and
        ability_to_reproduce >= parameter.MIN_VALUE_TO_ABILITY_TO_REPRODUCE
        and ability_to_reproduce <= parameter.MAX_VALUE_TO_ABILITY_TO_REPRODUCE
        and fertility_level >= parameter.MIN_FERTILITY_FOR_REPRODUCTION[0]
    )


def reproduce(p1: Individual, p2: Individual):
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
