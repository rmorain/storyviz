import utilityFunctions as utilityFunctions
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from classes import StorySchematics

def get_schematics():
    return StorySchematics(['house', 'church', 'farm'], ['small-convenient-house', 'evil-church', 'farm-wheat']).get_schematics()

def build_in_minecraft(level, box, terrain, village_skeleton):
    schematics = get_schematics()
    for building in village_skeleton:
        z, x = building.position[0], building.position[1]
        schematic = schematics[building.type]
        source_box = BoundingBox((0, 0, 0),(schematic.Width, schematic.Height, schematic.Length))
        level.copyBlocksFrom(schematic, source_box, (box.minx+x, box.miny, box.minz+z))
