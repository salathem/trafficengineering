from source import Source
from cell import Cell as Mastercell


class Cell(Mastercell):
    def __init__(self, length, lanes, delta_time, fd, flow=0, vehicles=0, beta=0, on_ramp_demand=0):
        super(Cell, self).__init__(length, lanes, delta_time, fd, flow, vehicles, beta, on_ramp_demand)

        # calculations
        self.critical_density = self.maximum_flow / self.freeflow_speed
        self.congestion_wave_speed = abs(self.maximum_flow / (self.critical_density - self.jam_density))

        # main parameters
        self.flow = self.get_flow()

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
                print("Error Negativ Outflow")
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




