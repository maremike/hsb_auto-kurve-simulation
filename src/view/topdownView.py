import matplotlib.pyplot as plt
import numpy as np

from resources import variables


def add_road(radius, theta):
    # calculate road values
    x1 = (radius - variables.roadWidth / 2) * np.cos(theta)  # inner road: x values
    z1 = -1 * (radius - variables.roadWidth / 2) * np.sin(theta)  # inner road: z values
    x2 = radius * np.cos(theta)  # middle road: x values
    z2 = -1 * radius * np.sin(theta)  # middle road: z values
    x3 = (radius + variables.roadWidth / 2) * np.cos(theta)  # outer road: x values
    z3 = -1 * (radius + variables.roadWidth / 2) * np.sin(theta)  # outer road: z values

    # plot road
    plt.plot(x1, z1, color='black', linestyle='-', label="Inner Road")  # inner road border
    plt.plot(x2, z2, color='black', linestyle='--', label="Middle Road")  # middle of the road
    plt.plot(x3, z3, color='black', linestyle='-', label="Outer Road")  # outer road border


def init_graph(plot, dataList, datasetNumber):
    # plot road
    theta = np.linspace(0, 2 * np.pi * (variables.curveAngle / 360), variables.functionT)
    add_road(variables.radius, theta)

    # calculate the range of the axes
    minX = None
    maxX = None
    minZ = None
    maxZ = None
    for i in theta:
        minX = min((variables.radius + variables.roadWidth / 2) * np.cos(theta))
        maxX = max((variables.radius + variables.roadWidth / 2) * np.sin(theta))
        minZ = min((variables.radius + variables.roadWidth / 2) * np.sin(theta))
        maxZ = max((variables.radius + variables.roadWidth / 2) * np.sin(theta))

    # initialize graph
    plot.set_xlim(-minX, maxX)
    plot.set_ylim(minZ, -maxZ)
    plot.set_title("Top-down View")
    plot.set_xlabel("X [m]")
    plot.set_ylabel("Z [m]")
    plot.set_aspect('equal', adjustable='datalim')
    plot.autoscale(True)

    # add relevant simulation data
    add_points(plot, dataList)
    add_vectors(plot, dataList[datasetNumber])


def add_points(plot, dataList):
    # add all car positions from the simulation
    for i in dataList:
        plot.scatter(i[0][0], i[0][2], color='grey', marker='.', s=65)


def add_vectors(plot, dataset):
    # display vectors
    plot.quiver(dataset[0][0], dataset[0][2], dataset[2][0], dataset[2][2], angles='xy', scale_units='xy', scale=1,
                color='red')  # f_velocity
    plot.quiver(dataset[0][0], dataset[0][2], dataset[3][0], dataset[3][2], angles='xy', scale_units='xy', scale=1,
                color='red')  # f_new_velocity
    plot.quiver(dataset[0][0], dataset[0][2], dataset[4][0], dataset[4][2], angles='xy', scale_units='xy', scale=1,
                color='orange')  # f_drag
    plot.quiver(dataset[0][0], dataset[0][2], dataset[5][0], dataset[5][2], angles='xy', scale_units='xy', scale=1,
                color='green')  # f_centripetal
    plot.quiver(dataset[0][0], dataset[0][2], dataset[6][0], dataset[6][2], angles='xy', scale_units='xy', scale=1,
                color='green')  # f_centrifugal
    plot.quiver(dataset[0][0], dataset[0][2], dataset[7][0], dataset[7][2], angles='xy', scale_units='xy', scale=999,
                color='purple')  # f_gravity_parallel
    plot.quiver(dataset[0][0], dataset[0][2], dataset[8][0], dataset[8][2], angles='xy', scale_units='xy', scale=999,
                color='blue')  # f_static_friction
