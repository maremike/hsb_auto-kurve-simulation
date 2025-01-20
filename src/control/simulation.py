from control.formulae import get_radius, init_vectors
from resources.constants import wheelDistance, turnAngle, velocity, gravityAcceleration, gasContent, \
    temperature

turnIncline = 0
mass = 0
staticFriction = 0
cdValue = 0
frontArea = 0
airPressure = 0
f_drag = 0
f_velocity = 0
f_new_velocity = 0
f_centrifugal = 0
f_gravity = 0
f_gravity_parallel = 0
f_neutral = 0
f_road = 0
f_static_friction = 0
f_centripetal = 0
radius = get_radius(wheelDistance, turnAngle)


def setOptimizationResults(new_turnIncline, new_mass, new_staticFriction, new_cdValue, new_frontArea, new_airPressure):
    global turnIncline, mass, staticFriction, cdValue, frontArea, airPressure

    turnIncline = new_turnIncline
    mass = new_mass
    staticFriction = new_staticFriction
    cdValue = new_cdValue
    frontArea = new_frontArea
    airPressure = new_airPressure


def simulate():
    print("Simulating values...")

    global f_drag, f_velocity, f_new_velocity, f_centrifugal, f_gravity, f_gravity_parallel, f_neutral, f_road, f_static_friction, f_centripetal
    (f_drag, f_velocity, f_new_velocity, f_centrifugal, f_gravity, f_gravity_parallel, f_neutral, f_road,
     f_static_friction, f_centripetal) = (
        init_vectors(turnIncline, mass, cdValue, frontArea, airPressure, gasContent, temperature, velocity, turnAngle,
                     gravityAcceleration)
    )

    

    print("Simulation finished.")
