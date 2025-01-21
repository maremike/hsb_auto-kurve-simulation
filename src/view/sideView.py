def init_graph(plot, dataset, focusingDataset):
    plot.set_title("Side View")
    plot.set_xlabel("X")
    plot.set_ylabel("Y")

    

    add_vectors(plot, dataset)


def add_vectors(plot, dataSet):
    plot.quiver(dataSet[0][0], dataSet[0][1], dataSet[4][0], dataSet[4][1], angles='xy', scale_units='xy', scale=1,
                color='green')  # f_centripetal
    plot.quiver(dataSet[0][0], dataSet[0][1], dataSet[5][0], dataSet[5][1], angles='xy', scale_units='xy', scale=1,
                color='blue')  # f_centrifugal
    plot.quiver(dataSet[0][0], dataSet[0][1], dataSet[6][0], dataSet[6][1], angles='xy', scale_units='xy', scale=1,
                color='purple')  # f_gravity_parallel
    plot.quiver(dataSet[0][0], dataSet[0][1], dataSet[7][0], dataSet[7][1], angles='xy', scale_units='xy', scale=1,
                color='grey')  # f_static_friction
    plot.quiver(dataSet[0][0], dataSet[0][1], dataSet[8][0], dataSet[7][1], angles='xy', scale_units='xy', scale=1,
                color='grey')  # f_neutral
    plot.quiver(dataSet[0][0], dataSet[0][1], dataSet[9][0], dataSet[7][1], angles='xy', scale_units='xy', scale=1,
                color='grey')  # f_road
    plot.quiver(dataSet[0][0], dataSet[0][1], dataSet[10][0], dataSet[7][1], angles='xy', scale_units='xy', scale=1,
                color='grey')  # f_gravity