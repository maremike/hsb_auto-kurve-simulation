import numpy as np

# simulation relevant constants:
turnAngle = 40  # [deg]
velocity = 10  # [m/s]
wheelDistance = 2  # [m]
temperature = 20  # [deg celsius]

# pre-specified constants:
gravityAcceleration = 9.81  # [m/s^2] average
gasContent = 287.05  # [J/(kg*pK)] dry air
roadWidth = 4 # [m]

# optimization
WEIGHTS = {
    #"turnIncline": 1.0,
    "mass": 4.0, # prioritize minimizing mass
    #"staticFriction": 1.0,
    #"cdValue": 1.0,
    #"frontArea": 2.0, # minimize size
    #"atmosphericPressure": 1.0
}

# standard values:
deltaT = 0.1  # time between simulation steps [s]
scaleT = 2 # multiplies deltaT by this value to manipulate the simulation time
inaccuracy_tolerance = 0.001
