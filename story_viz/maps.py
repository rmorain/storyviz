import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import skewnorm
import math
from buildings import *
from maps_viz import *
from terrain_generator import generate_terrain

class MultiAgentPositioningSystem:
    def __init__(self):
        self.author = "Dr. Robert Morain"



def init_village(terrain, building_spec):
    village_skeleton = []
    z, x = terrain.shape
    buildings = building_generator(building_spec)
    for building in buildings:
        building.set_position((random.randint(0, min(z, z - max(building.dim) - 1)), random.randint(0, min(x, x - max(building.dim) - 1))), z, x)
        village_skeleton.append(building)
    return village_skeleton

def position_village(village_skeleton, terrain):
    z, x = terrain.shape
    for building in village_skeleton:
        interest_vector = building.get_interest(village_skeleton, terrain)
        building.set_position(building.position + interest_vector, z, x)


def main():
    animator = VizAnimator()
    num_houses = 70
    num_farms = 20
    num_churches = 2
    building_spec = {'House': num_houses, 'Farm': num_farms, 'Church': num_churches}
    # generate_terrain(z, x, num_hills, max_hill_height, num_rivers, max_river_width)
    elevation_terrain, material_terrain = generate_terrain(500, 500, 10, 80, 1, 5)

    #print(terrain)
    village_skeleton = init_village(elevation_terrain, building_spec)
    plot(material_terrain, village_skeleton)

    for i in range(100):
        position_village(village_skeleton, elevation_terrain)
        animator.add(village_skeleton)

    # animator.plot(elevation_terrain, village_skeleton)
    animator.animate(elevation_terrain, material_terrain)

if __name__=='__main__':
    main()



