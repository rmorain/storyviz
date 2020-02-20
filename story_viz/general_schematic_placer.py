"""
Places general StorySchematic object in environment.
Returns 2D grid of placements. 
"""

import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *

import utilityFunctions as utilityFunctions
import numpy as np
from classes import StorySchematics

class GeneralSchematicPlacer:
    def __init__(self):
        pass

    def place(self, level, box, options, schematics, land_allocation_grid):
        #land_allocation_grid = np.zeros((box.width, box.length))
        #self.get_village_grid(land_allocation_grid, level, box)
        s = StorySchematics(['house'], ['small-convenient-house'])
        schematics = s.get_schematics()
        yards = self.get_yards(land_allocation_grid, level, box)
        for yard in yards:
            buildFence(level, yard)
            buildRoads(level, yard)
            #m.copyBlocksFrom(schematics['house'], level, yard, )
            source_box = BoundingBox((0,0,0), (schematics['house'].Width,schematics['house'].Height,schematics['house'].Length))
            level.copyBlocksFrom(schematics['house'], source_box, (yard.minx+2, yard.miny-5, yard.minz+2))
            # TODO: We are using yard.miny-5 because some schematics come with their own grass which way have to deal with.


    def get_yards(self, land_allocation_grid, level, box):
        yard_boxes = []
        house_size = (20, 20)
        max_length, max_width = land_allocation_grid.shape
        for length in range(max_length // house_size[0]):
            for width in range(max_width//house_size[1]):
                yard = land_allocation_grid[length * house_size[0]:length * house_size[0] + house_size[0],
                                            width * house_size[1]:width * house_size[1] + house_size[1]]
                if not np.any(yard!=0):
                    yard_box = BoundingBox((box.minx+width*house_size[1], box.miny, box.minz+length*house_size[0]),
                                           (house_size[1], box.maxy, house_size[0]))
                    yard_boxes.append(yard_box)
                land_allocation_grid[width*house_size[0], length*house_size[1]] = 1
        return yard_boxes

# builds a wooden fence around the perimeter of this box, like this photo
#			  Top - zmax
#       ----------------
#       |              |
#       |              |
#       |              |
# Left  |              | Right
# xmin  |              | xmax
#       |              |
#       |              |
#       ----------------
#			Bottom - zmin
def buildRoads(level, box):
    for x in range(box.minx, box.maxx):
        utilityFunctions.setBlock(level, (1, 0), x, box.miny, box.maxz)
        utilityFunctions.setBlock(level, (1, 0), x, box.miny, box.minz)
    for z in range(box.minz, box.maxz):
        utilityFunctions.setBlock(level, (1, 0), box.maxx, box.miny, z)
        utilityFunctions.setBlock(level, (1, 0), box.minx, box.miny, z)

def buildFence(level, box):

    # side by side, go row/column by row/column, and move down the pillar in the y axis starting from the top
    # look for the first non-air tile (id != 0). The tile above this will be a fence tile

    for x in range(box.minx+1, box.maxx-1):
        utilityFunctions.setBlock(level, (85, 0), x, box.miny+1, box.maxz-1)
        utilityFunctions.setBlock(level, (85, 0), x, box.miny+1, box.minz+1)
    for z in range(box.minz+1, box.maxz-1):
        utilityFunctions.setBlock(level, (85, 0), box.maxx-1, box.miny + 1, z)
        utilityFunctions.setBlock(level, (85, 0), box.minx+1, box.miny + 1, z)

