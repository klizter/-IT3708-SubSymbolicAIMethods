from phenotype import Phenotype


class PhenotypeSuprisingSequence(Phenotype):

    def __init__(self, genotype_suprising_sequence):
        super(PhenotypeSuprisingSequence, self).__init__(genotype_suprising_sequence)
        self.sequence = self.num_seq_to_char_seq()

    def __repr__(self):
        return self.sequence

    def num_seq_to_char_seq(self):
        sequence = ""
        for bit in self.bit_vector:
            sequence += chr(bit)

        return sequence
