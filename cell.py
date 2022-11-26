from source import Source


class Cell:
    def __init__(self, length, lanes, fd, delta_time, flow=0, vehicles=0, beta=0, on_ramp_demand=0):
        self.vehicles = vehicles
        self.length = length
        self.flow = flow
        self.density = self.vehicles / self.length
        if self.density:
            self.speed = self.flow / self.density
        else:
            self.speed = fd.freeflow_speed
        if on_ramp_demand:
            self.has_on_ramp = True
        else:
            self.has_on_ramp = False
        if beta:
            self.has_off_ramp = True
        else:
            self.has_off_ramp = False
        self.on_ramp_demand = on_ramp_demand
        self.delta_time = delta_time
        self.beta = beta
        self.lanes = lanes
        self.inflow = 0
        self.outflow = 0
        self.time_step = 0

        # objects
        self.add_on_ramp()
        self.previous_cell = None
        self.next_cell = None
        self.off_ramp = None

        # calculations
        self.freeflow_speed = fd.freeflow_speed
        self.jam_density = fd.jam_density * lanes
        self.maximum_flow = fd.maximum_flow * lanes

    def add_on_ramp(self, alinea=None):
        if self.has_on_ramp:
            demand_onramp_points = [0, 900 / 3600, 2700 / 3600, 3600 / 3600, 5000 / 3600]
            demand_onramp_values = [0, self.on_ramp_demand, self.on_ramp_demand, 0, 0]
            # initialize on-ramp cell
            on_ramp = Source(self.delta_time, demand_onramp_points, demand_onramp_values, alinea)
            on_ramp.next_cell = self
            self.on_ramp = on_ramp
        else:
            self.on_ramp = None

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




