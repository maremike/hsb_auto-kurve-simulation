import numpy as np
import sympy as sp
from scipy.optimize import minimize
from resources.constraints import CONSTRAINTS

from resources.constraints import CONSTRAINTS
from resources.constants_simulation import turnAngle, velocity, gravityAcceleration, airDensity

import numpy as np
from scipy.optimize import minimize

def conditions(x, turnAngle, velocity, airDensity):
    turnIncline, mass, staticFriction, cdValue, frontArea = x

    radius = 2.5 / np.tan(turnAngle)  # Wheel distance: e.g. 2.5 m
    F_centripetal = mass * velocity**2 / radius
    F_staticFriction = staticFriction * mass * gravityAcceleration * np.cos(turnIncline)
    f_incline = mass * gravityAcceleration * np.sin(turnIncline)
    return F_staticFriction + f_incline - F_centripetal  # Condition for the car to stay in the turn

def weighting(x):
    turnIncline, mass, staticFriction, cdValue, frontArea = x

    w1, w2, w3, w4 = 1, 1, 1, 1  # weight
    return w1 * mass + w2 * cdValue + w3 * frontArea + w4 * staticFriction # following values should be as low as possible

def optimize():
    print("Optimizing values...")

    # starting values
    x0 = [0, 800, 0.5, 0.21, 1.8]  # first guess

    # create bounds
    bounds = {
        CONSTRAINTS["turnIncline"],
        CONSTRAINTS["mass"],
        CONSTRAINTS["staticFriction"],
        CONSTRAINTS["cdValue"],
        CONSTRAINTS["frontArea"]
    }

    # create constraints
    constraints = [{"type": "ineq", "fun": conditions, "args": (turnAngle, velocity, airDensity)}]

    # optimize with scipy minimize (SLSQP method)
    result = minimize(weighting, x0, method="SLSQP", bounds=bounds, constraints=constraints)


    # results
    print("\tInput values:")
    print("\tTurn angle [deg]:", turnAngle)
    print("\tVelocity [m/s]:", velocity)
    print("\tAir density [kg/m³]:", airDensity)
    print("\n\tOutput values:")
    print("\tTurn incline [deg]:", result.x[0])
    print("\tMass [kg]:", result.x[1])
    print("\tStatic friction:", result.x[2])
    print("\tCd-Value:", result.x[3])
    print("\tFront area [m²]:", result.x[4])

    print("Optimization finished.")