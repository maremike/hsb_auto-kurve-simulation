from control.validation import validate
from control.optimization import optimize
from control.simulation import simulate
from control.viewController import view

if __name__ == '__main__':
    validate()  # checks values for domains
    optimize()  # determines best values for the simulation
    simulate()  # Simulates and plots the behaviour
    view() # View the simulation