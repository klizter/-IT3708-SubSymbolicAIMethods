__author__ = 'ocselvig'
from numpy import exp, dot, power, sin, append, array
from enum import Enum


class ActivationScheme(Enum):
    SIGMOID = 1
    GAUSSIAN = 2
    LOGISTIC = 3
    TANH = 4
    RELU = 5


class ContinuesTimeRecurrentNeuralNetwork:

    activation_scheme = ActivationScheme.SIGMOID

    def __init__(self, layers):
        self.layers = layers

    def process(self, downstream_signals):

        # fire neural pattern
        for layer in self.layers:

            # Add recurrent and bias signals to downstream iff CTRNN layer
            if layer.is_continues_time_recurrent():

                # TODO: Sigmodal/Logistic function for internal state
                recurrent_signals = []
                for neuron in layer.neuros:
                    recurrent_signals.append(neuron.memory*neuron.gain_term)

                recurrent_signals = NeuronLayer.logistic(array(recurrent_signals))

                append(downstream_signals, recurrent_signals) # HVA FAEN I HELVETE?

                append(downstream_signals, [1]) # TODO: if something goes wrong, check this!

            # Potentially fire each neuron in layer
            downstream_signals = layer.activation_function(dot(downstream_signals, layer.weights))

            # Calculate derivative for each neuron and apply to memory state iff CTRNN layer
            if layer.is_continues_time_recurrent():

                for i in xrange(len(layer.neuros)):
                    layer.neuros[i].calculate_derivative(downstream_signals[i])

        # return last neural layer's downstream as output
        return downstream_signals

    @classmethod
    def construct_ctrnn(cls, layer_weights, gain_terms, time_constants, activation_schemes=None):

        # Check if any activation scheme has been specified, else use Logistic function for all layers
        if activation_schemes is None:
            activation_schemes = [ActivationScheme.LOGISTIC for _ in xrange(len(layer_weights))]

        neuron_layers = list()

        for i in xrange(len(layer_weights)):

            # Construct layer neurons
            layer_neurons = [NeuronCTRNN(gain_terms[j], time_constants[j]) for j in xrange(len(gain_terms))]

            # Construct the layer
            neuron_layer = NeuronLayer(layer_weights[i], activation_schemes[i], layer_neurons)

            # Add layer to layer collection
            neuron_layers.append(neuron_layer)

        return cls(neuron_layers)


class NeuronLayer:

    def __init__(self, weights, activation_scheme, neurons=None):
        self.weights = weights
        self.activation_scheme = activation_scheme
        self.neurons = neurons

    def is_continues_time_recurrent(self):
        return len(self.neurons) > 0

    def activation_function(self, x):
        cls = self.__class__
        if self.activation_scheme == ActivationScheme.LOGISTIC:
            return cls.logistic(x)
        elif self.activation_scheme == ActivationScheme.GAUSSIAN:
            return cls.gaussian(x)
        elif self.activation_scheme == ActivationScheme.SINUSOID:
            return cls.sinusoid(x)
        elif self.activation_scheme == ActivationScheme.TANH:
            return cls.tanh(x)
        elif self.activation_scheme == ActivationScheme.RELU:
            return cls.relu(x)

    @classmethod
    def logistic(cls, x):
        return 1 / (1 + exp(-x))

    @classmethod
    def gaussian(cls, x):
        return exp(power(-x, 2))

    @classmethod
    def sinusoid(cls, x):
        return sin(x)

    @classmethod
    def tanh(cls, x):
        return (2 / (1 + exp(-2*x))) - 1

    @classmethod
    #TODO: write ReLu function
    def relu(cls, x):
        return x


class Neuron(object):

    def __init__(self):
        return


class NeuronCTRNN(Neuron):

    def __init__(self, gain_term, time_constant):
        super(NeuronCTRNN, self).__init__()
        self.time_constant = time_constant
        self.gain_term = gain_term
        self.memory = 0

    def calculate_derivative(self, signal):
        self.memory += (1 / self.time_constant) * ((-self.memory) + signal)

    @classmethod
    def generate_neurons(cls, time_constants, gain_terms):
        neurons = []

        for i in xrange(len(time_constants)):
            neurons.append(NeuronCTRNN(time_constants[i], gain_terms[i]))

        return neurons