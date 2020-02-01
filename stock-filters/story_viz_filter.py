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
    story = options['Story'] # When we
    if story.isspace() or story is '':
        story = "On a farm there was a house when out of nowhere a ufo abducted the cow"
    sch_man = SchematicManager()
    GSP = GeneralSchematicPlacer()
    SSP = StorySchematicPlacer()
    schematics = sch_man.get_schematics(story)
    land_allocation_grid = SSP.place(level, box, options, schematics)
    GSP.place(level, box, options, schematics, land_allocation_grid)

    # 