import numpy as np
import copy
import random

from lines import *
from heapq import *

class Terrain:
    def __init__(self):
        self.layers = {'material':None, 'elevation':None, 'road':None}
        self.materials = {'water': 9, 'road': 1, 'building': -1}
        self.material_points = {'road':set()}

    def offset_new_dim(self, dim, dim_offset, max_dim):
        new_dim = []
        for i in range(2):
            if dim[i] + dim_offset[i] < 0:
                new_dim.append(0)
            elif dim[i] + dim_offset[i] >= max_dim:
                new_dim.append(max_dim-1)
            else:
                new_dim.append(dim[i] + dim_offset[i])
        return tuple(new_dim)

    def handle_tree(self, z, x):
        elevation = self.layers['elevation']
        material = self.layers['material']
        maxz, maxx = elevation.shape
        tree_wood = [17, 162]
        tree_dims = {(z, x)}
        not_tree_dims = set()
        handled_tree_dim = set()
        neighbors = [(0,1),(0,-1),(1,0),(-1,0)]
        while len(tree_dims) > 0:
            tree_dim = tree_dims.pop()
            handled_tree_dim.add(tree_dim)
            for neighbor_offset in neighbors:
                neighbor_dim = self.offset_new_dim(tree_dim, neighbor_offset, (maxz, maxx))
                neighbor_material = material[neighbor_dim[0]][neighbor_dim[1]]
                if neighbor_material in tree_wood and neighbor_dim not in handled_tree_dim:
                    tree_dims.add(neighbor_dim)
                if neighbor_material not in tree_wood:
                    not_tree_dims.add(neighbor_dim)
        avg_terrain = int(round(np.average([elevation[dim[0]][dim[1]] for dim in not_tree_dims])))
        for dim in handled_tree_dim:
            self.layers['elevation'][dim[0]][dim[1]] = avg_terrain

    '''At the moment it just takes the avg surronding terrain elevation'''
    def handle_tree_elevation(self):
        for z in range(len(self.layers['elevation'])):
            for x in range(len(self.layers['elevation'][0])):
                if self.layers['elevation'][z][x] == np.inf:
                    self.handle_tree(z, x)

    def drill_down(self, level, box, z, x, y, min_y):
        material_id = level.blockAt(x, y, z)
        elevation = y
        tree_wood = [17, 162]
        tree_leaves = [18, 161]
        other_flora = [31, 32, 37, 38, 39, 40, 175]
        if y <= min_y:
            return material_id, elevation
        elif material_id == 0:
            material_id, elevation = self.drill_down(level, box, z, x, y-1, min_y)
        elif material_id in other_flora:
            _, elevation = self.drill_down(level, box, z, x, y-1, min_y)
        elif material_id in tree_wood:
            elevation = np.inf
        elif material_id in tree_leaves:
            material_id, elevation = self.drill_down(level, box, z, x, y-1, min_y)
        return material_id, elevation

    def load_map(self, level, box):
        self.layers['elevation'] = np.zeros((box.length, box.width))
        self.layers['material'] = np.zeros((box.length, box.width))
        self.layers['building'] = np.zeros((box.length, box.width))
        self.layers['road'] = np.full((box.length, box.width), np.inf)
        for z in range(box.minz, box.maxz):
            for x in range(box.minx, box.maxx):
                material_id, elevation = self.drill_down(level, box, z, x, box.maxy, box.miny)
                self.layers['elevation'][z-box.minz][x-box.minx] = elevation - box.miny
                self.layers['material'][z-box.minz][x-box.minx] = material_id
        self.handle_tree_elevation()

    def add_road(self, path):
        for point in path:
            self.add_material_point('road', point)
        self.update_material_dist('road')

    # Initialize a material distance layer
    # Pass in int for material you want to get distance from at each point
    def init_material_dist(self, material):
        x, y = self.layers['material'].shape  # Get dimensions of material terrain
        material_dist_layer = np.full((x, y), np.inf)   # Initialize to all inf
        self.material_points[material] = {}
        # Look at each cell in material layer
        for i, row in enumerate(self.layers['material']):
            for j, block in enumerate(row):
                # Check if cell contains material of interest
                if block == material: # TODO: Makes sense for water, might be issue with roads
                    # Set distance from material at that point equal to zero
                    material_dist_layer[i][j] = 0
                    self.material_points[material].add(np.array([i, j]))
                    # Other wise it remains infinity
        return material_dist_layer

    def add_material_point(self, material_dist_layer, point):
        if material_dist_layer not in self.layers:
            z, x = self.layers['elevation'].shape
            self.layers[material_dist_layer] = np.full((z, x), np.inf)
            self.material_points[material_dist_layer] = set()
        self.layers[material_dist_layer][point] = 0
        self.material_points[material_dist_layer].add(point)

    def update_material_dist(self, material):
        array = self.layers[material]
        points = self.material_points[material]

        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        close_set = points.copy()
        oheap = []

        for point in points:
            heappush(oheap, (0, point))

        while oheap:

            current = heappop(oheap)[1]
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j
                # out of bounds check
                if 0 <= neighbor[0] < array.shape[0]:
                    if neighbor[1] < 0 or neighbor[1] >= array.shape[1]:
                        continue
                else:
                    continue

                # Because we are using a priority queue,
                # all points updated will be at their minimum point so they don't need to be rechecked
                if neighbor in close_set:
                    continue

                tentative_dist = self.layers[material][current] + 1
                # If we update the neighbor than we need to update its neighbors
                if tentative_dist < self.layers[material][neighbor]:
                    self.layers[material][neighbor] = tentative_dist
                    heappush(oheap, (tentative_dist, neighbor))
                    close_set.add(neighbor)


    # # Iteratively updates the minimum distance from each point to a material of interest
    # def update_material_dist(self, material_dist_layer, material):
    #     # Runs at least once
    #         # Look at each cell, beginning at top left
    #     for i, row in enumerate(material_dist_layer):
    #         for j, block in enumerate(row):
    #             minimum = self.get_min_dist(np.array([i,j]), self.material_points[material])
    #             material_dist_layer[i][j] = minimum
    #     return material_dist_layer
    #
    # def get_min_dist(self, point, list_of_points):
    #     distances = []
    #     for p in list_of_points:
    #         distances.append(np.linalg.norm(point - p))
    #     return min(distances)

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

    def generate_terrain(self, z=200, x=200, num_hills=0, max_hill_height=0, num_rivers=1, max_river_width=1):
        self.layers['material'] = np.zeros((z, x))
        self.layers['elevation'] = np.zeros((z, x))
        self.layers['road'] = np.full((z, x), np.inf)
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


