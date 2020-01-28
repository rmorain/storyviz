from classes import StorySchematics
from pymclevel import MCSchematic

labels = ['farm', 'house', 'ufo']
schematics = ['farm-wheat', 'farm-house', 'flying-saucer-alien']
s = StorySchematics(labels, schematics)

print(s.get_schematics())
