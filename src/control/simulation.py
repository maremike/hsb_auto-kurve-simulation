import numpy as np
import time

from control.formulae import get_radius, init_vectors, get_circle_circumference
from resources.constants import wheelDistance, turnAngle, velocity, gravityAcceleration, gasContent, \
    temperature, deltaT, scaleT
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

turnLength = get_circle_circumference(radius) / 4


def setOptimizationResults(new_turnIncline, new_mass, new_staticFriction, new_cdValue, new_frontArea, new_airPressure):
    global turnIncline, mass, staticFriction, cdValue, frontArea, airPressure

    turnIncline = new_turnIncline
    mass = new_mass
    staticFriction = new_staticFriction
    cdValue = new_cdValue
    frontArea = new_frontArea
    airPressure = new_airPressure


def updatePosition():
    pass


def simulate():
    print("Simulating values...")

    global f_drag, f_velocity, f_new_velocity, f_centrifugal, f_gravity, f_gravity_parallel, f_neutral, f_road, f_static_friction, f_centripetal
    (f_drag, f_velocity, f_new_velocity, f_centrifugal, f_gravity, f_gravity_parallel, f_neutral, f_road,
     f_static_friction, f_centripetal) = (
        init_vectors(turnIncline, mass, cdValue, frontArea, airPressure, gasContent, temperature, velocity, turnAngle,
                     gravityAcceleration)
    )

    init_views()

    timePassed = 0
    isDone = False
    while not isDone:
        #updatePosition()
        #updateView()

        # Check if the velocity and time have traveled the length of the turn
        if velocity * timePassed >= turnLength:
            isDone = True
        else:
            timePassed += deltaT  # Update timePassed by deltaT

        # Sleep for the given time, adjusted by scaleT
        time.sleep(deltaT * scaleT)

    print("Simulation finished.")
