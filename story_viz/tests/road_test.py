from terrain import Terrain
from maps import *
from maps_viz import *


def mountain_gap_test():
    terrain = Terrain()
    terrain.generate_terrain(num_rivers=0)
    z, x = terrain.layers['elevation'].shape
    elevation = np.zeros((z, x))
    elevation[range(0, z//2 - 5), x//2] = 10
    elevation[range(z//2 + 5, z), x//2] = 10
    terrain.layers['elevation'] = elevation

    start_road = (random.randint(0, z-1), 0)
    end_road = (random.randint(0, z-1), x-1)
    terrain.add_road([end_road])
    connect_point(start_road, terrain)

    print('start road', start_road)
    print('end road', end_road)

    plot(terrain, [])

def river_test():
    terrain = Terrain()
    terrain.generate_terrain(num_rivers=0)

    z, x = terrain.layers['material'].shape
    sp1, ep1 = (0, x//2), (z//2 -5, x//2)
    sp2, ep2 = (z//2 + 5, x//2), (z-1, x//2)
    terrain.add_material_line(terrain.layers['material'], terrain.materials['water'], sp1, ep1, 1)
    terrain.add_material_line(terrain.layers['material'], terrain.materials['water'], sp2, ep2, 1)


    start_road = (random.randint(0, z-1), 0)
    end_road = (random.randint(0, z-1), x-1)
    terrain.add_road([end_road])
    connect_point(start_road, terrain)

    print('start road', start_road)
    print('end road', end_road)

    plot(terrain, [])


def main():
    river_test()


if __name__ == '__main__':
    main()