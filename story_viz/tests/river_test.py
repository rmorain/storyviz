import os
import sys
import numpy as np

sys.path.append(os.getcwd() + '/..')

from terrain import Terrain

t = Terrain()
print(t.materials)
assert not np.all(t.layers['material']==0), "No water"
