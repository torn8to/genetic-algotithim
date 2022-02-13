import enum
from enum import Enum
import random
from datetime import time,date,datetime


class floor_type(Enum):
    door = 'Door'
    wall = 'Wall'
    lookout = 'Lookout'

class tower_floor:
    def __init__(self,floor_type:str, width:int,strength:int,cost:int):
        self.floor_type = self.floor_type_enumeration(floor_type)
        self.width = int(width)
        self.strength = int(strength)
        self.cost = int(cost)

    def __eq__(self, other):
        return self.floor_type == other.floor_type and \
               self.cost == other.cost and\
               self.width == self.width and\
               self.strength == other.strength


    def floor_type_enumeration(self,type:str)->floor_type:
        if type.lower() == 'door':
            return floor_type.door
        if type.lower() == 'wall':
            return floor_type.wall
        if type.lower() == 'lookout':
            return floor_type.lookout

class tower:
    def __init__(self,floor_structre:list):
        self.floor_structure = floor_structre

    def multiples_of_floor_types(self,floor_type:floor_type)-> bool:
        count = 0
        for x in self.floor_structure:
            if x.floor_type == floor_type:
                count+=1
        return count > 1

    def repeat(self)-> bool:
        for x in range(len(self.floor_structure)):
            for y in range (len(self.floor_structure)):
                if x != y:
                    if self.floor_structure[x] == self.floor_structure[y]:
                        return True
        return False

    def mutate(self, data_pool):
        mutated_level= random.randint(0,len(self.floor_structure)-1)
        iteration = 0
        while(self.repeat()):
            self.floor_structure[mutated_level] = self.data_pool.select_random_floor()
            iteration += 1

    def valid_tower(self) -> bool:
        if not ( self.floor_structure[0].floor_type == floor_type.door and self.floor_structure[len(self.floor_structure)-1].floor_type == floor_type.lookout):
            return False
        elif  self.multiples_of_floor_types(floor_type.door) or self.multiples_of_floor_types(floor_type.lookout):
            return False
        for x in range(1,len(self.floor_structure)-1):
            if self.floor_structure[x].width > self.floor_structure[x-1].width:
                return False
        return True
    def get_floors(self):
        return self.floor_structure

    def set_floors(self,struct):
        self.floor_structure = struct

    def get_cost(self):
        sum = 0
        for x in self.floor_structure:
            sum += x.cost
        return sum

    def score(self):
        return 10 + len(self.floor_structure)**2 - self.get_cost()

    def evaluate(self) -> int:
        if not self.valid_tower():
            return 0
        return self.score()



class data_pool:
    def __init__(self,data:list):
        self.possible_floors = data

    def select_random_floor(self):
        return self.possible_floors[random.randint(0,len(self.possible_floors))]

    def already_in_tower(self,list,floor)-> bool:
        for x in list:
            if x == floor:
                return True

        return False

    def generate_random_tower(self):
        tow = []
        tower_height = random.randint(2,len(self.possible_floors) -1)
        for x in range(tower_height):
            tow.append(self.possible_floors[random.randint(0,len(self.possible_floors)-1)])
        return tower(tow)


#TODO implement the culling methods
class culling_method(Enum):
    top_half_crossover = 0 # keep top half and crossover
    elitism = 1
    culling = 2


class tower_stacker_genetics():
    def __init__(self,file:open, population = 1000, elitism = False, culling = False):
        self.options = data_pool(self.process_data(file))
        self.population_cap= population
        self.all_scores = []
        self.generation = 0
        self.elitism = elitism
        self.culling = culling



    def process_data(self,file, elitism = False, culling = True)->list:
        n1 = file.readline().split()
        floor_list = []
        while(len(n1) != 0):
            floor_type = n1[0]
            width = n1[1]
            strength = n1[2]
            cost = n1[3]
            floor_list.append(tower_floor(floor_type,width,strength,cost))
            n1 = file.readline().split()
        return floor_list


    def  random_generation(self):
        self.pool = []
        self.previous_generations = []
        self.previous_scores = []
        self.pool_scores = []
        for x in range(self.population_cap):
            self.pool.append(self.options.generate_random_tower())


    def score_generation(self):
        for x in self.pool:
            self.pool_scores.append(x.evaluate())
        zipped = zip(self.pool_scores,self.pool)
        sorted_pairs = sorted(zipped, key  = lambda pair:pair[0],reverse=True)
        tuples = zip(*sorted_pairs)
        self.pool_scores, self.pool = [list(tuple) for tuple in tuples]
        max = self.pool_scores[0]
        min = self.pool_scores[self.population_cap-1]
        median = self.pool_scores[int(self.population_cap/2)]
        return max,min,median



    def crossover(self,first, second):
        max_cross_spot = len(second) - 2
        if len(first) < len(second):
             max_cross_spot = len(first)
        cross_spot = 1
        if max_cross_spot == 1:
            cross_spot = random.randint(1,max_cross_spot)

        placeholder = first[cross_spot:]
        first[cross_spot:] = second[cross_spot:]
        second[cross_spot:] = placeholder
        return first , second



    def create_new_generation(self, mutation_rate = 0.05):
        current_max, current_min, current_median = self.score_generation()
        self.previous_scores.append([current_max,current_min,current_median])
        self. previous_generations.append(self.pool)
        new_generation = []


        if self.elitism == True:
            new_generation.append(self.pool[0])
            new_generation.append(self.pool[1])
        if self.culling == True:
            crossover_pool = self.pool[:int(self.population_cap*.75)]
        else :
            crossover_pool = self.pool

        while (len(new_generation) < self.population_cap):
            first_random_index = random.randint(0,len(crossover_pool)-1)
            second_random_index = random.randint(0,len(crossover_pool)-1)
            if second_random_index == first_random_index:
                second_random_index +=1
            if second_random_index == first_random_index and second_random_index >len(self.population_cap)-1:
                second_random_index -=2
            f, s = crossover_pool[first_random_index], crossover_pool[second_random_index]
            child_1, child_2= self.crossover(f.get_floors(),s.get_floors())
            f.set_floors(child_1)
            s.set_floors(child_2)

            new_generation.append(f)
            new_generation.append(s)

        print(len(new_generation))
        L = tower([tower_floor("door", 5, 5, 1), tower_floor("lookout",4,3,1)])
        print(L.evaluate())
        self.pool = new_generation
        self.pool_scores = []


    def run_for_n_time(self, max_run_time):
        begin = datetime.now()
        current_time = datetime.now()
        self.random_generation()
        while (current_time - begin).total_seconds() < 5.0:
            self.create_new_generation()
            print(self.previous_scores[len(self.previous_scores)-1])
            current_time = datetime.now()
        #TODO print a chart with median min and max data
        #be able to export data to csv
    #TODO Implement PDR creation


if __name__ == "__main__":
    f = open(r'C:\Users\nathan\PycharmProjects\genetic\genetic-algotithim\src\tower_example.txt',"r")
    t = tower_stacker_genetics(f)
    t.run_for_n_time(5)
