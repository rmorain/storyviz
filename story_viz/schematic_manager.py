"""
Takes in story and returns necessary schematics to build story
"""



from story_interpreter import StoryInterpreter 
from costume_dresser import CostumeDresser

class SchematicManager:
    def __init__(self):
        self.story_interp = StoryInterpreter()
	self.costume_dress = CostumeDresser()

    def get_schematics(self, story):
        return self.costume_dress.get_schematics(self.story_interp.get_keywords(story))
