import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import skewnorm
import math
from buildings import *
import maps_viz
from terrain_generator import generate_terrain

class MultiAgentPositioningSystem:
    def __init__(self):
        self.author = "Dr. Robert Morain"



def init_village(terrain, num_houses):
    village_skeleton = []
    z, x = terrain.shape
    for id in range(num_houses):
        h = House(id)
        h.set_position((random.randint(0, min(z, z - max(h.dim) - 1)), random.randint(0, min(x, x - max(h.dim) - 1))), z, x)
        village_skeleton.append(h)
    return village_skeleton

def position_village(village_skeleton, terrain):
    z, x = terrain.shape
    for building in village_skeleton:
        interest_vector = building.get_interest(village_skeleton, terrain)
        building.set_position(building.position + interest_vector, z, x)


def main():
    num_houses = 70
    elevation_terrain, material_terrain = generate_terrain(500, 500, 10, 80, 1, 5)

    #print(terrain)
    village_skeleton = init_village(elevation_terrain, num_houses)

    for i in range(100):
        position_village(village_skeleton, elevation_terrain)

    maps_viz.plot(elevation_terrain, village_skeleton)

if __name__=='__main__':
    main()



