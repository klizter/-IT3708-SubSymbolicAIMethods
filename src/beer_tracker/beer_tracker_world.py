from random import randint, uniform
from enum import Enum


class TrackerResult(Enum):
    AVOIDED = 1
    CAPTURED = 2
    NEITHER = 3
    UNAVAILABLE = 4


class BeerTrackerObject:

    x_max = 0
    y_max = 0
    wrap = False

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    @classmethod
    def parse_unit_to_world(cls, unit, unit_max):

        # If world is wrapped, correct unit value
        if cls.wrap:
            if (unit - unit_max) > 0:
                return unit - unit_max

        return unit

    def increment_fall(self):
        self.y += 1

    def fall_to_ground(self):
        cls = self.__class__
        self.y = cls.y_max

    def move_horizontally(self, units):
        cls = self.__class__
        x_proposed = self.x + units
        x = 0

        if cls.wrap:

            if x_proposed > cls.x_max:
                x = x_proposed - cls.x_max
            elif x_proposed < 1:
                x = cls.x_max - x_proposed
            else:
                x = x_proposed

        else:

            if x_proposed > cls.x_max:
                x = cls.x_max
            elif x_proposed < 1:
                x = 1
            else:
                x = x_proposed

        self.x = int(x)

    # Return all units occupied by object
    def get_unpacked(self):
        cls = self.__class__
        return [cls.parse_unit_to_world(self.x+dx, cls.x_max) for dx in xrange(self.size)]


class BeerTrackerWorld:

    def __init__(self, tracker_x, max_y, max_x, wrap):

        self.max_y = max_y
        self.max_x = max_x
        self.wrap = wrap

        BeerTrackerObject.x_max = max_x
        BeerTrackerObject.y_max = max_y
        BeerTrackerObject.wrap = wrap

        self.tracker = BeerTrackerObject(tracker_x, max_y, 5)
        self.falling_object = None
        self.generate_falling_object()

    # Generate new falling object on top of the world
    def generate_falling_object(self):

        roll = uniform(0.0, 1.0)
        if roll <= 0.3:
            size = randint(5, 6)
        else:
            size = randint(1, 4)
        x = randint(1, self.max_x - (size-1))

        self.falling_object = BeerTrackerObject(x, 1, size)

    # Check if tracker is capable of catching falling object
    def is_capturable(self):
        return (self.tracker.size - 1) >= self.falling_object.size

    # Check if falling object and tracker is vertically level
    def is_tracker_and_falling_object_vertically_level(self):
        return self.falling_object.y == self.tracker.y

    # Move falling object to ground
    def pull_falling_object(self):
        self.falling_object.fall_to_ground()

    def increment_falling_object(self):
        self.falling_object.increment_fall()

    # Move tracker, units are either negative or positive
    def move_tracker_horizontally(self, units):
        self.tracker.move_horizontally(units)

    # Get tacker occupied units
    def get_tracker_units(self):
        tracker = self.tracker.get_unpacked()
        return [tracker, self.tracker.y]

    # Get falling object occupied units
    def get_falling_object_units(self):
        falling_object = self.falling_object.get_unpacked()
        return [falling_object, self.falling_object.y]

    # Evaluate if tracker avoided, captured, or neither the falling object
    def get_tracker_result(self):
        tracker_unpacked = set(self.tracker.get_unpacked())
        falling_object_unpacked = set(self.falling_object.get_unpacked())

        # Check if every tracker unit element and no other is in falling_object
        if tracker_unpacked >= falling_object_unpacked:
            return TrackerResult.CAPTURED
        elif tracker_unpacked.isdisjoint(falling_object_unpacked):
            return TrackerResult.AVOIDED
        else:
            return TrackerResult.NEITHER

    # Generate the trackers shadow sensors reading
    def get_tracker_shadow_sensors_reading(self):

        # Make sets so we can intersect
        tracker_unpacked = set(self.tracker.get_unpacked())
        falling_object_unpacked = set(self.falling_object.get_unpacked())

        # Get intersecting units
        intersecting_units = tracker_unpacked.intersection(falling_object_unpacked)

        # Set sensor values for intersecting units
        tracker_unpacked = self.tracker.get_unpacked()
        sensor_values = [0 for _ in xrange(self.tracker.size)]
        for i in xrange(len(tracker_unpacked)):
            if tracker_unpacked[i] in intersecting_units:
                sensor_values[i] = 1

        return sensor_values

    # Generate the trackers edge sensor readings
    def get_tracker_edge_sensors_reading(self):
        tracker_unpacked = set(self.tracker.get_unpacked())

        # Set sensor value and return
        if 1 in tracker_unpacked:
            return [1, 0]
        elif self.max_x in tracker_unpacked:
            return [0, 1]
        else:
            return [0, 0]
