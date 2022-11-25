# libraries
# files
from fd import Fundamentaldiagram
from data import *
from network import Network
from alinea import Alinea
import numpy as np
from source import Source

# parameters to change by User
method = "metanet"
nr_of_steps = 500
delta_time = 10 / 3600
scenario = 2
k = 0.173
is_applied = True   # alinea is applied
precision = 0.0001 # precision of alinea optimizer


# initialize Fundamentaldiagram
fd = Fundamentaldiagram()

# initialize Network
net = Network(method)

# set Simulation Parameters from exercise
net.set_simulation(nr_of_steps, delta_time)

# set scenario Parameters from exercise
net.set_scenario(fd, scenario, method)

# set alinea
alinea = Alinea(k, is_applied)
alinea.optimize(net, precision)

# set scenario Parameters from exercise
net.set_scenario(fd, scenario, method, alinea, alinea.k, delta_time)

data = Data(nr_of_steps, net)

# cfl condition check
net.check_cfl()

# simulation
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



