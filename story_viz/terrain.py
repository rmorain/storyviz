import numpy as np

class Terrain:
    def __init__(self):
        self.elevation = None
        self.material = None

    def load_map(self, level, box):
        self.elevation = np.zeros((box.length, box.width))
        self.material = np.zeros((box.length, box.width))
        for z in range(box.minz, box.maxz):
            for x in range(box.minx, box.maxx):
                for y in range(box.maxy, box.miny, -1):
                    material_id = level.blockAt(x, y, z)
                    if material_id != 0: #If it isn't air
                        self.elevation[z-box.minz][x-box.minx] = y - box.miny
                        self.material[z-box.minz][x-box.minx] = material_id
                        break

    # Initialize a material distance layer
    # Pass in int for material you want to get distance from at each point
    def init_material_dist(material):
        x, y = self.material.shape  # Get dimensions of material terrain
        material_dist_layer = np.zeros((x, y), np.inf)   # Initialize to all inf
        return None # TODO more

    # TODO
    def update_material_dist():
        return None  

    


