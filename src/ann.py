from numpy import exp, dot, power, sin
from libs.enum import Enum

# TODO
# Add softmax og rectify activation functions
# Add support for different activation functions for each layer


class ActivationScheme(Enum):
    SIGMOID = 1
    GAUSSIAN = 2
    SINUSOID = 3
    TANH = 4


class NeuralNetwork:

    activation_scheme = ActivationScheme.SIGMOID

    def __init__(self, layers):
        self.layers = layers

    def activation_function(self, x):
        cls = self.__class__
        if cls.activation_scheme == ActivationScheme.SIGMOID:
            return self.sigmoid(x)
        elif cls.activation_scheme == ActivationScheme.GAUSSIAN:
            return self.gaussian(x)
        elif cls.activation_scheme == ActivationScheme.SINUSOID:
            return self.sinusoid(x)
        elif cls.activation_scheme == ActivationScheme.TANH:
            return self.tanh(x)

    def sigmoid(self, x):
        return 1 / (1 + exp(-x))

    def gaussian(self, x):
        return exp(power(-x, 2))

    def sinusoid(self, x):
        return sin(x)

    def tanh(self, x):
        return (2 / (1 + exp(-2*x))) - 1

    def process(self, downstream):
        for layer in self.layers:
            downstream = self.activation_function(dot(downstream, layer.weights))
        return downstream


class NeuronLayer:

    def __init__(self, weights):
        # Weights are evolved by EA
        self.weights = weights

