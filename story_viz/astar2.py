import numpy
from heapq import *


def heuristic(terrain, dim):
    return terrain.layers['road'][dim]
    # Take value from terrain.layers['road'] i.e. distance from any road
    # Take water into account






def astar(terrain, start, goal):
    array = terrain.layers['road']
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    close_set = set()
    all_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(terrain, start)}
    oheap = []

    heappush(oheap, (fscore[start], start))
    all_set.add(start)

    while oheap:

        current = heappop(oheap)[1]
        if terrain.layers['road'][current] == 0:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            # out of bounds check
            if 0 <= neighbor[0] < array.shape[0]:
                if neighbor[1] < 0 or neighbor[1] >= array.shape[1]:
                    continue
            else:
                continue

            tentative_g_score = gscore[current] + 1
            if neighbor in close_set:
                continue

            if neighbor not in all_set:
                all_set.add(neighbor)
            elif tentative_g_score >= gscore.get(neighbor, 0):
                continue

            came_from[neighbor] = current
            gscore[neighbor] = tentative_g_score
            fscore[neighbor] = tentative_g_score + heuristic(terrain, neighbor)
            heappush(oheap, (fscore[neighbor], neighbor))

    return False

if __name__=='__main__':

    '''Here is an example of using my algo with a numpy array,
       astar(array, start, destination)
       astar function returns a list of points (shortest path)'''

    nmap = numpy.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

    print astar(nmap, (0, 0), (2, 2))