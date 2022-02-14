import heapq
import numpy as np
import matplotlib.pyplot as plt
import random


class Analyzer:
    def __init__(self, generation_sample):
        self.current_generation = 0
        self.running_generation = 0
        self.fitness_list = []
        self.generation_sample = generation_sample
        self.sample_mean = []
        self.min_data_point = []
        self.data_point_x = []
        self.data_point_y = []
        self.best = [0,0,0]

        heapq.heapify(self.fitness_list)

    def update_best(self, child):
        if child.fitness > self.best[0]:
            self.best = [child.fitness, child, self.current_generation]

    def update_function(self, thing):
        self.data_point_y.append(max(self.fitness_list))
        self.data_point_x.append(self.current_generation)
        self.sample_mean.append(np.mean(self.fitness_list))
        self.min_data_point.append(min(self.fitness_list))

    def update_analyzer(self, thing, end):
        if self.current_generation == 0:
            self.update_function(thing)
            self.current_generation += 1
            self.running_generation += 1
        elif self.running_generation == self.generation_sample:
            self.update_function(thing)
            self.running_generation = 1
            self.current_generation += 1
        elif end == 'end':
            self.update_function(thing)
        else:
            self.current_generation += 1
            self.running_generation += 1

    def analyze(self):
        best_list = Toolbox.breakdown(self.best[1].gene)
        print("Best Fitness: ", self.best[0], "at generation", self.best[2])
        for thing in best_list:
            print(thing)


class FileHelper:

    @staticmethod
    def read_file(file):
        list = []
        fh = open(file, 'rt')
        for line in fh.readlines():
            value = float(line.strip())
            list.append(value)
        fh.close()
        return list


class Toolbox:

    @staticmethod
    def crossover(list1, list2):
        crossover_point = random.randint(0, len(list1))
        new_list_1 = list1[:crossover_point:] + list2[crossover_point::]
        return new_list_1

    # @staticmethod
    # def crossover(list1, list2):
    #     crossover_point = random.choice([10, 20, 30])
    #     new_list_1 = list1[:crossover_point:] + list2[crossover_point::]
    #     return new_list_1

    @staticmethod
    def pick_a_bin(starting_bin):
        while True:
            new_bin = random.choice([1, 2, 3, 4])
            if new_bin != starting_bin:
                return new_bin

    @staticmethod
    def pick_a_position(target_bin, bin_size):
        if target_bin == 1:
            return random.randint(0, (bin_size - 1))
        elif target_bin == 2:
            return random.randint(bin_size, ((2 * bin_size) - 1))
        elif target_bin == 3:
            return random.randint((2 * bin_size), ((3 * bin_size) - 1))
        elif target_bin == 4:
            return random.randint((3 * bin_size), ((4 * bin_size) - 1))

    @staticmethod
    def decision(prob):
        return random.random() < prob

    @staticmethod
    def breakdown(input_list):
        bin_size = len(input_list)/4
        output_list = [[], [], [], []]
        bin_number = 1
        bin_counter = 0
        i = 0
        while i in range(len(input_list)):
            if bin_counter == bin_size:
                bin_number += 1
                bin_counter = 0
            if bin_number == 1:
                output_list[0].append(input_list[i])
                i += 1
                bin_counter += 1
            elif bin_number == 2:
                output_list[1].append(input_list[i])
                i += 1
                bin_counter += 1
            elif bin_number == 3:
                output_list[2].append(input_list[i])
                i += 1
                bin_counter += 1
            elif bin_number == 4:
                output_list[3].append(input_list[i])
                i += 1
                bin_counter += 1
        return output_list

    # @staticmethod
    # def testing_function():
    #     test_gal = Gal(test_list, 20, 10)
    #     i = 0
    #     q = 0
    #     x_len = 100000000
    #     x_values = []
    #     max_y = []
    #     avg_y = []
    #     min_y = []
    #     avg_max_y = []
    #     avg_avg_y = []
    #     avg_min_y = []
    #     while i < 5:
    #         print("running", i)
    #         test_gal = Gal(test_list, 20, 60)
    #         list = test_gal.iterator("Combo")
    #         max_y.append(list[1])
    #         avg_y.append(list[2])
    #         min_y.append(list[3])
    #         if len(list[0]) < x_len:
    #             x_len = len(list[0])
    #             x_values = list[0]
    #         i += 1
    #     while q < x_len:
    #         print("averaging position: ", q)
    #         holder = []
    #         for lists in max_y:
    #             holder.append(lists[q])
    #         avg_max_y.append(np.mean(holder))
    #         holder = []
    #         for lists in avg_y:
    #             holder.append(lists[q])
    #         avg_avg_y.append(np.mean(holder))
    #         holder = []
    #         for lists in min_y:
    #             holder.append(lists[q])
    #         avg_min_y.append(np.mean(holder))
    #         q += 1
    #     plt.figure()
    #     plt.plot(x_values, avg_max_y, label="Best Fitness")
    #     plt.plot(x_values, avg_avg_y, label="Average Fitness")
    #     plt.plot(x_values, avg_min_y, label="Minimum Fitness")
    #     plt.legend()
    #     plt.title("Combo Retention")
    #     plt.show()
