import numpy as np
import random

def get_line_expansion(start_point, end_point, width_offset):
    dz = abs(start_point[0] - end_point[0])
    dx = abs(start_point[0] - end_point[0])
    offsets = range(-width_offset, width_offset + 1)
    if dz > dx:
        return [(0, x) for x in offsets]
    else:
        return [(z, 0) for z in offsets]

def expand_line(points, width_offset, start_point, end_point, box_length, box_width):
    expanded_points = set(points)
    if width_offset > 0:
        road_expansion = get_line_expansion(start_point, end_point, width_offset)
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