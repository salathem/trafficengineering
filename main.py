# import files
from cell import Fundamentaldiagram
from simulation import *
from network import Network
from alinea import Alinea
from functions import *
# -------------------------------------------------------------------------------------------------------------
# parameters to change by User
method = "metanet"  # method (ctm/metanet/all)
nr_of_steps = 500   # Nummer of Steps of Simulation
delta_time = 10 / 3600  # Delta T of Simulation [h]
scenario = "c"    # Scenario from Exercise (a/b/c/all)
precision = 0.0001  # precision of alinea optimizer and data print() [-]

# visualisation
show_plots = True      # (True/False)
show_animation = False  # (True/False)
show_values = True      # (True/False)
save_plots = False       # (True/False)
diagram_type = "3D"     # (2D/3D)
dpi = 600

# for metanet only
# set True to apply alinea Ramp metering
is_applied = True
# k = 0 : Ramp metering off
k = 0.173      # k Value for Metanet if not calculate [-]
optimise_k = True  # set True to calculate optimal K-Value

# -------------------------------------------------------------------------------------------------------------
if user_input_check(method, nr_of_steps, delta_time, scenario, precision, show_plots, show_animation, show_values, save_plots, diagram_type, dpi, is_applied, k, optimise_k):

    if not is_applied:
        k = 0
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
            if diagram_type == "2D":
                simulation.plot_2d(show_plots, save_plots, dpi)
            if diagram_type == "3D":
                simulation.plot_3d(show_plots, save_plots, dpi)
            if diagram_type == "all":
                simulation.plot_2d(show_plots, save_plots, dpi)
                simulation.plot_3d(show_plots, save_plots, dpi)
            if show_animation:
                simulation.animate()
            if show_values:
                simulation.print()
