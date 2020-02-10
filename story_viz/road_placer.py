
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

class RoadPlacer:
    def __init__(self):
        pass

    def place(self, level, box, options):
        only_main_roads = True
        if only_main_roads:
            road = np.array(Image.open('story_viz/procedural_road/mycity.png').convert('L').resize((144,192)))
            road = road == 0
            for x_offset, row in enumerate(road):
                for z_offset, block in enumerate(row):
                    if block == 1:
                        utilityFunctions.setBlock(level, (1, 0), box.minx+x_offset, box.miny, box.minz+z_offset)
