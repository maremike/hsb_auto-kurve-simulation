import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


def init_graph(plot, dataList, focusingDataset):
    plot.set_xlim(-10, 10)
    plot.set_ylim(0, 10)
    plot.set_title("Top-down View")
    plot.set_xlabel("X")
    plot.set_ylabel("Z")

    add_points(plot, dataList)
    add_vectors(plot, dataList[focusingDataset])


def add_points(plot, dataList):
    pass


def add_vectors(plot, dataSet):
    pass