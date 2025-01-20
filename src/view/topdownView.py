import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def init_graph(plot):
    plot.set_xlim(-10, 10)
    plot.set_ylim(0, 10)
    plot.set_title("Top-down View")
    plot.set_xlabel("X")
    plot.set_ylabel("Z")