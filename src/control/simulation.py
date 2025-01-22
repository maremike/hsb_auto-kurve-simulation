import numpy as np

from control.formulae import get_Coordinates, transform_vector, get_radius, get_circle_circumference
from resources import variables


def getDataset(distance):
    """
    Retrieves the dataset for a given distance along the curve. The dataset includes various forces and coordinates
    at that specific point.

    Parameters:
    distance (float): The distance along the curve for which the dataset is to be generated.

    Returns:
    list: A list containing the following elements:
        - Coordinates at the given distance.
        - The new angle in relation to the starting point.
        - Various force vectors (e.g., velocity, new velocity, drag, centripetal force, etc.).

    Formula:
    - newAngle = (distance * curveAngle) / totalDistance

    Where:
    - distance: The current position along the curve.
    - curveAngle: The total angle of the curve.
    - totalDistance: The total distance to travel along the curve.
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


def simulate():
    """
    Simulates the movement along the curve, calculating forces and coordinates at different points based on the
    given parameters. The simulation iterates over the curve's total distance and updates the dataset accordingly.

    Parameters:
    None

    Returns:
    None

    Function Logic:
    - First, calculates the radius and total distance of the curve.
    - Initializes the time simulation based on the velocity.
    - Iterates over the simulation time, collecting datasets at each timestep.
    - The simulation stops once the total time (for the entire distance) has passed.

    Formula:
    - radius = get_radius(wheelDistance, turnAngle)
    - totalDistance = get_circle_circumference(radius)
    - simulationTime = totalDistance / velocity
    - deltaT = simulationTime / simulationIterations
    - timePassed = timePassed + deltaT

    Where:
    - wheelDistance: The distance between the wheels of the vehicle.
    - turnAngle: The angle of the turn.
    - velocity: The velocity at which the vehicle moves.
    - simulationIterations: The number of iterations to divide the simulation into.
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
