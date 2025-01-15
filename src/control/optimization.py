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

    #print(f"Evaluating constraints at x = {x}")
    #f_drag = 0.5 * airDensity * cdValue * frontArea * velocity**2
    #f_friction = mass * gravityAcceleration * staticFriction
    #radius = velocity**2 / (gravityAcceleration * np.tan(turnIncline))
    #f_centripetal = mass * velocity**2 / radius
    #f_gravity = mass * gravityAcceleration
    #f_centrifugal = f_centripetal
    #f_velocity = f_drag

    # inequality constraints g(x) >= 0 (conditions must be more than or equal to 0 to succeed)
    # |f_centripetal| >= |f_centrifugal|
    # |f_velocity0| = |f_drag|
    # |f_velocity1| = |f_drag|
    # |f_velocity1| = |f_velocity0|
    # |f_gravity| = |f_neutral - f_centripetal|
    # |f_centripetal| = |f_drag + f_friction|
    # check whether all values are inside the constraints
    playroom = 1
    return [
        turnIncline - (CONSTRAINTS["turnIncline"][0] / playroom),  # turnIncline >= lower bound
        (CONSTRAINTS["turnIncline"][1] * playroom) - turnIncline,  # turnIncline <= upper bound
        frontArea - (CONSTRAINTS["frontArea"][0] / playroom),  # frontArea >= lower bound
        (CONSTRAINTS["frontArea"][1] * playroom) - frontArea,  # frontArea <= upper bound
        cdValue - (CONSTRAINTS["cdValue"][0] / playroom),  # cdValue >= lower bound
        (CONSTRAINTS["cdValue"][1] * playroom) - cdValue,  # cdValue <= upper bound
        mass - (CONSTRAINTS["mass"][0] / playroom),  # mass >= lower bound
        (CONSTRAINTS["mass"][1] * playroom) - mass,  # mass <= upper bound
        staticFriction - (CONSTRAINTS["staticFriction"][0] / playroom),  # staticFriction >= lower bound
        (CONSTRAINTS["staticFriction"][1] * playroom) - staticFriction  # staticFriction <= upper bound
    ]

def weighting(x):
    turnIncline, mass, staticFriction, cdValue, frontArea = x

    w1, w2, w3, w4 = 1, 1, 1, 1  # weight
    return w1 * mass + w2 * cdValue + w3 * frontArea + w4 * staticFriction # following values should be as low as possible

def findStartingValue(bounds, constraints):
    for i in CONSTRAINTS["turnIncline"]:
        for j in CONSTRAINTS["mass"]:
            for k in CONSTRAINTS["staticFriction"]:
                for l in CONSTRAINTS["cdValue"]:
                    for m in CONSTRAINTS["frontArea"]:
                        x0 = [i, j, k, l, m]
                        result = minimize(weighting, x0, method="SLSQP", bounds=bounds, constraints=constraints)
                        if result.success:
                            return x0
                        else:
                            print(".", end =" ")

def optimize():
    print("Optimizing values...")

    # create bounds
    bounds = [
        (CONSTRAINTS["turnIncline"][0], CONSTRAINTS["turnIncline"][1]),
        (CONSTRAINTS["mass"][0], CONSTRAINTS["mass"][1]),
        (CONSTRAINTS["staticFriction"][0], CONSTRAINTS["staticFriction"][1]),
        (CONSTRAINTS["cdValue"][0], CONSTRAINTS["cdValue"][1]),
        (CONSTRAINTS["frontArea"][0], CONSTRAINTS["frontArea"][1])
    ]

    # create constraints
    constraints = [{"type": "ineq", "fun": conditions, "args": (turnAngle, velocity, airDensity)}]

    # find starting value
    x0 = findStartingValue(bounds, constraints)

    # optimize with scipy minimize (SLSQP method)
    result = minimize(weighting, x0, method="SLSQP", bounds=bounds, constraints=constraints)

    if result.success:
        print(f"\t{result.message}")
        print(f"\t{result.nit} amount of iterations performed.")

        print("\n\tInput values:")
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
    else:
        print(result.message)
        print("Optimization failed.")
        exit(-1)