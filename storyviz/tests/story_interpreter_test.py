
from __future__ import unicode_literals
import os
import sys

sys.path.append(os.getcwd() + '/..')
print(sys.path)

from story_interpreter import StoryInterpreter

s = StoryInterpreter()

# story = "On a farm in the west there was a house when out of nowhere a hovering ufo abducted the cow"
story = "Once upon a time, there was a scary vampire, named Steve. He snuck into the US senate and sucked the blood of a young virgin."
keywords = s.get_keywords(story)

print(keywords)