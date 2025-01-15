import numpy as np

from control.validation import validate
from resources.constants import startPosition

if __name__ == "__main__":
    validate()
    position = startPosition # set starting position

    while np.all(position <= np.array([1000, 1000, 1000])):
        position += np.array([100, 100, 100])  # Bewegung in Richtung Ziel

    print("Simulation finished.")