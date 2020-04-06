import random

class VillageSpec:
    def __init__(self):
        self.building_specs = {}

    def add(self, building_class_name, num_buildings):
        b = BuildingSpec(building_class_name, num_buildings)
        self.building_specs[building_class_name] = b

    def get_all_village_schematics(self):
        schematic_files = set()
        for building_class_name, building_spec in self.building_specs.items():
            for schematic_file in building_spec.schematic_files:
                schematic_files.add(schematic_file)
        return list(schematic_files)

class BuildingSpec:
    def __init__(self, building_class_name, num_buildings):
        self.building_class_name = building_class_name
        self.num_buildings = num_buildings
        self.schematic_files = []
        self.schematic_dims = []
        self.schematic_y_offsets = []

    def sample(self):
        if len(self.schematic_files) > 0:
            rand_idx = random.randint(0, len(self.schematic_files)-1)
            print(rand_idx)
            print(self.schematic_files[rand_idx])
            print(self.schematic_dims[rand_idx])
            print(self.schematic_y_offsets[rand_idx])
            return self.schematic_files[rand_idx], self.schematic_dims[rand_idx], self.schematic_y_offsets[rand_idx]
        return None, None, None



