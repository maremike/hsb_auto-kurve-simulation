import numpy as np
from resources.constants import turnAngle, velocity, gravityAcceleration
from resources.constants import CONSTRAINTS
from resources import constants


def validate_parameters(parameters, constraints):
    """
    Validates parameters against the defined constraints in CONSTANT_RANGES.
    """
    errors = []
    ignored_count = 0  # Track the number of ignored parameters
    for param, value in parameters.items():
        if param in constraints:  # Check if a constraint is defined for the parameter
            min_value, max_value = constraints[param]
            if not (min_value <= value <= max_value):
                errors.append(f"'{param}' ({value}) is out of bounds [{min_value}, {max_value}].")
        else:
            print(f"\t'{param}' has no defined constraint. Ignoring...")
            ignored_count += 1  # Increment ignored parameters counter
    return errors, ignored_count


def validate():
    print("Validating values...")

    # Create a dictionary of all constants to validate by dynamically getting the variables
    parameters = {name: value for name, value in globals().items()
                  if name in dir(constants) and not name.startswith('__')
                  and not isinstance(value, type(constants))}

    # Validate all parameters
    validation_errors, ignored_count = validate_parameters(parameters, CONSTRAINTS)

    # Output validation results
    if validation_errors:
        for error in validation_errors:
            print("\t" + error)
        print("Validation failed.")
        exit(-1)
    else:
        print(f"\t{ignored_count} parameters have no constraint and have been ignored.")
        print("\tParameters with constraints are not out of bounds.")
        print("Validation finished.")
