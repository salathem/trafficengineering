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


class Cell(FundamentalDiagram):
    def __init__(self, fd, lanes=3, length=0.5, x_in=0, b_out=0):
        super().__init__()
        self.lanes = lanes  # Lanes [-]
        self.length = length  # Length[km]
        self.flow_capacity = lanes * fd.flow_capacity
        self.critical_density = lanes * fd.critical_density
        self.jam_density = lanes * fd.jam_density
        self.x_in = x_in  # Max Onramp Demand [veh/h]
        self.b_out = b_out  # Off ramp Split Ration [-]
        self.n = [0]  # Anzahl Veh in cell [veh]
        self.p = []  # Dichte Veh in cell [veh/km]
        self.q = []  # Flow aus Zelle [veh/h]
        self.x = []  # Onramp Demand [veh/h]
        self.r = []  # Metered Onramp Flow [veh/h]
        self.v = []  # Geschwindigkeit cell [km/h]
        self.s = []  # Outflow Cell
        self.free_flow_speed = fd.free_flow_speed
        self.congestion_wave_speed = fd.congestion_wave_speed
        self.on_ramp_queue = [0]
        self.is_first_cell = False
        self.is_last_cell = False

    def readattribute(self, attribute):
        if attribute == "volume":
            return self.n
        elif attribute == "density":
            return self.p
        elif attribute == "flow":
            return self.q
        elif attribute == "speed":
            return self.v
        elif attribute == "onrampflow":
            return self.x
        elif attribute == "meteredonrampflow":
            return self.r
        elif attribute == "offrampflow":
            return self.s
        else:
            print("Cell attribute could not be read. No valid Attribute give.")

    def print(self):
        try:
            print("Index: ", self.index)
        except:
            print("Indexes must be set first in Class Network")
        print("Anzahl Linien: ", self.lanes)
        print("Länge: ", self.length)
        print("Demand Onramp In: ", self.x_in)
        print("Ratio Onramp Out: ", self.b_out)
        if self.is_first_cell:
            print("is first cell")
        if self.is_last_cell:
            print("is last cell")
        print("Flow Capacity: ", self.flow_capacity)
        print("Critical Density: ", self.critical_density)
        print("Jam Density: ", self.jam_density)
        print("Free Flow Speed: ", self.free_flow_speed)
        print("Congestion Wave Speed: ", self.congestion_wave_speed)


class Network:
    def __init__(self, method):
        self.cells = []
        self.method = method
        self.q = []
        self.d = []

    def add_cell(self, cell):
        self.cells.append(cell)

    def indexcells(self):
        index = 0
        for cell in self.cells:
            cell.index = index
            index += 1

    def setfirstandlastcell(self):
        for cell in self.cells:

            if cell.index == 0:
                cell.is_first_cell = True
            else:
                cell.is_first_cell = False

            if cell.index == len(self.cells) - 1:
                cell.is_last_cell = True
            else:
                cell.is_last_cell = False

    def getpreviouscell(self, cell):
        if cell.index > 0:
            return self.cells[cell.index - 1]
        else:
            print("No Previous Cell")
            return self.cells[cell.index - 1]

    def getfollowingscell(self, cell):
        if cell.index < len(self.cells) - 1:
            return self.cells[cell.index + 1]
        else:
            print("No Following Cell")
            return self.cells[cell.index + 1]

    def print(self):
        for cell in self.cells:
            cell.print()
            print()

    def setscenario(self, fd, index):
        # cell = Cell(lanes, length, d_in, d_out, x_in, B_out)
        for i in range(6):
            self.add_cell(Cell(fd))

        if index == 1:
            # Scenario a)
            self.demand = 4000
            self.cells[2] = Cell(fd, 3, 0.5, 2000, 0)
        if index == 2:
            # Scenario b)
            self.demand = 4000
            self.cells[2] = Cell(fd, 3, 0.5, 2500, 0)
        if index == 3:
            # Scenario c)
            self.demand = 1500
            self.cells[2] = Cell(fd, 3, 0.5, 1500, 0)

        self.indexcells()
        self.setfirstandlastcell()
