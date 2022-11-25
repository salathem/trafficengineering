import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Simulation:
    def __init__(self, net, nr_of_steps, delta_time, network, precision):
        self.net = net
        self.dimension = len(network.cells)
        self.nr_of_steps = nr_of_steps
        self.delta_time = delta_time
        self.network = network
        self.precision = precision
        self.flow = np.zeros([self.dimension, nr_of_steps])
        self.density = np.zeros([self.dimension, nr_of_steps])
        self.speed = np.zeros([self.dimension, nr_of_steps])
        self.vkt = 0
        self.vht = 0

    # stores date from cell to data Matrix
    def update(self):
        for cell in self.net.cells:
            self.flow[cell.id-1, cell.time_step] = cell.flow
            self.density[cell.id-1, cell.time_step] = cell.density
            self.speed[cell.id-1, cell.time_step] = cell.speed

    def update_cell(self, cell):
        self.flow[cell.id - 1, cell.time_step] = cell.flow
        self.density[cell.id - 1, cell.time_step] = cell.density
        self.speed[cell.id - 1, cell.time_step] = cell.speed

    def run(self):
        for sim_step in range(self.nr_of_steps):

            # update network demand
            self.net.demand.update(sim_step)
            for cell in self.net.cells:
                # calculate cell
                cell.update(sim_step)

                # update performance parameters
                temp_vkt, temp_vht = cell.performance_calculation()
                self.vkt += temp_vkt
                self.vht += temp_vht

            # advance simulation
            sim_step += 1
            # get data for plots
            self.update()


    def plot(self):
        # plotting
        array = []
        for cell in self.network.cells:
            array.append(cell.id)
        xvalues = np.linspace(0, self.nr_of_steps, self.nr_of_steps)
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
        max_flow = self.flow.max()
        max_density = self.density.max()
        max_speed = self.speed.max()
        max_time = self.delta_time * self.nr_of_steps * 3600

        array = []
        for index in range(len(self.network.cells)):
            array.append(index)
        xvalues = []
        for cell in self.network.cells:
            xvalues.append(cell.id)

        for step in range(self.nr_of_steps):

            time = self.delta_time * step * 3600

            yvalues1 = self.flow[array, step]
            yvalues2 = self.density[array, step]
            yvalues3 = self.speed[array, step]

            # Plot the subplots
            # Plot 1
            plt.subplot(4, 1, 1)
            plt.plot(xvalues, yvalues1, 'g')
            plt.title('Animation')
            plt.ylim(0, max_flow)
            plt.xlabel('Cells')
            plt.ylabel('Flow [veh/h]')

            # Plot 2
            plt.subplot(4, 1, 2)
            plt.plot(xvalues, yvalues2, '-.r')
            plt.ylim(0, max_density)
            plt.xlabel('Cells')
            plt.ylabel('Density [veh/km]')

            # Plot 3
            plt.subplot(4, 1, 3)
            plt.plot(xvalues, yvalues3, '-.y')
            plt.ylim(0, max_speed)
            plt.xlabel('Cells')
            plt.ylabel('Speed [km/h]')

            # Plot 4
            plt.subplot(4, 1, 4)
            plt.barh("0", time)
            plt.xlim(0, max_time)
            #plt.xlabel('Time')
            plt.ylabel('Time [s]')

            plt.pause(0.01)
            plt.clf()

        plt.show()

    def print(self):
        print("VKT: "+str(round(self.vkt, len(str(round(1/self.precision)))))+"   VHT: "+str(round(self.vht, len(str(round(1/self.precision))))))
