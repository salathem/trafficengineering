from source import Source


class Fundamentaldiagram:
    def __init__(self, freeflow_speed=100, jam_density=180, maximum_flow=2000, lanes=1):
        # init
        self.freeflow_speed = freeflow_speed
        self.jam_density = jam_density * lanes
        self.maximum_flow = maximum_flow * lanes


class Cell(Fundamentaldiagram):
    def __init__(self, length, lanes, delta_time, fd, flow=0, vehicles=0, beta=0, on_ramp_demand=0, freeflow_speed=100, jam_density=180, maximum_flow=2000):
        super(Cell, self).__init__(freeflow_speed, jam_density, maximum_flow, lanes)
        self.id = None
        self.vehicles = vehicles
        self.length = length
        self.flow = flow
        self.density = self.vehicles / self.length
        if self.density:
            self.speed = self.flow / self.density
        else:
            self.speed = fd.freeflow_speed

        self.on_ramp_demand = on_ramp_demand
        self.delta_time = delta_time
        self.beta = beta
        self.lanes = lanes
        self.inflow = 0
        self.outflow = 0
        self.time_step = 0

        # objects
        self.previous_cell = None
        self.next_cell = None

        self.setup_ramps()

    def setup_ramps(self):
        if self.on_ramp_demand:
            self.has_on_ramp = True
            self.add_on_ramp()
        else:
            self.has_on_ramp = False
            self.on_ramp = None
        if self.beta:
            self.has_off_ramp = True
        else:
            self.has_off_ramp = False
            self.off_ramp = None

    def add_on_ramp(self, alinea=None):
        demand_onramp_points = [0, 900 / 3600, 2700 / 3600, 3600 / 3600, 5000 / 3600]
        demand_onramp_values = [0, self.on_ramp_demand, self.on_ramp_demand, 0, 0]
        # initialize on-ramp cell
        on_ramp = Source(self.delta_time, demand_onramp_points, demand_onramp_values, alinea)
        on_ramp.next_cell = self
        self.on_ramp = on_ramp

    def performance_calculation(self):
        cell_vkt = self.delta_time * self.flow * self.length
        cell_vht = self.delta_time * self.density * self.length

        if self.has_on_ramp:
            cell_vht += self.on_ramp.queue * self.delta_time

        return cell_vkt, cell_vht

    def check_cfl(self):
        if self.delta_time < (self.length/self.freeflow_speed):
            print("CFL Condition OK for Cell "+str(self.id)+".")
        else:
            print("CFL Condition Not OK for Cell "+str(self.id)+"!!!")

    def downstream_supply(self):
        return self.next_cell.congestion_wave_speed * (self.next_cell.jam_density - self.next_cell.density)     # 𝑤i+1 (𝜌i+1_jam− 𝜌i+1(𝑘))
