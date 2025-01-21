import numpy as np

from control.formulae import get_radius, init_vectors, get_circle_circumference, get_Coordinates, transform_vector
from resources.constants import wheelDistance, turnAngle, velocity, gravityAcceleration, gasContent, \
    temperature, deltaT, curveAngle, roadWidth
from view.wholeView import init_views

turnIncline = 0
mass = 0
staticFriction = 0
cdValue = 0
frontArea = 0
airPressure = 0
f_drag = 0
f_velocity = 0
f_new_velocity = 0
f_centrifugal = 0
f_gravity = 0
f_gravity_parallel = 0
f_neutral = 0
f_road = 0
f_static_friction = 0
f_centripetal = 0

radius = get_radius(wheelDistance, turnAngle)
totalDistance = get_circle_circumference(radius) / 4


def setOptimizationResults(new_turnIncline, new_mass, new_staticFriction, new_cdValue, new_frontArea, new_airPressure):
    # set results to global values
    global turnIncline, mass, staticFriction, cdValue, frontArea, airPressure
    turnIncline = new_turnIncline
    mass = new_mass
    staticFriction = new_staticFriction
    cdValue = new_cdValue
    frontArea = new_frontArea
    airPressure = new_airPressure


def getDataset(distance):
    # calculate new coordinates
    coordinates = get_Coordinates(radius, distance, totalDistance, curveAngle, turnIncline, roadWidth)
    # calculate new angle in relation to starting point
    newAngle = (distance * curveAngle / totalDistance)

    global currentAngle, f_drag, f_velocity, f_new_velocity, f_centrifugal, f_gravity, f_gravity_parallel, f_neutral, f_road, f_static_friction, f_centripetal
    dataset = [coordinates, newAngle, f_velocity, f_new_velocity, f_drag, f_centripetal, f_centrifugal,
               f_gravity_parallel, f_static_friction, f_neutral, f_road, f_gravity]

    # rotates vectors according to current position in the curve
    for i in range(2, 11):
        dataset[i] = transform_vector(dataset[i], 0, np.radians(newAngle), 0)

    return dataset


def simulate():
    print("Simulating values...")

    global f_drag, f_velocity, f_new_velocity, f_centrifugal, f_gravity, f_gravity_parallel, f_neutral, f_road, f_static_friction, f_centripetal
    (f_drag, f_velocity, f_new_velocity, f_centrifugal, f_gravity, f_gravity_parallel, f_neutral, f_road,
     f_static_friction, f_centripetal) = (
        init_vectors(turnIncline, mass, cdValue, frontArea, airPressure, gasContent, temperature, velocity, turnAngle,
                     gravityAcceleration)
    )

    timePassed = 0
    dataList = [] # fills list with all data from the simulation: position, angle and vector values
    while velocity * timePassed <= totalDistance:
        data = getDataset(velocity * timePassed) # retrieve dataset from current position on the curve
        dataList.append(data)
        timePassed += deltaT # increase time

    print("Simulation finished.")

    # initializes views with two graphs. Focuses on the middle dataset, where the current vectors will be displayed
    init_views(dataList, int(len(dataList) / 2))
