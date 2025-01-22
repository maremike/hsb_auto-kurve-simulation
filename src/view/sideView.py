import numpy as np

import control.simulation
from control.formulae import transform_vector
from resources import variables


def init_graph(plot, dataset):
    # calculate the range of the axes
    minX = dataset[0][0] - (np.cos(np.radians(variables.turnIncline)) * variables.roadWidth)
    maxX = dataset[0][0] + (np.cos(np.radians(variables.turnIncline)) * variables.roadWidth)
    minY = dataset[0][1] - (np.sin(np.radians(variables.turnIncline) * variables.roadWidth))
    maxY = dataset[0][1] + (np.sin(np.radians(variables.turnIncline) * variables.roadWidth))

    # plots triangle to graph (road)
    triangleX = dataset[0][0] - (np.cos(np.radians(variables.turnIncline)) * variables.roadWidth / 2)
    triangleY = dataset[0][1] - (np.sin(np.radians(variables.turnIncline) * variables.roadWidth / 2))
    add_road(plot, variables.roadWidth, variables.turnIncline, triangleX, triangleY)

    # initialize graph
    plot.set_xlim(minX, maxX)
    plot.set_ylim(minY, maxY)
    plot.set_title("Side View")
    plot.set_ylabel("Y [m]")
    plot.set_aspect('equal', adjustable='datalim')
    plot.autoscale(True)

    # add relevant simulation data
    add_point(plot, dataset)
    add_vectors(plot, dataset)


def add_road(plot, hypotenuse_length, angle_degrees, x1, y1):
    # calculate all sides of the triangle
    adjacent = hypotenuse_length * np.cos(np.radians(angle_degrees))  # Length of the adjacent side
    opposite = hypotenuse_length * np.sin(np.radians(angle_degrees))  # Length of the opposite side

    # calculate coordinates of each side
    x2 = x1 + adjacent
    y2 = y1 + opposite

    # plot the triangle
    plot.plot([x1, x2], [y1, y1], '-', color='black', label='Adjacent')  # Adjacent side
    plot.plot([x2, x2], [y1, y2], '-', color='black', label='Opposite')  # Opposite side
    plot.plot([x1, x2], [y1, y2], '-', color='black', label='Hypotenuse')  # Hypotenuse


def add_point(plot, dataset):
    # add the current position of the car to the graph
    plot.scatter(dataset[0][0], dataset[0][1], color='grey', marker='.', s=400)


def add_vectors(plot, dataset):
    # rotate vectors to be shown correctly on a 2D plane
    for i in range(2, 11):
        dataset[i] = transform_vector(dataset[i], 0, np.radians(dataset[1] * -1), 0)

    # display vectors
    plot.quiver(dataset[0][0], dataset[0][1], dataset[7][0], dataset[7][1], angles='xy', scale_units='xy', scale=6999,
                color='purple', alpha=1)  # f_gravity_parallel
    plot.quiver(dataset[0][0], dataset[0][1], dataset[8][0], dataset[8][1], angles='xy', scale_units='xy', scale=6999,
                color='blue', alpha=1)  # f_static_friction
    plot.quiver(dataset[0][0], dataset[0][1], dataset[9][0], dataset[9][1], angles='xy', scale_units='xy', scale=6999,
                color='purple', alpha=1)  # f_neutral
    plot.quiver(dataset[0][0], dataset[0][1], dataset[10][0], dataset[10][1], angles='xy', scale_units='xy', scale=6999,
                color='yellow', alpha=1)  # f_road
    plot.quiver(dataset[0][0], dataset[0][1], dataset[11][0], dataset[11][1], angles='xy', scale_units='xy',
                scale=6999, color='purple', alpha=1)  # f_gravity
