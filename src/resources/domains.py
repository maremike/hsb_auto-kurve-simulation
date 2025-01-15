import sympy
from sympy import Interval

# mass: 800-3000 [kg]
mass = Interval(800, 3000) # considering a standard automobile

# friction values
staticFriction = Interval(0.5, 0.9) # considering rubber tires on asphalt during wet and dry conditions
dynamicFriction = Interval(0.15, 0.3) # considering rubber tires on asphalt during wet and dry conditions

# air resistance coefficient
cdValue = Interval(0.21, 0.46) # possible values of standard automobiles

# front area of the car [m²]
frontArea = Interval(1.8, 3.4) # possible values of standard automobiles up to 3 tons

# air density [kg/m³]
airDensity = Interval(1.2922, 1.1455) # 0-35 degrees (celsius)

# turn inclination [degrees]
turnIncline = Interval(0, 89) # 0-89 degrees

# turning angle  [degrees]
turnAngle = Interval(0, 80) # 0-80 degrees

# velocity [m/s]
velocity = Interval(0, 42) # 0-150 km/h