import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import skewnorm
import math

class Building(object): # Should this be a namedtuple ???
    def __init__(self, type, position, dim):
        self.type = type
        self.position = position
        self.dim = dim
    # def __init__(self, type, position, dim, f_att_param, f_bal_param, f_close_param, f_open_param):
    #     self.type = type
    #     self.position = position
    #     self.dim = dim
    #     self.f_att_param = f_att_param
    #     self.f_bal_param = f_bal_param
    #     self.f_close_param = f_close_param
    #     self.f_open_param = f_open_param

    def get_interest(self, village_skeleton, terrain, p):
        pass

    def build(self, terrain):
        z_range = [self.position[0], self.position[0] + self.dim[0]]
        x_range = [self.position[1], self.position[1] + self.dim[1]]
        building_id = np.max(terrain)
        terrain[z_range[0] : z_range[1], x_range[0] : x_range[1]] = building_id

class House(Building):
    def __init__(self):
        super(House, self).__init__("house", (0,0), (10,10))

    def get_interest(self, village_skeleton, terrain, p):
        social_max = 40
        diff = lambda p1, p2, i : abs(p1[i] - p2[i])
        a = 1
        a_s = []
        #print('get_interest')
        for building in village_skeleton:
            if diff(building.position, p, 0) < (social_max * 3) or diff(building.position, p, 1) < (social_max * 3):
                new_a = LJ_potential(manhattan_distance(building.position, p), 10, social_max)
                #print(new_a, manhattan_distance(building.position, p))
                if new_a <= -1:
                    a = -1
                    break
                else:
                    a_s.append(new_a)
        if len(a_s) > 0:
            a = np.average(a_s)

        # a = LJ_potential(p, 10, social_max)
        d_slope = abs(get_slope_range(terrain, p, max(self.dim)))
        b = balance(d_slope, -.25, 1.5)
        return [a,b], [.75, .25]

def manhattan_distance(p1, p2):
    distance = 0
    for i in range(len(p1)):
        distance += abs(p1[i] - p2[i])
    return distance

def get_slope_range(terrain, position, max_dim):
    z, x = terrain.shape
    range_z = [position[0], min(position[0] + max_dim, z-1)]
    range_x = [position[1], min(position[1] + max_dim, x-1)]
    return np.max(terrain[range_z[0] : range_z[1], range_x[0]: range_x[1]])\
           - np.min(terrain[range_z[0] : range_z[1], range_x[0] : range_x[1]])

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

def get_local_interest(village_skeleton, terrain, building, position):
    interests, weights = building.get_interest(village_skeleton, terrain, position)
    for i, interest in enumerate(interests):
        if interest <= -.95:
            return -1
        interests[i] = max(0, interest) / len(interests) * weights[i]
    return sum(interests)

# def generate_building(terrain, village_skeleton, building):
#     z, x = terrain.shape
#     coord = random.randint(0, z-1), random.randint(0, x-1)
#     get_local_interest(terrain, village_skeleton, building, coord)

def fit_to_range(x, minx, maxx, min_range, max_range):
    normalized_x = (x - minx) / (maxx - minx)
    return (normalized_x * (max_range - min_range)) + min_range

def tanh_distance(x, minx=-4, maxx=4):
    min_range, max_range = -4, 4
    range_x = fit_to_range(x, minx, maxx, min_range, max_range)
    return -math.tanh(range_x)

def close_distance(x, minx=-4, maxx=4):
    if x <= minx:
        return -1
    elif x >= maxx:
        return -1
    else:
        return tanh_distance(x, minx, maxx)

def open_distance(x, minx=-4, maxx=4):
    if x <= minx:
        return 1
    elif x >= maxx:
        return -1
    else:
        return tanh_distance(x, minx, maxx)

def balance(x, minx, maxx):
    min_range, max_range = -.25, 1.25
    range_x = fit_to_range(x, minx, maxx, min_range, max_range)
    a = 3
    loc = 0
    scale = .33
    rv = skewnorm(a, loc, scale)
    return rv.pdf(range_x)

# Attraction - Repulsion
def LJ_potential(x, minx, maxx):
    if x > maxx or x < minx:
        return -1
    min_range, max_range = 1, 3
    range_x = fit_to_range(x, minx, maxx, min_range, max_range)
    sigma = 1.032
    e = 1
    return -4*e*((sigma/range_x)**12 - (sigma/range_x)**6)

def place_house(village_skeleton, terrain):
    num_segments = 10
    h = House()
    z, x = terrain.shape
    placed = False
    while not placed:
        for z_i in range(num_segments):
            for x_i in range(num_segments):
                z_min, z_max = (z // num_segments) * z_i, (z // num_segments) * (z_i + 1)
                x_min, x_max = (x // num_segments) * x_i, (x // num_segments) * (x_i + 1)

                #position = random.randint(0, z - max(h.dim) -1), random.randint(0, x - max(h.dim) -1)
                position = random.randint(z_min, min(z_max, z - max(h.dim) -1)), random.randint(x_min, min(x_max, x - max(h.dim) -1))
                local_interest = get_local_interest(village_skeleton, terrain, h, position)
                if random.random() <= local_interest:
                    #print(local_interest)
                    h.position = position
                    village_skeleton.append(h)
                    placed = True
                    return

def build_village(terrain, num_houses):
    village_skeleton = []
    # for _ in range(random.randint(3, 5)):
    for i in range(num_houses):
        place_house(village_skeleton, terrain)
        print('house', i)

    for building in village_skeleton:
        building.build(terrain)



def main():
    num_houses = 45
    num_hills = 6
    max_hill_height = 100
    terrain = np.zeros((500,500))
    for _ in range(num_hills):
        generate_hill(terrain, max_hill_height)
    #print(terrain)
    build_village(terrain, num_houses)
    plt.imshow(terrain, cmap='hot', interpolation='nearest')
    plt.show()

    # Attraction-Repulsion Interest Function Graph
    # minx = 10
    # maxx = 50
    # x = np.linspace(minx,maxx,1000)
    # y = [LJ_potential(r, minx, maxx) for r in x]
    # plt.plot(x, y)
    # plt.show()

    # Balance
    # minx = 10
    # maxx = 50
    # x = np.linspace(minx, maxx, 1000)
    # y = [balance(i, minx, maxx) for i in x]
    # plt.plot(x, y)
    # plt.show()

    # Close Distance
    # minx = 10
    # maxx = 50
    # x = np.linspace(minx - ((maxx-minx)//4), maxx, 1000)
    # y = [close_distance(i, minx=minx, maxx=maxx) for i in x]
    # plt.plot(x, y)
    # plt.show()

    # Open Distance
    # minx = 10
    # maxx = 50
    # x = np.linspace(minx - ((maxx-minx)//4), maxx, 1000)
    # y = [open_distance(i, minx=minx, maxx=maxx) for i in x]
    # plt.plot(x, y)
    # plt.show()


    village_skeleton = []

if __name__=='__main__':
    main()