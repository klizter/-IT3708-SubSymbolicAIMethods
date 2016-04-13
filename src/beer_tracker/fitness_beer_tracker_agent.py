from fitness import Fitness
from beer_tracker_world import BeerTrackerWorld, TrackerResult
from beer_tracker_agent import BeerTrackerAgent, TrackerActions
from ctrnn import ContinuesTimeRecurrentNeuralNetwork
from libs.multiprocess import parmap


class FitnessBeerTrackerAgent(Fitness):

    time_steps = 600
    world_wrap = True
    agent_start_position = 5
    pulling = False
    captured_scale = 0.5
    avoided_scale = 0.5


    @classmethod
    def evaluate_fitness_of_phenotype(cls, phenotype):

        # Initialize ctrnn, agent, and world
        ctrnn = ContinuesTimeRecurrentNeuralNetwork.construct_ctrnn(phenotype.layer_weights,
                                                                    phenotype.gain_terms,
                                                                    phenotype.time_constants)
        agent = BeerTrackerAgent(ctrnn)
        world = BeerTrackerWorld(cls.agent_start_position, 15, 30, cls.world_wrap)

        # Tracker scenario stats
        avoided_objects = 0
        captured_objects = 0
        pull_captured = 0
        capturable_objects = 0
        total_objects = 0

        # World state
        current_time_step = 1
        objects_level = False
        object_pulled = False

        # Run agent through world scenario
        while current_time_step < cls.time_steps:

            # Generate new falling object on next time step
            if objects_level:
                world.generate_falling_object()
                objects_level = False
                object_pulled = False

            # Get tracker shadow sensors reading
            sensor_readings = world.get_tracker_shadow_sensors_reading()

            # If no world wrap we also need edge sensors reading
            if not cls.world_wrap:
                sensor_readings += world.get_tracker_edge_sensors_reading()

            # Ask agent for action based on sensor inputs
            action = agent.choose_action(sensor_readings, cls.pulling)

            # Do tracker action
            if cls.pulling and action[0] is TrackerActions.PULL:
                world.pull_falling_object()
                object_pulled = True
            else:
                if action[0] is TrackerActions.MOVE_RIGHT:
                    world.move_tracker_horizontally(action[1])
                elif action[0] is TrackerActions.MOVE_LEFT:
                    world.move_tracker_horizontally(-action[1])

                # Increment fall of falling object
                world.increment_falling_object()

            # If tracker and falling object is at same Y coordinate check result
            if world.is_tracker_and_falling_object_vertically_level():

                # Keep track of all falling objects residing on tracker level
                total_objects += 1
                objects_level = True

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
                    if object_pulled:
                        pull_captured += 1

            current_time_step += 1

        # Evaluate fitness
        phenotype_fitness = cls.fitness_function(captured_objects, avoided_objects, capturable_objects,
                                                 total_objects - capturable_objects)

        # If pulling return captured total also
        if cls.pulling:

            # Return both total captured and fitness
            return cls.pull_fitness_function(phenotype_fitness, pull_captured, capturable_objects)

        # Return fitness
        return phenotype_fitness

    @classmethod
    def pull_fitness_function(cls, fitness, pull_captured, capturable_objects):
        pull_reward = 0
        if pull_captured > 0:
            pull_reward = 0.25
        return (fitness * 0.5) + ((pull_captured / capturable_objects) * 0.25) + pull_reward

    @classmethod
    def fitness_function(cls, captured_objects, avoided_objects, capturable_objects, avoidable_objects):

        # Evaluate fitness function parameters
        if capturable_objects:
            captured_score = captured_objects / float(capturable_objects)
        else:
            captured_score = 0

        if avoidable_objects:
            avoided_score = avoided_objects / float(avoidable_objects)
        else:
            avoided_score = 0

        # Return fitness of phenotype based on scales
        return (captured_score * cls.captured_scale) + (avoided_score * cls.avoided_scale)

    @classmethod
    def evaluate_fitness_of_phenotypes(cls, phenotypes):
        fitness_phenotypes = parmap(cls.evaluate_fitness_of_phenotype, phenotypes)
        return fitness_phenotypes
