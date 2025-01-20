from mpmath import lu_solve

losening = 5

CONSTRAINTS = {
    # mass: 800-3000 [kg]
    "mass": (250 / losening, 3500 * losening), # considering a standard automobile

    # friction value
    "staticFriction": (0.5 / losening, 0.9 * losening), # considering rubber tires on asphalt during wet and dry conditions

    # air resistance coefficient
    "cdValue": (0.21 / losening, 0.7 * losening), # possible values of standard automobiles

    # front area of the car [m²]
    "frontArea": (0 / losening, 9 * losening), # possible values of standard automobiles up to 3 tons

    # air density [kg/m³]
    "airDensity": (0.829, 1.473), # (-20)-(80) degrees (celsius)

    # turn inclination [degrees]
    "turnIncline": (0, 80), # 0-80 degrees

    # turning angle  [degrees]
    "turnAngle": (0, 90), # 0-90 degrees

    # velocity [m/s]
    "velocity": (0, 69) # 0-250 km/h
}