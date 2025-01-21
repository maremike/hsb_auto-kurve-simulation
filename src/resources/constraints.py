CONSTRAINTS = {
    # mass [kg]
    "mass": (800, 3500),  # considering a standard automobile 800-3500

    # friction value
    "staticFriction": (0.5, 0.9),  # considering rubber tires on asphalt during wet and dry conditions

    # air resistance coefficient
    "cdValue": (0.21, 0.45),  # values of various modern standard automobiles

    # front area of the car [m²]
    "frontArea": (2, 5),  # values of standard automobiles up to 3.5 tons

    # turn inclination [degrees]
    "turnIncline": (0, 60),  # 0-60 degrees

    # turning angle  [degrees]
    "turnAngle": (0, 80),  # 0-80 degrees

    # velocity [m/s]
    "velocity": (0, 69),  # 0-250 km/h

    # atmospheric pressure [Pa]
    "atmosphericPressure": (900, 1050), # minimum and maximum values for air pressure on earth

    # temperature [celsius]
    "temperature": (0, 50) # 0-50 degrees celsius
}
