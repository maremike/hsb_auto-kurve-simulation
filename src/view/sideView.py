import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def init_graph(plot, dataset):
    plot.set_title("Side View")
    plot.set_xlabel("X")
    plot.set_ylabel("Y")

    add_vectors(dataset)


def add_vectors(dataset):
    pass