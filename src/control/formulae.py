import numpy as np


def init_f_gravity(mass, gravityAcceleration):
    # vector points always down
    return np.array([0, -1 * mass * gravityAcceleration, 0])


def init_f_neutral(turnIncline, f_gravity):
    # points towards the road
    vector = np.array(transform_vector(
        [0, (-1) * (np.linalg.norm(f_gravity) / np.cos(np.radians(turnIncline))), 0],
        0, 0, turnIncline))
    return vector


def init_f_friction(f_neutral, staticFriction, turnIncline):  # parallel to the ground (not road)
    # vector points towards the curve (left of the car)
    return np.array([-np.linalg.norm(f_neutral) * staticFriction * np.cos(np.radians(turnIncline)), 0, 0])


def init_f_centripetal_gravity(f_gravity, f_neutral):  # parallel to the ground (not road)
    # vector points towards the curve (left of the car)
    return (np.array(f_gravity) - np.array(f_neutral))


def init_f_centripetal_curve(mass, velocity, radius):
    return np.array([-1 * mass * velocity ** 2 / radius, 0, 0])


def init_f_drag(airDensity, cdValue, frontArea, velocity):
    # vector points towards the back of the car
    return np.array([0, 0, 0.5 * airDensity * cdValue * frontArea * velocity ** 2])


def init_f_velocity(f_drag):
    return np.array(transform_vector(f_drag, 0, 180, 0))


def init_new_f_velocity(f_velocity, turnAngle):
    return np.array(transform_vector(f_velocity, 0, turnAngle, 0))


def init_new_f_centrifugal(f_velocity, f_new_velocity):
    return (np.array(f_velocity) - np.array(f_new_velocity))


def get_radius(velocity, gravityAcceleration, turnIncline):
    return (velocity ** 2 / (gravityAcceleration * np.tan(np.radians(turnIncline))))


def rotation_matrix(pitch, yaw, roll):  # pitch = x, yaw = y, roll = z (clockwise)
    # Convert angles to radians
    yaw, pitch, roll = np.radians([yaw, pitch, roll])

    # Rotation matrices
    R_x = np.array([
        [1, 0, 0],
        [0, np.cos(pitch), -np.sin(pitch)],
        [0, np.sin(pitch), np.cos(pitch)]
    ])

    R_y = np.array([
        [np.cos(yaw), 0, np.sin(yaw)],
        [0, 1, 0],
        [-np.sin(yaw), 0, np.cos(yaw)]
    ])

    R_z = np.array([
        [np.cos(roll), -np.sin(roll), 0],
        [np.sin(roll), np.cos(roll), 0],
        [0, 0, 1]
    ])

    # Combined rotation matrix
    return R_z @ R_y @ R_x

def transform_vector(vector, pitch, yaw, roll):  # pitch = x, yaw = y, roll = z (clockwise)
    R = rotation_matrix(pitch, yaw, roll)
    return R @ vector