"""
Takes in story and returns necessary schematics to build story
"""

import spacy
import numpy as np
from story_interpreter import StoryInterpreter 
from costume_dresser import CostumeDresser

class SchematicManager:
    def __init__(self):
        self.spacy_model = spacy.load("en_core_web_lg")
        self.story_interp = StoryInterpreter(self.spacy_model)
        self.costume_dress = CostumeDresser(self.spacy_model)

    def get_schematics(self, story, schematic_classes=None):
        keywords = self.story_interp.get_keywords(story)
        print('Keywords: ', keywords)
        schematics_obj = self.costume_dress.get_schematics(self.story_interp.get_keywords(story))
        if schematic_classes is None:
            return schematics_obj

        # Classify the schematics
        schematics = schematics_obj.schematics
        schem_classifications = {c:[] for c in schematic_classes}
        
        for schematic in schematics:
            print(schematic)
            found = False
            # add schematics to correct category
            for c in schematic_classes:
                if c in schematic.lower():
                    schem_classifications[c].append(schematic)
                    found = True
                    break
            if found:
                continue
            # If it hasn't been added yet, find one of the categories to add it to

            schem_token = self.spacy_model(unicode(schematic))
            class_score = [schem_token.similarity(self.spacy_model(unicode(c))) if schem_token.has_vector else 0 for c in schematic_classes]
            schem_classifications[schematic_classes[np.argmax(np.array(class_score))]].append(schematic)
        return schematics_obj, schem_classifications
