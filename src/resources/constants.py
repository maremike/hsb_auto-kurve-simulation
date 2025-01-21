import numpy as np

# simulation relevant constants:
turnAngle = 40  # [deg]
velocity = 20  # [m/s]
wheelDistance = 3  # [m]
temperature = 20  # [deg celsius]

# pre-specified constants:
gravityAcceleration = 9.81  # [m/s^2] average
gasContent = 287.05  # [J/(kg*pK)] dry air
roadWidth = 3 # [m]

# standard values:
deltaT = 0.01  # time between simulation steps [s]
functionT = 400 #
inaccuracy_tolerance = 0.003
curveAngle = 90 # [deg]