import matplotlib.pyplot as plt
import numpy as np

from control.formulae import get_radius
from resources.constants import functionT, curveAngle, roadWidth, wheelDistance, turnAngle


def init_graph(plot, dataList, focusingDataset):
    # Initialize limits with the first data point
    minX, maxX, minZ, maxZ = np.inf, -np.inf, np.inf, -np.inf

    # Plot road
    radius = get_radius(wheelDistance, turnAngle)
    theta = np.linspace(0, 2 * np.pi * (curveAngle / 360), functionT)  # Adjusted for curveAngle
    x1 = (radius - roadWidth / 2) * np.cos(theta)
    x2 = radius * np.cos(theta)
    x3 = (radius + roadWidth / 2) * np.cos(theta)
    z1 = -1 * (radius - roadWidth / 2) * np.sin(theta)
    z2 = -1 * radius * np.sin(theta)
    z3 = -1 * (radius + roadWidth / 2) * np.sin(theta)

    # Plotting the roads (inner, middle, and outer circles)
    plt.plot(x1, z1, color='black', linestyle='-', label="Inner Road")
    plt.plot(x2, z2, color='black', linestyle='--', label="Middle Road")
    plt.plot(x3, z3, color='black', linestyle='-', label="Outer Road")

    for i in theta:
        minX = min((radius + roadWidth / 2) * np.cos(theta))
        maxX = max((radius + roadWidth / 2) * np.sin(theta))
        minZ = min((radius + roadWidth / 2) * np.sin(theta))
        maxZ = max((radius + roadWidth / 2) * np.sin(theta))

    plot.set_xlim(-minX, maxX)
    plot.set_ylim(minZ, -maxZ)
    plot.set_title("Top-down View")
    plot.set_xlabel("X")
    plot.set_ylabel("Z")

    add_points(plot, dataList)
    add_vectors(plot, dataList[focusingDataset])


def add_points(plot, dataList):
    for i in dataList:
        plot.scatter(i[0][0], i[0][2], color='blue', marker='x', s=100)


def add_vectors(plot, dataSet):
    plot.quiver(dataSet[0][0], dataSet[0][2], dataSet[1][0], dataSet[1][2], angles='xy', scale_units='xy', scale=1,
                color='red')  # f_velocity
    plot.quiver(dataSet[0][0], dataSet[0][2], dataSet[2][0], dataSet[2][2], angles='xy', scale_units='xy', scale=1,
                color='orange')  # f_new_velocity
    plot.quiver(dataSet[0][0], dataSet[0][2], dataSet[3][0], dataSet[3][2], angles='xy', scale_units='xy', scale=1,
                color='yellow')  # f_drag
    plot.quiver(dataSet[0][0], dataSet[0][2], dataSet[4][0], dataSet[4][2], angles='xy', scale_units='xy', scale=1,
                color='green')  # f_centripetal
    plot.quiver(dataSet[0][0], dataSet[0][2], dataSet[5][0], dataSet[5][2], angles='xy', scale_units='xy', scale=1,
                color='blue')  # f_centrifugal
    plot.quiver(dataSet[0][0], dataSet[0][2], dataSet[6][0], dataSet[6][2], angles='xy', scale_units='xy', scale=1,
                color='purple')  # f_gravity_parallel
    plot.quiver(dataSet[0][0], dataSet[0][2], dataSet[7][0], dataSet[7][2], angles='xy', scale_units='xy', scale=1,
                color='grey')  # f_static_friction
