import os
import numpy as np
import matplotlib.pyplot as plt


class Simulation:
    def __init__(self, net, nr_of_steps, delta_time, precision):
        self.net = net
        self.dimension = len(net.cells)
        self.nr_of_steps = nr_of_steps
        self.delta_time = delta_time
        self.scenario = net.scenario
        self.method = net.method
        self.precision = precision
        self.flow = np.zeros([self.dimension, nr_of_steps])
        self.density = np.zeros([self.dimension, nr_of_steps])
        self.speed = np.zeros([self.dimension, nr_of_steps])
        self.vkt = 0
        self.vht = 0
        self.diagram_types = [["flow", "[veh/h]"], ["density", "[veh/km]"], ["speed", "[km/h]"]]

    def update(self):
        # stores date from cell to data Matrix
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

    def plot_2d(self, show_plots, save_plots, dpi):

        x_values = np.linspace(0, self.nr_of_steps * self.delta_time * 3600, self.nr_of_steps)

        # make folders
        for diagram_type in self.diagram_types:
            path = 'plots/' + diagram_type[0] + ' ' + self.method + ' scenario ' + self.scenario
            if not os.path.exists(path):
                os.mkdir(path)

            for cell in self.net.cells:
                plt.plot(x_values, self.flow[cell.id-1])
                plt.xlabel('Time [s]')
                plt.ylabel(diagram_type[0] + ' ' + diagram_type[1])
                plt.title('cell ' + str(cell.id) + ' ' + diagram_type[0] + ' ' + self.method + ' scenario ' + self.scenario)
                if save_plots:
                    plt.savefig(path + '/cell ' + str(cell.id) + ' ' + diagram_type[0] + ' ' + self.method + ' scenario ' + self.scenario + '.png', dpi=dpi)
                if show_plots:
                    plt.show()
                plt.clf()

    def plot_3d(self, show_plots, save_plots, dpi):
        # plotting
        array = []
        for cell in self.net.cells:
            array.append(cell.id)
        x_values = np.linspace(0, self.nr_of_steps * self.delta_time * 3600, self.nr_of_steps)
        y_values = np.array(array)
        X, Y = np.meshgrid(x_values, y_values)

        for diagram_type in self.diagram_types:
            fig1 = plt.figure()
            fig1.suptitle(diagram_type[0] + ' ' + self.method + ' scenario ' + self.scenario)
            ax1 = fig1.add_subplot(111, projection='3d')
            ax1.plot_surface(X, Y, getattr(self, diagram_type[0]), cmap="autumn_r", lw=10, rstride=1, cstride=1, alpha=0.6)
            ax1.plot_wireframe(X, Y, getattr(self, diagram_type[0]), rstride=1, cstride=0, color="black", linewidth=1)
            ax1.set_ylabel('Cell #')
            ax1.set_xlabel('Time [s]')
            ax1.set_zlabel(diagram_type[0] + ' ' + diagram_type[1])
            if save_plots:
                plt.savefig('plots/' + diagram_type[0] + ' ' + self.method + ' scenario ' + self.scenario + '.png', dpi=dpi)
            if show_plots:
                plt.show()

    def animate(self):
        max_flow = self.flow.max()
        max_density = self.density.max()
        max_speed = self.speed.max()
        max_time = self.delta_time * self.nr_of_steps * 3600

        array = []
        for index in range(len(self.net.cells)):
            array.append(index)
        x_values = []
        for cell in self.net.cells:
            x_values.append(cell.id)

        for step in range(self.nr_of_steps):

            time = self.delta_time * step * 3600

            y_values1 = self.flow[array, step]
            y_values2 = self.density[array, step]
            y_values3 = self.speed[array, step]

            # Plot the subplots
            # Plot 1
            plt.subplot(4, 1, 1)
            plt.plot(x_values, y_values1, 'g')
            plt.title('Animation')
            plt.ylim(0, max_flow)
            plt.xlabel('Cells')
            plt.ylabel('Flow [veh/h]')

            # Plot 2
            plt.subplot(4, 1, 2)
            plt.plot(x_values, y_values2, '-.r')
            plt.ylim(0, max_density)
            plt.xlabel('Cells')
            plt.ylabel('Density [veh/km]')

            # Plot 3
            plt.subplot(4, 1, 3)
            plt.plot(x_values, y_values3, '-.y')
            plt.ylim(0, max_speed)
            plt.xlabel('Cells')
            plt.ylabel('Speed [km/h]')

            # Time Counter Slider
            plt.subplot(4, 1, 4)
            plt.barh("0", time)
            plt.xlim(0, max_time)
            plt.ylabel('Time [s]')

            plt.pause(0.01)
            plt.clf()

        plt.show()

    def print(self):
        print("VKT: "+str(round(self.vkt, len(str(round(1/self.precision)))))+"   VHT: "+str(round(self.vht, len(str(round(1/self.precision))))))
