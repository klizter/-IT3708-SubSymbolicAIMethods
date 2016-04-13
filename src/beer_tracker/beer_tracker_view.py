from beer_tracker_world import BeerTrackerWorld, TrackerResult
from beer_tracker_agent import BeerTrackerAgent, TrackerActions
from genotype_ctrnn import GenotypeCTRNNWeights
from fitness_beer_tracker_agent import FitnessBeerTrackerAgent
from ctrnn import ContinuesTimeRecurrentNeuralNetwork
from Tkinter import *


class BeerTrackerView(Tk):

    viewport_height = 450
    viewport_width = 900
    colors = {1: "#99c794", 2: "#ec5f68", 3: "#c594c5", 4: "#cf7c3b", 5: "#5fb3b3"}

    def __init__(self, phenotype, world_wrap, pulling, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.configure(background="#2b2b2b")
        self.first_draw = True
        self.world = BeerTrackerWorld(FitnessBeerTrackerAgent.agent_start_position, 15, 30, world_wrap)
        self.ctrnn = ContinuesTimeRecurrentNeuralNetwork.construct_ctrnn(phenotype.layer_weights,
                                                                         phenotype.gain_terms,
                                                                         phenotype.time_constants)
        print phenotype.layer_weights
        print phenotype.gain_terms
        print phenotype.time_constants

        self.agent = BeerTrackerAgent(self.ctrnn)
        self.objects_level = False

        self.max_time_steps = 600
        self.time_steps = 0
        self.objects_level = False
        self.world_wrap = world_wrap
        self.pulling = pulling
        self.tracker_catch = False

        self.unit_dimensions = [60, 60]
        self.canvas = Canvas(self, width=BeerTrackerView.viewport_width, height=BeerTrackerView.viewport_height,
                             bg="#a0a0a0", highlightbackground="#000000")
        self.canvas.grid(rowspan=4, columnspan=8)
        self.draw_tracker()
        self.draw_falling_object()
        self.draw_canvas_lines()

        # GenotypeCTRNNWeights.topology
        # GenotypeCTRNNWeights.calculate_ctrnn_intervals()

    def draw_canvas_lines(self):
        for i in xrange(1, 30):

            # Vertical lines
            self.canvas.create_line(30*i, 0, 30*i, self.__class__.viewport_height)

        for i in xrange(1, 15):
            # # Horizontal lines
            self.canvas.create_line(0, 30*i, self.__class__.viewport_width, 30*i)

    def draw_tracker(self):
        cls = self.__class__
        tracker_units = self.world.get_tracker_units()

        fill_color = cls.colors[3]
        if self.tracker_catch:
            fill_color = cls.colors[4]

        for i in xrange(len(tracker_units[0])):
            self.canvas.create_rectangle((tracker_units[0][i]-1)*30,
                                         (tracker_units[1]-1)*30,
                                         (tracker_units[0][i]-1)*30+30,
                                         (tracker_units[1]-1)*30+30,
                                         fill=fill_color, outline="#000000", tags="dynamic")

    def draw_falling_object(self):
        cls = self.__class__

        falling_object_edge_units = self.world.get_falling_object_units()

        fill_color = cls.colors[5]
        if len(falling_object_edge_units[0]) < 5:
            fill_color = cls.colors[1]

        for i in xrange(len(falling_object_edge_units[0])):
            self.canvas.create_rectangle((falling_object_edge_units[0][i]-1)*30,
                                         (falling_object_edge_units[1]-1)*30,
                                         (falling_object_edge_units[0][i]-1)*30+30,
                                         (falling_object_edge_units[1]-1)*30+30,
                                         fill=fill_color, outline="#000000", tags="dynamic")

    def run_time_step(self):
        self.time_steps += 1

        # Generate new falling object on next time step
        if self.objects_level:
            self.world.generate_falling_object()
            self.objects_level = False

        # Get tracker shadow sensors reading
        sensor_readings = self.world.get_tracker_shadow_sensors_reading()

        # If no self.world wrap we also need edge sensors reading
        if not self.world_wrap:
            sensor_readings += self.world.get_tracker_edge_sensors_reading()

        # Ask agent for action based on sensor inputs
        action = self.agent.choose_action(sensor_readings, self.pulling)

        # Do tracker action
        if self.pulling and action[0] is TrackerActions.PULL:
            self.world.pull_falling_object()
        else:
            if action[0] is TrackerActions.MOVE_RIGHT:
                self.world.move_tracker_horizontally(action[1])
            elif action[0] is TrackerActions.MOVE_LEFT:
                self.world.move_tracker_horizontally(-action[1])

            # Increment fall of falling object
            self.world.increment_falling_object()

        # If tracker and falling object is at same Y coordinate check result
        if self.world.is_tracker_and_falling_object_vertically_level():

            self.objects_level = True

            result = self.world.get_tracker_result()
            if result == TrackerResult.CAPTURED:
                self.tracker_catch = True
        else:
            self.tracker_catch = False

        self.after(100, self.run_time_step)

    def agenda_loop(self):

        # Clear canvas
        self.canvas.delete("dynamic")

        # Start timesteps
        if self.first_draw:
            self.run_time_step()
            self.first_draw = False

        # Draw tracker and falling object
        self.draw_falling_object()
        self.draw_tracker()

        self.after(20, self.agenda_loop)
