from GalHelper import Toolbox
import numpy as np


class Individual:
    def __init__(self, gene, bin_size):
        self.gene = gene
        self.fitness = 0
        self.bin_size = bin_size
        self.get_fitness()

    def __lt__(self, object):
        return self.fitness > object.fitness

    def __eq__(self, object):
        return self.fitness == object.fitness

    def is_legal(self):
        first_seen = set()
        first_seen_add = first_seen.add
        for i in self.gene:
            if i in first_seen or first_seen_add(i):
                return False
        return True

    def mutation(self, prob):
        pos = 0
        bin_number = 1
        bin_counter = 0
        for base in self.gene:
            if bin_counter == self.bin_size:
                bin_number += 1
                bin_counter = 0
            if Toolbox.decision(prob):
                new_position = Toolbox.pick_a_position(Toolbox.pick_a_bin(bin_number), self.bin_size)
                sub = self.gene[new_position]
                self.gene[new_position] = base
                self.gene[pos] = sub
                bin_counter += 1
                pos += 1
            else:
                bin_counter += 1
                pos += 1
        self.get_fitness()

    def get_fitness(self):
        gene = self.gene.copy()
        alleles = Toolbox.breakdown(gene)
        bin_1 = np.prod(alleles[0])
        bin_2 = np.sum(alleles[1])
        bin_3 = max(alleles[2]) - min(alleles[2])
        self.fitness = bin_1 + bin_2 + bin_3
        return
