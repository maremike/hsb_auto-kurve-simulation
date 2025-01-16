import numpy as np


def get_f_drag(airDensity, cdValue, frontArea, velocity):
    return (0.5 * airDensity * cdValue * frontArea * velocity**2)

def get_f_friction(f_neutral, staticFriction):
    return (f_neutral * staticFriction)

def get_f_centripetal(mass, velocity, radius):
    return (mass * velocity**2 / radius)

def get_f_gravity(mass, gravityAcceleration):
    return (mass * gravityAcceleration)

def get_radius(velocity, gravityAcceleration, turnIncline):
    return (velocity**2 / (gravityAcceleration * np.tan(turnIncline)))

def get_f_neutral(turnIncline, f_gravity):
    return (np.cos(turnIncline) * f_gravity)