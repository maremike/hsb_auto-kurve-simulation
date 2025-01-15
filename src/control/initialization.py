import numpy as np
from resources.constants import flaeche, luftDruck, cwWert

# Radius = v² / (g * tan(neigungswinkel))
# Masse =

f_w = np.array([0, 0, 0.5 * cwWert * luftDruck * flaeche]) # Luftreibung = 1/2 * cw * pl * A
f_a = -f_w # Andere Richtung wie f_w Vektor (f_a für antrieb)

beschleunigung = f_v0 / masse

def optimisierung(x, y, z):
    