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
currentAngle = 0
radius = get_radius(wheelDistance, turnAngle)

totalDistance = get_circle_circumference(radius) / 4


def setOptimizationResults(new_turnIncline, new_mass, new_staticFriction, new_cdValue, new_frontArea, new_airPressure):
    global turnIncline, mass, staticFriction, cdValue, frontArea, airPressure

    turnIncline = new_turnIncline
    mass = new_mass
    staticFriction = new_staticFriction
    cdValue = new_cdValue
    frontArea = new_frontArea
    airPressure = new_airPressure


def rotate_vectors(v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, pitch, yaw, roll):
    v0 = transform_vector(v0, pitch, yaw, roll)
    v1 = transform_vector(v1, pitch, yaw, roll)
    v2 = transform_vector(v2, pitch, yaw, roll)
    v3 = transform_vector(v3, pitch, yaw, roll)
    v4 = transform_vector(v4, pitch, yaw, roll)
    v5 = transform_vector(v5, pitch, yaw, roll)
    v6 = transform_vector(v6, pitch, yaw, roll)
    v7 = transform_vector(v7, pitch, yaw, roll)
    v8 = transform_vector(v8, pitch, yaw, roll)
    v9 = transform_vector(v9, pitch, yaw, roll)
    return v0, v1, v2, v3, v4, v5, v6, v7, v8, v9


def getDataSet(distance):
    coordinates = get_Coordinates(radius, distance, totalDistance, curveAngle, turnIncline, roadWidth)

    global currentAngle, f_drag, f_velocity, f_new_velocity, f_centrifugal, f_gravity, f_gravity_parallel, f_neutral, f_road, f_static_friction, f_centripetal
    newAngleDelta = (distance * curveAngle / totalDistance) - currentAngle
    (f_velocity, f_new_velocity, f_drag, f_centripetal, f_centrifugal, f_gravity_parallel,
    f_static_friction, f_neutral, f_road, f_gravity) = rotate_vectors(f_velocity, f_new_velocity, f_drag, f_centripetal,
                                                                      f_centrifugal, f_gravity_parallel, f_static_friction,
                                                                      f_neutral, f_road, f_gravity,
                                                                      0, np.radians(newAngleDelta), 0,)
    currentAngle += newAngleDelta

    return (coordinates, f_velocity, f_new_velocity, f_drag, f_centripetal, f_centrifugal, f_gravity_parallel,
            f_static_friction, f_neutral, f_road, f_gravity)


def simulate():
    print("Simulating values...")

    global f_drag, f_velocity, f_new_velocity, f_centrifugal, f_gravity, f_gravity_parallel, f_neutral, f_road, f_static_friction, f_centripetal
    (f_drag, f_velocity, f_new_velocity, f_centrifugal, f_gravity, f_gravity_parallel, f_neutral, f_road,
     f_static_friction, f_centripetal) = (
        init_vectors(turnIncline, mass, cdValue, frontArea, airPressure, gasContent, temperature, velocity, turnAngle,
                     gravityAcceleration)
    )

    timePassed = 0
    dataList = []
    while velocity * timePassed <= totalDistance:
        data = getDataSet(velocity * timePassed)
        dataList.append(data)
        timePassed += deltaT

    print("Simulation finished.")
    #init_views(dataList, int(len(dataList) / 2))
    init_views(dataList, 1)
