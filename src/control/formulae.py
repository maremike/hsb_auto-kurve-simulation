import numpy as np


def init_vectors(turnIncline, mass, cdValue, frontArea, airPressure, gasContent, temperature, velocity, turnAngle,
                 gravityAcceleration):
    # calculates all for the optimization an simulation necessary vectors
    f_drag = init_f_drag(airPressure, gasContent, temperature, cdValue, frontArea, velocity)
    f_velocity = init_f_velocity(f_drag)
    f_new_velocity = init_new_f_velocity(f_velocity, turnAngle, turnIncline)
    f_centrifugal = init_f_centrifugal(f_velocity, f_new_velocity)
    f_gravity = init_f_gravity(mass, gravityAcceleration)
    f_gravity_parallel = init_f_gravity_parallel(f_gravity, turnIncline)
    f_neutral = init_f_neutral(turnIncline, f_gravity)
    f_road = init_f_road(f_neutral)
    f_static_friction = init_f_friction(f_centrifugal, f_gravity_parallel)
    f_centripetal = init_f_centripetal(f_centrifugal)

    return (f_drag, f_velocity, f_new_velocity, f_centrifugal, f_gravity, f_gravity_parallel, f_neutral, f_road,
            f_static_friction, f_centripetal)


def init_f_drag(airPressure, gasContent, temperature, cdValue, frontArea, velocity):
    return np.array(
        [0, 0, 0.5 * get_airDensity(airPressure, temperature, gasContent) * cdValue * frontArea * velocity ** 2])


def init_f_velocity(f_drag):
    return transform_vector(np.array(f_drag), 0, np.radians(180), 0)


def init_new_f_velocity(f_velocity, turnAngle, turnIncline):
    f_new_velocity = transform_vector(f_velocity, 0, np.radians(turnAngle), 0)
    f_new_velocity = transform_vector(f_new_velocity, 0, 0, np.radians(turnIncline))
    return np.array(f_new_velocity)


def init_f_centrifugal(f_velocity, f_new_velocity):
    return (np.array(f_velocity) - np.array(f_new_velocity))


def init_f_gravity(mass, gravityAcceleration):
    return np.array([0, -1 * mass * gravityAcceleration, 0])


def init_f_gravity_parallel(f_gravity, turnIncline):
    return transform_vector(
        np.array([0, -1 * np.linalg.norm(f_gravity) * np.sin(np.radians(turnIncline)), 0]),
        0, 0, np.radians(270 + turnIncline))


def init_f_neutral(turnIncline, f_gravity):
    return np.array(transform_vector(
        np.array([0, (-1) * (np.linalg.norm(f_gravity) * np.cos(np.radians(turnIncline))), 0]),
        0, 0, np.radians(turnIncline)))


def init_f_road(f_neutral):
    return transform_vector(f_neutral, 0, 0, np.radians(180))


def init_f_friction(f_centrifugal, f_gravity_parallel):  # parallel to the ground (not road)
    return (np.array(f_centrifugal) * -1) - np.array(f_gravity_parallel)


def init_f_centripetal(f_centrifugal):
    return np.array(f_centrifugal) * -1


def rotation_matrix(pitch, yaw, roll):
    # pitch = x, yaw = y, roll = z
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


def transform_vector(vector, pitch, yaw, roll):
    # pitch = x (counterclockwise), yaw = y (counterclockwise), roll = z (counterclockwise)
    R = rotation_matrix(pitch, yaw, roll)
    return R @ vector


def get_airDensity(airPressure, temperature, gasContent):
    return airPressure / ((temperature + 273.15) * gasContent)


def get_radius(wheelDistance, turnAngle):
    return wheelDistance / (np.tan(np.radians(turnAngle)))


def get_circle_circumference(radius):
    return 2 * np.pi * radius


def get_Coordinates(radius, distance, totalDistance, curveAngle, turnIncline, roadWidth):
    return [radius * np.cos(np.radians(distance * curveAngle / totalDistance)),
            roadWidth / 2 * np.sin(np.radians(turnIncline)),
            -1 * radius * np.sin(np.radians(distance * curveAngle / totalDistance))]
