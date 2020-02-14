"""
Places StorySchematic object in environment.
Returns 2D grid of placements. 
Height will be factored in separately
Look up keywords in an ontology database (wordnet?) to find if there is a "natural placement" for the schematic
"""

import random
import numpy as np
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox

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

    def _get_placement(self, level, box, options, schematics, keywords):
        total_width, total_length, max_height = 0,0,0
        print('schematics', schematics)
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
        # schematics are 1-indexed, 0 represents and empty space
        for i, schematic in enumerate(schematics):
            height, width, length = schematic._Blocks.shape
            
            ### ORIGINAL PLACEMENT ###

            # start_x = 0
            # start_z = 0
            # if i != 0:
            #     valid_placement = False
            #     while not valid_placement:
            #         start_x = random.randint(self.spacing, total_width-1-width-self.spacing)
            #         start_z = random.randint(self.spacing, total_length-1-length-self.spacing)
            #         print('startx', start_x)
            #         print('startz', start_z)
            #         print('placements', placements[start_z-self.spacing:start_z+length+self.spacing, start_x-self.spacing:start_x+width+self.spacing]!=0)
            #         valid_placement = np.any(placements[start_z-self.spacing:start_z+length+self.spacing, start_x-self.spacing:start_x+width+self.spacing]!=0)
            
            ### POSITION WORD PLACEMENT ###
            # TODO: Prevent overlap
            keyword_parts = keywords[i]
            pos_word = 'any' if len(keyword_parts) <= 1 else keyword_parts[1]
            y = 0

            # Position terms: above next far north south east west center
            if pos_word == 'above':
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
            # placements[y:y+height, start_z:start_z+length, start_x:start_x+width] = i+1
        return placements

    def place(self, level, box, options, schematics):
        keywords, schematics = self.convert_StorySchematic(schematics) 
        placements = self._get_placement(level, box, options, schematics, keywords)
        # TODO: Find a way to build things in the air
        placements = placements.astype(int)
        placed = [False for _ in schematics]
        for z, row in enumerate(placements):
            for x, val in enumerate(row):
                if val != 0 and not placed[val-1]:
                    make_schematic(level, box, options, schematics[val-1], (x,0,z))
                    placed[val-1] = True
        return placements

    def _expand_placements(self, placement, height, width, length):
        h, w, l = placement.shape
        new_placement = np.zeros((height+h, width+w, length+l))
        new_placement[0:h, 0:w, 0:l] = placement
        return new_placement


def make_schematic(level, box, options, schematic, offset):
	newBox = BoundingBox((0,0,0), (schematic.Width,schematic.Height,schematic.Length))
	b=range(4096)
	b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
	level.copyBlocksFrom(schematic, newBox, (box.minx+offset[0], box.miny+offset[1], box.minz+offset[2]),b)
	level.markDirtyBox(box)
