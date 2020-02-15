
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
import random

class SimpleRoadPlacer:
    def __init__(self):
        pass

    # box.width = x
    # box.length = z
    def place(self, level, box, options):
        road_placement = np.zeros((box.length, box.width))
        z, x = road_placement.shape
        start_point = (random.randint(0, z-1), 0)
        end_point = (random.randint(0, z-1), x-1)
        # for offset_x in range(x):
        #     road_placement[z//2][offset_x] = 1
        #     utilityFunctions.setBlock(level, (1, 0), box.minx+offset_x, box.miny, box.minz+(z//2))
        # utilityFunctions.setBlock(level, (1, 0), box.minx, box.miny, box.minz)
        points = get_grid_cells_btw(start_point, end_point)
        print(road_placement.shape)
        print(start_point, end_point)

        for pt_idx in range(len(points)):
            pt = tuple(points[pt_idx])
            print(pt)
            road_placement[pt] = 1
            connect_neighboring_points(road_placement, points, pt_idx)
        print(road_placement)
        return road_placement

def connect_neighboring_points(road_placement, points, pt_idx):
    if pt_idx == len(points)-1:
        return
    z_i, x_i = points[pt_idx]
    z_j, x_j = points[pt_idx+1]
    dz = z_j - z_i
    dx = x_j - x_i
    if dz != 0 and dx != 0:
        if random.random() > 0.5:
            road_placement[z_i][x_i+1] = 1
        else:
            road_placement[z_i+1][x_i] = 1

def remove_np_duplicates(data):
  # Perform lex sort and get sorted data
  sorted_idx = np.lexsort(data.T)
  sorted_data =  data[sorted_idx,:]

  # Get unique row mask
  row_mask = np.append([True],np.any(np.diff(sorted_data,axis=0),1))

  # Get unique rows
  out = sorted_data[row_mask]
  return out

def get_grid_cells_btw(p1,p2):
  x1,y1 = p1
  x2,y2 = p2
  dx = x2-x1
  dy = y2-y1

  if dx == 0: # will divide by dx later, this will cause err. Catch this case up here
    step = np.sign(dy)
    ys = np.arange(0,dy+step,step)
    xs = np.repeat(x1, ys.shape[0])
  else:
    m = dy/(dx+0.0)
    b = y1 - m * x1

    step = 1.0/(max(abs(dx),abs(dy)))
    xs = np.arange(x1, x2, step * np.sign(x2-x1))
    ys = xs * m + b

  xs = np.rint(xs)
  ys = np.rint(ys)
  pts = np.column_stack((xs,ys))
  pts = remove_np_duplicates(pts)

  return pts.astype(int)