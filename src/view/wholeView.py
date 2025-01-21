import matplotlib.pyplot as plot
from view import sideView
from view import topdownView


def init_views(dataList, focusingDataset):
    fig, (ax1, ax2) = plot.subplots(1, 2, figsize=(10, 5))  # 1 row, 2 columns

    sideView.init_graph(ax1, dataList, focusingDataset)  # plot side view on the first subplot
    topdownView.init_graph(ax2, dataList, focusingDataset)  # plot top-down view on the second subplot

    plot.show()  # show the combined figure
