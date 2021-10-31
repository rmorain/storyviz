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
    buildings_within_extent = find_buildings_within_extent(
        village_skeleton, location, (radius, radius)
    )
    for building in buildings_within_extent:
        if np.linalg.norm(building.position - location) <= radius:
            buildings_within_radius.append(building)
    return buildings_within_radius


def get_vector(building, neighbor, distance, scale):
    if distance == 0:
        unit_directions = [[10, 0], [-10, 0], [0, -10], [0, 10]]
        idx = random.randint(0, 3)
        return unit_directions[idx]
    else:
        return ((neighbor.position - building.position) / distance) * scale


def get_knn(village_skeleton, building, neighbor_types, k):
    distances = dict()
    for neighbor in village_skeleton:
        if neighbor.id != building.id:
            if neighbor.type in neighbor_types:
                distance = np.linalg.norm(building.position - neighbor.position)
                distances[neighbor] = distance
    return sorted(distances.items(), key=lambda kv: kv[1])[:k]


def sociability(terrain, village_skeleton, building):
    knn = building.knn
    attraction = building.attraction
    repulsion = building.repulsion

    # distances = dict()
    # for neighbor in village_skeleton:
    #     if neighbor.id != building.id:
    #         if neighbor.type in building.social_agents:
    #             distance = np.linalg.norm(building.position - neighbor.position)
    #             distances[neighbor] = distance
    # knn_neighbors = sorted(distances.items(), key = lambda kv : kv[1])[:knn]
    knn_neighbors = get_knn(village_skeleton, building, building.social_agents, knn)
    knn_vector = np.array([0.0, 0.0])
    for neighbor, distance in knn_neighbors:
        # print('knn', building.id, knn_vector)

        # print((neighbor.position - building.position), (neighbor.position - building.position) / distance)
        if distance > attraction:
            knn_vector += get_vector(
                building, neighbor, distance, distance - attraction
            )
            # knn_vector += get_vector(building, neighbor, distance, 1)

        elif distance < repulsion:
            knn_vector += get_vector(
                building, neighbor, distance, (repulsion - distance) * -1
            )
            # knn_vector += get_vector(building, neighbor, distance, 1)
    return knn_vector
    # return np.sum(knn_vector, axis=1)


def slope(terrain, village_skeleton, building):
    def get_side(z_start, z_end, x_start, x_end):
        if z_end >= max_z:
            z_end = max_z - 1
        if x_end >= max_x:
            x_end = max_x - 1
        return elevation[z_start: z_end, x_start: x_end]

    elevation = terrain.layers["elevation"]
    max_z, max_x = elevation.shape
    building_dim = [building.dim[0], building.dim[1]]
    if building.dim[0] <= 2:
        building_dim[0] = 3
    if building.dim[1] <= 2:
        building_dim[1] = 3
    building_center = [
        building.position[0] + (building.dim[0] // 2),
        building.position[1] + (building.dim[1] // 2),
    ]
    left_half = get_side(building.position[0], building.position[0] + building_dim[0],
                         building.position[1], building_center[1])
    right_half = get_side(building.position[0], building.position[0] + building_dim[0],
                          building_center[1], building.position[1] + building_dim[1])
    bottom_half = get_side(building.position[0], building_center[0],
                           building.position[1], building.position[1] + building_dim[1])
    top_half = get_side(building_center[0], building.position[0] + building_dim[0],
                        building.position[1], building.position[1] + building_dim[1])
    dz, dx = 0, 0
    if left_half.size != 0 and right_half.size != 0:
        dz = np.average(left_half) - np.average(right_half)
    if bottom_half.size != 0 and top_half.size != 0:
        dx = np.average(bottom_half) - np.average(top_half)
    return np.array([dz, dx])


# max_length = length * steps
def cast_rect_net(terrain, building, length, steps):
    net_positions = set()
    z, x = terrain.layers["elevation"].shape
    net_directions = np.array(
        [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
    )
    for step in range(1, steps + 1):
        for direction in net_directions:
            scaled_direction = direction * step
            position = building.get_valid_displacement(
                building.position + scaled_direction, z, x
            )
            net_positions.add(tuple(position))
    return list(net_positions)


def get_geographic_domination_position(terrain, village_skeleton, building, position):
    elevation = terrain.layers["elevation"]

    def height_comparison(elevation, main_position, compared_position):
        dy = float(
            elevation[tuple(main_position)] - elevation[tuple(compared_position)]
        )
        return dy / (1 + np.linalg.norm(main_position - compared_position))

    domination = 0
    buildings_under_influence = find_buildings_within_radius(
        village_skeleton, position, building.influence_radius
    )
    for building_under_influence in buildings_under_influence:
        domination += height_comparison(
            elevation, position, building_under_influence.position
        )
    return domination


def geographic_domination(terrain, village_skeleton, building):
    possible_positions = cast_rect_net(terrain, building, building.influence_radius, 2)
    domination_values = []
    for position in possible_positions:
        domination_val = get_geographic_domination_position(
            terrain, village_skeleton, building, position
        )
        domination_values.append(domination_val)
    i = np.argmax(domination_values)
    position = possible_positions[i]
    return position - building.position


def knn_centroid(terrain, village_skeleton, building):
    knn = building.centroid_knn
    knn_neighbors = get_knn(village_skeleton, building, building.centroid_types, knn)
    knn_centroid = np.array([0, 0])
    for neighbor, distance in knn_neighbors:
        knn_centroid += neighbor.position
    knn_centroid /= knn
    return knn_centroid - building.position


def repel_collision(terrain, village_skeleton, building):
    def get_building_to_position_repulsion(building, position):
        if np.linalg.norm(position - building.position, ord=np.inf) <= (
            max(building.dim) + 2
        ):
            x = building.position - position
            return (np.sign(x) * building_vector) - x
        return np.array([0, 0])

    repulsion = np.array([0, 0])
    building_vector = np.array([max(building.dim), max(building.dim)])
    for neighbor in village_skeleton:
        repulsion += get_building_to_position_repulsion(building, neighbor.position)
    for point in terrain.material_points["road"]:
        repulsion += get_building_to_position_repulsion(building, point)

    return repulsion


# Return vector to move building closer to a materials
def near(material, terrain, building):
    def get_side(z_start, z_end, x_start, x_end):
        if z_end >= max_z:
            z_end = max_z - 1
        if x_end >= max_x:
            x_end = max_x - 1
        return material_dist[z_start: z_end, x_start: x_end]

    material_dist = terrain.layers[material]
    # If the material does not exist, don't move at all
    if material_dist is None:
        return np.array([0, 0])
    max_z, max_x = material_dist.shape
    building_dim = [building.dim[0], building.dim[1]]
    if building.dim[0] <= 2:
        building_dim[0] = 3
    if building.dim[1] <= 2:
        building_dim[1] = 3
    building_center = [
        building.position[0] + (building.dim[0] // 2),
        building.position[1] + (building.dim[1] // 2),
    ]
    left_half = get_side(building.position[0], building.position[0] + building_dim[0],
                         building.position[1], building_center[1])
    right_half = get_side(building.position[0], building.position[0] + building_dim[0],
                          building_center[1], building.position[1] + building_dim[1])
    bottom_half = get_side(building.position[0], building_center[0],
                           building.position[1], building.position[1] + building_dim[1])
    top_half = get_side(building_center[0], building.position[0] + building_dim[0],
                        building.position[1], building.position[1] + building_dim[1])

    dz, dx = 0, 0
    if left_half.size != 0 and right_half.size != 0:
        dz = np.average(left_half) - np.average(right_half)
    if bottom_half.size != 0 and top_half.size != 0:
        dx = np.average(bottom_half) - np.average(top_half)
    return np.array([dz, dx])
