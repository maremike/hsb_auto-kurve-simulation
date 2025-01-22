import matplotlib.pyplot as plot
from view import sideView
from view import topdownView


def init_views(dataList, datasetNumber):
    """
    Initializes and displays the simulation views.
    This function creates a figure with two subplots. The first subplot displays
    a side view of the car's simulation at a specific dataset, and the second
    subplot provides a top-down view of the entire simulation path.

    Parameters:
        dataList (list): A list containing simulation data for all iterations. Each
            element in the list represents a dataset corresponding to a specific
            point in the simulation.
        datasetNumber (int): The index of the dataset within `dataList` that represents
            the specific moment of the simulation to be highlighted.

    Returns:
        None
    """
    fig, (ax1, ax2) = plot.subplots(1, 2, figsize=(10, 5))  # 1 row, 2 columns

    topdownView.init_graph(ax2, dataList, datasetNumber)  # plot top-down view on the second subplot
    sideView.init_graph(ax1, dataList[datasetNumber])  # plot side view on the first subplot

    plot.show()  # show the combined figure
