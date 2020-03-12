import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import skewnorm
import math
from buildings import *
from maps_viz import *
from terrain_generator import generate_terrain
from terrain import Terrain
from village_spec import VillageSpec
from astar import astar
from interests import get_knn

class MultiAgentPositioningSystem:
    def __init__(self):
        self.author = "Dr. Robert Morain"



def init_village(terrain, building_spec):
    village_skeleton = []
    z, x = terrain.shape
    buildings = building_generator(building_spec)
    for building in buildings:
        print(building.type, max(building.dim), (z, x))
        building.set_position((random.randint(0, min(z, z - max(building.dim) - 1)), random.randint(0, min(x, x - max(building.dim) - 1))), z, x)
        village_skeleton.append(building)
    return village_skeleton

def position_village(village_skeleton, terrain):
    z, x = terrain.shape
    for i, building in enumerate(village_skeleton):
        if not building.placed:
            interest_vector = building.get_interest(village_skeleton, terrain)
            building.set_position(building.position + interest_vector, z, x)
            building.random_stop()

# Connect stopped building to a road network
def draw_roads(village_skeleton, terrain):
    for i, building in enumerate(village_skeleton):
        if building.placed and not building.connected:
            connect(building, terrain)

# Connect a building to the nearest road using a*
def connect(building, terrain):
    start = np.subtract(building.position, (1, 1))  # Start road at top left of building?
    road = astar(terrain.layers['material'], start, terrain.materials['road'])
    # Road is not None
    if not road:
        road = astar(terrain.layers['material'], start, terrain.materials['building'])

    terrain.copy(road, terrain.layers['material'])


        



def create_minecraft_village(level, box, schematics, animate=False):
    animator = VizAnimator()
    # num_houses = 20
    # num_farms = 10
    # num_churches = 2
    # num_stores = 5
    # # building_spec = {'House': num_houses, 'Farm': num_farms, 'Church': num_churches, 'Store': num_stores}
    # building_spec = {'House': num_houses, 'Farm': num_farms, 'Church': num_churches}
    # generate_terrain(z, x, num_hills, max_hill_height, num_rivers, max_river_width)
    #elevation_terrain, material_terrain = generate_terrain(500, 500, 10, 80, 1, 5)
    terrain = Terrain()
    terrain.load_map(level, box)
    elevation_terrain, material_terrain = terrain.layers['elevation'], terrain.layers['material']

    #print(terrain)
    village_skeleton = init_village(elevation_terrain, building_spec)

    for i in range(100):
        position_village(village_skeleton, elevation_terrain)
        draw_roads(village_skeleton, terrain)
        if animate:
            animator.add(village_skeleton)

    # animator.plot(elevation_terrain, village_skeleton)
    if animate:
        animator.animate(elevation_terrain, material_terrain)
    return village_skeleton, terrain

def create_village(animate=True):
    animator = VizAnimator()
    num_houses = 20
    num_farms = 10
    num_churches = 1
    num_stores = 5
    # building_spec = {'House': num_houses, 'Farm': num_farms, 'Church': num_churches, 'Store': num_stores}
    # building_spec = {'House': num_houses, 'Farm': num_farms, 'Church': num_churches}
    #
    # building_spec = {'House': [num_houses, {}],
    #                  'Farm': [num_farms, {}],
    #                  'Church': [num_churches, {}]}

    village_spec = VillageSpec()
    village_spec.add("House", num_houses)
    village_spec.add("Farm", num_houses)
    village_spec.add("Church", num_houses)

    # generate_terrain(z, x, num_hills, max_hill_height, num_rivers, max_river_width)
    t = Terrain()

    #print(terrain)
    elevation_terrain = t.layers['elevation']
    material_terrain = t.layers['material']
    village_skeleton = init_village(elevation_terrain, village_spec)

    for i in range(100):
        position_village(village_skeleton, elevation_terrain)
        draw_roads(village_skeleton, t)
        if animate:
            animator.add(village_skeleton)

    # animator.plot(elevation_terrain, village_skeleton)
    if animate:
        animator.animate(elevation_terrain, material_terrain)
    return village_skeleton, t

def main():
    create_village()

if __name__=='__main__':
    main()



