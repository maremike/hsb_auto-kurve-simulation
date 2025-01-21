import numpy as np

import control.simulation
from resources.constants import roadWidth


def init_graph(plot, dataSet):
    from control.simulation import turnIncline

    minX = dataSet[0][0] - (np.cos(np.radians(turnIncline)) * roadWidth)
    maxX = dataSet[0][0] + (np.cos(np.radians(turnIncline)) * roadWidth)
    minY = dataSet[0][1] - (np.sin(np.radians(turnIncline) * roadWidth))
    maxY = dataSet[0][1] + (np.sin(np.radians(turnIncline) * roadWidth))

    triangleX = dataSet[0][0] - (np.cos(np.radians(turnIncline)) * roadWidth / 2)
    triangleY = dataSet[0][1] - (np.sin(np.radians(turnIncline) * roadWidth / 2))
    add_road(plot, roadWidth, turnIncline, triangleX, triangleY)

    plot.set_xlim(minX, maxX)
    plot.set_ylim(minY, maxY)
    plot.set_title("Side View")
    plot.set_xlabel("X [m]")
    plot.set_ylabel("Y [m]")
    plot.set_aspect('equal', adjustable='datalim')
    plot.autoscale(True)

    add_point(plot, dataSet)
    add_vectors(plot, dataSet)


def add_road(plot, hypotenuse_length, angle_degrees, x1, y1):
    """
    Plots a right triangle with a given hypotenuse length, angle, and starting point.

    Parameters:
    - hypotenuse_length: Length of the hypotenuse.
    - angle_degrees: Angle (in degrees) between the hypotenuse and the horizontal axis.
    - start_point: Tuple (x, y) specifying the starting vertex of the triangle.
    """
    # Calculate the other two sides of the triangle
    adjacent = hypotenuse_length * np.cos(np.radians(angle_degrees))  # Length of the adjacent side
    opposite = hypotenuse_length * np.sin(np.radians(angle_degrees))  # Length of the opposite side

    x2 = x1 + adjacent
    y2 = y1 + opposite

    # Plot the triangle
    plot.plot([x1, x2], [y1, y1], '-', color='black', label='Adjacent')  # Adjacent side
    plot.plot([x2, x2], [y1, y2], '-', color='black', label='Opposite')  # Opposite side
    plot.plot([x1, x2], [y1, y2], '-', color='black', label='Hypotenuse')  # Hypotenuse


def add_point(plot, dataSet):
    plot.scatter(dataSet[0][0], dataSet[0][1], color='grey', marker='.', s=400)


def add_vectors(plot, dataSet):
    plot.quiver(dataSet[0][0], dataSet[0][1], dataSet[4][0], dataSet[4][1], angles='xy', scale_units='xy', scale=1,
                color='green')  # f_centripetal
    plot.quiver(dataSet[0][0], dataSet[0][1], dataSet[5][0], dataSet[5][1], angles='xy', scale_units='xy', scale=1,
                color='green')  # f_centrifugal
    plot.quiver(dataSet[0][0], dataSet[0][1], dataSet[6][0], dataSet[6][1], angles='xy', scale_units='xy', scale=29999,
                color='purple')  # f_gravity_parallel
    plot.quiver(dataSet[0][0], dataSet[0][1], dataSet[7][0], dataSet[7][1], angles='xy', scale_units='xy', scale=29999,
                color='blue')  # f_static_friction
    plot.quiver(dataSet[0][0], dataSet[0][1], dataSet[8][0], dataSet[8][1], angles='xy', scale_units='xy', scale=49999,
                color='purple')  # f_neutral
    plot.quiver(dataSet[0][0], dataSet[0][1], dataSet[9][0], dataSet[9][1], angles='xy', scale_units='xy', scale=49999,
                color='yellow')  # f_road
    plot.quiver(dataSet[0][0], dataSet[0][1], dataSet[10][0], dataSet[10][1], angles='xy', scale_units='xy', scale=69999,
                color='purple')  # f_gravity