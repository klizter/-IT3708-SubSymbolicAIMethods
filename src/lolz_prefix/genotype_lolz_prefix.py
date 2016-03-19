from genotype import Genotype


class GenotypeLOLZPrefix(Genotype):

    bit_vector_length = 40

    def __init__(self, bit_vector):
        super(GenotypeLOLZPrefix, self).__init__(bit_vector)

    @classmethod
    def report_settings_content(cls):
        print "\tbit vector length: ", cls.bit_vector_length