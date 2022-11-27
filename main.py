# import files
from cell import Fundamentaldiagram
from simulation import *
from network import Network
from alinea import Alinea

# parameters to change by User
method = "all"  # method (ctm/metanet/all)
nr_of_steps = 500   # Nummer of Steps of Simulation
delta_time = 10 / 3600  # Delta T of Simulation [h]
scenario = "all"    # Scenario from Exercise (a/b/c/all)
precision = 0.001  # precision of alinea optimizer and data print() [-]

# visualisation
show_plots = False
show_animation = False
show_values = True
save_plots = True
dpi = 300

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

# set parameters for all methods
if method.lower() == "all":
    methods = ["ctm", "metanet"]
else:
    methods = [method.lower()]
# set parameters for all scenarios
if scenario.lower() == "all":
    scenarios = ["a", "b", "c"]
else:
    scenarios = [scenario.lower()]


for method in methods:
    print("-------------------------------------------")
    print("Method ", method.upper())
    for scenario in scenarios:
        print("--------------------")
        print("Scenario ", scenario)
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
        # net.check_cfl()

        # simulation
        simulation.run()

        # show data
        simulation.plot(show_plots, save_plots, dpi)
        if show_animation:
            simulation.animate()
        if show_values:
            simulation.print()
