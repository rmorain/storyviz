"""
Maps keywords provided by story interpreter to specific schematics.
Returns list of StorySchematic objects 
"""

import os
import random
import spacy
import numpy as np
#####################
# from classes import StorySchematics
#####################

class CostumeDresser:
    def __init__(self):
        #####################
        self.__PATH__TO__SCHEMATICS = 'stock-schematics'
        self.__FILE__TYPE = '.schematic'
        #####################
        # temp = StorySchematics()
        # self.__PATH__TO__SCHEMATICS = temp._StorySchematics__PATH__TO__SCHEMATICS
        # self.__FILE__TYPE = temp._StorySchematics__FILE__TYPE
        #####################

        self.schematic_paths = self.get_schematic_paths()
        self.lang_model = spacy.load('en_core_web_sm')
    # keywords should be a list of strings, each string will contain a keyword and supporting positional words
    def get_schematics(self, keywords, topn=1):
        print(keywords)
        # Get schematics from keywords
        found_schematics = []
        normalized_keywords = []
        for keyword in keywords:
            keyword_parts = keyword.lower().split()
            tokens = self.lang_model(unicode(keyword))
            key_i = 0
            for part in tokens:
                if part.pos_ == "NOUN":
                    break
                key_i += 1
            if key_i == len(tokens):
                key_i = 0
            key = keyword_parts[key_i]
            kw_token = self.lang_model(unicode(key))
            # Predict average similarity between keyword and each word in schematics relative path
            schem_scores = np.array([1 if key in schem
                else kw_token.similarity(self.lang_model(unicode(schem.replace('-', ' ').replace('_', ' ').replace('/', ' ').replace('\\', ' ')))) for schem in self.schematic_paths])

            top10 = []
            for i in range(topn):
                top = np.argmax(schem_scores)
                schem_scores[top] = -1
                top10.append(top)
            found_schematics.append(np.random.choice(np.array([self.schematic_paths[top10[i]].replace(self.__FILE__TYPE, '') for i in range(topn)])))
            # found_schematics.append(self.schematic_paths[np.argmax(schem_scores)].replace(self.__FILE__TYPE, ''))
            normalized_keywords.append("{} {}".format(key, self.select_pos_word(keyword)))
        print("Normalized keywords:", normalized_keywords)
        print("Found schematics:", found_schematics)
        #####################
        return normalized_keywords, found_schematics
        # return [StorySchematics(normalized_keywords, found_schematics)] # takes in array of labels and array of schematics
        #####################
    # Returns normalized position word, or the word itself if no similar word exists
    def normalize_pos_word(self, pos_word):
        """
        Normalized Terms
        relative: above, left, right, next, far
        cardinal: north, south, east, west, center
        terrain-relative: high, low, level
        """
        terms = "above next far north south east west center".split()
        pos_word = pos_word.lower()
        pos_token = self.lang_model(unicode(pos_word))
        scores = [pos_token.similarity(self.lang_model(unicode(term))) for term in terms]
        return terms[np.argmax(scores)]
    # Selects a normalized pos word for every schematic. If none are close to normalized pos words, place randomly
    def select_pos_word(self, keyword):
        terms = "above next far north south east west center floating".split()
        scores = [self.lang_model(unicode(t)).similarity(self.lang_model(unicode(keyword))) for t in terms]
        threshold = .1
        top_i = np.argmax(scores)
        return terms[top_i] if scores[top_i] > threshold else "random"
    # returns the relative paths to all schematics individually
    def get_schematic_paths(self):
        schematic_paths = []
        for dr, _, schematic_names in os.walk(self.__PATH__TO__SCHEMATICS):
            schematic_paths.extend([os.path.join(dr, schematic_name).replace(self.__PATH__TO__SCHEMATICS, '') for schematic_name in schematic_names if self.__FILE__TYPE in schematic_name])
        return schematic_paths

if __name__ == '__main__':
    cd = CostumeDresser()
    cd.get_schematics(["cow", "house", "farm in the west", "hovering ufo"], 20)