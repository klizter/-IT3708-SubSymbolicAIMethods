from fitness import Fitness
from beer_tracker_world import BeerTrackerWorld, TrackerResult
from beer_tracker_agent import BeerTrackerAgent, TrackerActions
from ctrnn import ContinuesTimeRecurrentNeuralNetwork
from multiprocessing import Process, Pipe
from itertools import izip
import copy_reg
import types


def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)


def spawn(f):
        def fun(pipe,x):
            pipe.send(f(x))
            pipe.close()
        return fun


def parmap(f,X):
    pipe=[Pipe() for x in X]
    proc=[Process(target=spawn(f),args=(c,x)) for x,(p,c) in izip(X,pipe)]
    [p.start() for p in proc]
    [p.join() for p in proc]
    return [p.recv() for (p,c) in pipe]


class FitnessBeerTrackerAgent(Fitness):

    time_steps = 600
    world_wrap = True
    agent_start_position = 5
    pulling = False

    @classmethod
    def evaluate_fitness_of_phenotype(cls, phenotype):

        # Initialize ctrnn, agent, and world
        ctrnn = ContinuesTimeRecurrentNeuralNetwork.construct_ctrnn(phenotype.layer_weights,
                                                                    phenotype.gain_terms,
                                                                    phenotype.time_constants)
        agent = BeerTrackerAgent(ctrnn)
        world = BeerTrackerWorld(cls.agent_start_position, 15, 30, cls.world_wrap)

        # Tracker stats
        avoided_objects = 0
        captured_objects = 0
        neither_avoided_nor_caputured = 0

        capturable_objects = 0
        total_objects = 0

        # World state
        current_time_step = 1
        objects_level = False

        # Run agent through world scenario
        while current_time_step < cls.time_steps:

            # Generate new falling object on next time step
            if objects_level:
                world.generate_falling_object()
                objects_level = False

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
                elif result == TrackerResult.NEITHER:
                    neither_avoided_nor_caputured += 1

            current_time_step += 1

        # Evaluate fitness of agent and add it to collection
        return cls.fitness_function(captured_objects, avoided_objects, capturable_objects,
                                    total_objects - capturable_objects, neither_avoided_nor_caputured)

    @classmethod
    def fitness_function(cls, captured_objects, avoided_objects, capturable_objects, avoidable_objects, neither_avoided_nor_captured):

        # Scales
        diminisher_scale = 0.05
        captured_scale = 0.5
        avoided_scale = 0.5

        # Fitness function parameters
        if capturable_objects:
            captured_score = captured_objects / float(capturable_objects)
        else:
            captured_score = 0

        if avoidable_objects:
            avoided_score = avoided_objects / float(avoidable_objects)
        else:
            avoided_score = 0

        # neither_diminisher = 1 + (neither_avoided_nor_captured * diminisher_scale)
        neither_diminisher = 1

        return ((captured_score * captured_scale) + (avoided_score * avoided_scale)) / neither_diminisher

    @classmethod
    def evaluate_fitness_of_phenotypes(cls, phenotypes):
        result = parmap(cls.evaluate_fitness_of_phenotype, phenotypes)
        return result
