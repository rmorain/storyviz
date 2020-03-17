import numpy as np
import copy
import random

from lines import *


class Terrain:
    def __init__(self):
        self.layers = {'material':None, 'elevation':None}
        self.materials = {'water': 9, 'road': 1, 'building': -1}
        self.material_points = {}
        self.generate_terrain()

    def load_map(self, level, box):
        self.layers['elevation'] = np.zeros((box.length, box.width))
        self.layers['material'] = np.zeros((box.length, box.width))
        self.layers['building'] = np.zeros((box.length, box.width))
        for z in range(box.minz, box.maxz):
            for x in range(box.minx, box.maxx):
                for y in range(box.maxy, box.miny, -1):
                    material_id = level.blockAt(x, y, z)
                    if material_id != 0: #If it isn't air
                        self.layers['elevation'][z-box.minz][x-box.minx] = y - box.miny
                        self.layers['material'][z-box.minz][x-box.minx] = material_id
                        break

    # Initialize a material distance layer
    # Pass in int for material you want to get distance from at each point
    def init_material_dist(self, material):
        x, y = self.layers['material'].shape  # Get dimensions of material terrain
        material_dist_layer = np.full((x, y), np.inf)   # Initialize to all inf
        self.material_points[material] = []
        # Look at each cell in material layer
        for i, row in enumerate(self.layers['material']):
            for j, block in enumerate(row):
                # Check if cell contains material of interest
                if block == material:
                    # Set distance from material at that point equal to zero
                    material_dist_layer[i][j] = 0
                    self.material_points[material].append(np.array([i, j]))
                    # Other wise it remains infinity
        return material_dist_layer

    # Iteratively updates the minimum distance from each point to a material of interest
    def update_material_dist(self, material_dist_layer, material):
        # Runs at least once
            # Look at each cell, beginning at top left
        for i, row in enumerate(material_dist_layer):
            for j, block in enumerate(row):
                minimum = self.get_min_dist(np.array([i,j]), self.material_points[material])
                material_dist_layer[i][j] = minimum
        return material_dist_layer  

    def get_min_dist(self, point, list_of_points):
        distances = []
        for p in list_of_points:
            distances.append(np.linalg.norm(point - p))
        return min(distances)

    def get_coord_offset(self, coord, offset, scale):
        scaled_offset = tuple(scale*x for x in offset)
        return tuple(coord[i]+scaled_offset[i] for i in range(len(coord)))

    def modify_terrain(self, terrain, coord, value):
        z, x = terrain.shape
        if coord[0] >= 0 and coord[0] < z and coord[1] >= 0 and coord[1] < x:
            if value > terrain[coord]:
                terrain[coord] = value

    def generate_hill(self, terrain, peak_max):
        z, x = terrain.shape
        hill_center = random.randint(0, z-1), random.randint(0, x-1)
        terrain_height = random.randint(peak_max//3, peak_max)
        terrain[hill_center] = terrain_height
        neighbors = [(1,0),(0,1),(-1,0),(0,-1)]
        for distance in range(1, terrain_height):
            for neighbor_idx in range(len(neighbors)):
                sz, sx = self.get_coord_offset(hill_center, neighbors[neighbor_idx], distance)
                self.modify_terrain(terrain, (sz, sx), terrain_height - distance)
                dz = neighbors[(neighbor_idx+1)%len(neighbors)][0] - neighbors[neighbor_idx][0]
                dx = neighbors[(neighbor_idx+1)%len(neighbors)][1] - neighbors[neighbor_idx][1]
                point = (sz, sx)
                for _ in range(distance-1):
                    point = (point[0] + dz, point[1] + dx)
                    self.modify_terrain(terrain, point, terrain_height - distance)

    def generate_material_line(self, material_terrain, max_width, material):
        z, x = material_terrain.shape
        start_point = (random.randint(0, z - 1), random.randint(0, z - 1))
        end_point = (random.randint(0, z - 1), random.randint(0, x - 1))
        points = get_grid_cells_btw(start_point, end_point)
        points = connect_neighboring_points(points)
        width_offset = random.randint(1, max_width) // 2
        points = expand_line(points, width_offset, start_point, end_point, z, x)
        for point in points:
            material_terrain[point] = material

    def generate_terrain(self):
        z, x, num_hills, max_hill_height, num_rivers, max_river_width = (200, 200, 0, 0, 1, 1)

        self.layers['material'] = np.zeros((z, x))
        self.layers['elevation'] = np.zeros((z, x))
        self.layers['road_dist'] = self.init_material_dist(self.materials['road'])
        for _ in range(num_hills):
            self.generate_hill(self.layers['elevation'], max_hill_height)

        for _ in range(num_rivers):
            self.generate_material_line(self.layers['material'], max_river_width, self.materials['water'])


        return None

    def update_buildings(self, village_skeleton, layer):
        for building in village_skeleton:
            if building.placed and not building.connected:
                points = building.get_footprint()
                self.copy(points, layer, self.materials['building'])

    # Copy of list of points of a material into a layer
    def copy(self, points, layer, material):
        for p in points:
            layer[p] = material


