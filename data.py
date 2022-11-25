import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Data:
    def __init__(self, steps, network, precision):
        self.dimension = len(network.cells)
        self.steps = steps
        self.network = network
        self.precision = precision
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


    def animate(self):
        array = []
        for index in range(len(self.network.cells)):
            array.append(index)
        xvalues = []
        for cell in self.network.cells:
            xvalues.append(cell.id)

        for step in range(self.steps):
            yvalues1 = self.flow[array, step]
            yvalues2 = self.density[array, step]
            #yvalues3 = self.speed[array, step]
            plt.ylim(0, 6000)

            plt.plot(xvalues, yvalues1, label="flow")
            plt.plot(xvalues, yvalues2, label="density")
            #plt.plot(xvalues, yvalues3, label="speed")

            plt.pause(0.0001)
            plt.clf()
        plt.show()

    def print(self):
        print("VKT: "+str(round(self.vkt, len(str(round(1/self.precision)))))+"   VHT: "+str(round(self.vht, len(str(round(1/self.precision))))))
