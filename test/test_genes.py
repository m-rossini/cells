from spike.life.cells import Gene, GeneType

def test_gene_standard_value_omitted():
    gene = Gene(GeneType.MOVEMENT)
    assert gene.gene_value >= 0.3 and gene.gene_value <= 0.65

def test_gene_standard_value_below():
    gene = Gene(GeneType.MOVEMENT, -3)
    assert gene.gene_value >= 0.3 and gene.gene_value <= 0.65

def test_gene_standard_value_above():
    gene = Gene(GeneType.MOVEMENT, 3)
    assert gene.gene_value >= 0.3 and gene.gene_value <= 0.65

def test_gene_standard_value_passed():
    gene = Gene(GeneType.MOVEMENT, 0.8)
    assert gene.gene_value == 0.8  
