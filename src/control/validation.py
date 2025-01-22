import yaml
import os

from resources import variables


def validate():
    """
    Orchestrates the validation of values by calling the `validate_and_assign_parameters` function.
    This function is an entry point for the validation process.

    Parameters:
        None

    Returns:
        None
    """
    print("Validating values...")

    validate_and_assign_parameters(get_absolute_path(variables.configFile))

    print("Validation finished.")


def get_absolute_path(relative_path):
    """
    Converts a relative file path to an absolute file path.

    Parameters:
        relative_path (str): The relative path of the file to be converted.

    Returns:
        str: The absolute file path formed by combining the script's directory with the relative path.
    """
    # construct the absolute path to the file
    script_dir = os.path.dirname(__file__)  # Directory of this script
    combined_path = os.path.join(script_dir, relative_path)  # combine two paths
    return os.path.normpath(combined_path)  # get absolute path


def validate_and_assign_parameters(path):
    """
    Validates and assigns values from a YAML configuration file to the `variables` module.

    Parameters:
        path (str): The absolute file path to the YAML configuration file.

    Function Logic:
        - Loads the configuration from the provided YAML file.
        - For each parameter in the configuration:
            - If a range is defined, validates if the value falls within the range.
            - If the value is valid, assigns the value to the `variables` module.
            - If no range is defined, assigns the value directly to the `variables` module.
        - The range values (if provided) are added to the `variables.CONSTRAINTS` dictionary.
        - Outputs the final `CONSTRAINTS` dictionary after all validations.

    Example of validation:
        If the `value` is `50` and `range_` is `(0, 100)`, then `50` is valid.
    """
    # load the file
    with open(path, 'r') as f:
        data = yaml.safe_load(f)

    parameters = data.get("parameters", {})

    for category, items in parameters.items():
        print(f"\tCategory: {category}")
        for param_name, param_details in items.items():
            value = param_details.get("value") # get current value
            range_ = param_details.get("range") # get current range

            # add the range to constraints if defined
            if range_ is not None:
                variables.CONSTRAINTS[param_name] = tuple(range_)  # Add to the constraints dictionary

            # skip validation if range is not defined
            if range_ is None:
                print(f"\t\t{param_name}: Skipping validation (no range). Assigned value: {value}")
                setattr(variables, param_name, value)  # Assign to variables module dynamically
                continue

            # validate value against range
            if value is not None and range_[0] <= value <= range_[1]:
                print(f"\t\t{param_name}: Valid. Assigned value: {value}")
                setattr(variables, param_name, value)  # Assign to variables module dynamically
            elif value is not None:
                print(f"\t\t{param_name}: Invalid. Value {value} out of range {range_}.")
            else:
                print(f"\t\t{param_name}: No value provided.")

    # print the populated CONSTRAINTS dictionary
    print("\tFinal CONSTRAINTS dictionary:")
    print(f"\t\t{variables.CONSTRAINTS}")
