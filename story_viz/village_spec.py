from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
import numpy as np
import utilityFunctions as utilityFunctions
import random

class VillageSpec:
    def __init__(self):
        self.building_specs = {}

    def add(self, building_class_name, num_buildings, schematic_files):
        b = BuildingSpec(building_class_name, num_buildings, schematic_files)
        self.building_specs[building_class_name] = b

    def get_all_village_schematics(self):
        schematic_files = set()
        for building_class_name, building_spec in self.building_specs.items():
            for schematic_file in building_spec.schematic_files:
                schematic_files.add(schematic_file)
        return list(schematic_files)

class BuildingSpec:
    def __init__(self, building_class_name, num_buildings, schematic_files):
        self.building_class_name = building_class_name
        self.num_buildings = num_buildings

        if schematic_files is None:
            self.schematic_files = []
        else:
            self.schematic_files = schematic_files
        self.schematic_dims = []
        self.schematic_y_offsets = []

        if len(self.schematic_files) > 0:
            self.schematic_dims, self.schematic_y_offsets = get_schematics_info(schematic_files)

    def sample(self):
        if len(self.schematic_files) > 0:
            rand_idx = random.randint(0, len(self.schematic_files)-1)
            return self.schematic_files[rand_idx], self.schematic_dims[rand_idx], self.schematic_y_offsets[rand_idx]
        return None, None, None

def get_schematics(schematic_files):
    __PATH__TO__SCHEMATICS = "stock-schematics/library/"
    __FILE__TYPE = ".schematic"
    schematics = []
    for schematic_file in schematic_files:
        schematics.append(MCSchematic(filename=__PATH__TO__SCHEMATICS + schematic_file + __FILE__TYPE))
    return schematics

def get_schematics_info(schematic_files):
    schematics = get_schematics(schematic_files)
    schematic_dims = []
    schematic_y_offsets = []
    for schematic in schematics:
        schematic_dims.append(np.array([schematic.Length, schematic.Width]))
        schematic_y_offsets.append(get_schematic_y_offset(schematic))

    return schematic_dims, schematic_y_offsets

def get_schematic_y_offset(schematic):
    maxz, maxx, maxy = schematic.Length - 1, schematic.Width - 1, schematic.Height - 1

    four_corner_materials = []
    for x in [0, maxx]:
        for z in [0, maxz]:
            corner_material = utilityFunctions.drillDown(schematic, x, z, 0, maxy)
            four_corner_materials.append(corner_material)

    for y, (mat1, mat2, mat3, mat4) in enumerate(zip(*four_corner_materials)):
        if mat1 == mat2 == mat3 == mat4 == 2:  # If the corners are all grass
            return maxy - y

    return 0
    # for y in range(maxy, 0, -1):
    # material_id = schematic.blockAt(x, y, z)

