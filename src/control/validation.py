import types
from resources import constants
from resources import domains

def extract_parameters(module):
    """
    Extracts all variables from a module, which are not private, not a function, and not an imported module.
    """
    return {
        name: value for name, value in vars(module).items()
        if not name.startswith("_") and not callable(value) and not isinstance(value, types.ModuleType)
    }

def validate_parameters(parameters, domain_module):
    """
    Validates parameters for defined domains.
    """
    errors = []
    ignored_count = 0  # Track the number of ignored parameters
    for param, value in parameters.items():
        if hasattr(domain_module, param):  # checks whether domain is defined.
            domain = getattr(domain_module, param)
            if not domain.contains(value):
                errors.append(f"'{param}' ({value}) is out of bounds {domain}.")
        else:
            print(f"'{param}' has no defined domain. Ignoring...")
            ignored_count += 1  # Increment ignored parameters counter
    return errors, ignored_count

def validate():
    parameters = extract_parameters(constants)  # Extract parameters from constants.py
    validation_errors, ignored_count = validate_parameters(parameters, domains)  # Validate values by comparing with domains

    # Return results
    if validation_errors:
        for error in validation_errors:
            print(error)
    else:
        print(f"{ignored_count} parameters have no domain and have been ignored.")
        print("Parameters with domains are not out of bounds.")
