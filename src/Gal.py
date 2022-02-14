import heapq
import time
from allocator import Individual
from GalHelper import Analyzer, FileHelper, Toolbox
import random


class Gal:
    def __init__(self, input_list, population_number, max_time):
        self.list = input_list
        self.population_number = population_number
        self.time = max_time
        self.bin_size = len(input_list)/4
        self.parents = []
        self.carry_over = 2
        self.cull_number = 10
        self.analyzer = Analyzer(50)

        heapq.heapify(self.parents)
        self.populate_gene()

    def populate_gene(self):
        while len(self.parents) < self.population_number:
            input_holder = self.list.copy()
            output_holder = []
            while len(input_holder) > 0:
                chosen = random.choice(input_holder)
                input_holder.remove(chosen)
                output_holder.append(chosen)
            new_individual = Individual(output_holder, self.bin_size)
            heapq.heappush(self.analyzer.fitness_list, new_individual.fitness)
            heapq.heappush(self.parents, new_individual)

    def get_weights(self):
        weight = []
        scale = abs(min(self.analyzer.fitness_list))
        for individual in self.parents:
            fitness = (individual.fitness + scale)
            weight.append(fitness)
        self.analyzer.fitness_list = []
        return weight

    def get_children(self):
        children = []
        weight = self.get_weights()
        i = 0
        while i < self.population_number:
            parents = random.choices(self.parents, weights=weight, k=2)
            if parents[0] != parents[1]:
                child = Individual(Toolbox.crossover(parents[0].gene, parents[1].gene), self.bin_size)
                child.mutation(0.03)
                if child.is_legal():
                    i += 1
                    self.analyzer.fitness_list.append(child.fitness)
                    self.analyzer.update_best(child)
                    children.append(child)
        return children

    def iterator(self, retention_policy):
        start_time = time.time()
        while True:
            if time.time() - start_time > self.time:
                print("Time to complete", time.time() - start_time)
                self.analyzer.analyze()
                break
            else:
                retained = heapq.nsmallest(self.carry_over, self.parents)
                self.analyzer.update_analyzer(self.parents, 'no')
                self.parents = self.get_children()
                heapq.heapify(self.parents)
                if retention_policy == "Elitism":
                    for individual in retained:
                        heapq.heappush(self.parents, individual)
                        self.analyzer.fitness_list.append(individual.fitness)
                if retention_policy == "Cull":
                    self.parents = heapq.nsmallest((self.population_number - self.cull_number), self.parents)
                    self.analyzer.fitness_list = heapq.nlargest((self.population_number - self.cull_number),
                                                                self.analyzer.fitness_list)
                if retention_policy == "Combo":
                    self.parents = heapq.nsmallest((self.population_number - self.cull_number), self.parents)
                    self.analyzer.fitness_list = heapq.nlargest((self.population_number - self.cull_number),
                                                                self.analyzer.fitness_list)
                    for individual in retained:
                        heapq.heappush(self.parents, individual)
                        self.analyzer.fitness_list.append(individual.fitness)


# test_list = FileHelper.read_file("testNumbers.txt")
# test_gal = Gal(test_list, 20, 10)
# test_gal.iterator("Combo")
