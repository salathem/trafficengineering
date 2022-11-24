import numpy as np
import matplotlib.pyplot as plt


class Data:
    def __init__(self, steps, network):
        self.dimension = len(network.cells)
        self.steps = steps
        self.network = network
        self.flow = np.zeros([self.dimension, steps])
        self.density = np.zeros([self.dimension, steps])
        self.speed = np.zeros([self.dimension, steps])
        self.vkt = 0
        self.vht = 0

    # stores date from cell to data Matrix
    def update(self, net):
        for cell in net.cells:
            self.flow[cell.id-1, cell.time_step] = cell.flow
            self.density[cell.id-1, cell.time_step] = cell.density
            self.speed[cell.id-1, cell.time_step] = cell.speed

    def update_cell(self, cell):
        self.flow[cell.id - 1, cell.time_step] = cell.flow
        self.density[cell.id - 1, cell.time_step] = cell.density
        self.speed[cell.id - 1, cell.time_step] = cell.speed


    def plot(self):
        # plotting
        array = []
        for cell in self.network.cells:
            array.append(cell.id)
        xvalues = np.linspace(0, self.steps, self.steps)
        yvalues = np.array(array)
        X, Y = np.meshgrid(xvalues, yvalues)

        # flow graph
        fig1 = plt.figure()
        fig1.suptitle('flow', fontsize=32)
        ax1 = fig1.add_subplot(111, projection='3d')
        ax1.plot_surface(X, Y, self.flow, cmap="plasma")
        plt.show()

        # density graph
        fig2 = plt.figure()
        fig2.suptitle('density', fontsize=32)
        ax2 = fig2.add_subplot(111, projection='3d')
        ax2.plot_surface(X, Y, self.density, cmap="plasma")
        plt.show()

        # speed graph
        fig3 = plt.figure()
        fig3.suptitle('speed', fontsize=32)
        ax3 = fig3.add_subplot(111, projection='3d')
        ax3.plot_surface(X, Y, self.speed, cmap="plasma")
        plt.show()

    def print(self):
        print("VKT: "+str(round(self.vkt, 2))+"   VHT: "+str(round(self.vht, 2)))
