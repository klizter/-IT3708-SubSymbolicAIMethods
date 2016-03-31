from beer_tracker_world import BeerTrackerWorld
from Tkinter import *
from random import randint


class BeerTrackerView(Tk):

    viewport_height = 450
    viewport_width = 900
    colors = {1: "#99c794", 2: "#ec5f68", 3: "#c594c5", 4: "#cf7c3b", 5: "#5fb3b3"}

    def __init__(self, beer_tracker_world, time_steps, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.configure(background="#2b2b2b")
        self.first_draw = True
        self.beer_tracker_world = beer_tracker_world
        self.max_time_steps = time_steps
        self.time_steps = 0
        self.unit_dimensions = [60, 60]
        self.canvas = Canvas(self, width=BeerTrackerView.viewport_width, height=BeerTrackerView.viewport_height,
                             bg="#a0a0a0", highlightbackground="#000000")
        self.canvas.grid(rowspan=4, columnspan=8)
        self.draw_tracker()
        self.draw_falling_object()
        self.draw_canvas_lines()

    def draw_canvas_lines(self):
        for i in xrange(1, 30):

            # Vertical lines
            self.canvas.create_line(30*i, 0, 30*i, self.__class__.viewport_height)

        for i in xrange(1, 15):
            # # Horizontal lines
            self.canvas.create_line(0, 30*i, self.__class__.viewport_width, 30*i)

    def draw_tracker(self):
        tracker_units = beer_tracker_world.get_tracker_units()
        for i in xrange(len(tracker_units[0])):
            self.canvas.create_rectangle((tracker_units[0][i]-1)*30,
                                         (tracker_units[1]-1)*30,
                                         (tracker_units[0][i]-1)*30+30,
                                         (tracker_units[1]-1)*30+30,
                                         fill="#6699cc", outline="#000000", tags="dynamic")

    def draw_falling_object(self):
        cls = self.__class__
        falling_object_edge_units = beer_tracker_world.get_falling_object_units()
        for i in xrange(len(falling_object_edge_units[0])):
            self.canvas.create_rectangle((falling_object_edge_units[0][i]-1)*30,
                                         (falling_object_edge_units[1]-1)*30,
                                         (falling_object_edge_units[0][i]-1)*30+30,
                                         (falling_object_edge_units[1]-1)*30+30,
                                         fill=cls.colors[1], outline="#000000", tags="dynamic")

    def run_time_step(self):
        self.time_steps += 1
        self.beer_tracker_world.move_tracker_horizontally(randint(-4, 4))
        self.after(100, self.run_time_step)

    def agenda_loop(self):

        # Clear canvas
        self.canvas.delete("dynamic")

        # Start timesteps
        if self.first_draw:
            self.run_time_step()
            self.first_draw = False

        # Draw tracker and falling object
        self.draw_tracker()
        self.draw_falling_object()

        self.after(20, self.agenda_loop)


beer_tracker_world = BeerTrackerWorld(27, 15, 30, True)
beer_tracker_view = BeerTrackerView(beer_tracker_world, 600)
beer_tracker_view.after(20, beer_tracker_view.agenda_loop())
beer_tracker_view.mainloop()