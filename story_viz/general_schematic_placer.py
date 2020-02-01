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
                print(max_width//house_size[0], max_length//house_size[1])
                print(width, length)
                yard = land_allocation_grid[width*house_size[0]:width*house_size[0]+house_size[0],
                                            length*house_size[1]:length*house_size[1]+house_size[1]]
                if not np.any(yard==1):
                    yard_box = BoundingBox((box.minx+width*house_size[0], box.miny, box.minz+length*house_size[1]),
                                (house_size[0], box.maxy, house_size[1]))
                    buildFence(level, yard_box)
                    yard_boxes.append(yard_box)
                land_allocation_grid[width*house_size[0], length*house_size[1]] = 1
        for yard_box in yard_boxes:
            print('yardbox', yard_box)
        print('box', box)
        #print(land_allocation_grid)

#splits the given box into 4 unequal areas
def binaryPartition(box):
    partitions = []
    # create a queue which holds the next areas to be partitioned
    queue = []
    queue.append(box)
    # for as long as the queue still has boxes to partition...
    count = 0
    while len(queue) > 0:
        count += 1
        splitMe = queue.pop(0)
        (width, height, depth) = utilityFunctions.getBoxSize(splitMe)
        # print "Current partition width,depth",width,depth
        centre = 0
        # this bool lets me know which dimension I will be splitting on. It matters when we create the new outer bound size
        isWidth = False
        # find the larger dimension and divide in half
        # if the larger dimension is < 10, then block this from being partitioned
        minSize = 12
        if width > depth:
            # roll a random die, 1% change we stop anyways
            chance = random.randint(100)

            if depth < minSize or chance == 1:
                partitions.append(splitMe)
                continue

            isWidth = True
            centre = width / 2
        else:
            chance = random.randint(10)
            if width < minSize or chance == 1:
                partitions.append(splitMe)
                continue
            centre = depth / 2

        # a random modifier for binary splitting which is somewhere between 0 and 1/16 the total box side length
        randomPartition = random.randint(0, (centre / 8) + 1)

        # creating the new bound
        newBound = centre + randomPartition

        #creating the outer edge bounds
        outsideNewBounds = 0
        if isWidth:
            outsideNewBound = width - newBound - 1
        else:
            outsideNewBound = depth - newBound - 1

        # creating the bounding boxes
        # NOTE: BoundingBoxes are objects contained within pymclevel and can be instantiated as follows
        # BoundingBox((x,y,z), (sizex, sizey, sizez))
        # in this instance, you specifiy which corner to start, and then the size of the box dimensions
        # this is an if statement to separate out binary partitions by dimension (x and z)
        if isWidth:
            queue.append(BoundingBox((splitMe.minx, splitMe.miny, splitMe.minz), (newBound-1, 256, depth)))
            queue.append(BoundingBox((splitMe.minx + newBound + 1, splitMe.miny, splitMe.minz), (outsideNewBound - 1, 256, depth)))
        else:
            queue.append(BoundingBox((splitMe.minx, splitMe.miny, splitMe.minz), (width, 256, newBound - 1)))
            queue.append(BoundingBox((splitMe.minx, splitMe.miny, splitMe.minz + newBound + 1), (width, 256, outsideNewBound - 1)))
    return partitions

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
        for y in xrange(box.maxy, box.miny, -1):
                # get this block
                tempBlock = level.blockAt(x, y, box.maxz)
                print(x, y, box.maxz)
                print(tempBlock)
                if tempBlock != 0:
                    newValue = 0
                    utilityFunctions.setBlock(level, (85, newValue), x, y+1, box.maxz)
                    break;
    # add bottom fence blocks (don't double count corner)
    for x in range(box.minx, box.maxx):
        for y in xrange(box.maxy, box.miny, -1):
                # get this block
                tempBlock = level.blockAt(x, y, box.minz)
                if tempBlock != 0:
                    newValue = 0
                    utilityFunctions.setBlock(level, (85, newValue), x, y+1, box.minz)
                    break;
    # add left fence blocks (don't double count corner)
    for z in range(box.minz+1, box.maxz):
        for y in xrange(box.maxy, box.miny, -1):
                # get this block
                tempBlock = level.blockAt(box.minx, y, z)
                if tempBlock != 0:
                    newValue = 0
                    utilityFunctions.setBlock(level, (85, newValue), box.minx, y+1, z)
                    break;
    # add right fence blocks
    for z in range(box.minz, box.maxz+1):
        for y in xrange(box.maxy, box.miny, -1):
                # get this block
                tempBlock = level.blockAt(box.maxx, y, z)
                if tempBlock != 0:
                    newValue = 0
                    utilityFunctions.setBlock(level, (85, newValue), box.maxx, y+1, z)
                    break;