
from __future__ import unicode_literals
import os
import sys

sys.path.append(os.getcwd() + '/..')
print(sys.path)

from story_interpreter import StoryInterpreterPositional

s = StoryInterpreterPositional()

story = "On a farm in the west there was a house when out of nowhere a hovering ufo abducted the cow"

keywords = s.get_keywords(story)

print(keywords)