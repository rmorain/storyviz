"""
Maps keywords provided by story interpreter to specific schematics.
Returns list of StorySchematic objects 
"""

import os
import random
from classes import StorySchematics

class CostumeDresser:
    def __init__(self):
        self.__PATH__TO__SCHEMATICS = "stock-schematics/library/"
        self.__FILE__TYPE = ".schematic"

    def get_schematics(self, keywords):
        schematic_names = os.listdir(self.__PATH__TO__SCHEMATICS)
        found_schematics = []
        for keyword in keywords:
            keyword = keyword.lower()
            # for now, it shuffles the schematic names to add some randomness
            random.shuffle(schematic_names)
            found_schematic = None
            for schem in schematic_names:
                if keyword in schem:
                    # Remove the file ending, since StorySchematics adds it on later
                    found_schematic = schem.replace(self.__FILE__TYPE, "")
                    break
            # What to do if keyword is not found?
            if found_schematic is not None:
                found_schematics.append(found_schematic)
        print('returning schem from CostumeDresser')
        return [StorySchematics(keywords, found_schematics)] # takes in array of labels and array of schematics
