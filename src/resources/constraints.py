from mpmath import lu_solve

losening = 2

CONSTRAINTS = {
    # mass: 800-3000 [kg]
    "mass": (800 / losening, 3000 * losening), # considering a standard automobile

    # friction values
    "staticFriction": (0.5 / losening, 0.9 * losening), # considering rubber tires on asphalt during wet and dry conditions
    #"dynamicFriction": (0.15, 0.3), # considering rubber tires on asphalt during wet and dry conditions

    # air resistance coefficient
    "cdValue": (0.21 / losening, 0.46 * losening), # possible values of standard automobiles

    # front area of the car [m²]
    "frontArea": (1.8 / losening, 3.4 * losening), # possible values of standard automobiles up to 3 tons

    # air density [kg/m³]
    "airDensity": (1.1455 / losening, 1.2922 * losening), # 0-35 degrees (celsius)

    # turn inclination [degrees]
    "turnIncline": (1 / losening, 50 * losening), # 1-50 degrees

    # turning angle  [degrees]
    "turnAngle": (0 / losening, 60 * losening), # 0-60 degrees

    # velocity [m/s]
    "velocity": (0 / losening, 69 * losening) # 0-250 km/h
}