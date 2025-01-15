import numpy as np

# simulation relevant constants:
turnAngle = 30 # [°]
velocity = 15.0 # [m/s]
airDensity = 1.2 # [kg/m³]

# standard values:
gravityAcceleration = 9.81 # gravity acceleration [m/s^2]
incrementDistance = 0.1 # increment [m]
incrementTime = 1 # time per simulation step [s]

# initialization
startPosition = np.array([0, 0, 0])