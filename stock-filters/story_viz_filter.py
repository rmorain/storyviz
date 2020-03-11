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
from maps_builder import build_in_minecraft

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

    s = StorySchematics(['House', 'Church', 'Farm'], ['small-convenient-house', 'evil-church', 'farm-wheat'])
    schematics = s.get_schematics()
    village_skeleton, terrain = create_minecraft_village(level, box, schematics)
    build_in_minecraft(level, box, terrain, village_skeleton)
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