import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import skewnorm
import math

# Make building.position np array

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

    def get_interest(self, village_skeleton, terrain, knn=10, attraction=40, repulsion=10):
        social_vector = sociability(village_skeleton, self, knn, attraction, repulsion)
        slope_vector = slope(self, terrain)
        print('social', social_vector)
        print('slope', slope_vector)
        #return social_vector * .5 + slope_vector * .5 + self.get_noise(10)
        # print(normalize_vector(social_vector, True) + normalize_vector(slope_vector, True) * .3)

        return normalize_vector(social_vector, True) + normalize_vector(slope_vector, True) * .3

    def get_noise(self, scale=1):
        noise_vector = np.array([random.uniform(-1,1), random.uniform(-1,1)])
        noise_vector = noise_vector / np.linalg.norm(noise_vector)
        return noise_vector * scale

class MultiAgentPositioningSystem:
    def __init__(self):
        self.author = "Dr. Robert Morain"


def get_vector(building, neighbor, distance, scale):
    if distance == 0:
        unit_directions = [[10,0], [-10,0], [0,-10], [0,10]]
        idx = random.randint(0,3)
        return unit_directions[idx]
    else:
        return ((neighbor.position - building.position) / distance) * scale #min(20, scale) #TODO: Magic number

def sociability(village_skeleton, building, knn, attraction, repulsion):
    distances = dict()
    for neighbor in village_skeleton:
        if neighbor.id != building.id:
            if neighbor.type in building.social_agents:
                distance = euclidean_distance(building.position, neighbor.position)
                distances[neighbor] = distance
    knn_neighbors = sorted(distances.items(), key = lambda kv : kv[1])[:knn]
    knn_vector = np.array([0.,0.])
    for neighbor, distance in knn_neighbors:
        # print('knn', building.id, knn_vector)

        # print((neighbor.position - building.position), (neighbor.position - building.position) / distance)
        if distance > attraction:
            knn_vector += get_vector(building, neighbor, distance, distance - attraction)
            # knn_vector += get_vector(building, neighbor, distance, 1)

        elif distance < repulsion:
            knn_vector += get_vector(building, neighbor, distance, (repulsion - distance) * -1)
            # knn_vector += get_vector(building, neighbor, distance, 1)
    return knn_vector
    #return np.sum(knn_vector, axis=1)

def slope(building, terrain):
    building_center = building.position + (max(building.dim) // 2) # TODO: This is 2d
    left_half = terrain[building.position[0]:building.position[0] + max(building.dim), building.position[1] : building_center[1]]
    right_half = terrain[building.position[0]:building.position[0] + max(building.dim), building_center[1] : building.position[1] + max(building.dim)]

    bottom_half = terrain[building.position[0] : building_center[0], building.position[1]:building.position[1] + max(building.dim)]
    top_half = terrain[building_center[0] : building.position[0] + max(building.dim), building.position[1]:building.position[1] + max(building.dim)]

    dz = np.average(left_half) - np.average(right_half)
    dx = np.average(bottom_half) - np.average(top_half)

    # print('dz, dx', type(dz), dz, type(dx), dx)
    # if np.isnan(dz):
    #     print(left_half)
    #     print(building.position[0], building.position[0] + max(building.dim), building.position[1], building_center[1])
    #     print(np.average(left_half))
    #     print(right_half)
    #     print(building.position[0], building.position[0] + max(building.dim), building_center[1], building.position[1] + max(building.dim))
    #     print(np.average(right_half))
    # if np.isnan(dx):
    #     print(bottom_half)
    #     print(building.position[0], building_center[0], building.position[1], building.position[1] + max(building.dim))
    #     print(np.average(bottom_half))
    #     print(top_half)
    #     print(building_center[0], building.position[0] + max(building.dim), building.position[1], building.position[1] + max(building.dim))
    #     print(np.average(top_half))

    return np.array([dz, dx])

def euclidean_distance(p1, p2):
    distance = 0
    for i in range(len(p1)):
        distance += (p1[i] - p2[i])**2
    return math.sqrt(distance)

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
    num_houses = 2
    num_hills = 10
    max_hill_height = 80
    terrain = np.zeros((500,500))
    for _ in range(num_hills):
        generate_hill(terrain, max_hill_height)
    #print(terrain)
    village_skeleton = init_village(terrain, num_houses)
    terrain_copy = np.copy(terrain)
    plt.ion()
    for i in range(100):
        # plot = False
        # if i % 30 == 0:
        #     plot = True
        position_village(village_skeleton, terrain, terrain_copy)
        plt.imshow(terrain_copy, cmap='hot', interpolation='nearest')
        plt.draw()
        plt.pause(.1)
        plt.clf()

    # plt.imshow(terrain, cmap='hot', interpolation='nearest')
    # plt.show()

if __name__=='__main__':
    main()



