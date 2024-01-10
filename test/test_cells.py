from spike.life.cells import Gene, GeneType, Cell
import spike.life.cells as cells

def test_cells_pool():
    c = Cell([])
    assert 11 == len(c.genes)

    for gene in c.genes.values():
        if gene.gene_type not in [GeneType.ABILITY_TO_REPRODUCE, GeneType.GENDER_FLUIDITY]:
            assert gene.gene_value >= cells.MIN_RANDOM_GENE_VALUE and gene.gene_value <= cells.MAX_RANDOM_GENE_VALUE

def test_cells_pool_info():
    pool = [Gene(GeneType.GENDER_FLUIDITY, 1), Gene(GeneType.MOVEMENT, 0.85)]

    c = Cell(pool)

    for gene in c.genes.values():
        match gene.gene_type:
            case GeneType.GENDER_FLUIDITY:
                assert 1 == gene.gene_value       
            case GeneType.MOVEMENT:
                assert 0.85 == gene.gene_value 