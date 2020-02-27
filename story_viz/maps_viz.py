import matplotlib.pyplot as plt

def plot(terrain, village_skeleton):
    colors = {'rural':'brown'}
    for building in village_skeleton:
        terrain[building.position[0], building.position[1]] = 50
    plt.imshow(terrain, cmap='hot', interpolation='nearest')
    plt.show()

    # plt.ion()
    # plt.imshow(terrain_copy, cmap='hot', interpolation='nearest')
    # plt.draw()
    # plt.pause(.1)
    # plt.clf()

# def animation() ????