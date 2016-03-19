from fitness import Fitness
from flatland import Flatland, Direction, Move
from ann import NeuralNetwork, NeuronLayer
from flatland_agent import FlatlandAgent
from copy import deepcopy


class FitnessFlatlandAgent(Fitness):

    agent_start = [0, 0, Direction.SOUTH]
    max_time_steps = 60
    max_foods = 100 * Flatland.food_prob
    number_of_scenarios = 4
    flatland_scenarios = list()
    dynamic_scenarios = True

    @classmethod
    def evaluate_fitness_of_phenotypes(cls, phenotypes):

        # Generate scenarios if dynamic or non have been generated yet
        if cls.dynamic_scenarios or not len(cls.flatland_scenarios):
            cls.generate_flatland_scenarios()

        phenotypes_fitness = list()

        for phenotype in phenotypes:

            # Copy flatland so we can reuse for all phenotypes
            flatland_scenarios = [deepcopy(flatland_scenario) for flatland_scenario in cls.flatland_scenarios]

            # Init neural network layers from phenotype weights
            layers = list()
            for layer_weight in phenotype.layer_weights:
                layers.append(NeuronLayer(layer_weight))

            # Init phenotype neural network
            ann = NeuralNetwork(layers)

            # Init phenotype agent
            agent = FlatlandAgent(ann)

            # Init fitness container used for avg computation
            fitness_scenarios = list()

            # Run agent for scenarios
            for flatland_scenario in flatland_scenarios:

                # Init variables for scenario fitness evaluation
                phenotype_timesteps = 1
                poisons = 0
                foods = 0

                while phenotype_timesteps != cls.max_time_steps:

                    # Get sensor data [left, front, right]
                    cells = flatland_scenario.get_sensible_cells()

                    # Let agent choose action based on sensor data
                    action = agent.choose_action(cells)

                    # Effect of action
                    if action != Move.STAND_STILL:
                        cell_value = cells[action.value - 1]
                        if cell_value == Flatland.food:
                            foods += 1
                        elif cell_value == Flatland.poison:
                            poisons += 1

                    # Commit action to world
                    flatland_scenario.move_agent(action)

                    phenotype_timesteps += 1

                # Add fitness evaluation for scenario
                fitness_scenarios.append(cls.fitness_function(foods, poisons))

            # Evaluate fitness of agent and add it to collection
            phenotypes_fitness.append(sum(fitness_scenarios) / len(fitness_scenarios))

        return phenotypes_fitness

    @classmethod
    def generate_flatland_scenarios(cls):
        cls.flatland_scenarios = list()
        for i in xrange(cls.number_of_scenarios):
            cls.flatland_scenarios.append(Flatland(10, cls.agent_start))

    @classmethod
    # TODO: Review function, might need better distinction between 0 food, and 0 food with k poisons
    def fitness_function(cls, foods, poisons):
        if foods == 0:
            return 0.0
        return (foods / float(cls.max_foods)) / float(1 + (poisons * 0.5))
