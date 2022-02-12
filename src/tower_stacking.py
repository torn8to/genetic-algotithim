from enum import Enum
import random

class floor_type(Enum):
    door = 'Door'
    wall = 'Wall'
    lookout = 'Lookout'

class tower_floor:
    def __init__(self,floor_type:str, width:int,strength:int,cost:int):
        self.floor_type = self.floor_type_enumeration(floor_type)
        self.width = width
        self.strength = strength
        self.cost = cost

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


    def valid_tower(self) -> bool:
        if not ( self.floor_structure[0].floor_type == floor_type.door and self.floor_structure[len(self.floor_structure)-1] == floor_type.lookout):
            return False
        elif  self.multiples_of_floor_types(floor_type.door) or self.multiples_of_floor_types(floor_type.lookout):
            return False
        for x in range(1,len(self.floor_structure)):
            if self.floor_structure[x].width > self.floor_structure[x-1].width:
                return False

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
        elif True:
            return self.score()



class data_pool:
    def __init__(self,data:list):
        self.possible_floors = data


    def generate_random_tower(self):
        tower = []
        tower_height = random.randint(2,len(self.possible_floors) -1)
        for x in range(tower_height):
            tower.append(self.possible_floors[random.randint(0,len(self.walls)-1)])


class tower_stacker_genetics():
    def __init__(self,file:open, population = 10):
        self.options = data_pool(self.process_data(file))
        self.population_cap= population
        self.generation = 0


    def process_data(self,file)->list:
        n1 = file.readline.split()
        floor_list = []
        while(len(n1) != 0):
            floor_type = n1[0]
            width = n1[1]
            strength = n1[2]
            cost = n1[3]
            floor_list.append(tower_floor(floor_type,width,strength,cost))
            n1 = file.readline.split()
        return floor_list


    def  random_generation(self):
        self.pool = []
        self.previous_iterations = []
        self.scores = []
        for x in range(self.population_cap):
            self.pool.append(self.options.generate_random_tower())























