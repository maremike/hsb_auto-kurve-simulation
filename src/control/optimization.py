import numpy as np
from scipy.stats import qmc
from scipy.optimize import minimize

from control.simulation import setOptimizationResults
from resources.constraints import CONSTRAINTS
from control.formulae import init_vectors, transform_vector
from resources.constants import turnAngle, velocity, gravityAcceleration, inaccuracy_tolerance, temperature, gasContent


def ineq_constraints(x):
    turnIncline, mass, staticFriction, cdValue, frontArea, atmosphericPressure = x

    # get forces
    (f_drag, f_velocity, f_new_velocity, f_centrifugal, f_gravity, f_gravity_parallel, f_neutral, f_road,
     f_static_friction, f_centripetal) = (
        init_vectors(turnIncline, mass, cdValue, frontArea, atmosphericPressure, gasContent, temperature, velocity,
                     turnAngle, gravityAcceleration)
    )

    # |f_static_friction| = |f_neutral| * staticFriction (alternative: |f_static_friction| <= |f_neutral| * staticFriction)
    constraint0 = np.linalg.norm(f_static_friction) - np.linalg.norm(f_neutral) * staticFriction
    tolerance0 = np.linalg.norm(f_static_friction) * inaccuracy_tolerance

    # f_centripetal = f_gravity_parallel + f_static_friction
    constraint1 = np.linalg.norm(f_centripetal) - np.linalg.norm(
        np.array(f_gravity_parallel) + np.array(f_static_friction))
    tolerance1 = np.linalg.norm(f_centripetal) * inaccuracy_tolerance

    # f_road = -f_neutral
    constraint2 = np.linalg.norm(np.array(f_road) + np.array(f_neutral))
    tolerance2 = np.linalg.norm(f_road) * inaccuracy_tolerance

    # |f_velocity| = |f_new_velocity|
    constraint3 = np.linalg.norm(f_velocity) - np.linalg.norm(f_new_velocity)
    tolerance3 = np.linalg.norm(f_velocity) * inaccuracy_tolerance

    # f_velocity = -f_drag
    constraint4 = np.linalg.norm(np.array(f_velocity) + np.array(f_drag))
    tolerance4 = np.linalg.norm(f_velocity) * inaccuracy_tolerance

    # f_velocity = f_new_velocity + f_centrifugal
    constraint5 = np.linalg.norm(np.array(f_velocity) - np.array(f_new_velocity) - np.array(f_centrifugal))
    tolerance5 = np.linalg.norm(f_velocity) * inaccuracy_tolerance

    # f_gravity = f_neutral + f_gravity_parallel
    constraint6 = np.linalg.norm(np.array(f_gravity) - np.array(f_neutral) - np.array(f_gravity_parallel))
    tolerance6 = np.linalg.norm(f_gravity) * inaccuracy_tolerance

    # f_centripetal = -f_centrifugal
    constraint7 = np.linalg.norm(np.array(f_centripetal) + np.array(f_centrifugal))
    tolerance7 = np.linalg.norm(f_centripetal) * inaccuracy_tolerance

    # f_new_velocity x and y degrees to f_velocity
    constraint8 = np.linalg.norm(np.array(f_new_velocity) - np.array(transform_vector(np.array(transform_vector(
        np.array(f_velocity), 0, np.radians(turnAngle), 0)), 0, 0, np.radians(turnIncline))))
    tolerance8 = np.linalg.norm(f_new_velocity) * inaccuracy_tolerance

    # arctan(f_gravity_parallel(y) / f_gravity_parallel(x)) = turnIncline
    constraint9 = np.arctan(f_gravity_parallel[1] / f_gravity_parallel[0]) - np.radians(turnIncline)
    tolerance9 = np.arctan(f_gravity_parallel[1] / f_gravity_parallel[0]) * inaccuracy_tolerance

    # inequality constraints g(x) >= 0 (conditions must be more than or equal to 0 to succeed)
    ineq_constraints = [
        (np.abs(constraint0) - tolerance0) * (-1),
        (np.abs(constraint1) - tolerance1) * (-1),
        (np.abs(constraint2) - tolerance2) * (-1),
        (np.abs(constraint3) - tolerance3) * (-1),
        (np.abs(constraint4) - tolerance4) * (-1),
        (np.abs(constraint5) - tolerance5) * (-1),
        (np.abs(constraint6) - tolerance6) * (-1),
        (np.abs(constraint7) - tolerance7) * (-1),
        (np.abs(constraint8) - tolerance8) * (-1),
        (np.abs(constraint9) - tolerance9) * (-1)
    ]
    return ineq_constraints


def constraints(x):
    g = ineq_constraints(x)  # retrieve constraints
    cons = [{'type': 'ineq', 'fun': lambda x, g_i=g_i: g_i} for g_i in g] # add constraints
    return cons


def objective(x):
    turnIncline, mass, staticFriction, cdValue, frontArea, atmosphericPressure = x

    # weighting factors for each parameter (higher weights give more priority)
    weight_mass = 1
    weight_staticFriction = 0
    weight_turnIncline = 0
    weight_cdValue = 0
    weight_frontArea = 0.5
    weight_atmosphericPressure = 0

    # penalties for each parameter (minimizing)
    mass_penalty = weight_mass * mass
    staticFriction_penalty = weight_staticFriction * staticFriction
    turnIncline_penalty = weight_turnIncline * turnIncline
    cdValue_penalty = weight_cdValue * cdValue
    frontArea_penalty = weight_frontArea * frontArea
    atmosphericPressure_penalty = weight_atmosphericPressure * atmosphericPressure

    # total objective function is a weighted sum of the penalties
    return (mass_penalty + staticFriction_penalty + turnIncline_penalty + cdValue_penalty + frontArea_penalty +
            atmosphericPressure_penalty)


def findStartingValue(bounds):
    print("\tFinding starting value", end='')

    # using Latin Hypercube Sampling (LHS) to sample points from the parameter space
    sampler = qmc.LatinHypercube(d=6) # amount of parameters
    num_samples = 4000 # number of samples
    sample = sampler.random(n=num_samples)

    # defining bounds
    lower_bounds = [b[0] for b in bounds]
    upper_bounds = [b[1] for b in bounds]
    assert len(lower_bounds) == len(upper_bounds) == 6, "Bounds should be defined for 6 parameters."
    assert all(
        lb < ub for lb, ub in zip(lower_bounds, upper_bounds)), "Each lower bound must be less than the upper bound."
    scaled_samples = qmc.scale(sample, lower_bounds, upper_bounds)

    tries = 1
    for x0 in scaled_samples: # tries multiple starting values
        cons = constraints(x0)  # construct constraints for the optimizer
        result = minimize(objective, x0, method="SLSQP", bounds=bounds, constraints=cons) # optimization

        if result.success:
            print("\n\tStarting value found.")
            return x0  # return the feasible starting value
        else:
            tries = tries + 1
            if (np.mod(tries, 40) == 0):
                print('.', end='')

    print(f"\n\tNo starting value found after {num_samples} samples.")
    exit(-1)


def optimize():
    print("Optimizing values...")

    # create bounds
    bounds = [
        (CONSTRAINTS["turnIncline"][0], CONSTRAINTS["turnIncline"][1]),
        (CONSTRAINTS["mass"][0], CONSTRAINTS["mass"][1]),
        (CONSTRAINTS["staticFriction"][0], CONSTRAINTS["staticFriction"][1]),
        (CONSTRAINTS["cdValue"][0], CONSTRAINTS["cdValue"][1]),
        (CONSTRAINTS["frontArea"][0], CONSTRAINTS["frontArea"][1]),
        (CONSTRAINTS["atmosphericPressure"][0], CONSTRAINTS["atmosphericPressure"][1])
    ]

    # find starting value
    x0 = findStartingValue(bounds)

    # create constraints
    cons = constraints(x0)

    # optimize with scipy minimize (SLSQP method)
    result = minimize(objective, x0, method="SLSQP", bounds=bounds, constraints=cons)

    if result.success:
        print(f"\t{result.message}.")

        print("\n\tInput values:")
        print("\tTurn angle [deg]:", turnAngle)
        print("\tVelocity [m/s]:", velocity)
        print("\tTemperature [celsius]:", temperature)

        print("\n\tOther values:")
        print("\tGravity acceleration [m/s²]:", gravityAcceleration)
        print("\tInaccuracy tolerance: ", inaccuracy_tolerance)
        print("\tGas content [J/(kg*pK)]: ", gasContent)

        print("\n\tOutput values:")
        print("\tTurn incline [deg]:", result.x[0])
        print("\tMass [kg]:", result.x[1])
        print("\tStatic friction:", result.x[2])
        print("\tCd-Value:", result.x[3])
        print("\tFront area [m²]:", result.x[4])
        print("\tAtmospheric pressure [Pa]:", result.x[5])

        setOptimizationResults(result.x[0], result.x[1], result.x[2], result.x[3], result.x[4], result.x[5])

        print(f"Optimization finished.")
    else:
        print(f"\t{result.message}.")
        print("Optimization failed.")
        exit(-1)