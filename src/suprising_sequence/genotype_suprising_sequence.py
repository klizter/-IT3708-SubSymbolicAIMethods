from genotype import Genotype
from phenotype_suprising_sequence import PhenotypeSuprisingSequence
from random import randrange, randint, uniform


class GenotypeSuprisingSequence(Genotype):

    symbols = 0
    length = 10

    def __init__(self, bit_vector):
        super(GenotypeSuprisingSequence, self).__init__(bit_vector)
        self.fitness = 0

    def __repr__(self):
        return "S=" + str(GenotypeSuprisingSequence.symbols) + \
               ", L=" + str(GenotypeSuprisingSequence.length) + \
               ": [" + ''.join(str(bit) + ", " for bit in self.bit_vector) + " | " + str(self.fitness) + "]"

    def mutate(self):

        mutation_position = randint(0, (len(self.bit_vector) - 1))

        # Mutate surprising sequence position
        mutation = self.bit_vector[mutation_position]
        while self.bit_vector[mutation_position] is mutation:
            mutation = randrange(65, 65 + GenotypeSuprisingSequence.symbols)

        self.bit_vector[mutation_position] = mutation

    def component_mutation(self, mutation_rate):
        for mutation_position in xrange(len(self.bit_vector)):
            if uniform(0.0, 1.0) < mutation_rate:

                # Mutate surprising sequence position
                mutation = self.bit_vector[mutation_position]
                while self.bit_vector[mutation_position] is mutation:
                    mutation = randrange(65, 65 + GenotypeSuprisingSequence.symbols)

                self.bit_vector[mutation_position] = mutation

    def translate_to_phenotype(self):
        return PhenotypeSuprisingSequence(self)

    @classmethod
    def construct_random_genotype(cls):
        bit_vector = []
        for i in xrange(cls.length):
            bit_vector.append(randrange(65, 65 + cls.symbols))
        return cls(bit_vector)

    @classmethod
    def report_settings_content(cls):
        print "\tsymbols:\t", cls.symbols
        print "\tlength:\t\t", cls.length



