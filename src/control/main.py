from control.validation import validate
from control.optimization import optimize
from control.simulation import simulate
from model import variables
from view.wholeView import init_views

"""
To whomever it may concern,

This code is part of a task for the course HMINF (WiSe 2024/2025) at the Hochschule Bremen (HSB). 
The coordinator is Prof. Dr. Patrick Draheim.

This is my work. It is a simulation which based on the input parameters, optimizes the remaining ones and simulates a 
car traversing an inclined turn. The parameters may be adjusted in the configuration file, allowing for the simulation 
of diverse vehicles and various types of curves. The program makes use of three dimensional space, and vector rotations.

The chief input parameters, which may be altered to change the result, are the velocity at which the car moves around 
the curve and the turnAngle between the front and rear tires, which arises due to the turn. Moreover, the temperature 
of the surrounding air may be modified as well. But beware, if you change the range, the realism will estrange.

Lastly, upon the completion of the simulation, the program presents a window displaying the course of the simulation. 
It reveals a particular span of time, during which the vectors did point in their respective directions.

Signed, Michael Markov (mmarkov)

January 22, 2025
"""

if __name__ == '__main__':
    validate()  # checks values for domains
    optimize()  # determines best values for the simulation
    simulate()  # Simulates and plots the behaviour

    # initializes views with two graphs. Focuses on the middle dataset, where the current vectors will be displayed
    init_views(variables.dataList, int(len(variables.dataList) / 2))
