import random
import numpy as np

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

    # print('dz, dx', type(dz), dz, type(dx), dx)
    # if np.isnan(dz):
    #     print(left_half)
    #     print(building.position[0], building.position[0] + max(building.dim), building.position[1], building_center[1])
    #     print(np.average(left_half))
    #     print(right_half)
    #     print(building.position[0], building.position[0] + max(building.dim), building_center[1], building.position[1] + max(building.dim))
    #     print(np.average(right_half))
    # if np.isnan(dx):
    #     print(bottom_half)
    #     print(building.position[0], building_center[0], building.position[1], building.position[1] + max(building.dim))
    #     print(np.average(bottom_half))
    #     print(top_half)
    #     print(building_center[0], building.position[0] + max(building.dim), building.position[1], building.position[1] + max(building.dim))
    #     print(np.average(top_half))

    return np.array([dz, dx])