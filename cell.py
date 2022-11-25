from source import Source


class Cell:
    def __init__(self, length, lanes, fd, delta_time, flow=0, vehicles=0, beta=0, on_ramp_demand=0):
        self.vehicles = vehicles
        self.length = length
        self.flow = flow
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
        if self.has_on_ramp:
            demand_onramp_points = [0, 900 / 3600, 2700 / 3600, 3600 / 3600, 5000 / 3600]
            demand_onramp_values = [0, self.on_ramp_demand, self.on_ramp_demand, 0, 0]
            # initialize on-ramp cell
            on_ramp = Source(delta_time, demand_onramp_points, demand_onramp_values)
            on_ramp.next_cell = self
            self.on_ramp = on_ramp
        else:
            self.on_ramp = None
        self.previous_cell = None
        self.next_cell = None
        self.off_ramp = None

        # calculations
        self.freeflow_speed = fd.freeflow_speed
        self.jam_density = fd.jam_density * lanes
        self.maximum_flow = fd.maximum_flow * lanes
        self.critical_density = self.maximum_flow / self.freeflow_speed
        self.congestion_wave_speed = fd.congestion_wave_speed

        # main parameters
        self.density = self.vehicles / self.length
        self.flow = self.get_flow()

        if self.density:
            self.speed = self.flow / self.density
        else:
            self.speed = fd.freeflow_speed

    # update parameters
    def update(self, time_step):

        self.time_step = time_step

        #inflow
        if self.has_on_ramp:
            self.inflow = self.previous_cell.outflow + self.on_ramp.outflow
        else:
            self.inflow = self.previous_cell.outflow

        #outflow
        if self.next_cell:
            if not self.next_cell.has_on_ramp:
                self.outflow = min((1-self.beta) * self.speed * self.density, self.next_cell.congestion_wave_speed * (self.next_cell.jam_density - self.next_cell.density), self.maximum_flow)
            else:
                temp_outflow_cell = min((1-self.beta) * self.speed * self.density, self.next_cell.congestion_wave_speed * (self.next_cell.jam_density - self.next_cell.density), self.maximum_flow)
                temp_outflow_on_ramp = self.next_cell.on_ramp.temp_outflow(time_step)

                downstream_supply = (self.next_cell.congestion_wave_speed * (self.next_cell.jam_density - self.next_cell.density))
                if (temp_outflow_on_ramp + temp_outflow_cell) <= downstream_supply:
                    self.outflow = temp_outflow_cell
                    self.next_cell.on_ramp.update_outflow_reduced(temp_outflow_on_ramp)
                else:
                    self.outflow = temp_outflow_cell / (temp_outflow_cell + temp_outflow_on_ramp) * downstream_supply
                    self.next_cell.on_ramp.update_outflow_reduced(temp_outflow_on_ramp / (temp_outflow_cell + temp_outflow_on_ramp) * downstream_supply)

            if self.outflow < 0:
                print("Negativ Outflow")
                self.outflow = 0

        # last cell
        else:
            self.outflow = min((1-self.beta) * self.speed*self.density, self.maximum_flow)

        #vehicles
        self.vehicles = self.vehicles + self.delta_time * (self.inflow - self.outflow)

        #parameters
        if self.vehicles:
            self.density = self.vehicles / self.length
            self.flow = self.get_flow()
            self.speed = self.flow / self.density
        else:
            self.density = 0
            self.flow = 0
            self.speed = self.freeflow_speed

    def get_flow(self):
        flow = 0
        if self.density >= self.critical_density:
            flow = (self.density - self.critical_density) * -self.congestion_wave_speed + self.maximum_flow
        elif self.density < self.critical_density:
            flow = self.density * self.freeflow_speed

        return flow

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




