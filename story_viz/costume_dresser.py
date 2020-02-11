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
    def __init__(self, path):
        self.__PATH__TO__SCHEMATICS = temp.__PATH__TO__SCHEMATICS
        self.__FILE__TYPE = temp.__FILE__TYPE
        self.schematic_paths = self.get_schematic_paths()
        self.lang_model = spacy.load('en_core_web_md')
    # keywords should be a list of strings, each string will contain a keyword and supporting positional words
    def get_schematics(self, keywords):
        # Get schematics from keywords
        found_schematics = []
        normalized_keywords = []
        for keyword in keywords:
            keyword_parts = keyword.lower().split()
            keyword = keyword_parts[0]
            kw_token = self.lang_model(keyword)
            # Predict average similarity between keyword and each word in schematics relative path
            schem_scores = np.array([kw_token.similarity(self.lang_model(schem.replace('-', ' ').replace('_', ' ').replace('/', ' ').replace('\\', ' '))) for schem in self.schematic_paths])
            found_schematics.append(self.schematic_paths[np.argmax(schem_scores)])
            # Normalize later keywords to known positional info
            if len(keyword_parts) > 1:
                for i,kw in enumerate(keyword_parts[1:]):
                    norm = self.normalize_pos_word(kw)
                    keyword_parts[i+1] = norm
            normalized_keywords.append(keyword_parts)
        return [StorySchematics(keywords, found_schematics)] # takes in array of labels and array of schematics
    # Returns normalized position word, or the word itself if no similar word exists
    def normalize_pos_word(self, pos_word):
        """
        Normalized Terms
        relative: above, left, right, next, far
        cardinal: north, south, east, west
        terrain-relative: high, low, level
        """
        terms = "above left right next far across north south east west high low".split()
        pos_word = pos_word.lower()
        pos_token = self.lang_model(pos_word)
        scores = [pos_token.similarity(self.lang_model(term)) for term in terms]
        return terms[np.argmax(scores)]
    # returns the relative paths to all schematics individually
    def get_schematic_paths(self):
        schematic_paths = []
        for dr, _, schematic_names in os.walk(self.__PATH__TO__SCHEMATICS):
            schematic_paths.extend([os.path.join(dr, schematic_name).replace(self.__PATH__TO__SCHEMATICS, ' ') for schematic_name in schematic_names])
        return schematic_paths