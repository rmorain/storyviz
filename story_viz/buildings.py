import random
import numpy as np
from interests import *

class Building(object):
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.position = np.array([0,0])
        self.dim = np.array([0,0])
        self.social_agents = []

    def set_position(self, position, z, x):
        new_z = position[0]
        if position[0] < 0:
            new_z = 0
        elif position[0] + max(self.dim) > z-1:
            new_z = z-1 - max(self.dim)

        new_x = position[1]
        if position[1] < 0:
            new_x = 0
        elif position[1] + max(self.dim) > x-1:
            new_x = x-1 - max(self.dim)

        print('id', self.id, 'old pos', self.position, 'new pos', np.round([new_z, new_x]).astype(int))
        self.position = np.round([new_z, new_x]).astype(int)

def normalize_vector(vector, only_greater_than=False):
    distance = np.linalg.norm(vector)
    if distance != 0:
        if not only_greater_than or distance > 1:
            return vector / distance
    return vector


class House(Building):
    def __init__(self, id):
        super(House, self).__init__(id, "house")
        self.dim = np.array([7,10])
        self.social_agents = ["house"]
        self.knn = 10
        self.attraction = 40
        self.repulsion = 10

    def get_interest(self, village_skeleton, terrain):
        social_vector = sociability(terrain, village_skeleton, self)
        slope_vector = slope(terrain, village_skeleton, self)
        print('social', social_vector)
        print('slope', slope_vector)
        #return social_vector * .5 + slope_vector * .5 + self.get_noise(10)
        # print(normalize_vector(social_vector, True) + normalize_vector(slope_vector, True) * .3)

        return normalize_vector(social_vector, True) * 5 + normalize_vector(slope_vector, True) * 2

    def get_noise(self, scale=1):
        noise_vector = np.array([random.uniform(-1,1), random.uniform(-1,1)])
        noise_vector = noise_vector / np.linalg.norm(noise_vector)
        return noise_vector * scale