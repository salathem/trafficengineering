class FundamentalDiagram:
    def __init__(self, flow_capacity=2000, jam_density=180, free_flow_speed=100):
        critical_density = flow_capacity / free_flow_speed
        congestion_wave_speed = flow_capacity / (jam_density - critical_density)
        self.flow_capacity = flow_capacity  # flow capacity (veh/h/lane)
        self.critical_density = critical_density  # Criticaltical density (veh/km/lane)
        self.jam_density = jam_density  # Jam density (veh/km/lane)
        self.free_flow_speed = free_flow_speed  # Free Flow Speed (km/h)
        self.congestion_wave_speed = congestion_wave_speed  # Congestion Wave Speed (km/h)

    def print(self):
        print("Flow Capacity: ", self.flow_capacity)
        print("Critical Density: ", self.critical_density)
        print("Jam Density: ", self.jam_density)
        print("Free Flow Speed: ", self.free_flow_speed)
        print("Congestion Wave Speed: ", self.congestion_wave_speed)


class Cell():
    def __init__(self, fd, lanes=3, length=0.5, x_in=0, b_out=0):
        super().__init__(fd)  # lanes * fd.flow_capacity, lanes * fd.jam_density, fd.free_flow_speed)
        self.lanes = lanes  # Lanes [-]
        self.length = length  # Length[km]
        # self.flow_capacity = lanes * fundamentaldiagram.flow_capacity
        # self.critical_density = lanes * fundamentaldiagram.critical_density
        # self.jam_density = lanes * fundamentaldiagram.jam_density
        self.x_in = x_in  # Max Onramp Demand [veh/h]
        self.b_out = b_out  # Off ramp Split Ration [-]
        self.n = [0]  # Anzahl Veh in cell [veh]
        self.p = []  # Dichte Veh in cell [veh/km]
        self.q = []  # Flow aus Zelle [veh/h]
        self.x = []  # Onramp Demand [veh/h]
        self.r = []  # Metered Onramp Flow [veh/h]
        self.s = []  # Outflow Cell
        # self.free_flow_speed = fundamentaldiagram.free_flow_speed
        # self.congestion_wave_speed = fundamentaldiagram.congestion_wave_speed
        self.onrampqueue = [0]

    def setindex(self, index):
        self.index = index

    def appendflow(self, flow):
        self.q.append(flow)

    def appenddensity(self, density):
        self.p.append(density)

    def setvolume(self, volume):
        self.volume = volume

    def readattribute(self, attribute):
        if attribute == "volume":
            return self.n
        elif attribute == "density":
            return self.p
        elif attribute == "flow":
            return self.q
        elif attribute == "onrampflow":
            return self.x
        elif attribute == "meteredonrampflow":
            return self.r
        elif attribute == "offrampflow":
            return self.s
        else:
            print("Cell attribute could not be read. No valid Attribute give.")

    def print(self):
        print("Index: ", self.index)
        print("Anzahl Linien: ", self.lanes)
        print("Länge: ", self.length)
        print("Demand Onramp In: ", self.x_in)
        print("Ratio Onramp Out: ", self.b_out)
        print("Flow Capacity: ", self.flow_capacity)
        print("Critical Density: ", self.critical_density)
        print("Jam Density: ", self.jam_density)
        print("Free Flow Speed: ", self.free_flow_speed)
        print("Congestion Wave Speed: ", self.congestion_wave_speed)


fd = FundamentalDiagram()
cell1 = Cell(fd)
cell1.setindex(1)
cell1.print()
