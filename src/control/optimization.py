import numpy as np
from scipy.stats import qmc
from scipy.optimize import minimize

from control.formulae import init_vectors, transform_vector
from resources import variables


def setOptimizationResults(turnIncline, mass, staticFriction, cdValue, frontArea, atmosphericPressure):
    """
    Sets the optimization results to global variables.

    Parameters:
        turnIncline (float): The turn incline (in degrees).
        mass (float): The mass of the vehicle (in kg).
        staticFriction (float): The static friction coefficient.
        cdValue (float): The drag coefficient.
        frontArea (float): The front area of the vehicle (in m²).
        atmosphericPressure (float): The atmospheric pressure (in Pa).

    Returns:
        None
    """
    # set results to global values
    variables.turnIncline = turnIncline
    variables.mass = mass
    variables.staticFriction = staticFriction
    variables.cdValue = cdValue
    variables.frontArea = frontArea
    variables.atmosphericPressure = atmosphericPressure

    (variables.f_drag, variables.f_velocity, variables.f_new_velocity, variables.f_centrifugal, variables.f_gravity,
     variables.f_gravity_parallel, variables.f_neutral, variables.f_road, variables.f_static_friction,
     variables.f_centripetal) = (
        init_vectors(turnIncline, mass, cdValue, frontArea, atmosphericPressure, variables.gasContent,
                     variables.temperature, variables.velocity, variables.turnAngle, variables.gravityAcceleration)
    )


def ineq_constraints(x):
    """
    Defines inequality constraints for the optimization process based on input parameters.

    Parameters:
        x (list): A list containing the parameters [turnIncline, mass, staticFriction, cdValue, frontArea, atmosphericPressure].

    Returns:
        list: A list of inequality constraints.
    """
    turnIncline, mass, staticFriction, cdValue, frontArea, atmosphericPressure = x

    # get forces
    (f_drag, f_velocity, f_new_velocity, f_centrifugal, f_gravity, f_gravity_parallel, f_neutral, f_road,
     f_static_friction, f_centripetal) = (
        init_vectors(turnIncline, mass, cdValue, frontArea, atmosphericPressure, variables.gasContent,
                     variables.temperature, variables.velocity, variables.turnAngle, variables.gravityAcceleration)
    )

    # |f_static_friction| = |f_neutral| * staticFriction (alternative: |f_static_friction| <= |f_neutral| * staticFriction)
    constraint0 = np.linalg.norm(f_static_friction) - np.linalg.norm(f_neutral) * staticFriction
    tolerance0 = np.linalg.norm(f_static_friction) * variables.inaccuracyTolerance

    # f_centripetal = f_gravity_parallel + f_static_friction
    constraint1 = np.linalg.norm(f_centripetal) - np.linalg.norm(
        np.array(f_gravity_parallel) + np.array(f_static_friction))
    tolerance1 = np.linalg.norm(f_centripetal) * variables.inaccuracyTolerance

    # f_road = -f_neutral
    constraint2 = np.linalg.norm(np.array(f_road) + np.array(f_neutral))
    tolerance2 = np.linalg.norm(f_road) * variables.inaccuracyTolerance

    # |f_velocity| = |f_new_velocity|
    constraint3 = np.linalg.norm(f_velocity) - np.linalg.norm(f_new_velocity)
    tolerance3 = np.linalg.norm(f_velocity) * variables.inaccuracyTolerance

    # f_velocity = -f_drag
    constraint4 = np.linalg.norm(np.array(f_velocity) + np.array(f_drag))
    tolerance4 = np.linalg.norm(f_velocity) * variables.inaccuracyTolerance

    # f_velocity = f_new_velocity + f_centrifugal
    constraint5 = np.linalg.norm(np.array(f_velocity) - np.array(f_new_velocity) - np.array(f_centrifugal))
    tolerance5 = np.linalg.norm(f_velocity) * variables.inaccuracyTolerance

    # f_gravity = f_neutral + f_gravity_parallel
    constraint6 = np.linalg.norm(np.array(f_gravity) - np.array(f_neutral) - np.array(f_gravity_parallel))
    tolerance6 = np.linalg.norm(f_gravity) * variables.inaccuracyTolerance

    # f_centripetal = -f_centrifugal
    constraint7 = np.linalg.norm(np.array(f_centripetal) + np.array(f_centrifugal))
    tolerance7 = np.linalg.norm(f_centripetal) * variables.inaccuracyTolerance

    # f_new_velocity x and y degrees to f_velocity
    constraint8 = np.linalg.norm(np.array(f_new_velocity) - np.array(transform_vector(np.array(transform_vector(
        np.array(f_velocity), 0, np.radians(variables.turnAngle), 0)), 0, 0, np.radians(turnIncline))))
    tolerance8 = np.linalg.norm(f_new_velocity) * variables.inaccuracyTolerance

    # arctan(f_gravity_parallel(y) / f_gravity_parallel(x)) = turnIncline
    constraint9 = np.arctan(f_gravity_parallel[1] / f_gravity_parallel[0]) - np.radians(turnIncline)
    tolerance9 = np.arctan(f_gravity_parallel[1] / f_gravity_parallel[0]) * variables.inaccuracyTolerance

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
    """
    Constructs constraints for the optimization process.

    Parameters:
        x (list): A list of input parameters for the optimization.

    Returns:
        list: A list of dictionaries representing inequality constraints.
    """
    g = ineq_constraints(x)  # retrieve constraints
    cons = [{'type': 'ineq', 'fun': lambda x, g_i=g_i: g_i} for g_i in g]  # add constraints
    return cons


def objective(x):
    """
    Defines the objective function for the optimization, which is a weighted sum of penalties.

    Parameters:
        x (list): A list of input parameters [turnIncline, mass, staticFriction, cdValue, frontArea, atmosphericPressure].

    Returns:
        float: The total penalty value to be minimized.
    """
    turnIncline, mass, staticFriction, cdValue, frontArea, atmosphericPressure = x

    # weighting factors for each parameter (higher weights give more priority)

    # penalties for each parameter (minimizing)
    mass_penalty = variables.weight_mass * mass
    staticFriction_penalty = variables.weight_staticFriction * staticFriction
    turnIncline_penalty = variables.weight_turnIncline * turnIncline
    cdValue_penalty = variables.weight_cdValue * cdValue
    frontArea_penalty = variables.weight_frontArea * frontArea
    atmosphericPressure_penalty = variables.weight_atmosphericPressure * atmosphericPressure

    # total objective function is a weighted sum of the penalties
    return (mass_penalty + staticFriction_penalty + turnIncline_penalty + cdValue_penalty + frontArea_penalty +
            atmosphericPressure_penalty)


def findStartingValue(bounds):
    """
    Finds a feasible starting point for the optimization process using Latin Hypercube Sampling.

    Parameters:
        bounds (list): The bounds for the optimization parameters.

    Returns:
        list: A feasible starting value for the optimization.
    """
    print("\tFinding starting value", end='')

    # using Latin Hypercube Sampling (LHS) to sample points from the parameter space
    sampler = qmc.LatinHypercube(d=6)  # amount of parameters
    num_samples = 4000  # number of samples
    sample = sampler.random(n=num_samples)

    # defining bounds
    lower_bounds = [b[0] for b in bounds]
    upper_bounds = [b[1] for b in bounds]
    assert len(lower_bounds) == len(upper_bounds) == 6, "Bounds should be defined for 6 parameters."
    assert all(
        lb < ub for lb, ub in zip(lower_bounds, upper_bounds)), "Each lower bound must be less than the upper bound."
    scaled_samples = qmc.scale(sample, lower_bounds, upper_bounds)

    tries = 1
    for x0 in scaled_samples:  # tries multiple starting values
        cons = constraints(x0)  # construct constraints for the optimizer
        result = minimize(objective, x0, method="SLSQP", bounds=bounds, constraints=cons)  # optimization

        if result.success:
            print("\n\tStarting value found.")
            return x0  # return the feasible starting value
        else:
            tries = tries + 1
            if (np.mod(tries, 40) == 0):
                print('.', end='')

    print(f"\n\tNo starting value found after {num_samples} samples.")
    exit(-1)


def get_bounds(constraints):
    """
    Extracts the bounds for each optimization parameter from the constraint definitions.

    Parameters:
        constraints (dict): A dictionary of constraints for each parameter.

    Returns:
        list: A list of tuples representing the bounds for each parameter.
    """
    return [(constraints["turnIncline"][0], constraints["turnIncline"][1]),
            (constraints["mass"][0], constraints["mass"][1]),
            (constraints["staticFriction"][0], constraints["staticFriction"][1]),
            (constraints["cdValue"][0], constraints["cdValue"][1]),
            (constraints["frontArea"][0], constraints["frontArea"][1]),
            (constraints["atmosphericPressure"][0], constraints["atmosphericPressure"][1])]


def optimize():
    """
    Performs the optimization process for the vehicle parameters.

    Returns:
        None
    """
    print("Optimizing values...")

    # create bounds
    bounds = get_bounds(variables.CONSTRAINTS)

    # find starting value
    x0 = findStartingValue(bounds)

    # create constraints
    cons = constraints(x0)

    # optimize with scipy minimize (SLSQP method)
    result = minimize(objective, x0, method="SLSQP", bounds=bounds, constraints=cons)

    if result.success:
        print(f"\t{result.message}.")

        print("\n\tInput values:")
        print("\tTurn angle [deg]:", variables.turnAngle)
        print("\tVelocity [m/s]:", variables.velocity)
        print("\tTemperature [celsius]:", variables.temperature)

        print("\n\tOther values:")
        print("\tGravity acceleration [m/s²]:", variables.gravityAcceleration)
        print("\tInaccuracy tolerance: ", variables.inaccuracyTolerance)
        print("\tGas content [J/(kg*pK)]: ", variables.gasContent)

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