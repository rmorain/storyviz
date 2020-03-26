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
import astar
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

def position_village(village_skeleton, terrain, record=False):
    distances = []
    z, x = terrain.layers['elevation'].shape
    for i, building in enumerate(village_skeleton):
        if not building.placed:
            interest_vector = building.get_interest(village_skeleton, terrain)
            building.set_position(building.position + interest_vector, z, x)
            if record:
                building.store_interest_info(interest_vector)
                distances.append(np.linalg.norm(interest_vector))
    return distances

# Connect stopped building to a road network
def draw_roads(village_skeleton, terrain):
    for i, building in enumerate(village_skeleton):
        if building.placed and not building.connected:
            connect_building(building, terrain)
            building.connected = True

def connect_building(building, terrain):
    start = np.subtract(building.position, (1, 1))  # Start road at top left of building
    if start[0] < 0 or start[1] < 0:
        start = np.add(building.position, (1,1))
    # Check if out of bounds
    if start[0] > len(terrain.layers['material']):
        start[0] = len(terrain.layers['material']) - 1
    if start[1] > len(terrain.layers['material']):
        start[1] = len(terrain.layers['material']) - 1

    connect_point(start, terrain)

    # if y > h or x > w or y < 0 or x < 0:
    #     building.position = np.array([0,0])
    # # TODO: Add something to put the building back in bounds

def connect_point(start, terrain):
    road = astar.astar(terrain, tuple(start), 0)
    if road is not None:
        print('adding road')
        print(road)
        terrain.add_road(road) # TODO: Houses that are close enough to roads should be counted as connected
    else:
        print('No road possible')


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

def place_buildings(village_skeleton, avg_distance):
    all_buildings_placed = True
    for building in village_skeleton:
        if not building.placed:
            all_buildings_placed = False
            distance = np.linalg.norm(building.last_interest_vector)
            if distance < avg_distance:
                if random.random() > ((distance + avg_distance) / (2*avg_distance)): # Normalize distance so 0 has 50% chance of being placed
                    building.placed = True
    return all_buildings_placed

def free_positioning(terrain, village_skeleton):
    free_positioning_epochs = 100
    distances = []
    for i in range(free_positioning_epochs):
        if i >= (free_positioning_epochs * .9):
            distances += position_village(village_skeleton, terrain, record=True)
        else:
            position_village(village_skeleton, terrain)
    return np.average(distances)

def plot_iterative_positioning(village_skeleton, distances):
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
    mins = []
    maxs = []
    avgs = []
    for building in village_skeleton:
        d_min, d_avg, d_max = building.get_interest_info()
        mins.append(d_min)
        maxs.append(d_max)
        avgs.append(d_avg)

    ax1.hist(distances)
    ax2.hist(mins)
    ax3.hist(maxs)
    ax4.hist(avgs)
    plt.show()

def iterative_positioning(terrain, village_skeleton, animate, animator):
    avg_distance = free_positioning(terrain, village_skeleton)
    distances = []
    for i in range(200):
        all_buildings_placed = place_buildings(village_skeleton, avg_distance)
        if all_buildings_placed:
            print('all buildings placed')
            break
        distances += position_village(village_skeleton, terrain, True)
        terrain.update_buildings(village_skeleton, terrain.layers['material'])
        draw_roads(village_skeleton, terrain)
        if animate:
            animator.add(village_skeleton)

    # plot_iterative_positioning(village_skeleton, distances)

def create_minecraft_village(level, box, building_spec, animate=False):
    animator = VizAnimator()
    terrain = Terrain()
    terrain.load_map(level, box)
    elevation_terrain, material_terrain = terrain.layers['elevation'], terrain.layers['material']

    village_skeleton = init_village(elevation_terrain, building_spec)

    iterative_positioning(terrain, village_skeleton, animate, animator)

    if animate:
        animator.animate(elevation_terrain, material_terrain)
    return village_skeleton, terrain

def create_village(animate=True):
    animator = VizAnimator()
    num_houses = 30
    num_farms = 30
    num_churches = 3
    num_stores = 1

    village_spec = VillageSpec()
    village_spec.add("House", num_houses)
    village_spec.add("Farm", num_farms)
    village_spec.add("Church", num_churches)

    # generate_terrain(z, x, num_hills, max_hill_height, num_rivers, max_river_width)
    t = Terrain()
    t.generate_terrain(500, 500, 6, 200, 2, 5)

    elevation_terrain = t.layers['elevation']
    material_terrain = t.layers['material']
    village_skeleton = init_village(elevation_terrain, village_spec)
    add_outside_roads(t)

    iterative_positioning(t, village_skeleton, animate, animator)

    if animate:
        animator.animate(elevation_terrain, material_terrain)
    plot(t, village_skeleton)
    return village_skeleton, t

def main():
    create_village(False)

if __name__=='__main__':
    main()



