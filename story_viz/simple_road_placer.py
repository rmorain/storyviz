
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

    def place(self, level, box, options):
        road_placement = np.zeros((box.width, box.length))
        x, y = road_placement.shape
        for i in range(y):
            road_placement[x//2][i] = 1
            utilityFunctions.setBlock(level, (1, 0), box.minx+(x//2), box.miny, box.minz+y)
        return road_placement