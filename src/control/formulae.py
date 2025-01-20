import numpy as np


def init_vectors(turnIncline, mass, staticFriction, cdValue, frontArea, airDensity, velocity, turnAngle,
                 gravityAcceleration):
    f_drag = init_f_drag(airDensity, cdValue, frontArea, velocity)
    f_velocity = init_f_velocity(f_drag)
    f_new_velocity = init_new_f_velocity(f_velocity, turnAngle, turnIncline)
    f_centrifugal = init_f_centrifugal(f_velocity, f_new_velocity)
    f_gravity = init_f_gravity(mass, gravityAcceleration)
    f_gravity_parallel = init_f_gravity_parallel(f_gravity, turnIncline)
    f_neutral = init_f_neutral(turnIncline, f_gravity)
    f_road = init_f_road(f_neutral)
    f_static_friction = init_f_friction(f_gravity, f_neutral, staticFriction, f_centrifugal)
    f_centripetal = init_f_centripetal(f_gravity, f_centrifugal, f_static_friction)

    return f_drag, f_velocity, f_new_velocity, f_centrifugal, f_gravity, f_gravity_parallel, f_neutral, f_road, f_static_friction, f_centripetal


def init_f_drag(airDensity, cdValue, frontArea, velocity):
    # vector points towards the back of the car
    return np.array([0, 0, 0.5 * airDensity * cdValue * frontArea * velocity ** 2])


def init_f_velocity(f_drag):
    return transform_vector(np.array(f_drag), 0, np.radians(180), 0)


def init_new_f_velocity(f_velocity, turnAngle, turnIncline):
    f_new_velocity = transform_vector(f_velocity, 0, np.radians(turnAngle), 0)
    f_new_velocity = transform_vector(f_new_velocity, 0, 0, np.radians(turnIncline))
    return np.array(f_new_velocity)


def init_f_centrifugal(f_velocity, f_new_velocity):
    return (np.array(f_velocity) - np.array(f_new_velocity))


def init_f_gravity(mass, gravityAcceleration):
    # vector points always down
    return np.array([0, -1 * mass * gravityAcceleration, 0])


def init_f_gravity_parallel(f_gravity, turnIncline):
    return transform_vector(
        np.array([0, -1 * np.linalg.norm(f_gravity) * np.sin(np.radians(turnIncline)), 0]),
        0, 0, np.radians(270+turnIncline))


def init_f_neutral(turnIncline, f_gravity):
    # points towards the road
    return np.array(transform_vector(
        np.array([0, (-1) * (np.linalg.norm(f_gravity) * np.cos(np.radians(turnIncline))), 0]),
        0, 0, np.radians(turnIncline)))

def init_f_road(f_neutral):
    # points away from the road
    return transform_vector(f_neutral, 0, 0, np.radians(180))


def init_f_friction(f_gravity, f_neutral, friction, f_centrifugal):  # parallel to the ground (not road)
    direction1, direction2 = compute_vector_direction(f_gravity, np.linalg.norm(f_neutral * friction),
                                                      np.array([0, 0, 0]), f_centrifugal)
    f_friction1 = direction1 * np.linalg.norm(f_neutral) * friction
    f_friction2 = direction2 * np.linalg.norm(f_neutral) * friction

    if (np.linalg.norm(np.array(f_gravity) + np.array(f_friction1)) - np.linalg.norm(f_centrifugal)) == 0:
        print(f_friction1)
        return np.array(f_friction1)
    elif np.linalg.norm(np.array(f_gravity) + np.array(f_friction2)) - np.linalg.norm(f_centrifugal) == 0:
        print(f_friction2)
        return np.array(f_friction2)
    return np.array([0,0,0])


def init_f_centripetal(f_gravity, f_centrifugal, f_friction):
    unit_vector_centrifugal = -1 * np.array(f_centrifugal) / np.linalg.norm(f_centrifugal)
    f_centripetal = np.array(unit_vector_centrifugal) * (np.linalg.norm(np.array(f_friction) + np.array(f_gravity)))

    return np.array(f_centripetal)


def rotation_matrix(pitch, yaw, roll):  # pitch = x, yaw = y, roll = z (clockwise)
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


def transform_vector(vector, pitch, yaw, roll):  # pitch = x (counterclockwise), yaw = y (counterclockwise), roll = z (counterclockwise)
    R = rotation_matrix(pitch, yaw, roll)
    return R @ vector


def compute_vector_direction(start_point, vector_length, line_point, line_direction):
    """
    Berechnet die Richtung eines Vektors mit gegebener Länge, sodass der Endpunkt des Vektors
    eine bestimmte Gerade trifft.

    :param start_point: np.array, der Startpunkt des Vektors (3D)
    :param vector_length: float, die Länge des Vektors
    :param line_point: np.array, ein Punkt auf der Geraden (3D)
    :param line_direction: np.array, der Richtungsvektor der Geraden (3D)
    :return: np.array, die Richtung des Vektors (Einheitsvektor) oder None, falls keine Lösung existiert
    """
    # Richtungsvektor der Geraden normalisieren
    line_direction = line_direction / np.linalg.norm(line_direction)

    # Relativer Vektor zwischen Startpunkt und Punkt auf der Geraden
    relative_vector = line_point - start_point

    # Quadratische Gleichung lösen: ||t * line_direction - relative_vector||^2 = vector_length^2
    a = np.dot(line_direction, line_direction)
    b = -2 * np.dot(line_direction, relative_vector)
    c = np.dot(relative_vector, relative_vector) - vector_length ** 2

    # Diskriminante berechnen
    discriminant = b ** 2 - 4 * a * c
    if discriminant >= 0:
        # t-Werte berechnen (es können zwei Lösungen existieren)
        t1 = (-b + np.sqrt(discriminant)) / (2 * a)
        t2 = (-b - np.sqrt(discriminant)) / (2 * a)

        # Endpunkte auf der Geraden für beide t-Werte berechnen
        intersection_1 = line_point + t1 * line_direction
        intersection_2 = line_point + t2 * line_direction

        # Die Richtung des Vektors berechnen
        direction_1 = (intersection_1 - start_point) / vector_length
        direction_2 = (intersection_2 - start_point) / vector_length

        return direction_1, direction_2
    return np.array([0, 0, 0]), np.array([0, 0, 0])
