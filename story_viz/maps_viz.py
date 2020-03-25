import matplotlib.pyplot as plt
import numpy as np
import random
import copy

def fit_to_range(x, minx, maxx, min_range, max_range):
    try:
        normalized_x = (x - minx) / (maxx - minx)
    except ZeroDivisionError:
        print(x, minx, maxx)
        normalized_x = minx
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
    norm_color = lambda r,g,b: (r/255., g/255., b/255.)
    for color_name in colors:
        colors[color_name] = norm_color(*colors[color_name])
    return colors

class VizAnimator:
    def __init__(self):
        self.history = []
        self.terrain_plot = None

    def add(self, village_skeleton):
        timestep = []
        for building in village_skeleton:
            z_ax = [building.position[0], building.position[0] + building.dim[0]]
            x_ax = [building.position[1], building.position[1] + building.dim[1]]
            building_type = building.building_type
            timestep.append((building_type, z_ax, x_ax))
        self.history.append(timestep)

    def animate(self, elevation_terrain, material_terrain):
        plt.ion()
        for timestep in self.history:
            self.plot(elevation_terrain, material_terrain, timestep)

    def plot(self, elevation_terrain, material_terrain, buildings_info, play_rate=.09):
        z, x = elevation_terrain.shape
        if self.terrain_plot is None:
            world = np.zeros((z, x, 3))
            plot_terrain(world, elevation_terrain)
            plot_terrain(world, material_terrain)
            self.terrain_plot = np.copy(world)
        else:
            world = np.copy(self.terrain_plot)

        building_colors = {'rural': 'brown', 'public': 'purple', 'residential': 'red', 'commercial': 'green',
                           'terrain': 'white', 'aesthetic': 'pink'}
        colors = get_normed_colors()


  
        for (building_type, z_ax, x_ax) in buildings_info:
            color_name = building_colors[building_type]
            world[z_ax[0]: z_ax[1], x_ax[0]: x_ax[1]] = colors[color_name]
        plt.imshow(world)
        plt.draw()
        plt.pause(play_rate)
        plt.clf()

def draw_river(terrain, world):
    for z, row in enumerate(terrain.layers['material']):
        for x, material in enumerate(row):
            if material == terrain.materials['water']:
                world[z][x] = [.2, .2, 1.]

def plot(terrain, village_skeleton):
    elevation = terrain.layers['elevation']
    z, x = elevation.shape
    world = np.zeros((z,x,3))
    building_colors = {'rural':'brown', 'public':'purple', 'residential':'red', 'commercial':'green', 'terrain':'white', 'aesthetic':'pink'}
    colors = get_normed_colors()
    plot_terrain(world, elevation)
    for building in village_skeleton:
        color_name = building_colors[building.building_type]
        world[building.position[0]: building.position[0]+building.dim[0], building.position[1]: building.position[1]+building.dim[1]] = colors[color_name]

    draw_river(terrain, world)

    for point in terrain.material_points['road']:
        world[point[0]][point[1]] = [1,1,1]

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