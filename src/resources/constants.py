import numpy as np

# simulation relevant constants:
turnAngle = 40  # [deg]
velocity = 10  # [m/s]
wheelDistance = 2  # [m]
temperature = 20  # [deg celsius]

# pre-specified constants:
gravityAcceleration = 9.81  # [m/s^2] average
gasContent = 287.05  # [J/(kg*pK)] dry air

# standard values:
deltaS = 0.1  # increment distance [m]
deltaT = 1  # time per simulation step [s]
inaccuracy_tolerance = 0.001

# initialization
currentPosition = [0, 0, 0]  # [x, y, z]
