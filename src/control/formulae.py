import numpy as np


def init_vectors(turnIncline, mass, cdValue, frontArea, airPressure, gasContent, temperature, velocity, turnAngle,
                 gravityAcceleration):
    """
    Initializes the necessary vectors for optimization and simulation based on the provided parameters.

    Parameters:
        turnIncline (float): The angle of the road in relation to the ground (in °).
        mass (float): The mass of the car (in kg).
        cdValue (float): The aerodynamic drag coefficient of the car.
        frontArea (float): The front area of the car (in m²).
        airPressure (float): The atmospheric air pressure (in Pa).
        gasContent (float): The specific gas content at the current temperature (in J/(kg·pK)).
        temperature (float): The temperature (in °C).
        velocity (float): The velocity of the car (in m/s).
        turnAngle (float): The angle between the front and back tires of the car (in °).
        gravityAcceleration (float): The acceleration due to gravity (in m/s²).

    Returns:
        tuple: A tuple of vectors representing different forces involved in the simulation.
    """
    # calculates all for the necessary vectors for optimization and simulation
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
    """
    Calculates the drag force experienced by the car based on the provided parameters.

    Formula:
        F_drag = 0.5 * airDensity * cdValue * frontArea * velocity²

    Parameters:
        airPressure (float): The atmospheric air pressure (in Pa).
        gasContent (float): The specific gas content at the current temperature (in J/(kg·pK)).
        temperature (float): The temperature (in °C).
        cdValue (float): The aerodynamic drag coefficient of the car.
        frontArea (float): The front area of the car (in m²).
        velocity (float): The velocity of the car (in m/s).

    Returns:
        np.array: A numpy array containing the drag force vector.
    """
    return np.array(
        [0, 0, 0.5 * get_airDensity(airPressure, temperature, gasContent) * cdValue * frontArea * velocity ** 2])


def init_f_velocity(f_drag):
    """
    Transforms the drag force vector into the velocity vector.

    Parameters:
        f_drag (np.array): The drag force vector.

    Returns:
        np.array: The transformed velocity vector.
    """
    return transform_vector(np.array(f_drag), 0, np.radians(180), 0)


def init_new_f_velocity(f_velocity, turnAngle, turnIncline):
    """
    Transforms the velocity vector based on the turn angle and incline of the road.

    Formula:
        Transforms f_velocity first by turnAngle, then by turnIncline.

    Parameters:
        f_velocity (np.array): The velocity vector.
        turnAngle (float): The angle between the front and back tires of the car (in °).
        turnIncline (float): The angle of the road in relation to the ground (in °).

    Returns:
        np.array: The transformed new velocity vector.
    """
    f_new_velocity = transform_vector(f_velocity, 0, np.radians(turnAngle), 0)
    f_new_velocity = transform_vector(f_new_velocity, 0, 0, np.radians(turnIncline))
    return np.array(f_new_velocity)


def init_f_centrifugal(f_velocity, f_new_velocity):
    """
    Calculates the centrifugal force vector based on the difference between the velocity and new velocity vectors.

    Formula:
        F_centrifugal = F_velocity - F_new_velocity

    Parameters:
        f_velocity (np.array): The initial velocity vector.
        f_new_velocity (np.array): The transformed velocity vector based on the turn and incline.

    Returns:
        np.array: The centrifugal force vector.
    """
    return (np.array(f_velocity) - np.array(f_new_velocity))


def init_f_gravity(mass, gravityAcceleration):
    """
    Calculates the gravitational force on the car.

    Formula:
        F_gravity = [0, -mass * gravityAcceleration, 0]

    Parameters:
        mass (float): The mass of the car (in kg).
        gravityAcceleration (float): The acceleration due to gravity (in m/s²).

    Returns:
        np.array: The gravitational force vector.
    """
    return np.array([0, -1 * mass * gravityAcceleration, 0])


def init_f_gravity_parallel(f_gravity, turnIncline):
    """
    Calculates the component of the gravitational force that is parallel to the incline of the road.

    Formula:
        F_gravity_parallel = F_gravity * sin(turnIncline)

    Parameters:
        f_gravity (np.array): The gravitational force vector.
        turnIncline (float): The angle of the road in relation to the ground (in °).

    Returns:
        np.array: The gravitational force vector parallel to the incline.
    """
    return transform_vector(
        np.array([0, -1 * np.linalg.norm(f_gravity) * np.sin(np.radians(turnIncline)), 0]),
        0, 0, np.radians(270 + turnIncline))


def init_f_neutral(turnIncline, f_gravity):
    """
    Calculates the neutral force acting on the car, factoring in the incline of the road.

    Formula:
        F_neutral = -1 * (norm(F_gravity) * cos(turnIncline))

    Parameters:
        turnIncline (float): The angle of the road in relation to the ground (in °).
        f_gravity (np.array): The gravitational force vector.

    Returns:
        np.array: The neutral force vector.
    """
    return np.array(transform_vector(
        np.array([0, (-1) * (np.linalg.norm(f_gravity) * np.cos(np.radians(turnIncline))), 0]),
        0, 0, np.radians(turnIncline)))


def init_f_road(f_neutral):
    """
    Transforms the neutral force into the force acting along the road.

    Parameters:
        f_neutral (np.array): The neutral force vector.

    Returns:
        np.array: The force vector along the road.
    """
    return transform_vector(f_neutral, 0, 0, np.radians(180))


def init_f_friction(f_centrifugal, f_gravity_parallel):
    """
    Calculates the static friction force by combining the centrifugal force and the parallel gravitational force.

    Formula:
        F_friction = -F_centrifugal - F_gravity_parallel

    Parameters:
        f_centrifugal (np.array): The centrifugal force vector.
        f_gravity_parallel (np.array): The parallel gravitational force vector.

    Returns:
        np.array: The static friction force vector.
    """
    return (np.array(f_centrifugal) * -1) - np.array(f_gravity_parallel)


def init_f_centripetal(f_centrifugal):
    """
    Calculates the centripetal force by reversing the centrifugal force.

    Formula:
        F_centripetal = -F_centrifugal

    Parameters:
        f_centrifugal (np.array): The centrifugal force vector.

    Returns:
        np.array: The centripetal force vector.
    """
    return np.array(f_centrifugal) * -1


def rotation_matrix(pitch, yaw, roll):
    """
    Creates a rotation matrix based on pitch, yaw, and roll angles.
    Positive values rotate counterclockwise.

    Formula:
        R_x = rotation matrix for pitch
        R_y = rotation matrix for yaw
        R_z = rotation matrix for roll
        R = combined rotation matrix: R = R_z @ R_y @ R_x

    Parameters:
        pitch (float): The pitch rotation angle (in radians).
        yaw (float): The yaw rotation angle (in radians).
        roll (float): The roll rotation angle (in radians).

    Returns:
        np.array: The resulting combined rotation matrix.
    """
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
    """
    Transforms a vector based on pitch, yaw, and roll angles by applying a rotation matrix.
    Positive values rotate counterclockwise.

    Parameters:
        vector (np.array): The vector to be transformed.
        pitch (float): The pitch rotation angle (in radians).
        yaw (float): The yaw rotation angle (in radians).
        roll (float): The roll rotation angle (in radians).

    Returns:
        np.array: The transformed vector.
    """
    # pitch = x (counterclockwise), yaw = y (counterclockwise), roll = z (counterclockwise)
    R = rotation_matrix(pitch, yaw, roll)
    return R @ vector


def get_airDensity(airPressure, temperature, gasContent):
    """
    Calculates the air density using the ideal gas law.

    Formula:
        airDensity = airPressure / ((temperature + 273.15) * gasContent)

    Parameters:
        airPressure (float): The atmospheric air pressure (in Pa).
        temperature (float): The temperature (in °C).
        gasContent (float): The specific gas content at the current temperature (in J/(kg·pK)).

    Returns:
        float: The calculated air density (in kg/m³).
    """
    return airPressure / ((temperature + 273.15) * gasContent)


def get_radius(wheelDistance, turnAngle):
    """
    Calculates the radius of the turn based on wheel distance and turn angle.

    Formula:
        radius = wheelDistance / tan(turnAngle)

    Parameters:
        wheelDistance (float): The distance between the wheels (in meters).
        turnAngle (float): The angle of the turn (in °).

    Returns:
        float: The radius of the turn (in meters).
    """
    return wheelDistance / (np.tan(np.radians(turnAngle)))


def get_circle_circumference(radius):
    """
    Calculates the circumference of a circle given its radius.

    Formula:
        circumference = 2 * π * radius

    Parameters:
        radius (float): The radius of the circle (in meters).

    Returns:
        float: The circumference of the circle (in meters).
    """
    return 2 * np.pi * radius


def get_Coordinates(radius, distance, totalDistance, curveAngle, turnIncline, roadWidth):
    """
    Calculates the coordinates of a point on the curve based on the provided parameters.

    Formula:
        x = radius * cos(distance * curveAngle / totalDistance)
        y = roadWidth / 2 * sin(turnIncline)
        z = -radius * sin(distance * curveAngle / totalDistance)

    Parameters:
        radius (float): The radius of the turn (in meters).
        distance (float): The distance along the road (in meters).
        totalDistance (float): The total length of the curve (in meters).
        curveAngle (float): The total angle of the curve (in °).
        turnIncline (float): The angle of the road incline (in °).
        roadWidth (float): The width of the road (in meters).

    Returns:
        list: A list containing the x, y, and z coordinates of the point.
    """
    return [radius * np.cos(np.radians(distance * curveAngle / totalDistance)),
            roadWidth / 2 * np.sin(np.radians(turnIncline)),
            -1 * radius * np.sin(np.radians(distance * curveAngle / totalDistance))]
