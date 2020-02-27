import matplotlib.pyplot as plt

def plot(terrain):
    colors = {'rural':'brown'}
    plt.imshow(terrain, cmap='hot', interpolation='nearest')
    plt.show()

    # plt.ion()
    # plt.imshow(terrain_copy, cmap='hot', interpolation='nearest')
    # plt.draw()
    # plt.pause(.1)
    # plt.clf()