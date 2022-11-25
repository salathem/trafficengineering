# import files
from fd import Fundamentaldiagram
from data import *
from network import Network
from alinea import Alinea

# parameters to change by User
method = "metanet"  # method (ctm/metanet)
nr_of_steps = 500   # Nummer of Steps of Simulation
delta_time = 10 / 3600  # Delta T of Simulation
scenario = 3    # Scenario from Exercise (1=1, 2=b, 3=c)
k = 0.173       # k Value for Metanet if not calculate
is_applied = True   # alinea is applied
precision = 0.0000001  # precision of alinea optimizer

# -------------------------------------------------------------------------------------------------------------

# initialize Fundamentaldiagram
fd = Fundamentaldiagram()
# initialize Network
net = Network(method)
# set Simulation Parameters from exercise
net.set_simulation(nr_of_steps, delta_time)
net.set_scenario(fd, scenario, method)

# set alinea
alinea = Alinea(k, is_applied)
alinea.optimize(net, precision)

# set scenario Parameters from exercise
net.set_scenario(fd, scenario, method, alinea)

data = Data(nr_of_steps, net)

# cfl condition check
#net.check_cfl()

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


#data.animate()
data.print()
#data.plot()



