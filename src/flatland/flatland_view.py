from flatland import Flatland, Direction
from ann import NeuralNetwork, NeuronLayer
from flatland_agent import FlatlandAgent
from Tkinter import *
import tkFont
from math import cos, sin, radians
from copy import deepcopy


class FlatlandView(Tk):

    viewport_height = 1000
    viewport_width = 1000
    edible_radius = 30
    edible_colors = {1: "#99c794", 2: "#ec5f68"}
    first_draw = True

    agent_body_scale = 2
    agent_sensor_scale = 2

    def __init__(self, flatland_scenarios, genotype_agent, time_steps, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.configure(background="#2b2b2b")

        # Static view state variables
        self.max_time_steps = time_steps
        self.phenotype_agent = genotype_agent.translate_to_phenotype()
        self.flatland_agent = FlatlandAgent(NeuralNetwork([NeuronLayer(w) for w in self.phenotype_agent.layer_weights]))
        self.canvas = Canvas(self, width=FlatlandView.viewport_width, height=FlatlandView.viewport_height,
                             bg="#a0a0a0", highlightbackground="#000000")
        self.agent_polygon_x_y = [10, -10, 30, 0, 10, 10, 0, 30, -10, 10, -30, 0, -10, -10]
        self.agent_senors_x_y = [30, -10, 40, 0, 30, 10, 20, 0,
                                 0, 40, -10, 30, 0, 20, 10, 30,
                                 -30, -10, -20, 0, -30, 10, -40, 0]
        self.flatland_length = flatland_scenarios[0].length
        self.agent_start = flatland_scenarios[0].agent_start

        # Dynamic view state variables
        self.flatland_scenarios = flatland_scenarios
        self.current_scenario = 0
        self.current_flatland_scenario = deepcopy(self.flatland_scenarios[self.current_scenario])
        self.time_steps = 0
        self.time_step_delay = IntVar(self, 1000)
        self.time_step_stringvar = StringVar(self, str(self.time_steps))
        self.sensor_rotation = 0

        # Draw flatland grid and configure canvas
        self.draw_canvas_lines()
        self.canvas.grid(rowspan=18, columnspan=3)

        self.time_step_num_font = tkFont.Font(family="Helvetica", size=72, weight="bold")
        self.time_step_text_font = tkFont.Font(family="Helvetica", size=18, weight="bold")
        self.time_step_frame = Frame(self, background="#2b2b2b")

        Label(self.time_step_frame, textvariable=self.time_step_stringvar, font=self.time_step_num_font,
              background="#2b2b2b", foreground="#a9b7c6").pack()
        Label(self.time_step_frame, text="time steps", font=self.time_step_text_font,
              background="#2b2b2b", foreground="#a9b7c6").pack()
        self.time_step_frame.grid(row=0, column=4)

        Scale(self, from_=250, to=5000, resolution=250, background="#2b2b2b", foreground="#a9b7c6",
              label="Time step delay (ms)", variable=self.time_step_delay).grid(row=16, column=4, padx=20)

        Button(self, text="New Scenarios", width=25, command=self.generate_new_scenarios, foreground="#a9b7c6",
               background="#2b2b2b", highlightbackground="#2b2b2b").grid(row=17, column=4, padx=20)

    def generate_new_scenarios(self):
        self.flatland_scenarios = [Flatland(self.flatland_length, self.agent_start)
                                   for _ in xrange(len(self.flatland_scenarios))]
        self.current_scenario = 0
        self.set_scenario()

    def draw_canvas_lines(self):
        for i in xrange(1, self.flatland_length):

            # Vertical lines
            self.canvas.create_line(100*i, 0, 100*i, self.__class__.viewport_height)

            # Horizontal lines
            self.canvas.create_line(0, 100*i, self.__class__.viewport_width, 100*i)

    def draw_grid_content(self):
        for i in xrange(1, self.flatland_length + 1):
            for j in xrange(1, self.flatland_length + 1):

                center_x = (100*j) - 50
                center_y = (100*i) - 50

                if self.current_flatland_scenario.grid[i-1][j-1] == Flatland.food:
                    self.draw_edible(center_x, center_y, Flatland.food)

                elif self.current_flatland_scenario.grid[i-1][j-1] == Flatland.poison:
                    self.draw_edible(center_x, center_y, Flatland.poison)

                elif self.current_flatland_scenario.grid[i-1][j-1] == Flatland.agent:
                    self.draw_agent(center_x, center_y)

        self.canvas.tag_raise("agent")

    def draw_edible(self, center_x, center_y, edible_type):
        self.canvas.create_oval(
            center_x - self.__class__.edible_radius,
            center_y - self.__class__.edible_radius,
            center_x + self.__class__.edible_radius,
            center_y + self.__class__.edible_radius,
            fill=self.__class__.edible_colors[edible_type], outline="#000000", tags="dynamic")

    def agent_rotate(self):
        if self.current_flatland_scenario.agent_direction == Direction.NORTH:
            return radians(180)
        elif self.current_flatland_scenario.agent_direction == Direction.WEST:
            return radians(90)
        elif self.current_flatland_scenario.agent_direction == Direction.EAST:
            return radians(-90)
        else:
            return 0

    def rotate_points(self, list_points, radians):
        rotated_points = []
        for i in xrange(0, len(list_points), 2):
            x = list_points[i]
            y = list_points[i+1]
            rotated_points.append((x * cos(radians)) - (y * sin(radians)))
            rotated_points.append((y * cos(radians)) + (x * sin(radians)))

        return rotated_points

    def translate_points(self, list_points, center_x, center_y):
        translated_points = []
        for i in xrange(0, len(list_points), 2):
            translated_points.append(list_points[i] + center_x)
            translated_points.append(list_points[i+1] + center_y)

        return translated_points

    def scale_points(self, list_points, scale):
        scaled_points = []
        for i in xrange(0, len(list_points)):
            scaled_points.append(list_points[i] * scale)

        return scaled_points


    def draw_agent(self, center_x, center_y):

        agent_polygon_x_y = list(self.agent_polygon_x_y)
        agent_sensors_x_y = list(self.agent_senors_x_y)
        rotate = self.agent_rotate()
        cls = self.__class__

        agent_polygon_x_y = self.rotate_points(agent_polygon_x_y, rotate)
        agent_polygon_x_y = self.scale_points(agent_polygon_x_y, cls.agent_body_scale)
        agent_polygon_x_y = self.translate_points(agent_polygon_x_y, center_x, center_y)

        agent_sensors_x_y = self.rotate_points(agent_sensors_x_y, rotate)
        agent_sensors_x_y = self.scale_points(agent_sensors_x_y, cls.agent_sensor_scale)
        agent_sensors_x_y = self.translate_points(agent_sensors_x_y, center_x, center_y)

        self.canvas.create_polygon(agent_polygon_x_y, fill="#6699cc",
                                   outline="#000000", tags=("dynamic", "agent"))
        self.canvas.create_polygon(list(agent_sensors_x_y[0:8]), fill="#f99157",
                                   outline="#000000", tags=("dynamic", "agent"))
        self.canvas.create_polygon(list(agent_sensors_x_y[8:16]), fill="#f99157",
                                   outline="#000000", tags=("dynamic", "agent"))
        self.canvas.create_polygon(list(agent_sensors_x_y[16:24]), fill="#f99157",
                                   outline="#000000", tags=("dynamic", "agent"))

    def run_time_step(self):
        self.time_steps += 1
        if not self.first_draw:
            # Agent move
            cells = self.current_flatland_scenario.get_sensible_cells()
            action = self.flatland_agent.choose_action(cells)
            self.current_flatland_scenario.move_agent(action)

            if self.time_steps == self.max_time_steps:
                self.change_scenario()
                self.time_steps = 0

            self.update_time_step_label()

        else:
            self.first_draw = False

        self.after(self.time_step_delay.get(), self.run_time_step)

    def change_scenario(self):
        if self.current_scenario + 1 < len(self.flatland_scenarios):
            self.current_scenario += 1
        else:
            self.current_scenario = 0

        self.set_scenario()

    def set_scenario(self):
        self.current_flatland_scenario = deepcopy(self.flatland_scenarios[self.current_scenario])
        self.time_steps = 0
        FlatlandView.first_draw = True

    def update_time_step_label(self):
        self.time_step_stringvar.set(str(self.time_steps))

    def agenda_loop(self):
        self.canvas.delete('dynamic')

        if self.first_draw:
            self.run_time_step()

        self.draw_grid_content()

        self.after(30, self.agenda_loop)
