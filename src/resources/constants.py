import numpy as np

# simulation relevant constants:
turnAngle = 60  # [deg]
velocity = 20  # [m/s]
wheelDistance = 2  # [m]
temperature = 20  # [deg celsius]

# pre-specified constants:
gravityAcceleration = 9.81  # [m/s^2] average
gasContent = 287.05  # [J/(kg*pK)] dry air
roadWidth = 1 # [m]

# standard values:
deltaT = 0.01  # time between simulation steps [s]
functionT = 400 #
inaccuracy_tolerance = 0.001
curveAngle = 90 # [deg]