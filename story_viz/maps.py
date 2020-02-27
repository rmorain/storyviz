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

def position_village(village_skeleton, terrain, terrain_copy, plot=False): #TODO: DOn't overwrite the terrain
    z, x = terrain.shape
    for building in village_skeleton:
        terrain_copy[building.position[0], building.position[1]] = 50

    # building_heat = np.max(terrain)
    building_heat = 75
    for building in village_skeleton:
        interest_vector = building.get_interest(village_skeleton, terrain)
        building.set_position(building.position + interest_vector, z, x)
        terrain_copy[building.position[0], building.position[1]] = building_heat


def main():
    num_houses = 70
    terrain, material_terrain = generate_terrain(500, 500, 10, 80, 1, 5)

    #print(terrain)
    village_skeleton = init_village(terrain, num_houses)
    terrain_copy = np.copy(terrain)

    for i in range(100):
        plot = False
        # if i % 10 == 0:
        #     plot = True
        position_village(village_skeleton, terrain, terrain_copy, plot)


    for building in village_skeleton:
        terrain[building.position[0], building.position[1]] = 50
    maps_viz.plot(terrain)

if __name__=='__main__':
    main()



