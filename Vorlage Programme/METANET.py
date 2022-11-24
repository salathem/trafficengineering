
import copy
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

#Inputs
sektorenanzahl = int(input("hom much cells? "))
länge = int(input("How long are the cells in m? "))
spuren = list(range(0,sektorenanzahl))
input("ATTENTION: THE FIRST CELL IS CELL 0")
for x in spuren:
    spuren[x] = int(input("How many lanes in cell {}? ".format(x)))
einfahrtssektor1 = int(input("In which cell is the on ramp? "))
einfahrtssektor = einfahrtssektor1+1

jam = int(input("How high is the jam density in veh//km//lane? "))
critical = int(input("How high is the critical density in veh//km//lane? "))
maximum = int(input("How high is the maximum flow in veh//km//lane? "))
#simulationduration = int(input("How long is the Simulation in s? "))
simulationduration = 5000
highwaydemand = int(input("How high is the highway demand [d] in veh//h? "))
onrampdemand = int(input("How high is the onramp demand [x] in veh//h? "))


zellen = list(range(0,sektorenanzahl))
zellen1 = list(range(0,sektorenanzahl+1))



t = 18
v = 60
k = 40
a = 2
sigma = 1.4
timeperiod = 10
timeintervall = int(simulationduration/timeperiod)
timeslots = list(range(0,timeintervall))

matrix = list(range(0,sektorenanzahl))
for x in zellen:
    matrix[x] = copy.deepcopy(timeslots)


for x in zellen:
    for y in timeslots:
        matrix[x][y] = 0


matrix2 = list(range(0,sektorenanzahl+1))
for x in zellen1:
    matrix2[x] = copy.deepcopy(timeslots)

for x in zellen1:
    for y in timeslots:
        matrix2[x][y] = 0

flowmatrix = copy.deepcopy(matrix)
densitymatrix = copy.deepcopy(matrix2)
vmatrix = copy.deepcopy(matrix)
vehmatrix = copy.deepcopy(matrix)
capacitymatrix = copy.deepcopy(matrix)
vp = copy.deepcopy(matrix)
N1 = copy.deepcopy(timeslots)+[1]
for x in N1:
    N1[x] = 0
N2 = copy.deepcopy(N1)
highwaygo = copy.deepcopy(N1)
onrampgo = copy.deepcopy(N1)
r1 = copy.deepcopy(N1)
startgo = copy.deepcopy(N1)
Qmax = copy.deepcopy(N1)



highwaydemandlist = copy.deepcopy(timeslots)

peakpoint1 = 450/timeperiod
peakpoint2 = 3150/timeperiod
endpoint1 = 3600/timeperiod

# The Demand befor the first Cell ist set up over the whole timelenght
for x in highwaydemandlist:
    if x < peakpoint1:
        highwaydemandlist[x] = (x+x+1)/2*highwaydemand/peakpoint1
    elif x < peakpoint2:
        highwaydemandlist[x] = highwaydemand
    elif x < endpoint1:
        highwaydemandlist[x] = highwaydemand-((x+x+1)/2*timeperiod-3150)/timeperiod*highwaydemand/(endpoint1-peakpoint2)
    else:
        highwaydemandlist[x] = 0

# The Demand for the onramp is set up for the whole time length
onrampdemandlist = copy.deepcopy(timeslots)
peakpoint3 = 900/timeperiod
peakpoint4 = 2700/timeperiod
endpoint2 = 3600/timeperiod

for x in onrampdemandlist:
    if x < peakpoint3:
        onrampdemandlist[x] = (x+x+1)/2*onrampdemand/peakpoint3
    elif x < peakpoint4:
        onrampdemandlist[x] = onrampdemand
    elif x < endpoint2:
        onrampdemandlist[x] = onrampdemand-((x+x+1)/2*timeperiod-2700)/timeperiod*onrampdemand/(endpoint2-peakpoint4)
    else:
        onrampdemandlist[x] = 0


vi = maximum/critical
wi = maximum/(jam-critical)
# Kontrolle damit die CL Kondition eingehalten wird
if vi > (länge/1000)/(timeperiod/3600):
    print("Die Länge ist zu kurz!")
    exit()

timing = range(0,timeintervall-1)

for z in zellen1:
    for y in timing:

        # Speed as a function of density
        for x in zellen:
            vp[x][y] = (vi) * np.exp((-1 / a) * (densitymatrix[x][y] / critical) ** a)

        #Virtual Que
        startgo[y] = highwaydemandlist[y] + N2[y] / (timeperiod / 3600)
        if startgo[y] > maximum * spuren[0]:
            startgo[y] = maximum * spuren[0]
        if startgo[y] > (vp[0][y]*critical)/(jam-critical)* (jam - densitymatrix[0][y]) * spuren[0]:
            startgo[y] = (vp[0][y]*critical)/(jam-critical)* (jam - densitymatrix[0][y]) * spuren[0]


        #Capacity
        for x in zellen:
            capacitymatrix[x][y] = vmatrix[x][y]*densitymatrix[x][y]*spuren[x]

        # Onrampcapacity
        highwaygo[y] = vmatrix[einfahrtssektor - 2][y] * densitymatrix[einfahrtssektor - 2][y] * int(spuren[einfahrtssektor - 2])
        Qmax[y] = vp[einfahrtssektor-1][y]*critical
        if highwaygo[y] > (Qmax[y]/(jam-critical)) * (jam - densitymatrix[einfahrtssektor - 1][y]) * int(spuren[einfahrtssektor - 1]):
            highwaygo[y] = (maximum)/(jam-critical) * (jam - densitymatrix[einfahrtssektor - 1][y]) * int(spuren[einfahrtssektor - 1])
        elif highwaygo[y] > int(spuren[einfahrtssektor - 2]) * maximum:
            highwaygo[y] = int(spuren[einfahrtssektor - 2]) * maximum
        r1[y] = N1[y] / (timeperiod / 3600) + onrampdemandlist[y]
        if highwaygo[y] + r1[y] <= (Qmax[y]/(jam-critical)) * (jam - densitymatrix[einfahrtssektor - 1][y]) * int(spuren[einfahrtssektor - 1]):
            capacitymatrix[einfahrtssektor - 2][y] = copy.deepcopy(highwaygo[y])
            onrampgo[y] = copy.deepcopy(r1[y])
        else:
            capacitymatrix[einfahrtssektor - 2][y] = highwaygo[y] / (highwaygo[y] + r1[y]) * (Qmax[y]/(jam-critical)) * (jam - densitymatrix[einfahrtssektor - 1][y]) * int(spuren[einfahrtssektor - 1])
            onrampgo[y] = r1[y] / (highwaygo[y] + r1[y]) *(Qmax[y]/(jam-critical)) * (jam - densitymatrix[einfahrtssektor - 1][y]) * int(spuren[einfahrtssektor - 1])

        #densitymatrix
        for x in zellen:
            if x == 0:
                densitymatrix[x][y + 1] = densitymatrix[x][y] + (timeperiod / 3600) / (länge / 1000 * spuren[x]) * (startgo[y] - capacitymatrix[x][y])
            elif x == einfahrtssektor-1:
                densitymatrix[x][y + 1] = densitymatrix[x][y] + (timeperiod / 3600) / (länge / 1000 * spuren[x]) * (capacitymatrix[x - 1][y] - capacitymatrix[x][y] + onrampgo[y])
            else:
                densitymatrix[x][y + 1] = densitymatrix[x][y] + (timeperiod / 3600) / (länge / 1000 * spuren[x]) * (capacitymatrix[x - 1][y] - capacitymatrix[x][y])
        densitymatrix[sektorenanzahl][y] = copy.deepcopy(densitymatrix[sektorenanzahl - 1][y])



        #Speed
        for x in zellen:
            if x == 0:
                vmatrix[x][y + 1] = vmatrix[x][y] + (timeperiod/3600) / (t/3600) * (vp[x][y] - vmatrix[x][y]) - ( v * timeperiod / 3600) / (t / 3600 * länge / 1000) * (densitymatrix[x + 1][y] - densitymatrix[x][y]) / (densitymatrix[x][y] + k)
            elif x == einfahrtssektor-1:
                vmatrix[x][y + 1] = vmatrix[x][y] + (timeperiod/3600) / (t/3600) * (vp[x][y] - vmatrix[x][y]) + (timeperiod / 3600) / (länge / 1000) * vmatrix[x][y] * (vmatrix[x - 1][y] - vmatrix[x][y]) - (v * timeperiod / 3600) / (t / 3600 * länge / 1000) * ((densitymatrix[x + 1][y] - densitymatrix[x][y]) / (densitymatrix[x][y] + k)) - (sigma * timeperiod / 3600) / (länge / 1000 * spuren[x]) * ((onrampgo[y] + vmatrix[x][y]) / (densitymatrix[x][y] + k))
            else:
                vmatrix[x][y + 1] = vmatrix[x][y] + (timeperiod / 3600) / (t / 3600) * (vp[x][y] - vmatrix[x][y]) + (timeperiod / 3600) / (länge / 1000) * vmatrix[x][y] * (vmatrix[x - 1][y] - vmatrix[x][y]) - (v * timeperiod / 3600) / (t / 3600 * länge / 1000) * ((densitymatrix[x + 1][y] - densitymatrix[x][y]) / (densitymatrix[x][y] + k))

        #Virtual Ques
        N1[y + 1] = N1[y] + (onrampdemandlist[y] - onrampgo[y]) * timeperiod / 3600
        N2[y + 1] = N2[y] + float(highwaydemandlist[y] - startgo[y]) * timeperiod / 3600




question = 'yes'
while question == 'yes':
    diagrammtyp = int(input("Which diagram do you want?[density=1,flow=2,speed=3]"))

    if diagrammtyp == 1:
        # Diagramm erstellen
        ax = plt.axes( projection="3d")
        x = np.array(zellen1)
        x, y = np.meshgrid(timeslots, x)
        z = np.asmatrix(densitymatrix)

        ax.plot_surface(x, y, z, lw=0, cmap='gray')

        # Diagramm Beschriftungen
        ax.set_xlabel('Timeslot')
        ax.set_ylabel('Cells')
        ax.set_zlabel('Density per Line[veh/km/lane]')
        ax.set(title='Density')
        plt.savefig("plot.png")
        plt.show()
    elif diagrammtyp == 2:
        # Diagramm erstellen
        ax = plt.axes(projection="3d")
        x = np.array(zellen)
        x, y = np.meshgrid(timeslots, x)
        z = np.asmatrix(capacitymatrix)

        ax.plot_surface(x, y, z, lw=0, cmap='gray')

        # Diagramm Beschriftungen
        ax.set_xlabel('Timeslot')
        ax.set_ylabel('Measurepoints')
        ax.set_zlabel('Capacity [veh/h]')
        ax.set(title='Flow')

        plt.savefig("plot.png")
        plt.show()
    elif diagrammtyp == 3:
        # Diagramm erstellen
        ax = plt.axes(projection="3d")
        x = np.array(zellen)
        x, y = np.meshgrid(timeslots, x)
        z = np.asmatrix(vmatrix)

        ax.plot_surface(x, y, z, lw=0, cmap='gray')

        # Diagramm Beschriftungen
        ax.set_xlabel('Timeslot')
        ax.set_ylabel('Cells')
        ax.set_zlabel('speed in km/h')
        ax.set(title='Speed')

        plt.savefig("plot.png")
        plt.show()
    else:
        print("These Diagram type is not available!")
    question = str(input("Wanna see a other Diagramm?[yes/no]"))

VKT = 0 #Berechnung von VKT
VHT = 0 #Berechnung von VHT
for y in timeslots:
    for x in zellen:
        VKT = VKT+capacitymatrix[x][y]*länge/1000
        VHT = VHT+densitymatrix[x][y]*spuren[x]*länge/1000
    VKT = VKT +N1[y]+N2[y]
VKT = VKT*timeperiod/3600
VHT = VHT*timeperiod/3600
print("VKT is ",int(VKT)," km")
print("VHT is ",int(VHT)," h")