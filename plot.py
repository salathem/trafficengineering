import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


#Plot
class Plot():
    def __init__(self, simulation, parameter):
        net = simulation.net
        ax = plt.axes(projection="3d")

        x_data = simulation.all_steps * 3600
        y_data = np.arange(6)
        X, Y = np.meshgrid(x_data, y_data)

        Z = np.zeros((len(net.cells), len(simulation.all_steps)))
        for cell in net.cells:
            Z[cell.index] = cell.readattribute(parameter)
        #Z = np.matrix([net.cells[0].q, net.cells[1].q, net.cells[2].q, net.cells[3].q, net.cells[4].q, net.cells[5].q])

        ax.plot_surface(X, Y, Z, cmap="plasma")


        plt.show()


