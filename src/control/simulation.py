import numpy as np

from control.formulae import init_vectors, get_Coordinates, transform_vector, get_radius, get_circle_circumference
from resources import variables
from view.wholeView import init_views


def getDataset(distance):
    # calculate new coordinates
    coordinates = get_Coordinates(variables.radius, distance, variables.totalDistance, variables.curveAngle,
                                  variables.turnIncline, variables.roadWidth)
    # calculate new angle in relation to starting point
    newAngle = (distance * variables.curveAngle / variables.totalDistance)

    dataset = [coordinates, newAngle, variables.f_velocity, variables.f_new_velocity, variables.f_drag,
               variables.f_centripetal, variables.f_centrifugal, variables.f_gravity_parallel,
               variables.f_static_friction, variables.f_neutral, variables.f_road, variables.f_gravity]

    # rotates vectors according to current position in the curve
    for i in range(2, 11):
        dataset[i] = transform_vector(dataset[i], 0, np.radians(newAngle), 0)

    return dataset


def simulate():
    print("Simulating values...")

    variables.radius = get_radius(variables.wheelDistance, variables.turnAngle)
    variables.totalDistance = get_circle_circumference(variables.radius)

    timePassed = 0
    simulationTime = variables.totalDistance / variables.velocity
    deltaT = simulationTime / variables.simulationIterations
    while timePassed <= simulationTime:
        data = getDataset(variables.velocity * timePassed)  # retrieve dataset from current position on the curve
        variables.dataList.append(data)
        timePassed += deltaT  # increase time

    print("Simulation finished.")

    # initializes views with two graphs. Focuses on the middle dataset, where the current vectors will be displayed
    init_views(variables.dataList, int(len(variables.dataList) / 2))
