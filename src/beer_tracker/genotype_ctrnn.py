from genotype import Genotype
from numpy import reshape, array
from random import uniform, randrange
from phenotype_ctrnn import PhenotypeCTRNN


class GenotypeCTRNNWeights(Genotype):

    neuron_count_layers = [5, 2, 2]  # [Input, Hidden 1, Hidden N, Output]
    ctrnn = True

    weight_lower_bound = -5.0
    weight_upper_bound = 5.0
    time_constant_lower_bound = 1.0
    time_constant_upper_bound = 2.0
    gain_term_lower_bound = 1.0
    gain_term_upper_bound = 5.0
    bias_weight_lower_bound = -10.0
    bias_weight_upper_bound = 0

    nr_weights = 0
    nr_gain_terms = 0
    nr_time_constants = 0
    nr_bias_weights = 0
    nr_weights_layer = []
    nr_gain_terms_layer = []
    nr_time_constants_layer = []
    nr_bias_weights_layer = []

    interval_start_weights = 0
    interval_end_weights = 0
    interval_start_gain_terms = 0
    interval_end_gain_terms = 0
    interval_start_time_constants = 0
    interval_end_time_constants = 0
    interval_start_bias_weights = 0
    interval_end_bias_weights = 0

    def __init__(self, bit_vector):
        super(GenotypeCTRNNWeights, self).__init__(bit_vector)

    # TODO: Merge ANN and CTRNN genotype?
    def mutate(self):
        # Cache class reference
        cls = self.__class__

        # Get random bit_vector position
        mutation_position = randrange(0, len(self.bit_vector))

        if mutation_position < cls.interval_end_weights:
            self.bit_vector[mutation_position] = uniform(cls.weight_lower_bound, cls.weight_upper_bound)

        elif mutation_position <= cls.interval_end_gain_terms:
            self.bit_vector[mutation_position] = uniform(cls.gain_term_lower_bound, cls.gain_term_upper_bound)

        elif mutation_position <= cls.interval_end_time_constants:
            self.bit_vector[mutation_position] = uniform(cls.time_constant_lower_bound, cls.time_constant_upper_bound)

        elif mutation_position <= cls.interval_end_bias_weights:
            self.bit_vector[mutation_position] = uniform(cls.bias_weight_lower_bound, cls.bias_weight_upper_bound)

        else:
            raise Exception("Mutation @ position {0} was out of genotype bound {1} -> {2}".format(mutation_position, 0, len(self.bit_vector)-1))


    # TODO: Merge ANN and CTRNN genotype?
    def translate_to_phenotype(self):
        cls = self.__class__
        weights = list()
        gain_terms = list()
        time_constants = list()

        slice_weights_start = 0
        slice_weights_end = 0

        slice_gain_terms_start = cls.interval_start_gain_terms
        slice_gain_terms_end = cls.interval_start_gain_terms

        slice_time_constants_start = cls.interval_start_time_constants
        slice_time_constants_end = cls.interval_start_time_constants

        slice_bias_weights_start = cls.interval_start_bias_weights
        slice_bias_weights_end = cls.interval_start_bias_weights

        for i in xrange(0, len(cls.nr_weights_layer)):

            slice_weights_end += cls.nr_weights_layer[i]
            slice_gain_terms_end += cls.nr_gain_terms_layer[i]
            slice_time_constants_end += cls.nr_time_constants_layer[i]
            slice_bias_weights_end += cls.nr_bias_weights_layer[i]

            # Extract layer weights from bit vector
            weights = self.bit_vector[slice_weights_start:slice_weights_end]
            bias_weights = self.bit_vector[slice_bias_weights_start:slice_bias_weights_end]
            layer_weights = array(weights + bias_weights)

            # Calculate number of layer inputs (downstream + recurrent + bias)
            nr_layer_inputs = cls.neuron_count_layers[i-1] + cls.neuron_count_layers[i] + 1
            nr_layer_neurons = cls.neuron_count_layers[i]

            weights.append(reshape(layer_weights, (nr_layer_inputs, nr_layer_neurons)))

            # Extract layer gain terms from bit vector
            gain_terms.append(self.bit_vector[slice_gain_terms_start:slice_gain_terms_end])

            # Extract layer time constants from bit vector
            time_constants.append(self.bit_vector[slice_time_constants_start:slice_time_constants_end])

            slice_weights_start = slice_weights_end
            slice_gain_terms_start = slice_gain_terms_end
            slice_time_constants_start = slice_time_constants_end
            slice_bias_weights_start = slice_bias_weights_end

        return PhenotypeCTRNN(weights, gain_terms, time_constants)

    @classmethod
    # TODO: Merge ANN and CTRNN genotype?
    def construct_random_genotype(cls):
        bit_vector = [uniform(cls.weight_lower_bound, cls.weight_upper_bound) for _ in xrange(cls.nr_weights)]
        bit_vector += [uniform(cls.gain_term_lower_bound, cls.gain_term_upper_bound) for _ in xrange(cls.nr_gain_terms)]
        bit_vector += [uniform(cls.time_constant_lower_bound, cls.time_constant_upper_bound) for _ in xrange(cls.nr_time_constants)]
        bit_vector += [uniform(cls.bias_weight_lower_bound, cls.bias_weight_upper_bound) for _ in xrange(cls.nr_bias_weights)]

        return bit_vector

    @classmethod
    # TODO: Plug it in to main view and call it when genotype is selected for EA
    def calculate_ctrnn_intervals(cls):

        cls.nr_weights = 0
        cls.nr_gain_terms = 0
        cls.nr_time_constants = 0
        cls.nr_bias_weights = 0

        for i in xrange(1, len(cls.neuron_count_layers)):

            # Calculate number of normal weights between layers
            nr_weights = cls.neuron_count_layers[i-1]*cls.neuron_count_layers[i]
            # Number of recurrent weights between neurons in layer
            nr_weights += cls.neuron_count_layers[i] * cls.neuron_count_layers[i]
            # Add weight count to layer total
            cls.nr_weights_layer.append(nr_weights)
            # Add layer total to global total
            cls.nr_weights += nr_weights

            # Calculate number of gain terms for each neuron in layer
            nr_gain_terms = cls.neuron_count_layers[i]
            # Add gain term count to layer total
            cls.nr_gain_terms_layer.append(nr_gain_terms)
            # Add layer total to global total
            cls.nr_gain_terms += nr_gain_terms

            # Calculate number of time constants for each neuron in layer
            nr_time_constants = cls.neuron_count_layers[i]
            # Add time constants count to layer total
            cls.nr_time_constants_layer.append(nr_time_constants)
            # Add layer total to global total
            cls.nr_time_constants += nr_time_constants

            # Number of bias weights between bias node and layer
            nr_bias_weights = cls.neuron_count_layers[i]
            # Add bias weight count to layer total
            cls.nr_bias_weights_layer.append(nr_bias_weights)
            # Add layer total to global total
            cls.nr_bias_weights += nr_bias_weights

        # Set intervals
        cls.interval_start_weights = 0
        cls.interval_end_weights = cls.nr_weights - 1
        cls.interval_start_gain_terms = cls.nr_weights
        cls.interval_end_gain_terms = cls.nr_weights + cls.nr_gain_terms - 1
        cls.interval_start_time_constants = cls.nr_weights + cls.nr_gain_terms
        cls.interval_end_time_constants = cls.nr_weights + cls.nr_gain_terms + cls.nr_time_constants - 1
        cls.interval_start_bias_weights = cls.nr_weights + cls.nr_gain_terms + cls.nr_time_constants
        cls.interval_end_bias_weights = cls.nr_weights + cls.nr_gain_terms + cls.nr_time_constants + cls.nr_bias_weights - 1
