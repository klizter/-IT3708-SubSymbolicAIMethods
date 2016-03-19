from flatland import Flatland, Move
from numpy import array


class FlatlandAgent:

    action_threshold = 0.2

    def __init__(self, ann):
        self.ann = ann

    def choose_action(self, cells):

        # Parse agent sensor data to ANN downstream inputs
        ann_inputs = FlatlandAgent.parse_sensor_inputs(cells)

        # Process downstream inputs with ANN
        action_vector = self.ann.process(array(ann_inputs))

        # Find output of ANN with max value and index of value
        action_vector = action_vector.tolist()
        max_action_value = max(action_vector)
        index = action_vector.index(max_action_value)

        # Stand still if non of the outputs are higher the action threshold
        action = Move.STAND_STILL
        if max_action_value > self.__class__.action_threshold:
            action = Move(index + 1)

        return action

    @staticmethod
    # Parse cells content to [LF, TF, RF, LP, TP, RP]
    # This format is recommended in the assignment
    def parse_sensor_inputs(cells):

        sensor_output = [0 for _ in xrange(6)]

        for i in xrange(len(cells)):
            if cells[i] == Flatland.food:
                sensor_output[i] = 1
            elif cells[i] == Flatland.poison:
                sensor_output[i+3] = 1

        return sensor_output
