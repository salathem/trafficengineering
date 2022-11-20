import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


#Plot
class Plot():
    def __init__(self, simulation, parameter="all"):
        net = simulation.net
        ax = plt.axes(projection="3d")

        x_data = simulation.all_steps * 3600
        y_data = np.arange(6)
        X, Y = np.meshgrid(x_data, y_data)
        Z = np.zeros((len(net.cells), len(simulation.all_steps)))

        if parameter == "all":
            # flow graph
            for cell in net.cells:
                Z[cell.index] = cell.readattribute("flow")
            fig1 = plt.figure()
            fig1.suptitle('flow', fontsize=32)
            ax1 = fig1.add_subplot(111, projection='3d')
            ax1.plot_surface(X, Y, Z, cmap="plasma")
            plt.show()

            # density graph
            for cell in net.cells:
                Z[cell.index] = cell.readattribute("density")
            fig2 = plt.figure()
            fig2.suptitle('density', fontsize=32)
            ax2 = fig2.add_subplot(111, projection='3d')
            ax2.plot_surface(X, Y, Z, cmap="plasma")
            plt.show()

            # speed graph
            for cell in net.cells:
                Z[cell.index] = cell.readattribute("speed")
            fig3 = plt.figure()
            fig3.suptitle('speed', fontsize=32)
            ax3 = fig3.add_subplot(111, projection='3d')
            ax3.plot_surface(X, Y, Z, cmap="plasma")
            plt.show()

        else:
            for cell in net.cells:
                Z[cell.index] = cell.readattribute(parameter)
            fig = plt.figure()
            fig.suptitle(parameter, fontsize=32)
            ax = fig.add_subplot(111, projection='3d')
            ax.plot_surface(X, Y, Z, cmap="plasma")
            plt.show()


