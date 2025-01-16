import numpy as np

# simulation relevant constants:
turnAngle = 30 # [°]
velocity = 40.0 # [m/s]
airDensity = 1.2 # [kg/m³]
gravityAcceleration = 9.81 # gravity acceleration [m/s^2]

# standard values:
incrementDistance = 0.1 # increment [m]
incrementTime = 1 # time per simulation step [s]

# initialization
startPosition = np.array([0, 0, 0])