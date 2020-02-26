"""
Places StorySchematic object in environment.
Returns 2D grid of placements. 
Height will be factored in separately
Look up keywords in an ontology database (wordnet?) to find if there is a "natural placement" for the schematic
"""

import random
import numpy as np
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
import matplotlib.pyplot as plt

class StorySchematicPlacer:
    def __init__(self, spacing=5, height_spacing=15):
        self.spacing = spacing # distance between each schematic
        self.height_spacing = height_spacing # distance between schematic placed in air and max height

    def convert_StorySchematic(self, StorySchematics):
        schematics = []
        keywords = []
        for StorySchematic in StorySchematics:
            schematics_dict = StorySchematic.get_schematics()
            for key, schematic in schematics_dict.items():
                keywords.append(key)
                schematics.append(schematic)
        return keywords, schematics

    def _expand_box(self, level, box, placements):
        z, x = placements.shape
        origin_x, origin_y, origin_z = box.origin
        level_box = level.bounds
        offset_x = level_box.maxx - (origin_x + x)
        offset_z = level_box.maxz - (origin_z + z)
        if offset_z < 0 and offset_x < 0:
            new_z = origin_z
            new_x = origin_x
            if offset_z < 0:
                new_z += offset_z - 1
            if offset_x < 0:
                new_x += offset_x - 1
            return BoundingBox((new_x, origin_y, new_z), (x, box.maxy, z))
        return box

    def _get_placement(self, level, box, options, schematics, keywords):
        total_width, total_length, max_height = 0,0,0
        for schematic in schematics:
            height, width, length = schematic._Blocks.shape
            total_width += width + self.spacing
            total_length += length + self.spacing
            max_height = max(height, max_height)
        # total_width, total_length = box.width, box.length
        total_height = max_height + self.height_spacing

        #TODO: Handle potential infinite loop if box isn't big enough
        # The following line ensures all placements must be within the selection box
        # placements = np.zeros((total_height, total_length, total_width))
        placements = np.zeros((total_length, total_width))
        schematic_heights = np.zeros(len(schematics))
        # schematics are 1-indexed, 0 represents and empty space
        for i, schematic in enumerate(schematics):
            height, length, width = schematic._Blocks.shape # y,z,x = _Blocks.shape
 
            # TODO: Prevent overlap
            keyword_parts = keywords[i].split()
            pos_word = 'any' if len(keyword_parts) <= 1 else keyword_parts[1]
            y = 0

            # Position terms: above next far north south east west center
            if pos_word == 'above' or pos_word=='floating':
                # TODO: Add a way to build something in the air
                start_x = random.randint(0, total_width-width-1)
                start_z = random.randint(0, total_length-length-1)
                y = total_height - height - 1
            # elif pos_word == 'next':
            #     # TODO: To what?
            #     pass
            # elif pos_word == 'far':
            #     # TODO: From what?
            #     pass
            # TODO: Add relative functionality
            elif pos_word == 'north':
                start_z = random.randint(0, 10)
                start_x = random.randint(0, total_width-width-1)
            elif pos_word == 'south':
                start_z = random.randint(total_length-length-1, total_length-length-11)
                start_x = random.randint(0, total_width-width-1)
            elif pos_word == 'east':
                start_x = random.randint(total_width-width-1, total_width-width-11)
                start_z = random.randint(0, total_length-length-1)
            elif pos_word == 'west':
                start_x = random.randint(0, 10)
                start_z = random.randint(0, total_length-length-1)
            elif pos_word == 'center':
                quarter_width = total_width//4
                quarter_length = total_length//4
                start_x = random.randint(quarter_width, total_width-quarter_width)
                start_z = random.randint(quarter_length, total_length-quarter_length)
            else: # pos_word == 'any', and any others not used
                start_x = random.randint(0, total_width-width-1)
                start_z = random.randint(0, total_length-length-1)
                
            placements[start_z:start_z+length, start_x:start_x+width] = i+1
            schematic_heights[i] = y
            # placements[y:y+height, start_z:start_z+length, start_x:start_x+width] = i+1
        return placements, schematic_heights

    def place(self, level, box, options, schematics):
        keywords, schematics = self.convert_StorySchematic(schematics) 
        placements, schematic_heights = self._get_placement(level, box, options, schematics, keywords)
        box = self._expand_box(level, box, placements)
        # TODO: Find a way to build things in the air
        placements = placements.astype(int)
        placed = [False for _ in schematics]
        for z, row in enumerate(placements):
            for x, val in enumerate(row):
                if val != 0 and not placed[val-1]:
                    make_schematic(level, box, options, schematics[val-1], (x,schematic_heights[val-1],z))
                    placed[val-1] = True

        # plt.imshow(np.flipud(np.fliplr(placements)), cmap='hot', interpolation='nearest')
        # plt.show()

        return box, placements

    def _expand_placements(self, placement, height, width, length):
        h, w, l = placement.shape
        new_placement = np.zeros((height+h, width+w, length+l))
        new_placement[0:h, 0:w, 0:l] = placement
        return new_placement


def make_schematic(level, box, options, schematic, offset):
	# newBox = BoundingBox((0,0,0), (schematic.Width,schematic.Height,schematic.Length))
	# b=range(4096)
	# b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics
	# level.copyBlocksFrom(schematic, newBox, (box.minx+offset[0], box.miny+offset[1], box.minz+offset[2]),b)
	# level.markDirtyBox(box)

    print('Schematic size', (schematic.Width, schematic.Height, schematic.Length))

    source_box = BoundingBox((0, 0, 0), (schematic.Width, schematic.Height, schematic.Length))
    level.copyBlocksFrom(schematic, source_box, (box.minx + offset[0], box.miny + offset[1], box.minz + offset[2]))
