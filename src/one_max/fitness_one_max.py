from fitness import Fitness
from random import randint


class FitnessOneMax(Fitness):

    first_iteration = True
    random_solution = True
    solution = []

    @classmethod
    # Evaluate fitness for all ONEMAX phenotypes
    def evaluate_fitness_of_phenotypes(cls, phenotypes):

        phenotypes_fitness = []
        bit_vector_length = len(phenotypes[0].bit_vector)

        if cls.first_iteration:
            cls.get_solution(bit_vector_length)
            cls.first_iteration = False

        for phenotype in phenotypes:

            fitness = 0
            for i in xrange(len(phenotype.bit_vector)):
                if phenotype.bit_vector[i] != cls.solution[i]:
                    fitness += 1

            fitness /= float(bit_vector_length)
            phenotypes_fitness.append(fitness)

        return phenotypes_fitness

    @classmethod
    # Get ONEMAX solution or generate a random one
    def get_solution(cls, length):
        if cls.random_solution:
            cls.solution = [randint(0,1) for i in xrange(length)]
        else:
            cls.solution = [1 for i in xrange(length)]
