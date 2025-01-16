import numpy as np
import sympy as sp
from scipy.optimize import minimize

from resources.constraints import CONSTRAINTS
from control.formulae import get_f_drag, get_f_friction, get_f_centripetal, get_radius, get_f_gravity, get_f_neutral, \
    get_f_velocity, get_new_f_velocity

from resources.constraints import CONSTRAINTS
from resources.constants_simulation import turnAngle, velocity, gravityAcceleration, airDensity

import numpy as np
from scipy.optimize import minimize

def conditions(x, turnAngle, velocity, airDensity, gravityAcceleration):
    turnIncline, mass, staticFriction, cdValue, frontArea = x # todo: more variables (center of mass, wheel distance)

    f_drag = get_f_drag(airDensity, cdValue, frontArea, velocity)
    f_gravity = get_f_gravity(mass, gravityAcceleration)
    f_neutral = get_f_neutral(turnIncline, f_gravity)
    f_friction = get_f_friction(f_neutral, staticFriction, turnIncline)
    f_centripetal = get_f_centripetal(mass, velocity, get_radius(velocity, gravityAcceleration, turnIncline), f_friction)
    f_velocity = get_f_velocity(f_drag)
    f_new_velocity = get_new_f_velocity(f_velocity, turnAngle)
    f_centrifugal = f_new_velocity - f_velocity

    # inequality constraints g(x) >= 0 (conditions must be more than or equal to 0 to succeed)
    playroom = 1
    return [
        turnIncline - (CONSTRAINTS["turnIncline"][0] / playroom), # turnIncline >= lower bound
        (CONSTRAINTS["turnIncline"][1] * playroom) - turnIncline, # turnIncline <= upper bound
        frontArea - (CONSTRAINTS["frontArea"][0] / playroom), # frontArea >= lower bound
        (CONSTRAINTS["frontArea"][1] * playroom) - frontArea, # frontArea <= upper bound
        cdValue - (CONSTRAINTS["cdValue"][0] / playroom), # cdValue >= lower bound
        (CONSTRAINTS["cdValue"][1] * playroom) - cdValue, # cdValue <= upper bound
        mass - (CONSTRAINTS["mass"][0] / playroom), # mass >= lower bound
        (CONSTRAINTS["mass"][1] * playroom) - mass, # mass <= upper bound
        staticFriction - (CONSTRAINTS["staticFriction"][0] / playroom), # staticFriction >= lower bound
        (CONSTRAINTS["staticFriction"][1] * playroom) - staticFriction, # staticFriction <= upper bound
        np.linalg.norm(f_centripetal) - np.linalg.norm(f_centrifugal), # |f_centripetal| >= |f_centrifugal|
        np.linalg.norm(f_centripetal) - np.linalg.norm(f_drag + f_friction), # |f_centripetal| = |f_drag + f_friction|
        np.linalg.norm(f_gravity) - np.linalg.norm(f_neutral + f_centripetal) # |f_gravity| = |f_neutral + f_centripetal|
    ]

def weighting(x):
    turnIncline, mass, staticFriction, cdValue, frontArea = x

    w1, w2, w3, w4 = 1, 1, 1, 1  # weight
    return w1 * mass + w2 * cdValue + w3 * frontArea + w4 * staticFriction # following values should be as low as possible

def findStartingValue(bounds, constraints):
    print("\tFinding starting value", end='')
    for i in CONSTRAINTS["turnIncline"]:
        for j in CONSTRAINTS["mass"]:
            for k in CONSTRAINTS["staticFriction"]:
                for l in CONSTRAINTS["cdValue"]:
                    for m in CONSTRAINTS["frontArea"]:
                        x0 = [i, j, k, l, m]
                        result = minimize(weighting, x0, method="SLSQP", bounds=bounds, constraints=constraints)
                        if result.success:
                            print("\n\tStarting value found.")
                            return x0
                        else:
                            print('.', end='')

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
    constraints = [{"type": "ineq", "fun": conditions, "args": (turnAngle, velocity, airDensity, gravityAcceleration)}]

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