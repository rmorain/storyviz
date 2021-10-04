# Generates schematics lists to be used as general schematics

import os
import numpy as np
import json

schems_per_type = {'house':[], 'farm':[], 'church':[], 'store':[]}
schem_keywords = {'house': ['house','home','inn','hotel','apartment'], 'farm':['farm','ranch','plant','garden'], 'church':['church','temple','shrine', 'castle', 'fort', 'fortress', 'capitol', 'hall'], 'store':['store','shop','market', 'bazaar', 'trade', 'bank']}

# returns the relative paths to all schematics individually
def get_schematic_paths():
  schematic_paths = []
  path_to_schematics = 'stock-schematics'
  for dr, _, schematic_names in os.walk(path_to_schematics):
    schematic_paths.extend([os.path.join(dr, schematic_name).replace(path_to_schematics, '') for schematic_name in schematic_names if '.schematic' in schematic_name])
  return schematic_paths

schematics = get_schematic_paths()

for t, schems in schems_per_type.items():
  for schematic in schematics:
    schem_name = schematic.split('\\')[-1].lower()
    is_type = np.any(np.array([kw in schem_name for kw in schem_keywords[t]]))
    if is_type:
      schems.append(schematic.replace('\\','/'))

with open('stock-schematics/general_schematics_list.json', 'w') as f:
  json.dump(schems_per_type, f)