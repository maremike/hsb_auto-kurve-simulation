import numpy as np

from control.formulae import get_Coordinates, transform_vector, get_radius, get_circle_circumference
from resources import variables


def simulate():
    """
    Simulates the movement along the curve, calculating forces and coordinates at different points based on the
    given parameters. The simulation iterates over the curve's total distance and updates the dataset accordingly.
    Fills a datalist list with all datasets containing the relevant data to demonstrate the movement along the curve.

    Parameters:
        None

    Returns:
        None
    """
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


def getDataset(distance):
    """
    Retrieves the dataset for a given distance along the curve. The dataset includes various forces and coordinates
    at that specific point. Rotates vectors according to this formula:
    - newAngle = (distance * curveAngle) / totalDistance

    Parameters:
        distance (float): The distance along the curve for which the dataset is to be generated.

    Returns:
        list: A list containing a total of 12 elements:
            - 0: Coordinates at the given distance.
            - 1: The new angle in relation to the starting point.
            - 2-11: Various force vectors (e.g., velocity, new velocity, drag, centripetal force, etc.).
    """
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
