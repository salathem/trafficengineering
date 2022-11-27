# import files
from cell import Fundamentaldiagram
from simulation import *
from network import Network
from alinea import Alinea

# parameters to change by User
method = "metanet"  # method (ctm/metanet)
nr_of_steps = 500   # Nummer of Steps of Simulation
delta_time = 10 / 3600  # Delta T of Simulation [h]
scenario = 2    # Scenario from Exercise (1=1, 2=b, 3=c)
precision = 0.0001  # precision of alinea optimizer and data print() [-]

# visualisation
show_plots = True
show_animation = False
show_values = True
save_plots = False

# for metanet only
# set True to apply alinea Ramp metering
is_applied = True
# k = 0 : Ramp metering off
k = 0      # k Value for Metanet if not calculate [-]
optimise_k = True  # set True to calculate optimal K-Value

# -------------------------------------------------------------------------------------------------------------

if not is_applied:
    k = 1
    optimise_k = False

# initialize Fundamentaldiagram
fd = Fundamentaldiagram()

# initialize Network
net = Network(method)
net.set_simulation(nr_of_steps, delta_time)
# set Simulation Parameters from exercise
#net.set_scenario(fd, scenario)
net.set_scenario(fd, scenario)

# initialize alinea
alinea = Alinea(k, is_applied, optimise_k)

if method == "metanet":
    if optimise_k:
        alinea.optimize(net, precision)

    # set scenario Parameters from exercise
    net.set_scenario(fd, scenario, alinea)

simulation = Simulation(net, nr_of_steps, delta_time, precision)

# cfl condition check
net.check_cfl()

# simulation
simulation.run()

# show data
if show_plots:
    simulation.plot(save_plots)
if show_animation:
    simulation.animate()
if show_values:
    simulation.print()
