from math import sqrt


class Fitness:

    def __init__(self):
        pass

    avg_fitness = 0
    best_fitness = 0
    standard_deviation = 0
    fitness_threshold = 1.0

    @classmethod
    # Evaluate fitness for all phenotypes
    # Fitness array returned is a one-to-one mapping of the phenotypes array
    def evaluate_fitness_of_phenotypes(cls, phenotypes):

        phenotypes_fitness = []
        bit_vector_length = float(len(phenotypes[0].bit_vector))
        for phenotype in phenotypes:

            fitness = 0
            for bit in phenotype.bit_vector:
                fitness += bit

            fitness /= bit_vector_length
            phenotypes_fitness.append(fitness)

        return phenotypes_fitness

    @classmethod
    def check_for_solution(cls, fitnesses):
        for i in xrange(len(fitnesses)):
            if cls.fitness_threshold <= fitnesses[i]:
                return i

        return -1

    @classmethod
    def index_of_best_solution(cls, fitnesses):
        return fitnesses.index(max(fitnesses))

    @classmethod
    # Wrapper for calculating average and best
    def get_fitness_of_phenotypes(cls, phenotypes):

        # Determine fitness for phenotypes
        phenotypes_fitness = cls.evaluate_fitness_of_phenotypes(phenotypes)

        # Determine average fitness and best fitness
        best_fitness = 0
        total_fitness = 0

        for fitness in phenotypes_fitness:

            total_fitness += fitness

            if fitness > best_fitness:
                best_fitness = fitness

        cls.best_fitness = best_fitness
        cls.avg_fitness = (total_fitness / len(phenotypes_fitness))
        cls.standard_deviation = cls.evaluate_standard_deviation(phenotypes_fitness)

        return phenotypes_fitness

    @classmethod
    # Standard deviation of fitness
    def evaluate_standard_deviation(cls, phenotypes_fitness):
        avg_deviation = 0
        for fitness in phenotypes_fitness:
            avg_deviation += pow(fitness - cls.avg_fitness, 2)

        return sqrt(avg_deviation/len(phenotypes_fitness))