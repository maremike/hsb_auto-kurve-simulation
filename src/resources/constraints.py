CONSTRAINTS = {
    # mass [kg]
    "mass": (800, 1500),  # considering a standard automobile 800-3500

    # friction value
    "staticFriction": (0.5, 0.9),  # considering rubber tires on asphalt during wet and dry conditions

    # air resistance coefficient
    "cdValue": (0.28, 0.41),  # values of various modern standard automobiles

    # front area of the car [m²]
    "frontArea": (2.5, 3.7),  # values of standard automobiles

    # turn inclination [degrees]
    "turnIncline": (0, 30),  # 0-30 degrees

    # turning angle  [degrees]
    "turnAngle": (1, 40),  # 1-40 degrees

    # velocity [m/s]
    "velocity": (0, 23),  # 0-80 km/h

    # atmospheric pressure [Pa]
    "atmosphericPressure": (950, 1000), # minimum and maximum average values for air pressure on earth

    # temperature [celsius]
    "temperature": (5, 30) # 5-30 degrees celsius
}
