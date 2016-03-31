from numpy import array
from enum import Enum


class TrackerActions(Enum):
    MOVE_RIGHT = 1
    MOVE_LEFT = 2
    PULL = 3


class BeerTrackerAgent:

    def __int__(self, ctrnn):
        self.ctrnn = ctrnn
        self.max_velocity = 4

    def choose_action(self, sensor_values, pulling):

        action_vector = self.ctrnn.process(array(sensor_values))
        action_vector = action_vector.tolist()

        if pulling and action_vector[3] > 0.7:
            return [TrackerActions.PULL, 0]

        if action_vector[0] > 0.5:
            return [TrackerActions.MOVE_RIGHT, round(4 / action_vector[1])]
        else:
            return [TrackerActions.MOVE_LEFT, round(4 / action_vector[1])]
