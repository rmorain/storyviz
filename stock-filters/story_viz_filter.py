"""
Filter to do story visualization.
"""
import sys
import os
import json
# Add story_viz folder to path

sys.path.append(os.getcwd() + '/story_viz')

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
import classes
from schematic_manager import SchematicManager
from general_schematic_placer import GeneralSchematicPlacer 
from story_schematic_placer import StorySchematicPlacer


inputs = (
	("Story Viz", "label"),
	("Story", "string"), # the material we want to use to build the mass of the structures
	("Creators: Robert Morain, Jack Demke, Connor Wilhelm", "label"),
	)

# Gets the levels z,x dim, but keeps box y dim.
def expand_box_to_level(level, box):
    level_box = level.bounds
    x = level_box.maxx - level_box.minx
    y = level_box.maxy - box.miny
    z = level_box.maxz - level_box.minz
    return BoundingBox((level_box.minx, box.miny, level_box.minz), (x, y, z))

def perform(level, box, options):
    story = options['Story']
    if story.isspace() or story is '':
        story = "On a farm in the west there was a house when out of nowhere a hovering ufo abducted the cow"

    box = expand_box_to_level(level, box)

    schematic_begin = time.time()
    sch_man = SchematicManager()
    schematics, class_schem = sch_man.get_schematics(story, ['house', 'farm', 'church', 'store'])
    print("schematics:",schematics)
    print("classified schematics:",class_schem)
    print("Found story schematics in {} seconds".format(time.time()-schematic_begin))

    village_spec = get_village_spec(class_schem)
    village_skeleton, terrain = create_minecraft_village(level, box, village_spec, animate=False)
    build_road(level, box, terrain)
    build_village_skeleton(level, box, village_skeleton, terrain, village_spec.get_all_village_schematics())


def build_village_skeleton(level, box, village_skeleton, terrain, schematic_files):
    elevation = terrain.layers['elevation']
    schematics = classes.StorySchematics(schematic_files, schematic_files).get_schematics()
    for building in village_skeleton:
        z, x = building.position[0], building.position[1]
        elevation_offset = elevation[z][x]
        schematic = schematics[building.schematic_file]
        source_box = BoundingBox((0, 0, 0),(schematic.Width, schematic.Height, schematic.Length))
        level.copyBlocksFrom(schematic, source_box, (box.minx+x, box.miny - building.y_offset + elevation_offset, box.minz+z))

def build_road(level, box, terrain):
    points = terrain.material_points['road']
    for point in points:
        z, x = point[0], point[1]
        y = terrain.layers['elevation'][z][x]
        utilityFunctions.setBlock(level, (1, 0), box.minx+x, box.miny+y, box.minz + z)

def fill_building_spec_info(village_spec, building_class_name, schematic_files):
    schematic_dims, schematic_y_offsets = get_schematics_info(schematic_files)
    village_spec.building_specs[building_class_name].schematic_files = schematic_files
    village_spec.building_specs[building_class_name].schematic_dims = schematic_dims
    village_spec.building_specs[building_class_name].schematic_y_offsets = schematic_y_offsets

def get_minmax_buildings(village_size):
    if village_size == 'small':
        minmax_houses = (5, 10)
        minmax_farms = (5,10)
        minmax_churches = (0,1)
        minmax_stores = (0,1)

    elif village_size == 'medium':
        minmax_houses = (10, 15)
        minmax_farms = (10,15)
        minmax_churches = (0,1)
        minmax_stores = (1,2)
    else:
        minmax_houses = (15, 25)
        minmax_farms = (10,15)
        minmax_churches = (1,2)
        minmax_stores = (2,4)
    return minmax_houses, minmax_farms, minmax_churches, minmax_stores

def get_num_buildings(village_size):
    minmax_buildings = get_minmax_buildings(village_size)
    return tuple(random.randint(minmax_building[0], minmax_building[1]) for minmax_building in minmax_buildings)

# TODO: Use each story schematic ONCE and then randomly sample from general schematics for the rest
def get_village_spec(story_schematics):
    village_sizes = ["small", "medium", "big"]
    num_houses, num_farms, num_churches, num_stores = get_num_buildings(village_size=random.choice(village_sizes))

    village_spec = VillageSpec()
    general_schematics = load_general_schematics()

    village_spec.add("House", num_houses)
    house_schems = story_schematics['house']
    if len(house_schems) < num_houses:
        house_schems.extend(random.choice(general_schematics['house'], num_houses - len(house_schems)))
    fill_building_spec_info(village_spec, "House", house_schems)

    village_spec.add("Farm", num_farms)
    farm_schems = story_schematics['farm']    
    if len(farm_schems) < num_farms:
        farm_schems.extend(random.choice(general_schematics['farm'], num_farms - len(farm_schems)))
    fill_building_spec_info(village_spec, "Farm", farm_schems)

    village_spec.add("Church", num_churches)
    church_schems = story_schematics['church']    
    if len(church_schems) < num_churches:
        church_schems.extend(random.choice(general_schematics['church'], num_churches - len(church_schems)))
    fill_building_spec_info(village_spec, "Church", church_schems)
    
    village_spec.add("Store", num_stores)
    store_schems = story_schematics['store']

    if len(store_schems) < num_stores:
        store_schems.extend(random.choice(general_schematics['store'], num_stores - len(store_schems)))
    fill_building_spec_info(village_spec, "Store", store_schems)
    return village_spec

def get_schematics(schematic_files):
    temp = classes.StorySchematics()
    __PATH__TO__SCHEMATICS = temp._StorySchematics__PATH__TO__SCHEMATICS
    __FILE__TYPE = temp._StorySchematics__FILE__TYPE
    schematics = []
    for i,schematic_file in enumerate(schematic_files):
        path = __PATH__TO__SCHEMATICS + schematic_file + __FILE__TYPE
        path = path.replace('//', '/').replace('.schematic.schematic', '.schematic')
        try:
            schematics.append(MCSchematic(filename=path))
        except:
            print("\n{} IS NOT VALID\n".format(path))
            # If that schematic isn't valid, just throw in a generic stand-in
            schematics.append(MCSchematic(filename='stock-schematics/library/small-convenient-house.schematic'))
            schematic_files[i] = 'library/small-convenient-house.schematic'
    return schematics

def get_schematics_info(schematic_files):
    schematics = get_schematics(schematic_files)
    schematic_dims = []
    schematic_y_offsets = []
    for i, schematic in enumerate(schematics):
        if schematic.Length < 100 or schematic.Width < 100:
            schematic_dims.append(array([schematic.Length, schematic.Width]))
            schematic_y_offsets.append(get_schematic_y_offset(schematic))
        else:
            # Ensure that the schematic_files match the dims and y_offsets
            print("SCHEMATIC",schematic_files[i],"TOO LARGE")
            schematic_files.pop(i)

    print("FILES:", schematic_files)
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

def load_general_schematics():
    with open("stock-schematics/general_schematics_list.json") as j:
        general_schematics = json.load(j)
    return general_schematics