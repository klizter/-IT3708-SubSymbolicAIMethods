from fitness import Fitness


class FitnessLocallySuprisingSequence(Fitness):

    distance = 1
    fitness_threshold = 1

    @classmethod
    def evaluate_fitness_of_phenotypes(cls, phenotypes):

        phenotypes_fitness = []
        sequences_found = {}
        violations = 0

        for phenotype in phenotypes:
            for i in xrange(1, len(phenotype.sequence)):
                sub_sequence = phenotype.sequence[i-1] + phenotype.sequence[i]
                if sub_sequence in sequences_found:
                    sequences_found[sub_sequence] += 1
                    violations += 1
                else:
                    sequences_found[sub_sequence] = 1

            fitness = 1 / float(1 + (0.01 * violations))   # Adjust scaling factor for a larger spectrum
            phenotypes_fitness.append(fitness)
            sequences_found = {}
            violations = 0

        return phenotypes_fitness
