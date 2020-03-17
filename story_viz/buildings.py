import random
import numpy as np
from interests import *
import importlib

# Takes a dictionary specifying {building_class : [num_buildings, schematic_info]}
# def building_generator(building_spec):
#     buildings = []
#     building_id = 0
#     for building_class_name, building_info in building_spec.items():
#         num_buildings, schematic_info = building_info[0], list(building_info[1].items())
#         for _ in range(num_buildings):
#             # Load "module.submodule.MyClass"
#             BuildingClass = getattr(importlib.import_module("buildings"), building_class_name)
#             # Instantiate the class (pass arguments to the constructor, if needed)
#             building = BuildingClass(building_id)
#             if len(schematic_info) > 0:
#                 print('schem info', schematic_info)
#                 schematic_file, schematic_dim = random.choice(schematic_info)
#                 building.schematic_file = schematic_file
#                 print('schem dim', schematic_dim)
#                 building.dim = np.array([schematic_dim[0],schematic_dim[1]])
#             buildings.append(building)
#             building_id += 1
#     return buildings

def building_generator(village_spec):
    buildings = []
    building_id = 0
    for building_class_name, building_spec in village_spec.building_specs.items():
        for _ in range(building_spec.num_buildings):
            # Load "module.submodule.MyClass"
            BuildingClass = getattr(importlib.import_module("buildings"), building_class_name)
            # Instantiate the class (pass arguments to the constructor, if needed)
            building = BuildingClass(building_id)

            schematic_file, schematic_dim, schematic_y_offset = building_spec.sample()
            if schematic_file is not None:
                building.schematic_file = schematic_file
                building.dim = np.array([schematic_dim[0],schematic_dim[1]])
                building.y_offset = schematic_y_offset
            buildings.append(building)
            building_id += 1
    return buildings

def normalize_vector(vector, only_greater_than=False):
    distance = np.linalg.norm(vector)
    if distance != 0:
        if not only_greater_than or distance > 1:
            return vector / distance
    return vector

class Building(object):
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.building_type = ""
        self.schematic_file = ""
        self.position = np.array([0,0])
        self.dim = np.array([0,0])
        self.social_agents = []
        self.knn = 0
        self.attraction = np.inf
        self.repulsion = max(self.dim) # TODO: Pass in dim? Because nothing should collide
        self.placed = False
        self.connected = False
        self.place_probability = .5

    def indices_array_generic(self,m,n):
        r0 = np.arange(m) # Or r0,r1 = np.ogrid[:m,:n], out[:,:,0] = r0
        r1 = np.arange(n)
        out = np.empty((m,n,2),dtype=int)
        out[:,:,0] = r0[:,None]
        out[:,:,1] = r1
        return out

    def get_footprint(self):
        indices = self.indices_array_generic(self.dim[0], self.dim[1])
        footprint = indices + self.position
        return footprint


    def get_valid_displacement(self, position, z, x):
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
        return np.round([new_z, new_x]).astype(int)

    def set_position(self, position, z, x):
        self.position = self.get_valid_displacement(position, z, x)

    def get_noise(self, scale=1):
        noise_vector = np.array([random.uniform(-1,1), random.uniform(-1,1)])
        noise_vector = noise_vector / np.linalg.norm(noise_vector)
        return noise_vector * scale

    def get_interest(self, village_skeleton, terrain):
        return normalize_vector(repel_collision(terrain, village_skeleton, self), True) * 5

    def random_stop(self):
        if random.random() < self.place_probability:
            self.placed = True



class Rural(Building):
    def __init__(self, id, type):
        super(Rural, self).__init__(id, type)
        self.building_type = "rural"


class Residential(Building):
    def __init__(self, id, type):
        super(Residential, self).__init__(id, type)
        self.building_type = "residential"


class Commercial(Building):
    def __init__(self, id, type):
        super(Commercial, self).__init__(id, type)
        self.building_type = "commercial"


class Public(Building):
    def __init__(self, id, type):
        super(Public, self).__init__(id, type)
        self.building_type = "public"


class Aesthetic(Building):
    def __init__(self, id, type):
        super(Aesthetic, self).__init__(id, type)
        self.building_type = "aesthetic"



class House(Residential):
    def __init__(self, id):
        super(House, self).__init__(id, "house")
        self.dim = np.array([7,10])
        self.social_agents = ["house"]
        self.knn = 10
        self.attraction = 40
        self.repulsion = 10

    def get_interest(self, village_skeleton, terrain):
        residential_vector = super(House, self).get_interest(village_skeleton, terrain)
        social_vector = sociability(terrain, village_skeleton, self)
        slope_vector = slope(terrain, village_skeleton, self)

        return normalize_vector(social_vector, True) * 5 + normalize_vector(slope_vector, True) * 2 + residential_vector

class Farm(Rural):
    def __init__(self, id):
        super(Farm, self).__init__(id, "farm")
        self.dim = np.array([10,10])
        self.social_agents = ["farm"]
        self.knn = 4
        self.attraction = 20
        self.repulsion = 10

    def get_interest(self, village_skeleton, terrain):
        rural_vector = super(Farm, self).get_interest(village_skeleton, terrain)
        social_vector = sociability(terrain, village_skeleton, self)
        slope_vector = slope(terrain, village_skeleton, self)
        return normalize_vector(social_vector, True) * 2 + normalize_vector(slope_vector, True) * 2 + rural_vector

class Church(Public):
    def __init__(self, id):
        super(Church, self).__init__(id, "church")
        self.dim = np.array([40,40])
        self.influence_radius = 200
        self.knn = 30
        self.attraction = 300
        self.repulsion = max(self.dim) + 30
        self.social_agents = ["house"]

    def get_interest(self, village_skeleton, terrain):
        public_vector = super(Church, self).get_interest(village_skeleton, terrain)
        domination_vector = geographic_domination(terrain, village_skeleton, self)
        social_vector = sociability(terrain, village_skeleton, self)
        return normalize_vector(domination_vector, True) * 5 + normalize_vector(social_vector, True) * 2 + public_vector

class Store(Commercial):
    def __init__(self, id):
        super(Store, self).__init__(id, "store")
        self.dim = np.array([18, 18])
        self.centroid_types = ["house"]
        self.centroid_knn = 7

    def get_interest(self, village_skeleton, terrain):
        commercial_vector = super(Store, self).get_interest(village_skeleton, terrain)
        centroid_vector = knn_centroid(terrain, village_skeleton, self)
        return normalize_vector(centroid_vector, True) * 5 + commercial_vector

