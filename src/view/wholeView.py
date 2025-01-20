import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from view import sideView
from view import topdownView


def init_views():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))  # 1 row, 2 columns

    sideView.init_graph(ax1)  # plot side view on the first subplot
    topdownView.init_graph(ax2)  # plot top-down view on the second subplot

    # Adjust the layout to prevent overlap
    plt.tight_layout()

    # Show the combined figure
    plt.show()


def updateView(frame):
    # Plot the car's position (as a point)
    #ax_top.plot(car_pos[0], car_pos[1], 'bo', markersize=10)  # Top-Down
    #ax_side.plot(car_pos[0], car_pos[1], 'bo', markersize=10)  # Side View (z is the same as y for simplicity)

    # Plot the velocity vector (for both views)
    #ax_top.quiver(car_pos[0], car_pos[1], car_vel[0], car_vel[1], angles='xy', scale_units='xy', scale=1, color='r')
    #ax_side.quiver(car_pos[0], car_pos[1], car_vel[0], car_vel[1], angles='xy', scale_units='xy', scale=1, color='r')