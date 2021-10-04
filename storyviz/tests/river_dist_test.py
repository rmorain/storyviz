import os
import sys
import numpy as np

sys.path.append(os.getcwd() + '/..')

from terrain import Terrain

t = Terrain()
t.generate_terrain()

assert not np.all(t.layers['material']==0), "No water"

t.layers['water_dist'] = t.init_material_dist(t.materials['water'])

assert not np.all(t.layers['water_dist']==np.inf), "Not initialized correctly"

t.layers['water_dist'] = t.update_material_dist(t.layers['water_dist'], t.materials['water'])

assert np.all(t.layers['water_dist'] != np.inf), "Water distances has infinity"


