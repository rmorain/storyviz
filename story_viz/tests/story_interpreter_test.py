import os
import sys

sys.path.append(os.getcwd() + '/..')
print(sys.path)

from story_interpreter import StoryInterpreter

s = StoryInterpreter()

story = "On a farm there was a house when out of nowhere a ufo abducted the cow"

print(s.get_keywords(story))