

class Phenotype(object):

    def __init__(self, genotype):
        self.bit_vector = genotype.bit_vector

    def __repr__(self):
        return ''.join(str(bit) for bit in self.bit_vector)