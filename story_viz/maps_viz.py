import matplotlib.pyplot as plt
import numpy as np
import random

def fit_to_range(x, minx, maxx, min_range, max_range):
    normalized_x = (x - minx) / (maxx - minx)
    return (normalized_x * (max_range - min_range)) + min_range

def plot_terrain(world, terrain):
    peak = np.max(terrain)
    min_green, max_green = 150, 255
    for z, row in enumerate(terrain):
        for x, height in enumerate(row):
            # green_color = fit_to_range(height, 0, peak, min_green, max_green)
            # world[z, x, 1] = green_color/255

            gray_scale = fit_to_range(height, 0, peak, 0, 1)
            world[z, x, :] = gray_scale

def get_normed_colors():
    colors = {'brown': (139,69,19), 'purple': (128,0,128), 'red': (255,0,0), 'green': (0,255,0), 'pink': (255,20,147)}
    norm_color = lambda (r,g,b): (r/255., g/255., b/255.)
    for color_name in colors:
        colors[color_name] = norm_color(colors[color_name])
    return colors

def plot(terrain, village_skeleton):
    z, x = terrain.shape
    world = np.zeros((z,x,3))
    building_colors = {'rural':'brown', 'public':'purple', 'residential':'red', 'commercial':'green', 'terrain':'white', 'aesthetic':'pink'}
    colors = get_normed_colors()
    plot_terrain(world, terrain)
    for building in village_skeleton:
        color_name = building_colors[building.building_type]
        world[building.position[0]: building.position[0]+building.dim[0], building.position[1]: building.position[1]+building.dim[1]] = colors[color_name]
    #     terrain[building.position[0], building.position[1]] = 50
    #
    # plt.imshow(terrain, cmap='hot', interpolation='nearest')
    # plt.show()

    plt.imshow(world)
    plt.show()




    # plt.ion()
    # plt.imshow(terrain_copy, cmap='hot', interpolation='nearest')
    # plt.draw()
    # plt.pause(.1)
    # plt.clf()

# def animation() ????