import numpy as np

from resources.constants_simulation import currentPosition


def get_f_gravity(mass, gravityAcceleration):
    # vector points always down
    return [0, -1 * mass * gravityAcceleration, 0]


def get_f_neutral(turnIncline, f_gravity):
    # points towards the road
    return get_vectorOrientation(np.cos(turnIncline) * np.linalg.norm(f_gravity),
                                 currentPosition[3] + 90, currentPosition[4] + 0, currentPosition[5] - turnIncline)


def get_f_drag(airDensity, cdValue, frontArea, velocity):
    # vector points towards the back of the car
    return get_vectorOrientation(0.5 * airDensity * cdValue * frontArea * velocity ** 2,
                                 currentPosition[3], currentPosition[4] + 180, currentPosition[5])


def get_f_friction(f_neutral, staticFriction, turnIncline):  # parallel to the ground (not road)
    # vector points towards the curve (left of the car)
    return get_vectorOrientation(np.linalg.norm(f_neutral) * staticFriction * np.cos(turnIncline),
                                 currentPosition[3], currentPosition[4] - 90, currentPosition[5])


def get_f_centripetal(mass, velocity, radius, f_friction):  # parallel to the ground (not road)
    # vector points towards the curve (left of the car)
    return get_vectorOrientation(mass * velocity ** 2 / radius + np.linalg.norm(f_friction),
                                 currentPosition[3], currentPosition[4] - 90, currentPosition[5])


def get_f_velocity(f_drag):
    return get_vectorOrientation(np.linalg.norm(f_drag), currentPosition[3], currentPosition[4], currentPosition[5])


def get_new_f_velocity(f_velocity, turnAngle):
    return get_vectorOrientation(np.linalg.norm(f_velocity), currentPosition[3], currentPosition[4] - turnAngle, currentPosition[5])


def get_radius(velocity, gravityAcceleration, turnIncline):
    return (velocity ** 2 / (gravityAcceleration * np.tan(turnIncline)))


def rotation_matrix(roll, yaw, pitch):
    # convert angles to radians
    yaw = np.radians(yaw)
    pitch = np.radians(pitch)
    roll = np.radians(roll)

    # rotation matrices
    rx = np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll), np.cos(roll)]
    ])
    ry = np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)]
    ])
    rz = np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw), np.cos(yaw), 0],
        [0, 0, 1]
    ])

    r = rx @ ry @ rz  # combine rotation matrix
    return r


def get_vectorOrientation(length, roll, yaw, pitch):
    r = rotation_matrix(roll, yaw, pitch)  # creates rotation matrix using the specified orientations
    unit_vector = np.array([0, 0, -length])  # initial orientation points towards the negative z-axis
    rotated_vector = r @ unit_vector  # rotates the vector
    return rotated_vector
