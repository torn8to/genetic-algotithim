import enum
from enum import Enum
import random
from datetime import time,date,datetime
import pandas as pd
import matplotlib.pyplot as plt



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

    def contatined_in(self,floor_struct):
        for x in self.floor_structure:
            if x == floor_struct:
                return True
        return False

    def repeat(self)-> bool:
        for x in range(len(self.floor_structure)):
            for y in range (len(self.floor_structure)):
                if x != y:
                    if self.floor_structure[x] == self.floor_structure[y]:
                        return True
        return False

    def mutate(self, data_pool):
        mutated_level= random.randint(0,len(self.floor_structure)-1)
        random_floor = data_pool.select_random_floor()
        for x in range(10):
            if  self.contatined_in(random_floor):
                self.floor_structure[mutated_level] = random_floor
                break
            else:
                random_floor = data_pool.select_random_floor()





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
        return self.possible_floors[random.randint(0,len(self.possible_floors)-1)]

    def already_in_tower(self,list,floor)-> bool:
        for x in list:
            if x == floor:
                return True

        return False

    def generate_random_tower(self):
        tow = []
        #len self.possible_floors
        tower_height = random.randint(2,len(self.possible_floors) -1)
        for x in range(tower_height):
            tow.append(self.possible_floors[random.randint(0,len(self.possible_floors)-1)])
        return tower(tow)





class tower_stacker_genetics():
    def __init__(self,file:open, population = 2000, elitism = False, culling = False):
        self.options = data_pool(self.process_data(file))
        self.population_cap= population
        self.all_scores = []
        self.generation = 1
        self.elitism = elitism
        self.culling = culling
        self.all_time_max_score = 0
        self.all_time_max_tower = None



    def process_data(self,file)->list:
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
        first_mutation_spot = random.randint(0,len(first.floor_structure)-1)
        second_mutation_spot  = random.randint(0,len(second.floor_structure)-1)
        first_mutated_floor = first.floor_structure[first_mutation_spot]
        second_mutated_floor = second.floor_structure[second_mutation_spot]

        if not  first.contatined_in(second_mutated_floor) and not second.contatined_in(first_mutated_floor):
            first.floor_structure[first_mutation_spot] = second_mutated_floor
            second.floor_structure[second_mutation_spot] = first_mutated_floor
        return first,second



    def create_new_generation(self, mutation_rate = 0.05):
        print(self.generation)
        current_max, current_min, current_median = self.score_generation()
        max = self.pool[0]
        if self.all_time_max_score <= current_max:
            max = self.pool[0]
            self.all_time_max_score = current_max
            self.all_time_max_tower = max
        if self.all_time_max_score > current_max and self.elitism == True:
            current_max = self.all_time_max_score
            max = self.all_time_max_tower
            self.pool[20] = self.all_time_max_tower


        second_max = self.pool[1]
        self.previous_scores.append([self.generation,current_max,current_min,current_median])
        self.previous_generations.append(self.pool)
        new_generation = []


        pdr,pdr_max = self.pdr_generation(self.pool_scores)


        if self.culling == True:
            crossover_pool = self.pool[:int(self.population_cap*.5)]
        else :
            crossover_pool = self.pool
        new_generation.append(max)
        new_generation.append(second_max)
        while(len(new_generation) < self.population_cap):
            first, second = pdr[random.randint(0,pdr_max-1)], pdr[random.randint(0,pdr_max-1)]
            f,s = crossover_pool[first],crossover_pool[second]
            f,s = self.crossover(f,s)
            new_generation.append(f)
            new_generation.append(s)

        for x in range(2,len(new_generation)):
            mutation_limit = 100000 * mutation_rate
            mutation_random = int(random.randint(0,100000))
            if  mutation_limit >  mutation_random:
                print("mutation")
                mutation_decider = random.randint(0,4)
                if mutation_decider %2 == 0:
                    new_generation[x] = self.options.generate_random_tower()
                    pass
                else:
                    new_generation[x].mutate(self.options)


        self.pool = new_generation
        self.pool_scores = []
        self.generation+=1


    def run_for_n_time(self, max_run_time):
        begin = datetime.now()
        current_time = datetime.now()
        self.random_generation()
        while (current_time - begin).total_seconds() < max_run_time:
            self.create_new_generation()
            print(self.previous_scores[len(self.previous_scores)-1])
            current_time = datetime.now()

    def export_to_csv(self):
        generational_data = []
        for x in range(len(self.previous_scores)):
            if x<100:
                generational_data.append(self.previous_scores[x])
            elif x< 1000 and x % 50 == 1:
                generational_data.append(self.previous_scores[x])

        df = pd.DataFrame(generational_data,columns=['Generation','Max','Min','Median'])
        df.plot(x="Generation", y=["Max","Min","Median"])
        plt.show()
        print(df.head())
        df.to_csv('results.csv')

    def pdr_generation(self,list):
        pdr = []
        max = self.population_cap
        if self.culling == True:
            max = int(self.population_cap*.5)
        for x in range(int(max)):
                for y in range(self.pool_scores[x]+1):
                    pdr.append(x)
        return pdr, len(pdr)-1

if __name__ == "__main__":
    f = open(r'C:\Users\nathan\PycharmProjects\genetic\genetic-algotithim\src\tower_example.txt',"r")
    t = tower_stacker_genetics(f)
    t.run_for_n_time(5)
    t.export_to_csv()
