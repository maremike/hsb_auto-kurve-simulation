import yaml
import os

from resources import variables


def get_absolute_path(relative_path):
    # construct the absolute path to the file
    script_dir = os.path.dirname(__file__)  # Directory of this script
    combined_path = os.path.join(script_dir, relative_path)  # combine two paths
    return os.path.normpath(combined_path)  # get absolute path


def validate_and_assign_parameters(path):
    # load the file
    with open(path, 'r') as f:
        data = yaml.safe_load(f)

    parameters = data.get("parameters", {})

    for category, items in parameters.items():
        print(f"\tCategory: {category}")
        for param_name, param_details in items.items():
            value = param_details.get("value")
            range_ = param_details.get("range")

            # Add the range to constraints if defined
            if range_ is not None:
                variables.CONSTRAINTS[param_name] = tuple(range_)  # Add to the constraints dictionary

            # Skip validation if range is not defined
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


# Example usage
def validate():
    print("Validating values...")

    validate_and_assign_parameters(get_absolute_path(variables.configFile))

    print("Validation finished.")
