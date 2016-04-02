from random import uniform, randint
from copy import deepcopy
from math import exp

# In general, a good EA provides a solid backbone of code for running the basic evolutionary loop along with
# a library of reusable phenotypes, genotypes, genotype-to-phenotype translators, and selection strategies. It
# also includes simple hooks for adding in new representations and translators, preferably as sub-classes to
# existing ones.


class EA:

    """ Parameters """

    """ The exploration and exploitation coupling """
    # In general, to achieve the full power of parallel stochastic search in tough solution spaces, large populations
    # are necessary. But to find a satisfactory combination of 30 parameters, for example, a small population
    # of only 10 or 20 may be sufficient.

    child_pool_size = 30
    adult_pool_size = 30
    elitism = 3

    """ The exploration and exploitation coupling """
    # Goldberg and De Jong provide some useful, general, tips for choosing EA parameters. One of the most critical,
    # and most general, involves the well-known balance between exploration and exploitation. To wit, De Jong emphasizes
    # a balance of strength between the explorative forces of reproduction and the exploitative powers of selection.
    # Key message is that if reproductive exploration is high (e.g., the mutation rate is high),
    # then selection should be highly exploitative as well. Conversely, low reproductive exploration should
    # be complemented with weak selection.

    """ Crossover rate """
    # If the representational choices have been so difficult that no recombination operator can
    # guarantee high heritability, then a low crossover rate, of say 0.2, might be wise.

    crossover_rate = 0.75
    crossover_points = 1

    """ Mutation rate """
    # Mutation rates typically come in at least two varieties: per genome and per genome component (e.g., per bit
    # in a bit-vector genome). Depending upon the problem, these may vary from as high as .05 per component
    # (e.g. 5% of all genome components are modified) to .01 per individual (e.g. 1 % of all individuals are mutated
    # in just ONE of their components).

    mutation_rate = 0.75
    mutation_scheme = 1  # 1: Single Mutation 2: Component Mutation

    adult_selection_scheme = 1  # 1:Full, 2:Over-production, 3:Mixing
    fitness_scaling_scheme = 2  # 0:Fitness-Proportionate, 1:Sigma-Scaling, 2:Tournament, 3:Boltzmann-Scaling
    local_selection_schemes = [2]

    """ Boltzmann """

    boltzmann_temperature = 30

    """ Tournament """

    tournament_size = 9
    tournament_random_choice_rate = 0.35

    """ Thresholds """

    fitness_threshold = 1
    maximum_generations = 40

    def __init__(self, genotype, fitness, ea_config):
        self.genotype = genotype
        self.fitness = fitness
        self.child_pool = []
        self.adult_pool = []
        self.parent_pool = []
        self.current_generation = 1
        self.gen_avg_fitness = []
        self.gen_best_fitness = []
        self.gen_standard_deviation = []
        self.global_adult_selection_scheme = True

        # Configure EA parameters
        EA.child_pool_size = ea_config.child_pool_size
        EA.adult_pool_size = ea_config.adult_pool_size
        EA.crossover_rate = ea_config.crossover_rate
        EA.crossover_points = ea_config.crossover_points
        EA.mutation_scheme = ea_config.mutation_scheme
        EA.mutation_rate = ea_config.mutation_rate
        EA.adult_selection_scheme = ea_config.adult_selection_scheme
        EA.fitness_scaling_scheme = ea_config.fitness_scaling_scheme
        EA.elitism = ea_config.elitism
        EA.maximum_generations = ea_config.maximum_generations
        EA.tournament_size = ea_config.tournament_size
        EA.tournament_random_choice_rate = ea_config.tournament_random_choice_rate
        EA.boltzmann_temperature = ea_config.boltzmann_temperature

        if EA.fitness_scaling_scheme in EA.local_selection_schemes:
            self.global_adult_selection_scheme = False

    def evolve(self):

        self.child_pool = self.genotype.generate_random_genotypes(EA.child_pool_size)
        while True:

            # Generate phenotypes from genotypes
            phenotypes = []
            for genotype in self.child_pool:
                phenotypes.append(genotype.translate_to_phenotype())

            # Evaluate fitness of phenotypes
            phenotypes_fitness = self.fitness.get_fitness_of_phenotypes(phenotypes)
            for i in xrange(len(self.child_pool)):
                self.child_pool[i].fitness = phenotypes_fitness[i]

            # Add average fitness, best fitness, and standard deviation to generational timeline
            self.gen_avg_fitness.append(self.fitness.avg_fitness)
            self.gen_best_fitness.append(self.fitness.best_fitness)
            self.gen_standard_deviation.append(self.fitness.standard_deviation)

            # Report current generation stats
            self.logging_routine()

            # Check for solution
            solution_index = self.fitness.check_for_solution(phenotypes_fitness)
            if solution_index != -1:
                print "Solution found: ", self.child_pool[solution_index], " after ", self.current_generation, " generations."
                return self.child_pool[solution_index]

            # Check if reached max number of generations
            if self.current_generation == EA.maximum_generations:
                print "Maximum number of generations (", self.current_generation, ") has been reached!"
                return self.child_pool[self.fitness.index_of_best_solution(phenotypes_fitness)]

            # Generate adult pool with selection scheme of choice
            if EA.adult_selection_scheme == 1:
                self.adult_pool = self.full_generational_replacement()
            elif EA.adult_selection_scheme == 2:
                self.adult_pool = self.adult_over_production()
            elif EA.adult_selection_scheme == 3:
                self.adult_pool = self.adult_generation_mixing()

            mating_pairs = []
            if self.global_adult_selection_scheme:

                # Fitness scaling for adjusting exploration and exploitation
                if EA.fitness_scaling_scheme == 1:
                    self.sigma_scaling()
                elif EA.fitness_scaling_scheme == 3:
                    self.boltzmann_scaling()

                    # Decrease boltzmann temperature for next generation
                    if EA.boltzmann_temperature > 1:
                        EA.boltzmann_temperature -= 1

                intervals = self.generate_intervals()

                # Select parents from adult pool
                crossover_index_pairs = []
                for i in xrange(EA.child_pool_size / 2):

                    genotype_x = self.grab_genotype(intervals)
                    genotype_y = genotype_x

                    while genotype_y is genotype_x:
                        genotype_y = self.grab_genotype(intervals)

                    crossover_index_pairs.append([genotype_x, genotype_y])

                for index_pair in crossover_index_pairs:
                    mating_pairs.append([deepcopy(self.adult_pool[index_pair[0]]), deepcopy(self.adult_pool[index_pair[1]])])
            else:
                if EA.fitness_scaling_scheme == 2:
                    mating_pairs = self.tournament()

            # Clear child pool for next generation
            self.child_pool = []

            # Elitism
            for i in xrange(EA.elitism):
                self.child_pool.append(self.adult_pool[i])

            # Reproduce mating pairs
            for mating_pair in mating_pairs:

                # Crossover by chance
                if uniform(0.00, 1.00) <= EA.crossover_rate:
                    children = self.genotype.crossover(mating_pair, EA.crossover_points)
                else:
                    children = [mating_pair[0].bit_vector, mating_pair[1].bit_vector]

                # Mutate by chance
                for child_chromosome in children:
                    child_genotype = self.genotype(child_chromosome)
                    if uniform(0.00, 1.00) <= EA.mutation_rate:
                        if EA.mutation_scheme == 1:
                            child_genotype.mutate()
                        elif EA.mutation_scheme == 2:
                            child_genotype.component_mutation(EA.mutation_rate)

                    self.child_pool.append(child_genotype)

            self.current_generation += 1

    def logging_routine(self):
        print "Generation: ", self.current_generation, "  \t", \
            "Average fitness: ", "%.3f" % self.fitness.avg_fitness, "\t", \
            "Best fitness: ", "%.3f" % self.fitness.best_fitness, "\t", \
            "Standard deviation: ", "%.3f" % self.fitness.standard_deviation

    """ ADULT SELECTION """

    def full_generational_replacement(self):
        return sorted(list(self.child_pool), key=lambda genotype: genotype.fitness, reverse=True)

    def adult_over_production(self):
        fitness_ordered_genotypes = sorted(list(self.child_pool), key=lambda genotype: genotype.fitness, reverse=True)
        return fitness_ordered_genotypes[0:EA.adult_pool_size]

    def adult_generation_mixing(self):
        fitness_ordered_genotypes = sorted(list(self.adult_pool + self.child_pool), key=lambda genotype: genotype.fitness, reverse=True)
        return fitness_ordered_genotypes[0:EA.adult_pool_size]

    """ MATE SELECTION """

    def grab_genotype(self, intervals):
        grab_index = uniform(0.0000, 1.0000)
        for i in xrange(len(intervals)):
            if intervals[i][0] <= grab_index < intervals[i][1]:
                return i

    def total_fitness(self):
        total_fitness = 0
        for genotype in self.adult_pool:
            total_fitness += genotype.fitness

        return total_fitness

    def generate_intervals(self):

        fitness_proportionate_intervals = []
        total_fitness = self.total_fitness()

        interval_start = 0
        for genotype in self.adult_pool:
            interval_end = interval_start + (genotype.fitness / float(total_fitness))
            fitness_proportionate_intervals.append([interval_start, interval_end, interval_end-interval_start])
            interval_start = interval_end

        return fitness_proportionate_intervals

    def sigma_scaling(self):

        fitness_average = self.fitness.avg_fitness
        fitness_standard_deviation = self.fitness.standard_deviation

        if fitness_standard_deviation != 0:
            for genotype in self.child_pool:
                genotype.fitness *= 1 + ((genotype.fitness - fitness_average) / (2*(fitness_standard_deviation * 100)))

    def tournament(self):

        # Container for all winner pairs
        mating_pairs = []

        for i in xrange(EA.child_pool_size/2):

            # Generate tournament poo (individuals that will compete for mating)
            competitors = self.pick_tournament_competitors()

            pair = []
            current_best = 0

            # Pick first individual of mating pair
            if uniform(0.0, 1.0) < (1 - EA.tournament_random_choice_rate):
                pair.append(deepcopy(competitors[current_best]))
                current_best = 1
            else:
                pair.append(deepcopy(competitors[randint(0, (len(competitors) - 1))]))

            # Pick second individual of mating pair
            mating_pair = pair[0]
            while mating_pair is pair[0]:
                if uniform(0.0, 1.0) < (1 - EA.tournament_random_choice_rate):
                    mating_pair = competitors[current_best]
                else:
                    mating_pair = competitors[randint(0, (len(competitors) - 1))]

            pair.append(deepcopy(mating_pair))
            mating_pairs.append(pair)

        return mating_pairs

    def pick_tournament_competitors(self):
        adults = list(self.adult_pool)
        competitors = []
        while len(competitors) < EA.tournament_size:
            competitors.append(adults.pop(randint(0, (len(adults) - 1))))

        competitors.sort(key=lambda genotype: genotype.fitness, reverse=True)
        return competitors

    def boltzmann_scaling(self):
        avg_of_fitness_exp = self.avg_of_fitness_exp()
        for genotype in self.child_pool:
            genotype.fitness *= (EA.fitness_exp(genotype) / avg_of_fitness_exp)

    def avg_of_fitness_exp(self):
        total_exponential_fitness = 0
        for genotype in self.child_pool:
            total_exponential_fitness += self.fitness_exp(genotype)

        return total_exponential_fitness / float(len(self.adult_pool))

    @staticmethod
    def fitness_exp(genotype):
        return exp(genotype.fitness/EA.boltzmann_temperature)
