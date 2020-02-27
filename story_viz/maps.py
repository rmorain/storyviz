import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import skewnorm
import math
from buildings import *

class MultiAgentPositioningSystem:
    def __init__(self):
        self.author = "Dr. Robert Morain"

def get_coord_offset(coord, offset, scale):
    scaled_offset = tuple(scale*x for x in offset)
    return tuple(coord[i]+scaled_offset[i] for i in range(len(coord)))

def modify_terrain(terrain, coord, value):
    z, x = terrain.shape
    if coord[0] >= 0 and coord[0] < z and coord[1] >= 0 and coord[1] < x:
        if value > terrain[coord]:
            terrain[coord] = value

def generate_hill(terrain, peak_max):
    z, x = terrain.shape
    hill_center = random.randint(0, z-1), random.randint(0, x-1)
    terrain_height = random.randint(peak_max//3, peak_max)
    terrain[hill_center] = terrain_height
    neighbors = [(1,0),(0,1),(-1,0),(0,-1)]
    for distance in range(1, terrain_height):
        for neighbor_idx in range(len(neighbors)):
            sz, sx = get_coord_offset(hill_center, neighbors[neighbor_idx], distance)
            modify_terrain(terrain, (sz, sx), terrain_height - distance)
            dz = neighbors[(neighbor_idx+1)%len(neighbors)][0] - neighbors[neighbor_idx][0]
            dx = neighbors[(neighbor_idx+1)%len(neighbors)][1] - neighbors[neighbor_idx][1]
            point = (sz, sx)
            for _ in range(distance-1):
                point = (point[0] + dz, point[1] + dx)
                modify_terrain(terrain, point, terrain_height - distance)

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
        print('interest_vector', interest_vector)
        building.set_position(building.position + interest_vector, z, x)
        terrain_copy[building.position[0], building.position[1]] = building_heat

    if plot:
        plt.imshow(terrain_copy, cmap='hot', interpolation='nearest')
        plt.show()


def main():
    num_houses = 70
    num_hills = 10
    max_hill_height = 80
    terrain = np.zeros((500,500))
    for _ in range(num_hills):
        generate_hill(terrain, max_hill_height)
    #print(terrain)
    village_skeleton = init_village(terrain, num_houses)
    terrain_copy = np.copy(terrain)

    # plt.ion()
    for i in range(100):
        plot = False
        # if i % 10 == 0:
        #     plot = True
        position_village(village_skeleton, terrain, terrain_copy, plot)
        plt.imshow(terrain_copy, cmap='hot', interpolation='nearest')
        # plt.draw()
        # plt.pause(.1)
        # plt.clf()

    for building in village_skeleton:
        terrain[building.position[0], building.position[1]] = 50
    plt.imshow(terrain, cmap='hot', interpolation='nearest')
    plt.show()

if __name__=='__main__':
    main()



