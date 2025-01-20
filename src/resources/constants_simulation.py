import numpy as np

# simulation relevant constants:
turnAngle = 15 # [°]
velocity = 30 # [m/s]
gravityAcceleration = 9.81 # gravity acceleration [m/s^2]

# standard values:
deltaS = 0.1 # increment distance [m]
deltaT = 1 # time per simulation step [s]

# initialization
currentPosition = [0, 0, 0] # [x, y, z]