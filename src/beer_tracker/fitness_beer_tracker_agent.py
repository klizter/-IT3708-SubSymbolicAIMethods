from fitness import Fitness
from beer_tracker_world import BeerTrackerWorld, TrackerResult
from beer_tracker_agent import BeerTrackerAgent, TrackerActions
from ctrnn import ContinuesTimeRecurrentNeuralNetwork


class FitnessBeerTrackerAgent(Fitness):

    time_steps = 600
    world_wrap = True
    agent_start_position = 5
    pulling = False

    @classmethod
    def evaluate_fitness_of_phenotypes(cls, phenotypes):
        phenotypes_fitness = list()

        for phenotype in phenotypes:

            # Initialize ctrnn, agent, and world
            ctrnn = ContinuesTimeRecurrentNeuralNetwork.construct_ctrnn(phenotype.layer_weights,
                                                                        phenotype.gain_terms,
                                                                        phenotype.time_constants)
            agent = BeerTrackerAgent(ctrnn)
            world = BeerTrackerWorld(cls.agent_start_position, 15, 30, cls.world_wrap)

            # Tracker stats
            avoided_objects = 0
            captured_objects = 0
            capturable_objects = 0
            total_objects = 0

            # World time state
            current_time_step = 1

            # Run agent through world scenario
            while current_time_step < cls.time_steps:

                # Get tracker shadow sensors reading
                sensor_readings = world.get_tracker_shadow_sensors_reading()

                # If no world wrap we also need edge sensors reading
                if cls.world_wrap is not True:
                    sensor_readings += world.get_tracker_edge_sensors_reading()

                # Ask agent for action based on sensor inputs
                action = agent.choose_action(sensor_readings, cls.pulling)

                # Do tracker action
                if cls.pulling and action[0] is TrackerActions.PULL:
                    world.pull_falling_object()
                elif action[0] is TrackerActions.MOVE_RIGHT:
                    world.move_tracker_horizontally(action[1])
                elif action[0] is TrackerActions.MOVE_LEFT:
                    world.move_tracker_horizontally(-action[1])

                # If tracker and falling object is at same Y coordinate check result
                if world.is_tracker_and_falling_object_vertically_level():

                    # Keep track of all falling objects residing on tracker level
                    total_objects += 1

                    # Set capturable condition
                    capturable = world.is_capturable()

                    # Keep tracker of how many capturable objects in world scenario
                    if capturable:
                        capturable_objects += 1

                    # Get tracker result
                    result = world.get_tracker_result()

                    # Check tracker result and update stats
                    if result == TrackerResult.AVOIDED and capturable is False:
                        avoided_objects += 1
                    elif result == TrackerResult.CAPTURED and capturable is True:
                        captured_objects += 1

                current_time_step += 1

            # Evaluate fitness of agent and add it to collection
            phenotypes_fitness.append(cls.fitness_function(captured_objects, avoided_objects,
                                                           capturable_objects, total_objects - capturable_objects))

        return phenotypes_fitness

    @classmethod
    def fitness_function(cls, captured_objects, avoided_objects, capturable_objects, avoidable_objects):
        return (captured_objects + avoided_objects) / (capturable_objects + avoidable_objects)
