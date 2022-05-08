from matplotlib import pyplot as plt


def graph_scatter(data):
    graph_data = []

    dim_am = len(data[0])
    if dim_am not in [2, 3]:
        return

    for i in range(dim_am):
        dim = [el[i] for el in data]
        graph_data.append(dim)

    fig, ax = plt.subplots(figsize=(10, 10))

    if dim_am == 3:
        ax = fig.add_subplot(111, projection='3d')

    ax.scatter(*graph_data)

    plt.show()
