import random
import numpy as np

def find_buildings_within_bbox(village_skeleton, bounding_box):
    valid_buildings = []
    for building in village_skeleton:
        if bounding_box[0][0] <= building.position[0] <= bounding_box[1][0]:
            if bounding_box[0][1] <= building.position[1] <= bounding_box[1][1]:
                valid_buildings.append(building)
    return valid_buildings

def find_buildings_within_extent(village_skeleton, location, extent):
    min_z, max_z = location[0] - extent[0], location[0] + extent[0]
    min_x, max_x = location[1] - extent[1], location[1] + extent[1]
    bounding_box = ((min_z, min_x), (max_z, max_x))
    return find_buildings_within_bbox(village_skeleton, bounding_box)

def find_buildings_within_radius(village_skeleton, location, radius):
    buildings_within_radius = []
    buildings_within_extent = find_buildings_within_extent(village_skeleton, location, (radius, radius))
    for building in buildings_within_extent:
        if np.linalg.norm(building.position - location) <= radius:
            buildings_within_radius.append(building)
    return buildings_within_radius

def get_vector(building, neighbor, distance, scale):
    if distance == 0:
        unit_directions = [[10,0], [-10,0], [0,-10], [0,10]]
        idx = random.randint(0,3)
        return unit_directions[idx]
    else:
        return ((neighbor.position - building.position) / distance) * scale #min(20, scale) #TODO: Magic number


def sociability(terrain, village_skeleton, building):
    knn = building.knn
    attraction = building.attraction
    repulsion = building.repulsion

    distances = dict()
    for neighbor in village_skeleton:
        if neighbor.id != building.id:
            if neighbor.type in building.social_agents:
                distance = np.linalg.norm(building.position - neighbor.position)
                distances[neighbor] = distance
    knn_neighbors = sorted(distances.items(), key = lambda kv : kv[1])[:knn]
    knn_vector = np.array([0.,0.])
    for neighbor, distance in knn_neighbors:
        # print('knn', building.id, knn_vector)

        # print((neighbor.position - building.position), (neighbor.position - building.position) / distance)
        if distance > attraction:
            knn_vector += get_vector(building, neighbor, distance, distance - attraction)
            # knn_vector += get_vector(building, neighbor, distance, 1)

        elif distance < repulsion:
            knn_vector += get_vector(building, neighbor, distance, (repulsion - distance) * -1)
            # knn_vector += get_vector(building, neighbor, distance, 1)
    return knn_vector
    #return np.sum(knn_vector, axis=1)

def slope(terrain, village_skeleton, building):
    building_center = building.position + (max(building.dim) // 2) # TODO: This is 2d
    left_half = terrain[building.position[0]:building.position[0] + max(building.dim), building.position[1] : building_center[1]]
    right_half = terrain[building.position[0]:building.position[0] + max(building.dim), building_center[1] : building.position[1] + max(building.dim)]

    bottom_half = terrain[building.position[0] : building_center[0], building.position[1]:building.position[1] + max(building.dim)]
    top_half = terrain[building_center[0] : building.position[0] + max(building.dim), building.position[1]:building.position[1] + max(building.dim)]

    dz = np.average(left_half) - np.average(right_half)
    dx = np.average(bottom_half) - np.average(top_half)

    return np.array([dz, dx])

def geographic_domination(terrain, village_skeleton, building):
    def height_comparison(terrain, main_position, compared_position):
        dy = terrain[main_position] - terrain[compared_position]
        dy / (1 + np.linalg.norm(main_position - compared_position))

    buildings_under_influence = find_buildings_within_radius(village_skeleton, building.position, building.influence_radius)
    for building_under_influence in buildings_under_influence:
        height_comparison(terrain, building.position, building_under_influence.position)

    return np.array([0,0]) # TODO: Finish


