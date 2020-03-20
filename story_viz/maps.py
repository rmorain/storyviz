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
import astar2
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
    z, x = terrain.layers['elevation'].shape
    for i, building in enumerate(village_skeleton):
        if not building.placed:
            interest_vector = building.get_interest(village_skeleton, terrain)
            building.set_position(building.position + interest_vector, z, x)
            building.random_stop()

# Connect stopped building to a road network
def draw_roads(village_skeleton, terrain):
    for i, building in enumerate(village_skeleton):
        if building.placed and not building.connected:
            connect2(building, terrain)
            building.connected = True

# def get_min_road(building_road, road_road):
#     if building_road is None:
#         return road_road
#     if road_road is None:
#         return building_road
#     if len(building_road) < len(road_road)*.5:
#         return building_road
#     return road_road
#
# # Connect a building to the nearest road using a*
# def connect(building, terrain):
#     start = np.subtract(building.position, (1, 1))  # Start road at top left of building
#     building_road = None
#     road_road = None
#     if np.any(terrain.layers['material'] == terrain.materials['building']):  # Check if there are placed buildings
#         building_road = astar(terrain, start, terrain.materials['building'])  # Connect to nearest stopped building
#     if np.any(terrain.layers['material'] == terrain.materials['road']):  # Check if there are roads to connect to
#         road_road = astar(terrain, start, terrain.materials['road']) # Connect to nearest road
#     road = get_min_road(building_road, road_road)
#     # Road is not None
#     if road:
#         terrain.copy(road, terrain.layers['material'], terrain.materials['road'])

def connect2(building, terrain):
    # Fix position if it is too far off
    y,x = building.position
    h,w = terrain.layers['elevation'].shape
    if y > h or x > w or y < 0 or x < 0:
        building.position = np.array([0,0])
    # TODO: Add something to put the building back in bounds
    start = np.subtract(building.position, (1, 1))  # Start road at top left of building
    road = astar2.astar(terrain, tuple(start), 0)
    if road is not None:
        print('adding road')
        print(road)
        terrain.add_road(road) # TODO: Houses that are close enough to roads should be counted as connected
    else:
        print('No road possible')
    # Road is not None
    # if road:
    #     terrain.copy(road, terrain.layers['material'], terrain.materials['road'])

def add_outside_roads(terrain):
    num_outside_roads = random.randint(2, 3)
    maxz, maxx = terrain.layers['material'].shape
    for _ in range(num_outside_roads):
        if random.choice([True, False]):
            z = random.randint(0, maxz-1)
            x = random.choice([0, maxx-1])
        else:
            z = random.choice([0, maxz-1])
            x = random.randint(0, maxx-1)
        terrain.add_road([(z,x)])

def create_minecraft_village(level, box, building_spec, animate=False):
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
        position_village(village_skeleton, terrain)
        draw_roads(village_skeleton, terrain)
        if animate:
            animator.add(village_skeleton)

    # animator.plot(elevation_terrain, village_skeleton)
    if animate:
        animator.animate(elevation_terrain, material_terrain)
    return village_skeleton, terrain

def create_village(animate=True):
    animator = VizAnimator()
    num_houses = 30
    num_farms = 30
    num_churches = 3
    num_stores = 1
    # building_spec = {'House': num_houses, 'Farm': num_farms, 'Church': num_churches, 'Store': num_stores}
    # building_spec = {'House': num_houses, 'Farm': num_farms, 'Church': num_churches}
    #
    # building_spec = {'House': [num_houses, {}],
    #                  'Farm': [num_farms, {}],
    #                  'Church': [num_churches, {}]}

    village_spec = VillageSpec()
    village_spec.add("House", num_houses)
    village_spec.add("Farm", num_farms)
    village_spec.add("Church", num_churches)

    # generate_terrain(z, x, num_hills, max_hill_height, num_rivers, max_river_width)
    t = Terrain()
    t.generate_terrain(500, 500, 6, 200, 2, 5)

    #print(terrain)
    elevation_terrain = t.layers['elevation']
    material_terrain = t.layers['material']
    village_skeleton = init_village(elevation_terrain, village_spec)
    add_outside_roads(t)

    for i in range(300):
        position_village(village_skeleton, t)
        t.update_buildings(village_skeleton, t.layers['material'])
        draw_roads(village_skeleton, t)
        if animate:
            animator.add(village_skeleton)

    # a = t.layers['road']
    # fig, (ax1, ax2) = plt.subplots(1, 2)
    # ax1.imshow(np.clip(a, 0, 1), cmap='hot', interpolation='nearest')
    # ax2.imshow(a, cmap='hot', interpolation='nearest')
    # plt.show()

    # animator.plot(elevation_terrain, village_skeleton)
    if animate:
        animator.animate(elevation_terrain, material_terrain)
    plot(t, village_skeleton)
    return village_skeleton, t

def main():
    create_village(False)

if __name__=='__main__':
    main()



