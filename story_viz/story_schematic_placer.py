"""
Places StorySchematic object in environment.
Returns 2D grid of placements. 
Height will be factored in separately
"""

import random
import numpy as np

class StorySchematicPlacer:
    def __init__(self, spacing=5):
        self.spacing = spacing # distance between each schematic
        
    def _get_placement(self, level, box, options, schematics):
        total_width, total_length = 0,0
        for schematic in schematics:
            height, width, length = schematic._Blocks.shape
            total_width += width + self.spacing
            total_length += length + self.spacing
        placements = np.zeros((total_length, total_width))
        # always place the first schematic in the center
        # schematics are 1-indexed, 0 represents and empty space
        for i, schematic in enumerate(schematics):
            height, width, length = schematic._Blocks.shape
            start_x = 0
            start_z = 0
            if i != 0:
                valid_placement = False
                while not valid_placement:
                    start_x = random.randint(self.spacing, total_width-1-width-self.spacing)
                    start_z = random.randint(self.spacing, total_length-1-length-self.spacing)
                    valid_placement = np.all(placements[start_z-self.spacing:start_z+length+self.spacing, start_x-self.spacing:start_x+width+self.spacing]==0)
            placements[start_z:start_z+length, start_x:start_x+width] = i+1
        return placements

    def place(self, level, box, options, schematics):
        placements = self._get_placement(level, box, options, schematics)
        placed = [False for _ in schematics]
        for z, row in enumerate(placements):
            for x, val in enumerate(row):
                if val != 0 and not placed[val-1]:
                   make_schematic(level, box, options, schematics[val-1], (x,0,z))
                   placed[val-1] = True
        return placements

def make_schematic(level, box, options, schematic, offset):
	newBox = BoundingBox((0,0,0), (schematic.Width,schematic.Height,schematic.Length))
	b=range(4096)
	b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
	level.copyBlocksFrom(schematic, newBox, (box.minx+offset[0], box.miny+offset[1], box.minz+offset[2]),b)
	level.markDirtyBox(box)
