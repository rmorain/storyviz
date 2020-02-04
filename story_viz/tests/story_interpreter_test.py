import os
import sys

sys.path.append(os.getcwd() + '/..')
print(sys.path)

from story_interpreter import StoryInterpreter

s = StoryInterpreter()

story = "Once upon a time, there was a gay little fish named Reed. He was very sad and he lived underwater. Then one day he had a million friends and he was happy. The End."

print(s.get_keywords(story))