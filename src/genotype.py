from random import randint, uniform
from phenotype import Phenotype


class Genotype(object):

    bit_vector_length = 10

    def __init__(self, bit_vector):
        self.bit_vector = bit_vector
        self.fitness = 0

    def __cmp__(self, other):
        return cmp(self.fitness, other.fitness)

    def __repr__(self):
        return "[" + ''.join(str(bit) for bit in self.bit_vector) + " | " + str(self.fitness) + "]"

    def component_mutation(self, mutation_rate):
        for mutation_position in xrange(self.bit_vector):
            if uniform(0.0, 1.0) < mutation_rate:

                # Mutate bit_vector position
                if self.bit_vector[mutation_position]:
                    self.bit_vector[mutation_position] = 0
                else:
                    self.bit_vector[mutation_position] = 1

    def mutate(self):

        # Get random bit_vector position
        mutation_position = randint(0, (len(self.bit_vector) - 1))

        # Mutate bit_vector position
        if self.bit_vector[mutation_position]:
            self.bit_vector[mutation_position] = 0
        else:
            self.bit_vector[mutation_position] = 1

    def translate_to_phenotype(self):
        return Phenotype(self)

    """ CLASS METHODS """

    @classmethod
    def crossover(cls, mating_genotypes, num_crossover_points):

        crossover_points = [0]
        for i in xrange(num_crossover_points):

            crossover_point = 0
            while crossover_point in crossover_points:
                crossover_point = randint(1, (len(mating_genotypes[0].bit_vector) - 2))

            crossover_points.append(crossover_point)

        crossover_points.append(len(mating_genotypes[0].bit_vector))
        crossover_points.sort()

        # print "Crossover points: ", crossover_points

        parents_genotype = []
        for genotype in mating_genotypes:
            parents_genotype.append(list(genotype.bit_vector))

        # print "Parents genotypes: ", parents_genotype

        parent_chromosomes = []
        for i in xrange(num_crossover_points + 1):
            parent_chromosomes.append([])

        for parent_genotype in parents_genotype:
            for i in xrange(len(crossover_points) - 1):
                parent_chromosomes[i].append(parent_genotype[crossover_points[i]:crossover_points[i+1]])

        # print "Parents chromosoms: ", parent_chromosomes

        # TODO: Refactor names for clearer semantics
        # TODO: FIX crossover not crossing correcly on multiple points
        while len(parent_chromosomes) > 1:
            combined = []

            for i in xrange(len(parent_chromosomes[0])):

                chromosome_x = parent_chromosomes[0][i]

                for j in xrange(len(parent_chromosomes[1])):
                    chromosome_y = parent_chromosomes[1][j]
                    if i != j:
                        combined.append(chromosome_x + chromosome_y)

            parent_chromosomes[0] = list(combined)
            parent_chromosomes.pop(1)

        combined_chromosomes = parent_chromosomes[0]

        return combined_chromosomes

    @classmethod
    def construct_random_genotype(cls):
        bit_vector = []
        for i in xrange(cls.bit_vector_length):
            bit_vector.append(randint(0, 1))
        return cls(bit_vector)

    @classmethod
    def generate_random_genotypes(cls, num_initialized_genotypes):
        initialized_genotypes = []
        for i in xrange(num_initialized_genotypes):
            initialized_genotypes.append(cls.construct_random_genotype())
        return initialized_genotypes

    @classmethod
    def report_genotype_settings(cls):
        print "--------------------------------------------------------------------------------------------"
        print " ", cls.__name__, "settings:"
        print "--------------------------------------------------------------------------------------------"
        cls.report_settings_content()
        print ""

    @classmethod
    def report_settings_content(cls):
        print "\tbit vector length: ", cls.bit_vector_length

