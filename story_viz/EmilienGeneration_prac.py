import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import skewnorm

class Building: # Should this be a namedtuple ???
    def __init__(self, type):
        self.type = "house"
        self.position = (0,0)


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

def get_local_interest():
    pass

def generate_building(terrain, village_skeleton, building):
    z, x = terrain.shape
    coord = random.randint(0, z-1), random.randint(0, x-1)
    get_local_interest(terrain, village_skeleton, building, coord)

def close_distance():
    pass

def balance(x):
    a = 3
    loc = 0
    scale = .33
    rv = skewnorm(a, loc, scale)
    return rv.pdf(x)

# Attraction - Repulsion
def LJ_potential(r):
    sigma = 1.03
    e = 1
    return -4*e*((sigma/r)**12 - (sigma/r)**6)

def main():
    terrain = np.zeros((100,100))
    for _ in range(random.randint(1,5)):
        generate_hill(terrain, 30)
    #print(terrain)
    # plt.imshow(terrain, cmap='hot', interpolation='nearest')

    # Attraction-Repulsion Interest Function Graph
    # x = np.linspace(1,3,1000)
    # y = [LJ_potential(r) for r in x]
    # plt.plot(x, y)
    # plt.show()

    # Balance
    # x = np.linspace(-.25, 1.25, 1000)
    # y = [balance(i) for i in x]
    # plt.plot(x, y)
    # plt.show()


    village_skeleton = []

if __name__=='__main__':
    main()