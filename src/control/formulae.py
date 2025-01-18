import numpy as np


def init_f_gravity(mass, gravityAcceleration):
    # vector points always down
    return [0, -1 * mass * gravityAcceleration, 0]


def init_f_neutral(turnIncline, f_gravity):
    # points towards the road
    return transform_vector([0, -np.cos(turnIncline) * np.linalg.norm(f_gravity), 0],
                                 0, 0, turnIncline)


def init_f_friction(f_neutral, staticFriction, turnIncline):  # parallel to the ground (not road)
    # vector points towards the curve (left of the car)
    return [-np.linalg.norm(f_neutral) * staticFriction * np.cos(turnIncline), 0, 0]


def init_f_centripetal(mass, velocity, radius, f_friction):  # parallel to the ground (not road)
    # vector points towards the curve (left of the car)
    return [-mass * velocity ** 2 / radius, 0, 0]


def init_f_drag(airDensity, cdValue, frontArea, velocity):
    # vector points towards the back of the car
    return [0, 0, 0.5 * airDensity * cdValue * frontArea * velocity ** 2]


def init_f_velocity(f_drag):
    return transform_vector(f_drag, 0, 180, 0)


def init_new_f_velocity(f_velocity, turnAngle):
    return transform_vector(f_velocity, 0, turnAngle, 0)


def init_new_f_centrifugal(f_velocity, f_new_velocity):
    return np.array(f_new_velocity) - np.array(f_velocity)


def get_radius(velocity, gravityAcceleration, turnIncline):
    return (velocity ** 2 / (gravityAcceleration * np.tan(turnIncline)))


def test(vector):
    return transform_vector(vector, 0, 90, 90)


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