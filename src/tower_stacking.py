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
    #todo implement tower validation
    def valid_tower(self) -> bool:
        if not ( self.floor_structure[0].floor_type == floor_type.door and self.floor_structure[len(self.floor_structure)-1] == floor_type.lookout):
            return False

    #Todo implement tower score evaluation
    def evaluate(self) -> int:
        pass


class data_pool:
    def __init__(self,data:list):
        self.doors = []
        self.walls =[]
        self.lookouts = []
        for x in data:
            if x.floor_type == floor_type.door:
                self.doors.append(x)
            elif x.floor_type == floor_type.wall:
                self.walls.append(x)
            elif x.floor_type == floor_type.lookout:
                self.lookouts.append(x)

    def generate_random_tower(self):
        tower = []
        bottom_floor = self.doors[random.randint(0,len(self.doors)-1)]
        top_floor = self.lookouts[random.randint(0, len(self.doors)-1)]
        tower_height = len(self.walls)-1







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
        self.scores = []
        for x in range(self.population_cap):
            self.pool.append(self.options.generate_random_tower())

    def scores(self):
















