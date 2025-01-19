from doctest import testfile

import numpy as np
from scipy.stats import qmc
from scipy.optimize import minimize
from resources.constraints import CONSTRAINTS
from control.formulae import init_vectors
from resources.constants_simulation import turnAngle, velocity, gravityAcceleration, airDensity


def ineq_constraints(x):
    turnIncline, mass, staticFriction, cdValue, frontArea = x

    (f_drag, f_velocity, f_new_velocity, f_centrifugal, f_gravity, f_gravity_parallel, f_neutral, f_road,
     f_static_friction, f_centripetal) = (
        init_vectors(turnIncline, mass, staticFriction, cdValue, frontArea, airDensity, velocity, turnAngle,
                     gravityAcceleration)
    )
    # inequality constraints g(x) >= 0 (conditions must be more than or equal to 0 to succeed)
    ineq_constraints = [
        # |f_centripetal| = |f_gravity_parallel + f_static_friction|
        #np.round(np.linalg.norm(f_centripetal) - np.linalg.norm(np.array(f_gravity_parallel) + np.array(f_static_friction))) ** 2 * (-1)

        # f_centrifugal = -f_centripetal | |f_centrifugal| = |f_centripetal|
        np.round(np.linalg.norm(np.array(f_centrifugal) + np.array(f_centripetal))) ** 2 * (-1),

        # f_road = -f_neutral
        np.round(np.linalg.norm(np.array(f_road) + np.array(f_neutral))) ** 2 * (-1),

        # |f_velocity| = |f_new_velocity|
        np.round(np.linalg.norm(f_velocity) - np.linalg.norm(f_new_velocity)) ** 2 * (-1),

        # f_velocity = -f_drag
        np.round(np.linalg.norm(np.array(f_velocity) + np.array(f_drag))) ** 2 * (-1),

        # f_velocity = f_new_velocity + f_centrifugal
        np.round(np.array(f_velocity) - np.array(f_new_velocity) - np.array(f_centrifugal)) ** 2 * (-1)

        # f_gravity = f_neutral + f_gravity_parallel
        #np.round(np.array(f_gravity) - np.array(f_neutral) - np.array(f_gravity_parallel)) ** 2 * (-1)
    ]
    return ineq_constraints


def constraints(x):
    g = ineq_constraints(x)  # retrieve constraints
    cons = [{'type': 'ineq', 'fun': lambda x, g_i=g_i: g_i} for g_i in g]  # inequality constraints: g(x) >= 0
    return cons


def objective(x):
    return 0


def findStartingValue(bounds):
    print("\tFinding starting value", end='')

    # using Latin Hypercube Sampling to sample points from the parameter space
    sampler = qmc.LatinHypercube(d=5)  # d=5 for 5 parameters
    num_samples = 99999
    sample = sampler.random(n=num_samples)
    lower_bounds = [b[0] for b in bounds]
    upper_bounds = [b[1] for b in bounds]
    assert len(lower_bounds) == len(upper_bounds) == 5, "Bounds should be defined for 5 parameters."
    assert all(
        lb < ub for lb, ub in zip(lower_bounds, upper_bounds)), "Each lower bound must be less than the upper bound."
    scaled_samples = qmc.scale(sample, lower_bounds, upper_bounds)

    for x0 in scaled_samples:
        cons = constraints(x0)  # construct constraints for the optimizer
        result = minimize(objective, x0, method="SLSQP", bounds=bounds, constraints=cons)  # optimization

        if result.success:
            print("\n\tStarting value found.")
            return x0  # return the feasible starting value
        else:
            print('.', end='')

    print("\n\tNo starting value found after sampling.")
    exit(-1)


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
    result = minimize(objective, x0, method="SLSQP", bounds=bounds, constraints=cons)

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