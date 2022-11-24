# libraries
# files
from fd import Fundamentaldiagram
from data import *
from network import Network
from source import Source

# parameters to change by User
method = "metanet"
nr_of_steps = 500
delta_time = 10 / 3600
scenario = 1
alinea = False
alinea_k = 0.5



# initialize Fundamentaldiagram
fd = Fundamentaldiagram()
# initialize Network
net = Network(method)
# set scenario from exercise
net.set_scenario(fd, delta_time, scenario, method, alinea, alinea_k)
data = Data(nr_of_steps, net)

#   cfl condition check
for cell in net.cells:
     cell.check_cfl()

#   simulation
for sim_step in range(nr_of_steps):

    # update network demand
    net.demand.update(sim_step)
    for cell in net.cells:

        # calculate cell
        cell.update(sim_step)

        # update performance parameters
        temp_vkt, temp_vht = cell.performance_calculation()
        data.vkt += temp_vkt
        data.vht += temp_vht

    # advance simulation
    sim_step += 1
    # get data for plots
    data.update(net)

data.print()
data.plot()

if False:
        # scenario selection
        alinea = "n" #input('Alinea ramp metering active? y/n: ')
        alinea_k = 0
        alinea_optimisation = False
        if alinea == 'y':
            try:
                alinea_k = float(input('K value for ALINEA? (float): '))
                alinea_optimisation = input('run k factor optimisation? y/n: ')
            except:
                print('not a float value. Enter a float value')
                alinea_k = float(input('K value for ALINEA?: '))
                alinea_optimisation = input('run k factor optimisation? y/n: ')

        if alinea_optimisation == 'y':
            alinea_optimisation = True
        else:
            alinea_optimisation = False
        # parameters default
        ALINEA = False
        ALINEA_K = 0
        LANES_PER_CELL = 3
        LANES_PER_CELL_5 = 3
        DEMAND_PEAK_UPSTREAM = 4000
        DEMAND_PEAK_ONRAMP = 2000

        if scenario == 1:
            if alinea == 'y':
                ALINEA = True
                ALINEA_K = alinea_k
            else:
                ALINEA = False
                ALINEA_K = 0
            lanes = 3
            DEMAND_PEAK_UPSTREAM = 4000
            DEMAND_PEAK_ONRAMP = 2000
            fd = Fundamentaldiagram()
        # initialize all cells
        length = 0.5
        cell1 = Cell(length, lanes, fd, delta_time, 1)
        cell2 = Cell(length, lanes, fd, delta_time, 2)
        cell3 = Cell(length, lanes, fd, delta_time, 3, on_ramp_demand=DEMAND_PEAK_ONRAMP)
        cell4 = Cell(length, lanes, fd, delta_time, 4)
        cell5 = Cell(length, lanes, fd, delta_time, 5)
        cell6 = Cell(length, lanes, fd, delta_time, 6)

        # define upstream demand
        demand_upstream_points = [0, 450 / 3600, 3150 / 3600, 3600 / 3600, 5000 / 3600]
        demand_upstream_values = [0, DEMAND_PEAK_UPSTREAM, DEMAND_PEAK_UPSTREAM, 0, 0]
        # initialize upstream cell
        upstream = Source(delta_time, demand_upstream_points, demand_upstream_values, False, 0)

        # define on-ramp demand
        demand_onramp_points = [0, 900 / 3600, 2700 / 3600, 3600 / 3600, 5000 / 3600]
        demand_onramp_values = [0, DEMAND_PEAK_ONRAMP, DEMAND_PEAK_ONRAMP, 0, 0]
        # initialize on-ramp cell
        on_ramp1 = Source(delta_time, demand_onramp_points, demand_onramp_values, ALINEA, ALINEA_K, 7)

        # network structure
        upstream.next_cell = cell1
        cell1.previous_cell = upstream
        cell1.next_cell = cell2
        cell2.previous_cell = cell1
        cell2.next_cell = cell3
        cell3.previous_cell = cell2
        cell3.next_cell = cell4
        cell4.previous_cell = cell3
        cell4.next_cell = cell5
        cell5.previous_cell = cell4
        cell5.next_cell = cell6
        cell6.previous_cell = cell5
        on_ramp1.next_cell = cell3
        cell3.on_ramp = on_ramp1

        cells = [upstream, cell1, cell2, cell3, cell4, cell5, cell6]
        #    cells = [upstream] + net.cells
        print(cells)

        # for optimsation of k factor (alinea)
        temp_best_k = 0
        temp_min_vht = None
        temp_min_vht = None
        k_runner = 0

        # simulation
        while k_runner <= 1:
            # initialize on-ramp cell
            if alinea_optimisation:
                on_ramp1 = Source(delta_time, demand_onramp_points, demand_onramp_values, ALINEA, k_runner, 7)
            else:
                on_ramp1 = Source(delta_time, demand_onramp_points, demand_onramp_values, ALINEA, ALINEA_K, 7)

            # network structure
            upstream.next_cell = cell1
            cell1.previous_cell = upstream
            cell1.next_cell = cell2
            cell2.previous_cell = cell1
            cell2.next_cell = cell3
            cell3.previous_cell = cell2
            cell3.next_cell = cell4
            cell4.previous_cell = cell3
            cell4.next_cell = cell5
            cell5.previous_cell = cell4
            cell5.next_cell = cell6
            cell6.previous_cell = cell5
            on_ramp1.next_cell = cell3
            cell3.on_ramp = on_ramp1

            # network order
            cells = [upstream, cell1, cell2, cell3, cell4, cell5, cell6]

            # data collection
            flow_data = np.zeros([6, nr_of_steps])
            density_data = np.zeros([6, nr_of_steps])
            speed_data = np.zeros([6, nr_of_steps])
            vkt = 0
            vht = 0

            # simulation
            simstep = 0

            # simulation loop
            while (simstep < nr_of_steps):
                # simulation step
                for cell in cells:

                    # calculate cell
                    cell.update(timestep=simstep)

                    # update performance parameters
                    temp_vkt, temp_vht = cell.performance_calculation()
                    vkt += temp_vkt
                    vht += temp_vht

                    # get data for plots
                    if type(cell) is Cell:
                        cell.dump_data(flow_data, density_data, speed_data)
                        #data.update_cell(cell)
                # advance simulation
                simstep += 1
            print(vkt, vht, k_runner)

            if not alinea_optimisation:
                break
            else:
                if not temp_min_vht == None:
                    if temp_min_vht > vht:
                        temp_min_vht = vht
                        temp_min_vkt = vkt
                        temp_best_k = k_runner
                else:
                    temp_min_vht = vht
                    temp_min_vkt = vkt

                k_runner += 0.001
        if alinea_optimisation:
            print('optimized results\nBest K:', temp_best_k, 'Minimal VHT:', temp_min_vht, 'Minimal VKT:', temp_min_vkt)

        if True:
            # plotting
            xvalues = np.linspace(0, nr_of_steps, nr_of_steps)
            yvalues = np.array([1, 2, 3, 4, 5, 6])
            X, Y = np.meshgrid(xvalues, yvalues)

            # flow graph
            fig1 = plt.figure()
            fig1.suptitle('flow', fontsize=32)
            ax1 = fig1.add_subplot(111, projection='3d')
            ax1.plot_wireframe(X, Y, flow_data)
            plt.show()

            # density graph
            fig2 = plt.figure()
            fig2.suptitle('density', fontsize=32)
            ax2 = fig2.add_subplot(111, projection='3d')
            ax2.plot_wireframe(X, Y, density_data)
            plt.show()

            # speed graph
            fig3 = plt.figure()
            fig3.suptitle('speed', fontsize=32)
            ax3 = fig3.add_subplot(111, projection='3d')
            ax3.plot_wireframe(X, Y, speed_data)
            plt.show()


