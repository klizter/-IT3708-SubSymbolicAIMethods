from fitness import Fitness


class FitnessLOLZPrefix(Fitness):

    avg_fitness = 0
    z = 0
    fitness_threshold = 1.0

    def __init__(self):
        return

    @classmethod
    # Evaluate fitness for all phenotypes
    # Fitness array returned is a one-to-one mapping of the phenotypes array
    def evaluate_fitness_of_phenotypes(cls, phenotypes):

        phenotypes_fitness = []
        for phenotype in phenotypes:

            fitness = 0
            lead = phenotype.bit_vector[0]
            for bit in phenotype.bit_vector:

                if bit != lead:
                    break

                if lead == 0:
                    if fitness < cls.z:
                        fitness += 1
                    else:
                        break
                else:
                    fitness += 1

            fitness /= float(len(phenotype.bit_vector))
            phenotypes_fitness.append(fitness)

        return phenotypes_fitness
