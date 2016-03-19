

class EAConfig:

    def __init__(self, child_pool_size, adult_pool_size, crossover_rate, crossover_points, mutation_scheme,
                 mutation_rate, adult_selection_scheme, fitness_scaling_scheme, elitism, maximum_generations,
                 tournament_size, tournament_random_choice_rate, boltzmann_temperature):
        self.child_pool_size = child_pool_size
        self.adult_pool_size = adult_pool_size
        self.crossover_rate = crossover_rate
        self.crossover_points = crossover_points
        self.mutation_scheme = mutation_scheme
        self.mutation_rate = mutation_rate
        self.adult_selection_scheme = adult_selection_scheme
        self.fitness_scaling_scheme = fitness_scaling_scheme
        self.elitism = elitism
        self.maximum_generations = maximum_generations
        self.tournament_size = tournament_size
        self.tournament_random_choice_rate = tournament_random_choice_rate
        self.boltzmann_temperature = boltzmann_temperature

        self.names_pss = {0: "fitness proportionate",
                          1: "sigman scaling",
                          2: "tournament",
                          3: "boltzmann scaling"}

        self.names_ass = {1: "full generational replacement",
                          2: "generational over production",
                          3: "mixing of generations"}

    def report(self):
        print "--------------------------------------------------------------------------------------------"
        print " Problem ran with the following EA configurations: "
        print "--------------------------------------------------------------------------------------------"
        print "     child pool size:\t\t\t\t", self.child_pool_size
        print "     adult pool size:\t\t\t\t", self.adult_pool_size
        print "     crossover rate:\t\t\t\t", self.crossover_rate
        print "     crossover points:\t\t\t\t", self.crossover_points
        print "     mutation_rate:\t\t\t\t\t", self.mutation_rate
        print "     adult selection scheme:\t\t", self.names_ass[self.adult_selection_scheme]
        print "     fitness scaling scheme:\t\t", self.names_pss[self.fitness_scaling_scheme]
        print "     elitism:\t\t\t\t\t\t", self.elitism
        print "     maximum number of generations:\t", self.maximum_generations
        print "     tournament size:\t\t\t\t", self.tournament_size
        print "     tournament random choice rate:\t", self.tournament_random_choice_rate
        print "     boltzmann temperature:\t\t", self.boltzmann_temperature
        print ""
