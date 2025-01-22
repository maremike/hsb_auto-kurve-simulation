from control.validation import validate
from control.optimization import optimize
from control.simulation import simulate
from resources import variables
from view.wholeView import init_views

if __name__ == '__main__':
    validate()  # checks values for domains
    optimize()  # determines best values for the simulation
    simulate()  # Simulates and plots the behaviour

    # initializes views with two graphs. Focuses on the middle dataset, where the current vectors will be displayed
    init_views(variables.dataList, int(len(variables.dataList) / 2))
