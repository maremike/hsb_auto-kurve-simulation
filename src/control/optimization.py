import bounds
import numpy as np
import sympy as sp
from scipy.optimize import minimize

from resources.constraints import CONSTRAINTS
from resources.constants_simulation import turnAngle, velocity, gravityAcceleration


def extract_intervals(domain_module):
    """
    Extracts interval values from the given domain module.
    """
    return {
        name: value for name, value in vars(domain_module).items()
        if isinstance(value, sp.Interval)
    }

# Nebenbedingungen
def constraint1(x, turnAngle, v):
    alpha, m, mu_H, cw, A, rho = x
    r = 2.5 / np.tan(turnAngle)  # Radstand angenommen als 2.5 m
    F_z = m * v**2 / r
    F_H = mu_H * m * gravityAcceleration * np.cos(alpha)
    F_neigung = m * gravityAcceleration * np.sin(alpha)
    return F_H + F_neigung - F_z

# Zielfunktion
def objective(x):
    alpha, m, mu_H, cw, A, rho = x
    w1, w2, w3, w4 = 1, 1, 1, 1  # Gewichtungen
    return w1 * m + w2 * cw + w3 * A + w4 * mu_H

def optimize():
    print("Optimizing values...")

    # Extract intervals for bounds
    domain_intervals = extract_intervals(CONSTRAINTS)

    # Map the intervals to bounds for optimization
    bounds = [
        (domain_intervals["turnIncline"].start, domain_intervals["turnIncline"].end),
        (domain_intervals["mass"].start, domain_intervals["mass"].end),
        (domain_intervals["staticFriction"].start, domain_intervals["staticFriction"].end),
        (domain_intervals["cdValue"].start, domain_intervals["cdValue"].end),
        (domain_intervals["frontArea"].start, domain_intervals["frontArea"].end),
        (domain_intervals["airDensity"].start, domain_intervals["airDensity"].end),
    ]

    # Starting values
    x0 = [0.1, 1000, 1.0, 0.3, 2.0, 1.2]  # First guess

    # Optimization
    constraints = [{"type": "ineq", "fun": constraint1, "args": (turnAngle, velocity)}]
    result = minimize(objective, x0, method="SLSQP", bounds=list(bounds.values()), constraints=constraints)

    # Ergebnisse
    print("\tOptimale Werte:")
    print("\tNeigungswinkel (rad):", result.x[0])
    print("\tMasse (kg):", result.x[1])
    print("\tHaftreibungskonstante:", result.x[2])
    print("\tcw-Wert:", result.x[3])
    print("\tFrontalfläche (m^2):", result.x[4])
    print("\tLuftdruck (kg/m^3):", result.x[5])

    print("Optimization finished.")