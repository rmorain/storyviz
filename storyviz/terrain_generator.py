import random
import numpy as np
from lines import *

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

def generate_river(material_terrain, max_width):
    still_water_id = 9
    z, x = material_terrain.shape
    start_point = (random.randint(0, z - 1), random.randint(0, z - 1))
    end_point = (random.randint(0, z - 1), random.randint(0, x - 1))
    points = get_grid_cells_btw(start_point, end_point)
    points = connect_neighboring_points(points)
    width_offset = random.randint(1, max_width) // 2
    points = expand_line(points, width_offset, start_point, end_point, z, x)
    for point in points:
        material_terrain[point] = still_water_id

def generate_terrain(z, x, num_hills, max_hill_height, num_rivers, max_river_width):
    elevation_terrain = np.zeros((z, x))
    material_terrain = np.zeros((z, x))
    for _ in range(num_hills):
        generate_hill(elevation_terrain, max_hill_height)

    for _ in range(num_rivers):
        generate_river(material_terrain, max_river_width)

    return elevation_terrain, material_terrain