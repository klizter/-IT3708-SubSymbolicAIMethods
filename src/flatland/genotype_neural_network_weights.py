from genotype import Genotype
from numpy import random, reshape, array
from random import uniform, randrange
from phenotype_neural_network_weights import PhenotypeNeuralNetworkWeights


class GenotypeNeuralNetworkWeights(Genotype):

    neuron_count_layers = [6, 3]  # [Input, Hidden 1, Hidden N, Output]
    weight_upper_bound = 2.0
    weight_lower_bound = -2.0

    def __init__(self, bit_vector):
        super(GenotypeNeuralNetworkWeights, self).__init__(bit_vector)

    def mutate(self):
        # Get random bit_vector position
        mutation_position = randrange(0, len(self.bit_vector))

        # Mutate bit_vector position
        cls = self.__class__
        self.bit_vector[mutation_position] = uniform(cls.weight_lower_bound, cls.weight_upper_bound)

    def translate_to_phenotype(self):
        cls = self.__class__
        weights = list()
        slice_start = 0
        slice_end = 0
        for i in xrange(1, len(cls.neuron_count_layers)):
            slice_end += cls.neuron_count_layers[i-1]*cls.neuron_count_layers[i]
            layer_weights = array(self.bit_vector[slice_start:slice_end])
            weights.append(reshape(layer_weights, (cls.neuron_count_layers[i-1], cls.neuron_count_layers[i])))
            slice_start = slice_end

        return PhenotypeNeuralNetworkWeights(weights)

    @classmethod
    def construct_random_genotype(cls):
        nr_weights = 0
        for i in xrange(1, len(cls.neuron_count_layers)):
            nr_weights += cls.neuron_count_layers[i-1]*cls.neuron_count_layers[i-1]

        return cls([uniform(cls.weight_lower_bound, cls.weight_upper_bound) for _ in xrange(nr_weights)])
