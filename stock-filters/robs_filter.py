import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *
import os

import utilityFunctions as utilityFunctions

inputs = (
	("Rob's Filter", "label"),
	("Material", alphaMaterials.Cobblestone), # the material we want to use to build the mass of the structures
	("Creator: Robert Morain", "label"),
	)

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def perform(level, box, options):
	print('making library')
	f = get_immediate_subdirectories(os.getcwd())
	print(f)
	sourceSchematic = MCSchematic(filename="stock-schematics/library/Indrae_Library.schematic")
	print('here')
	newBox = BoundingBox((0,0,0),(sourceSchematic.Width,sourceSchematic.Height,sourceSchematic.Length))
	b=range(4096)
	b.remove(0) # @CodeWarrior0 and @Wout12345 explained how to merge schematics			
	level.copyBlocksFrom(sourceSchematic, newBox, (box.minx, box.miny, box.minz ),b)
	level.markDirtyBox(box)