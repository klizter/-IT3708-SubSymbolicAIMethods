from fitness import Fitness


class FitnessGloballySuprisingSequence(Fitness):

    distance = 1
    fitness_threshold = 1

    @classmethod
    def evaluate_fitness_of_phenotypes(cls, phenotypes):

        phenotypes_fitness = []
        sequences_found = {}
        violations = 0

        for phenotype in phenotypes:

            # Global distances
            for distance in xrange(len(phenotype.sequence)):

                sub_seq_start = 0

                # Discover all sub sequences for given distance
                while sub_seq_start + (distance + 1) < len(phenotype.sequence):

                    sub_sequence = str(phenotype.sequence[sub_seq_start]) + \
                                   str(distance) + \
                                   str(phenotype.sequence[sub_seq_start+(distance + 1)])

                    if sub_sequence in sequences_found:
                        violations += 1
                        sequences_found[sub_sequence] += 1
                    else:
                        sequences_found[sub_sequence] = 1

                    sub_seq_start += 1

            fitness = 1 / float(1 + (0.01 * violations))
            phenotypes_fitness.append(fitness)
            sequences_found = {}
            violations = 0

        return phenotypes_fitness
