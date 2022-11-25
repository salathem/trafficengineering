# import files
from fd import Fundamentaldiagram
from data import *
from network import Network
from alinea import Alinea

# parameters to change by User
method = "metanet"  # method (ctm/metanet)
nr_of_steps = 500   # Nummer of Steps of Simulation
delta_time = 10 / 3600  # Delta T of Simulation [h]
scenario = 4    # Scenario from Exercise (1=1, 2=b, 3=c)
precision = 0.001  # precision of alinea optimizer and data print() [-]

# visualisation
show_plots = True
show_animation = False
show_values = True

# for metanet only
# set True to apply alinea Ramp metering
is_applied = True
# k = 0 : Ramp metering off
k = 0.5       # k Value for Metanet if not calculate [-]
optimise_k = False  # set True to calculate optimal K-Value

# -------------------------------------------------------------------------------------------------------------

if not is_applied:
    k = 1
    optimise_k = False

# initialize Fundamentaldiagram
fd = Fundamentaldiagram()

# initialize Network
net = Network(method)
net.set_simulation(nr_of_steps, delta_time)

# initialize alinea
alinea = Alinea(k, is_applied, optimise_k)

if method == "metanet":

    # set Simulation Parameters from exercise
    net.set_scenario(fd, scenario, method)

    if optimise_k:
        alinea.optimize(net, precision)

    # set scenario Parameters from exercise
    net.set_scenario(fd, scenario, method, alinea)

else:
    net.set_scenario(fd, scenario, method)

data = Data(nr_of_steps, delta_time, net, precision)

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

# show data
if show_plots:
    data.plot()
if show_animation:
    data.animate()
if show_values:
    data.print()



