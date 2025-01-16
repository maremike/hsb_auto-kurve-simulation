CONSTRAINTS = {
    # mass: 800-3000 [kg]
    "mass": (800, 3000), # considering a standard automobile

    # friction values
    "staticFriction": (0.5, 0.9), # considering rubber tires on asphalt during wet and dry conditions
    #"dynamicFriction": (0.15, 0.3), # considering rubber tires on asphalt during wet and dry conditions

    # air resistance coefficient
    "cdValue": (0.21, 0.46), # possible values of standard automobiles

    # front area of the car [m²]
    "frontArea": (1.8, 3.4), # possible values of standard automobiles up to 3 tons

    # air density [kg/m³]
    "airDensity": (1.1455, 1.2922), # 0-35 degrees (celsius)

    # turn inclination [degrees]
    "turnIncline": (1, 50), # 1-50 degrees

    # turning angle  [degrees]
    "turnAngle": (0, 60), # 0-60 degrees

    # velocity [m/s]
    "velocity": (0, 69) # 0-250 km/h
}