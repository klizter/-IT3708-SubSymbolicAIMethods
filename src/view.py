from Tkinter import *
from ea import EA
from ea_config import EAConfig
from genotype import Genotype
from one_max.fitness_one_max import FitnessOneMax
from lolz_prefix.fitness_lolz_prefix import FitnessLOLZPrefix
from lolz_prefix.genotype_lolz_prefix import GenotypeLOLZPrefix
from suprising_sequence.fitness_globally_suprising_sequence import FitnessGloballySuprisingSequence
from suprising_sequence.fitness_locally_suprising_sequence import FitnessLocallySuprisingSequence
from suprising_sequence.genotype_suprising_sequence import GenotypeSuprisingSequence
from flatland.fitness_flatland_agent import FitnessFlatlandAgent
from flatland.genotype_neural_network_weights import GenotypeNeuralNetworkWeights
from beer_tracker.genotype_ctrnn import GenotypeCTRNNWeights
from beer_tracker.fitness_beer_tracker_agent import FitnessBeerTrackerAgent
from beer_tracker.beer_tracker_view import BeerTrackerView
from plot_evolution import PlotEvolution
from flatland.flatland_view import FlatlandView



class View(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("EA Configuration Panel")

        # Available Genotypes Classes
        self.genotype_classes = {1: Genotype,
                                 2: GenotypeLOLZPrefix,
                                 3: GenotypeSuprisingSequence,
                                 4: GenotypeSuprisingSequence,
                                 5: GenotypeNeuralNetworkWeights,
                                 6: GenotypeCTRNNWeights}

        # Available Fitness Classes
        self.fitness_classes = {1: FitnessOneMax,
                                2: FitnessLOLZPrefix,
                                3: FitnessGloballySuprisingSequence,
                                4: FitnessLocallySuprisingSequence,
                                5: FitnessFlatlandAgent,
                                6: FitnessBeerTrackerAgent}

        # GUI State variables
        self.child_pool_size = IntVar(self, EA.child_pool_size)
        self.adult_pool_size = IntVar(self, EA.adult_pool_size)
        self.crossover_rate = DoubleVar(self, EA.crossover_rate)
        self.crossover_points = IntVar(self, EA.crossover_points)
        self.mutation_rate = DoubleVar(self, EA.mutation_rate)
        self.mutation_scheme = IntVar(self, EA.mutation_scheme)
        self.adult_selection_scheme = IntVar(self, EA.adult_selection_scheme)
        self.parent_selection_scheme = IntVar(self, EA.fitness_scaling_scheme)
        self.elitism = IntVar(self, EA.elitism)
        self.tournament_size = IntVar(self, EA.tournament_size)
        self.tournament_random_choice_rate = DoubleVar(self, EA.tournament_random_choice_rate)
        self.boltzmann_temperature = IntVar(self, EA.boltzmann_temperature)
        self.maximum_generations = IntVar(self, EA.maximum_generations)
        self.problem_selected = IntVar(self, 6)
        self.one_max_length = IntVar(self, 100)
        self.one_max_random = IntVar(self, 1)
        self.lolz_prefix_z = IntVar(self, 4)
        self.lolz_prefix_length = IntVar(self, 80)
        self.gss_symbols = IntVar(self, 37)
        self.gss_length = IntVar(self, 75)
        self.lss_symbols = IntVar(self, 32)
        self.lss_length = IntVar(self, 720)
        self.aggregate_plot_data = IntVar(self, 0)
        self.accumulation_bound = IntVar(self, 10)
        self.accumulations = 0
        self.ea_iterations = 0
        self.flatland_num_scenarios = IntVar(self, FitnessFlatlandAgent.number_of_scenarios)
        self.flatland_dynamic_scenarios = IntVar(self, int(FitnessFlatlandAgent.dynamic_scenarios))
        self.flatland_time_steps = IntVar(self, FitnessFlatlandAgent.max_time_steps)
        self.beer_tracker_world_wrap = IntVar(self, int(FitnessBeerTrackerAgent.world_wrap))
        self.beer_tracker_pulling = IntVar(self, int(FitnessBeerTrackerAgent.pulling))


        # Create GUI Elements
        Label(self, text="EA General Settings").grid(row=0, columnspan=6, pady=20)

        Label(self, text="Child pool size: ").grid(row=1, column=0)
        Entry(self, textvariable=self.child_pool_size).grid(row=1, column=1)
        Label(self, text="Adult pool size: ").grid(row=1, column=2)
        Entry(self, textvariable=self.adult_pool_size) .grid(row=1, column=3)
        Label(self, text="Max generations: ").grid(row=1, column=4)
        Entry(self, textvariable=self.maximum_generations) .grid(row=1, column=5)

        Label(self, text="Crossover rate: ").grid(row=2, column=0)
        Entry(self, textvariable=self.crossover_rate).grid(row=2, column=1)
        Label(self, text="Crossover points: ").grid(row=2, column=2)
        Entry(self, textvariable=self.crossover_points).grid(row=2, column=3)

        Label(self, text="Mutation scheme: ").grid(row=3, column=0)
        Radiobutton(self, text="Single",
                    variable=self.mutation_scheme, value=1).grid(row=3, column=1)
        Radiobutton(self, text="Component",
                    variable=self.mutation_scheme, value=2).grid(row=3, column=2)
        Label(self, text="Mutation rate: ").grid(row=3, column=4)
        Entry(self, textvariable=self.mutation_rate).grid(row=3, column=5)

        Label(self, text="Adult Selection Scheme").grid(row=4, columnspan=6, pady=20)

        Radiobutton(self, text="Full replacement",
                    variable=self.adult_selection_scheme, value=1).grid(row=5, column=1)
        Radiobutton(self, text="Over production",
                    variable=self.adult_selection_scheme, value=2).grid(row=5, column=2, columnspan=2)
        Radiobutton(self, text="Mixing",
                    variable=self.adult_selection_scheme, value=3).grid(row=5, column=4)
        Label(self, text="Parent Selection Scheme").grid(row=6, columnspan=6, pady=20)

        Radiobutton(self, text="Fitness proportionate scaling",
                    variable=self.parent_selection_scheme, value=0).grid(row=7, column=0)
        Radiobutton(self, text="Sigma Scaling", variable=self.parent_selection_scheme, value=1).grid(row=7, column=1)
        Radiobutton(self, text="Tournament",
                    variable=self.parent_selection_scheme, value=2).grid(row=7, column=2)
        Radiobutton(self, text="Boltzmann Scaling",
                    variable=self.parent_selection_scheme, value=3).grid(row=7, column=3)
        Label(self, text="Elitism: ").grid(row=7, column=4)
        Entry(self, textvariable=self.elitism).grid(row=7, column=5)

        Label(self, text="Tournament Settings").grid(row=8, column=0, pady=20)

        Label(self, text="Size: ").grid(row=8, column=1)
        Entry(self, textvariable=self.tournament_size).grid(row=8, column=2)
        Label(self, text="Random choice rate: ").grid(row=8, column=3)
        Entry(self, textvariable=self.tournament_random_choice_rate).grid(row=8, column=4)

        Label(self, text="Boltzmann Settings").grid(row=9, column=0, pady=20)
        Label(self, text="Temperature: ").grid(row=9, column=1)
        Entry(self, textvariable=self.boltzmann_temperature).grid(row=9, column=2)

        Label(self, text="Problem Settings").grid(row=11, columnspan=6, pady=20)

        Radiobutton(self, text="ONE-MAX",
                    variable=self.problem_selected, value=1).grid(row=12, column=0)
        Radiobutton(self, text="LOLZ-Prefix",
                    variable=self.problem_selected, value=2).grid(row=12, column=1)
        Radiobutton(self, text="Globally SS",
                    variable=self.problem_selected, value=3).grid(row=12, column=2)
        Radiobutton(self, text="Locally SS",
                    variable=self.problem_selected, value=4).grid(row=12, column=3)
        Radiobutton(self, text="Flatland",
                    variable=self.problem_selected, value=5).grid(row=12, column=4)
        Radiobutton(self, text="Beer Tracker",
                    variable=self.problem_selected, value=6).grid(row=12, column=5, pady=20)

        Label(self, text="ONE-MAX Settings").grid(row=13, column=0, pady=12)

        Label(self, text="Length: ").grid(row=13, column=1)
        Entry(self, textvariable=self.one_max_length).grid(row=13, column=2)
        Checkbutton(self, text="Random Solution", variable=self.one_max_random,
                    onvalue=1, offvalue=0, height=2, width=20).grid(row=13, column=4)

        Label(self, text="LOLZ-Prefix Settings").grid(row=14, column=0, pady=12)

        Label(self, text="Length: ").grid(row=14, column=1)
        Entry(self, textvariable=self.lolz_prefix_length).grid(row=14, column=2)
        Label(self, text="Z: ").grid(row=14, column=3)
        Entry(self, textvariable=self.lolz_prefix_z).grid(row=14, column=4)

        Label(self, text="GSS Settings").grid(row=15, column=0, pady=12)

        Label(self, text="Symbols: ").grid(row=15, column=1)
        Entry(self, textvariable=self.gss_symbols).grid(row=15, column=2)
        Label(self, text="Length: ").grid(row=15, column=3)
        Entry(self, textvariable=self.gss_length).grid(row=15, column=4)

        Label(self, text="LSS Settings").grid(row=16, column=0, pady=12)

        Label(self, text="Symbols: ").grid(row=16, column=1)
        Entry(self, textvariable=self.lss_symbols).grid(row=16, column=2)
        Label(self, text="Length: ").grid(row=16, column=3)
        Entry(self, textvariable=self.lss_length).grid(row=16, column=4)

        Label(self, text="Flatland Settings").grid(row=17, column=0, pady=12)

        Label(self, text="Scenarios: ").grid(row=17, column=1)
        Entry(self, textvariable=self.flatland_num_scenarios).grid(row=17, column=2)
        Label(self, text="Time steps: ").grid(row=17, column=3)
        Entry(self, textvariable=self.flatland_time_steps).grid(row=17, column=4)
        Checkbutton(self, text="Dynamic", variable=self.flatland_dynamic_scenarios,
                    onvalue=1, offvalue=0, height=2, width=20).grid(row=17, column=5)

        Label(self, text="Beer Tracker Settings").grid(row=18, column=0, pady=12)

        Checkbutton(self, text="Pulling", variable=self.beer_tracker_pulling,
                    onvalue=1, offvalue=0, height=2, width=20).grid(row=18, column=2)
        Checkbutton(self, text="Wrap", variable=self.beer_tracker_world_wrap,
                    onvalue=1, offvalue=0, height=2, width=20).grid(row=18, column=3)

        Label(self, text="Runtime Configurations").grid(row=19, columnspan=6, pady=20)

        Button(self, text="Start EA", width=25, command=self.load_ea).grid(row=20, column=0, pady=20, padx=20)
        Checkbutton(self, text="Aggregated plotting", variable=self.aggregate_plot_data,
                    onvalue=1, offvalue=0, height=5, width=20).grid(row=20, column=3)
        Label(self, text="Accumulations: ").grid(row=20, column=4)
        Entry(self, textvariable=self.accumulation_bound).grid(row=20, column=5, padx=20)

    # Configure EA meta settings before
    def load_ea(self):

        if self.aggregate_plot_data.get() == 1:
            self.ea_iterations = self.accumulation_bound.get()
        else:
            self.ea_iterations = 1

        self.run_ea()

    def run_ea(self):
        iterations_completed = 0
        PlotEvolution.x_limit = self.maximum_generations.get()
        while self.ea_iterations != iterations_completed:

            ea_config = EAConfig(self.child_pool_size.get(),
                                 self.adult_pool_size.get(),
                                 self.crossover_rate.get(),
                                 self.crossover_points.get(),
                                 self.mutation_scheme.get(),
                                 self.mutation_rate.get(),
                                 self.adult_selection_scheme.get(),
                                 self.parent_selection_scheme.get(),
                                 self.elitism.get(),
                                 self.maximum_generations.get(),
                                 self.tournament_size.get(),
                                 self.tournament_random_choice_rate.get(),
                                 self.boltzmann_temperature.get())

            genotype_class = self.genotype_classes[self.problem_selected.get()]
            fitness_class = self.fitness_classes[self.problem_selected.get()]

            ea = EA(genotype_class, fitness_class, ea_config)

            # Configure problems
            if self.problem_selected.get() == 1:
                self.genotype_classes[1].bit_vector_length = self.one_max_length.get()
                self.fitness_classes[1].random = bool(self.one_max_random.get())
            elif self.problem_selected.get() == 2:
                self.genotype_classes[2].bit_vector_length = self.lolz_prefix_length.get()
                self.fitness_classes[2].z = self.lolz_prefix_z.get()
            elif self.problem_selected.get() == 3:
                self.genotype_classes[3].symbols = self.gss_symbols.get()
                self.genotype_classes[3].length = self.gss_length.get()
            elif self.problem_selected.get() == 4:
                self.genotype_classes[4].symbols = self.lss_symbols.get()
                self.genotype_classes[4].length = self.lss_length.get()
            elif self.problem_selected.get() == 5:
                self.fitness_classes[5].max_time_steps = self.flatland_time_steps.get()
                self.fitness_classes[5].number_of_scenarios = self.flatland_num_scenarios.get()
                self.fitness_classes[5].dynamic_scenarios = bool(self.flatland_dynamic_scenarios.get())
            elif self.problem_selected.get() == 6:
                self.fitness_classes[6].pulling = bool(self.beer_tracker_pulling.get())
                self.fitness_classes[6].world_wrap = bool(self.beer_tracker_world_wrap.get())

                # Configure CTRNN for pulling scenario
                if self.fitness_classes[6].pulling:
                    self.genotype_classes[6].topology[-1] = 3

                # Configure CTRNN for world wrap scenario
                if not self.fitness_classes[6].world_wrap:
                    self.genotype_classes[6].topology[0] = 7
                    self.genotype_classes[6].weight_lower_bound = -7.0
                    self.genotype_classes[6].weight_upper_bound = 7.0

                self.genotype_classes[6].calculate_ctrnn_intervals()

            # Report settings and start evolution
            solution = ea.evolve()
            genotype_class.report_genotype_settings()
            ea_config.report()

            # # Plot aggregated data
            # if self.aggregate_plot_data.get() == 1:
            #
            #     PlotEvolution.accumulate_average_data(ea.gen_avg_fitness,
            #                                           ea.gen_best_fitness,
            #                                           ea.gen_standard_deviation)
            #     self.accumulations += 1
            #
            #     if self.accumulations == self.accumulation_bound.get():
            #         PlotEvolution.plot_evolution(PlotEvolution.aggregated_avg_fitness,
            #                                      PlotEvolution.aggregated_best_fitness,
            #                                      PlotEvolution.aggregated_standard_deviation)
            #         self.accumulations = 0
            #         PlotEvolution.clear_aggregated_data()
            # else:
            #
            #     PlotEvolution.plot_evolution(ea.gen_best_fitness,
            #                                  ea.gen_best_fitness,
            #                                  ea.gen_standard_deviation)

            # If Flatland, run simulation
            if self.problem_selected.get() == 5:
                view = FlatlandView(fitness_class.flatland_scenarios, solution, self.flatland_time_steps.get())
                view.after(20, view.agenda_loop())
                view.mainloop()

            # If Beer Tracker, run simulation
            if self.problem_selected.get() == 6:
                view = BeerTrackerView(solution.translate_to_phenotype(), self.beer_tracker_world_wrap.get(),
                                       self.beer_tracker_pulling.get())
                view.after(20, view.agenda_loop())
                view.mainloop()

            iterations_completed += 1

view = View()
view.lift()
view.call('wm', 'attributes', '.', '-topmost', True)
view.after_idle(view.call, 'wm', 'attributes', '.', '-topmost', False)
view.mainloop()
