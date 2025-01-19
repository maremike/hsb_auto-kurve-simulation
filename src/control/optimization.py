from doctest import testfile

import numpy as np
from scipy.optimize import minimize
from resources.constraints import CONSTRAINTS
from control.formulae import init_f_drag, init_f_friction, init_f_gravity, \
    init_f_neutral, \
    init_f_velocity, init_new_f_velocity, init_new_f_centrifugal, init_f_centripetal2, init_f_centripetal1, get_radius
from resources.constants_simulation import turnAngle, velocity, gravityAcceleration, airDensity


def ineq_constraints(x):
    turnIncline, mass, staticFriction, cdValue, frontArea = x

    f_drag = init_f_drag(airDensity, cdValue, frontArea, velocity)
    f_gravity = init_f_gravity(mass, gravityAcceleration)
    f_neutral = init_f_neutral(turnIncline, f_gravity)
    f_friction = init_f_friction(f_neutral, staticFriction, turnIncline)
    radius = get_radius(velocity, gravityAcceleration, turnIncline)
    f_centripetal = init_f_centripetal1(mass, velocity, radius)
    f_centripetal2 = init_f_centripetal2(f_gravity, f_neutral)
    f_velocity = init_f_velocity(f_drag)
    f_new_velocity = init_new_f_velocity(f_velocity, turnAngle)
    f_centrifugal = init_new_f_centrifugal(f_velocity, f_new_velocity)

    # inequality constraints g(x) >= 0 (conditions must be more than or equal to 0 to succeed)
    ineq_constraints = [
        turnIncline - (CONSTRAINTS["turnIncline"][0]), # turnIncline >= lower bound
        (CONSTRAINTS["turnIncline"][1]) - turnIncline, # turnIncline <= upper bound
        frontArea - (CONSTRAINTS["frontArea"][0]), # frontArea >= lower bound
        (CONSTRAINTS["frontArea"][1]) - frontArea, # frontArea <= upper bound
        cdValue - (CONSTRAINTS["cdValue"][0]), # cdValue >= lower bound
        (CONSTRAINTS["cdValue"][1]) - cdValue, # cdValue <= upper bound
        mass - (CONSTRAINTS["mass"][0]), # mass >= lower bound
        (CONSTRAINTS["mass"][1]) - mass, # mass <= upper bound
        staticFriction - (CONSTRAINTS["staticFriction"][0]), # staticFriction >= lower bound
        (CONSTRAINTS["staticFriction"][1]) - staticFriction, # staticFriction <= upper bound
        (np.linalg.norm(f_gravity) - np.linalg.norm(np.array(f_neutral) + np.array(f_centripetal))) ** 2 * -1, # |f_gravity| = |f_neutral + f_centripetal|
        np.linalg.norm(f_centripetal) - np.linalg.norm(f_centrifugal), # |f_centripetal| >= |f_centrifugal|
        #np.linalg.norm(f_centripetal) - np.linalg.norm(np.array(f_drag) + np.array(f_friction)) # |f_centripetal| = |f_drag + f_friction|
    ]
    return ineq_constraints


def eq_constraints(x):
    turnIncline, mass, staticFriction, cdValue, frontArea = x

    f_drag = init_f_drag(airDensity, cdValue, frontArea, velocity)
    f_gravity = init_f_gravity(mass, gravityAcceleration)
    f_neutral = init_f_neutral(turnIncline, f_gravity)
    f_friction = init_f_friction(f_neutral, staticFriction, turnIncline)
    f_centripetal = init_f_centripetal2(f_gravity, f_neutral)
    f_velocity = init_f_velocity(f_drag)
    f_new_velocity = init_new_f_velocity(f_velocity, turnAngle)
    f_centrifugal = init_new_f_centrifugal(f_velocity, f_new_velocity)

    # equality constraints: h(x) = 0 (conditions must be equal to 0 to succeed)
    eq_constraints = [
        np.linalg.norm(f_centripetal) - np.linalg.norm(f_centrifugal), # |f_centripetal| >= |f_centrifugal|
        np.linalg.norm(f_centripetal) - np.linalg.norm(np.array(f_drag) + np.array(f_friction)), # |f_centripetal| = |f_drag + f_friction|
        np.linalg.norm(f_gravity) - np.linalg.norm(np.array(f_neutral) + np.array(f_centripetal)) # |f_gravity| = |f_neutral + f_centripetal|
    ]

    return eq_constraints


def weighting(x):
    turnIncline, mass, staticFriction, cdValue, frontArea = x

    w1, w2, w3, w4 = 1, 1, 1, 1  # weight
    return w1 * mass + w2 * cdValue + w3 * frontArea + w4 * staticFriction  # following values should be as low as possible


def findStartingValue(bounds):
    print("\tFinding starting value", end='')

    turn_incline_range = np.arange(CONSTRAINTS["turnIncline"][0], CONSTRAINTS["turnIncline"][1], 0.1)
    mass_range = np.arange(CONSTRAINTS["mass"][0], CONSTRAINTS["mass"][1], 0.1)
    static_friction_range = np.arange(CONSTRAINTS["staticFriction"][0], CONSTRAINTS["staticFriction"][1], 0.1)
    cd_value_range = np.arange(CONSTRAINTS["cdValue"][0], CONSTRAINTS["cdValue"][1], 0.1)
    front_area_range = np.arange(CONSTRAINTS["frontArea"][0], CONSTRAINTS["frontArea"][1], 0.1)

    # iterate through all combinations of constraint values
    for i in turn_incline_range:
        for j in mass_range:
            for k in static_friction_range:
                for l in cd_value_range:
                    for m in front_area_range:
                        x0 = [i, j, k, l, m]
                        cons = constraints(x0) # construct constraints for the optimizer
                        result = minimize(weighting, x0, method="SLSQP", bounds=bounds, constraints=cons) # perform optimization

                        if result.success:
                            print("\n\tStarting value found.")
                            return x0  # return the feasible starting value
                        else:
                            print('.', end='')

    # If no feasible starting value is found
    print("\n\tOptimization failed. No feasible starting value found.")
    exit(-1)


def constraints(x):
    g = ineq_constraints(x) # retrieve constraints

    cons= [{'type': 'ineq', 'fun': lambda x, g_i=g_i: g_i} for g_i in g] # inequality constraints: g(x) >= 0
    #constraints.extend({'type': 'eq', 'fun': lambda x, h_i=h_i: h_i} for h_i in h) # equality constraints: h(x) = 0

    return cons


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

    # find starting value
    x0 = findStartingValue(bounds)

    # create constraints
    cons = constraints(x0)

    # optimize with scipy minimize (SLSQP method)
    result = minimize(weighting, x0, method="SLSQP", bounds=bounds, constraints=cons)

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
        print(f"\t{result.message}")
        print("Optimization failed.")
        exit(-1)