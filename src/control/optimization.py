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

    f_drag = 0.5 * airDensity * cdValue * frontArea * velocity**2
    f_friction = mass * gravityAcceleration * staticFriction
    radius = velocity**2 / (gravityAcceleration * np.tan(turnIncline))
    f_centripetal = mass * velocity**2 / radius
    f_gravity = mass * gravityAcceleration
    f_centrifugal = f_centripetal
    f_velocity = f_drag

    # inequality constraints g(x) >= 0 (conditions must be more than or equal to 0 to succeed)
    return [
        #f_friction - f_centripetal,  # Ensure friction can sustain the turn
        #turnIncline - CONSTRAINTS["turnIncline"][0],  # turnIncline >= lower bound
        #CONSTRAINTS["turnIncline"][1] - turnIncline,  # turnIncline <= upper bound
        #frontArea - CONSTRAINTS["frontArea"][0],  # frontArea >= lower bound
        #CONSTRAINTS["frontArea"][1] - frontArea,  # frontArea <= upper bound
        #cdValue - CONSTRAINTS["cdValue"][0],  # cdValue >= lower bound
        #CONSTRAINTS["cdValue"][1] - cdValue,  # cdValue <= upper bound
        #mass - CONSTRAINTS["mass"][0],  # mass >= lower bound
        #CONSTRAINTS["mass"][1] - mass,  # mass <= upper bound
        #staticFriction - CONSTRAINTS["staticFriction"][0],  # staticFriction >= lower bound
        #CONSTRAINTS["staticFriction"][1] - staticFriction  # staticFriction <= upper bound
    ]


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