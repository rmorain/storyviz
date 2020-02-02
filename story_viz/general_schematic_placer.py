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

class GeneralSchematicPlacer:
    def __init__(self):
        pass

    def place(self, level, box, options, schematics, land_allocation_grid):
        print(box)
        land_allocation_grid = np.zeros((box.width, box.length))
        self.get_village_grid(land_allocation_grid, level, box)

        pass

    def get_village_grid(self, land_allocation_grid, level, box):
        yard_boxes = []
        house_size = (10, 10)
        max_width, max_length = land_allocation_grid.shape
        for width in range(max_width//house_size[0]):
            for length in range(max_length//house_size[1]):
                yard = land_allocation_grid[width*house_size[0]:width*house_size[0]+house_size[0],
                                            length*house_size[1]:length*house_size[1]+house_size[1]]
                if not np.any(yard==1):
                    yard_box = BoundingBox((box.minx+width*house_size[0], box.miny, box.minz+length*house_size[1]),
                                           (house_size[0], box.maxy, house_size[1]))
                    yard_boxes.append(yard_box)
                land_allocation_grid[width*house_size[0], length*house_size[1]] = 1

        for yard_box in yard_boxes:
            buildFence(level, yard_box)

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
def buildFence(level, box):

    # side by side, go row/column by row/column, and move down the pillar in the y axis starting from the top
    # look for the first non-air tile (id != 0). The tile above this will be a fence tile

    # add top fence blocks
    for x in range(box.minx, box.maxx):
        for z in xrange(box.maxz, box.minz, -1):
                # get this block
                tempBlock = level.blockAt(x, box.miny, box.maxz)
                if tempBlock != 0:
                    newValue = 0
                    utilityFunctions.setBlock(level, (85, newValue), x, box.miny+1, box.maxz)
                    break;
    # add bottom fence blocks (don't double count corner)
    for x in range(box.minx, box.maxx):
        for z in xrange(box.maxz, box.minz, -1):
                # get this block
                tempBlock = level.blockAt(x, box.miny, box.minz)
                if tempBlock != 0:
                    newValue = 0
                    utilityFunctions.setBlock(level, (85, newValue), x, box.miny+1, box.minz)
                    break;
    # add left fence blocks (don't double count corner)
    for z in range(box.minz+1, box.maxz):
        for x in xrange(box.maxx, box.minx, -1):
                # get this block
                tempBlock = level.blockAt(box.minx, box.miny, z)
                if tempBlock != 0:
                    newValue = 0
                    utilityFunctions.setBlock(level, (85, newValue), box.minx, box.miny+1, z)
                    break;
    # add right fence blocks
    for z in range(box.minz, box.maxz+1):
        for x in xrange(box.maxx, box.minx, -1):
                # get this block
                tempBlock = level.blockAt(box.maxx, box.miny, z)
                if tempBlock != 0:
                    newValue = 0
                    utilityFunctions.setBlock(level, (85, newValue), box.maxx, box.miny+1, z)
                    break;
