
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
    def place(self, level, box, options, start_point=None, end_point=None, width=3):
        road_placement = np.zeros((box.length, box.width))
        z, x = road_placement.shape
        if start_point is None or not is_valid_point(start_point, box.length, box.width):
            start_point = (random.randint(0, z-1), 0)
        if end_point is None or not is_valid_point(end_point, box.length, box.width):
            end_point = (random.randint(0, z-1), x-1)

        points = get_grid_cells_btw(start_point, end_point)
        points = connect_neighboring_points(points)
        width_offset = width//2
        points = expand_road(points, width_offset, start_point, end_point, box.length, box.width)
        build_road(level, box, np.zeros((box.length, box.width)), points)
        return road_placement

def is_valid_point(start_point, box_length, box_width):
    z, x = start_point
    if z >= 0 and z < box_length and x >= 0 and x < box_width:
        return True
    return False

def build_road(level, box, road_placement, points):
    for pt in points:
        road_placement[pt] = 1
        utilityFunctions.setBlock(level, (1, 0), box.minx+pt[1], box.miny, box.minz+pt[0])

def get_road_expansion(start_point, end_point, width_offset):
    dz = abs(start_point[0] - end_point[0])
    dx = abs(start_point[0] - end_point[0])
    offsets = range(-width_offset, width_offset + 1)
    if dz > dx:
        return [(0, x) for x in offsets]
    else:
        return [(z, 0) for z in offsets]

def expand_road(points, width_offset, start_point, end_point, box_length, box_width):
    expanded_points = set()
    if width_offset > 0:
        road_expansion = get_road_expansion(start_point, end_point, width_offset)
        for z, x in points:
            for offset in road_expansion:
                if z + offset[0] < box_length and z + offset[0] >= 0:
                    if x + offset[1] < box_width and x + offset[0] >= 0:
                        expanded_points.add((z+offset[0], x+offset[1]))
    return expanded_points

def connect_neighboring_points(points):
    connected_points = []
    for pt_idx in range(len(points)):
        connected_points.append(tuple(points[pt_idx]))
        if pt_idx == len(points) - 1:
            break
        z_i, x_i = points[pt_idx]
        z_j, x_j = points[pt_idx+1]
        dz = z_j - z_i
        dx = x_j - x_i
        if dz != 0 and dx != 0:
            if random.random() > 0.5:
                x_i = x_i + dx
            else:
                z_i = z_i + dz
            connected_points.append((z_i, x_i))
    return connected_points

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