import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from objects import *
from simulation import *
from plot import *
#from ctm import *
from metanet import *

Q = 2000                # Maximum Flow [veh/h/lane]
p_jam = 180             # Maximum Flow [veh/h/lane]
v_f = 100               # Free Flow Speed [km/h]
time_step = 1/3600                # Time Intervall [s]
t_simu = 5000           # Duration of Simulation [s]

fundamentaldiagram = FundamentalDiagram(Q, p_jam, v_f)
method = "metanet"       # "ctm" or "metanet"


#Define Network
net = Network(method)
net.setscenario(fundamentaldiagram, 1)
net.print()

#Run Simulation
simu = Simulation(net, step_time=time_step)
simu.cflcheck()
if True:
    for time in simu.all_steps:
        k = simu.k
        t = k * simu.step_time
        simu.setdemand(t)
        simu.updatedensity(k)   #
        simu.updateflow(k)
        simu.updatevolume(k)
        simu.updatespeed(k)
        simu.k += 1

    plt = Plot(simu, "all")        #  "all", "flow", "density", "speed"


#net.print()