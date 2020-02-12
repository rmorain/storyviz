
import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *

import utilityFunctions as utilityFunctions
import numpy as np
from classes import StorySchematics
from PIL import Image
import matplotlib.pyplot as plt

class SimpleRoadPlacer:
    def __init__(self):
        pass

    # box.width = x
    # box.length = z
    def place(self, level, box, options):
        road_placement = np.zeros((box.length, box.width))
        z, x = road_placement.shape
        for offset_x in range(x):
            road_placement[z//2][offset_x] = 1
            utilityFunctions.setBlock(level, (1, 0), box.minx+offset_x, box.miny, box.minz+(z//2))
        utilityFunctions.setBlock(level, (1, 0), box.minx, box.miny, box.minz)
        print(road_placement)
        return road_placement
