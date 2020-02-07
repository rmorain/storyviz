"""
Maps keywords provided by story interpreter to specific schematics.
Returns list of StorySchematic objects 
"""

import os
import random
import spacy
import numpy as np
from classes import StorySchematics

class CostumeDresser:
    def __init__(self):
        temp = StorySchematics()
        self.__PATH__TO__SCHEMATICS = temp.__PATH__TO__SCHEMATICS
        self.__FILE__TYPE = temp.__FILE__TYPE
        self.schematic_paths = self.get_schematic_paths()
        self.lang_model = spacy.load('en_core_web_md')

    # keywords should be a list of strings, each string will contain a keyword and supporting positional words
    def get_schematics(self, keywords):
        found_schematics = []
        for keyword in keywords:
            keyword = keyword.lower().split()[0]
            kw_token = self.lang_model(keyword)
            # Predict average similarity between keyword and each word in schematics relative path
            schem_scores = np.array([kw_token.similarity(self.lang_model(schem.replace('-', ' ').replace('_', ' ').replace('/', ' ').replace('\\', ' '))) for schem in self.schematic_paths])
            found_schematics.append(self.schematic_paths[np.argmax(schem_scores)])
        print('returning schem from CostumeDresser')
        return [StorySchematics(keywords, found_schematics)] # takes in array of labels and array of schematics

    # returns the relative paths to all schematics individually
    def get_schematic_paths(self):
        schematic_paths = []
        for dr, _, schematic_names in os.walk(self.__PATH__TO__SCHEMATICS):
            schematic_paths.extend([os.path.join(dr, schematic_name).replace(self.__PATH__TO__SCHEMATICS, ' ') for schematic_name in schematic_names])
        return schematic_paths