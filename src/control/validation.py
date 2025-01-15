from resources import constants
from resources import domains

def extract_parameters(module):
    """
    Extracts all variables from a module, which are not private or a function.
    """
    return {
        name: value for name, value in vars(module).items()
        if not name.startswith("_") and not callable(value)
    }

def validate_parameters(parameters, domain_module):
    """
    Validates parameters for defined domains.
    """
    errors = []
    for param, value in parameters.items():
        if hasattr(domain_module, param):  # Checks whether domain is defined.
            domain = getattr(domain_module, param)
            if not domain.contains(value):
                errors.append(f"'{param}' ({value}) is out of bounds {domain}.")
        else:
            print(f"'{param}' has no defined domain. Ignoring...")
    return errors

# Extrahiere Parameter aus constants.py
parameters = extract_parameters(constants)

# Führe Validierung durch
validation_errors = validate_parameters(parameters, domains)

# Ergebnisse ausgeben
if validation_errors:
    for error in validation_errors:
        print(error)
else:
    print("parameters with a domain are not out of bounds.")