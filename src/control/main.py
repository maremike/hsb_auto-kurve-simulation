import numpy as np

from control.validation import validate
from control.optimization import optimize
from control.simulation import simulate

if __name__ == "__main__":
    validate()  # checks values for domains
    optimize()  # determines best values for the simulation
    simulate()  # Simulates and plots the behaviour
