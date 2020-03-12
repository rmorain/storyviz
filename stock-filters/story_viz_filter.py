"""
Filter to do story visualization.
"""
import sys
import os
# Add story_viz folder to path

sys.path.append(os.getcwd() + '/story_viz')

print(sys.path)

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *



import utilityFunctions as utilityFunctions
from maps import create_minecraft_village
from village_spec import VillageSpec

# Import files you want
from classes import *
from schematic_manager import SchematicManager
from general_schematic_placer import GeneralSchematicPlacer 
from story_schematic_placer import StorySchematicPlacer


inputs = (
	("Story Viz", "label"),
	("Story", "string"), # the material we want to use to build the mass of the structures
	("Creators: Robert Morain, Jack Demke, Connor Wilhelm", "label"),
	)

def perform(level, box, options):
    story = options['Story']
    if story.isspace() or story is '':
        story = "On a farm in the west there was a house when out of nowhere a hovering ufo abducted the cow"

    # s = StorySchematics(['House', 'Church', 'Farm'], ['small-convenient-house', 'evil-church', 'farm-wheat'])
    # schematics = s.get_schematics()
    building_spec = get_village_spec()
    village_skeleton, terrain = create_minecraft_village(level, box, building_spec)
    build_village_skeleton(level, box, village_skeleton, building_spec.get_all_village_schematics())



    # sch_man = SchematicManager()
    # GSP = GeneralSchematicPlacer()
    # SSP = StorySchematicPlacer()
    # print('before')
    # schematics = sch_man.get_schematics(story)
    # print('got schem')
    # box, land_allocation_grid = SSP.place(level, box, options, schematics)
    # print('finished ssp')
    # GSP.place(level, box, options, schematics, land_allocation_grid)
    # print('finished gps')
    #

def build_village_skeleton(level, box, village_skeleton, schematic_files):
    schematics = StorySchematics(schematic_files, schematic_files).get_schematics()
    for building in village_skeleton:
        z, x = building.position[0], building.position[1]
        schematic = schematics[building.schematic_file]
        source_box = BoundingBox((0, 0, 0),(schematic.Width, schematic.Height, schematic.Length))
        level.copyBlocksFrom(schematic, source_box, (box.minx+x, box.miny, box.minz+z))

def fill_building_spec_info(village_spec, building_class_name, schematic_files):
    schematic_dims, schematic_y_offsets = get_schematics_info(schematic_files)
    village_spec.building_specs[building_class_name].schematic_files = schematic_files
    village_spec.building_specs[building_class_name].schematic_dims = schematic_dims
    village_spec.building_specs[building_class_name].schematic_y_offsets = schematic_y_offsets

def get_village_spec():
    num_houses = 20
    num_farms = 10
    num_churches = 0
    num_stores = 5

    # building_spec = {'House': [num_houses, {'small-convenient-house': (-1,-1), 'First survival House (copy)': (-1,-1)}],
    #                  'Farm': [num_farms, {'farm-wheat': (-1,-1)}],
    #                  'Church': [num_churches, {'evil-church': (-1,-1)}]}
    village_spec = VillageSpec()
    village_spec.add("House", num_houses)
    village_spec.add("Farm", num_farms)
    village_spec.add("Church", num_churches)

    fill_building_spec_info(village_spec, "House", ['small-convenient-house', 'First survival House (copy)'])
    fill_building_spec_info(village_spec, "Farm", ['farm-wheat'])
    fill_building_spec_info(village_spec, "Church", ['evil-church'])

    return village_spec

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
        schematic_dims.append(array([schematic.Length, schematic.Width]))
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