import numpy as np
from source import Source
from cell import Cell as Mastercell


class Cell(Mastercell):
    def __init__(self, length, lanes, delta_time, fd, beta=0, on_ramp_demand=0, flow=0, vehicles=0, tao=22, ny=15, kappa=10, delta=1.4, alinea=None):
        super(Cell, self).__init__(length, lanes, delta_time, fd, flow, vehicles, beta, on_ramp_demand)

        self.time_step = 0
        self.r = 0

        # add on_ramp
        self.add_on_ramp(alinea)

        # calculations
        self.critical_density = self.maximum_flow / (self.freeflow_speed * np.exp(-1/2))
        self.congestion_wave_speed = self.maximum_flow / (self.jam_density - self.critical_density)

        # model parameters metanet
        self.tao = tao / 3600
        self.ny = ny
        self.kappa = kappa
        self.delta = delta
        self.lambdai = self.lanes
        
    #update parameters    
    def update(self, timestep):
        self.time_step = timestep

        if self.has_on_ramp:
            self.r = self.on_ramp.outflow

        self.flow_update()
        self.density_update()
        self.speed_update()

    def flow_update(self):
        self.outflow = min(self.density * self.speed, self.maximum_flow)
        if self.next_cell:
            self.outflow = min(self.density * self.speed, self.maximum_flow, self.next_cell.congestion_wave_speed * (self.next_cell.jam_density - self.next_cell.density))
            if self.next_cell.has_on_ramp:
                if self.next_cell.on_ramp.alinea.is_applied:
                    self.next_cell.on_ramp.outflow_alinea(self.time_step, self.next_cell.critical_density, self.next_cell.density)
                else:
                    temp_outflow_cell = self.outflow
                    temp_outflow_on_ramp = self.next_cell.on_ramp.temp_outflow(self.time_step)
                    downstream_supply = self.next_cell.congestion_wave_speed * (self.next_cell.jam_density - self.next_cell.density)
                    if (temp_outflow_on_ramp + temp_outflow_cell) <= downstream_supply:
                        self.outflow = temp_outflow_cell
                        self.next_cell.on_ramp.update_outflow_reduced(temp_outflow_on_ramp)
                    else:
                        self.outflow = temp_outflow_cell / (temp_outflow_cell + temp_outflow_on_ramp) * downstream_supply
                        self.next_cell.on_ramp.update_outflow_reduced(temp_outflow_on_ramp / (temp_outflow_cell + temp_outflow_on_ramp) * downstream_supply)
        self.flow = self.outflow
      
    def density_update(self):
        if self.previous_cell:
            self.density = self.density + self.delta_time / (self.length * self.lambdai) * (self.previous_cell.outflow - self.outflow + self.r)
            if self.density > self.jam_density:
                print("Error Overflow")

    def speed_update(self):
        if self.previous_cell and self.next_cell:
            self.speed = self.speed + self.delta_time / self.tao * (self.get_speed(self.density) - self.speed) \
                         + (self.delta_time / self.length) * self.speed * (self.previous_cell.speed - self.speed) \
                         - (self.ny * self.delta_time) / (self.tao * self.length) * (
                                     self.next_cell.density - self.density) / (self.density + self.kappa) \
                         - (self.delta * self.delta_time) / (self.length * self.lambdai) * (self.r * self.speed) / (
                                     self.density + self.kappa)

        if not self.next_cell:
            self.speed = self.speed + self.delta_time / self.tao * (self.get_speed(self.density) - self.speed) \
                         + self.delta_time / self.length * self.speed * (self.previous_cell.speed - self.speed) \
                         - (self.delta * self.delta_time) / (self.length * self.lambdai) * (self.r * self.speed) / (
                                     self.density + self.kappa)

        if self.speed < 0:
            # print("Error negativ Speed")
            self.speed = 0

    def get_speed(self, density):
        alpha = 2
        if density > self.jam_density:
            print("Error Overflow")
            return 0
        return self.freeflow_speed * np.exp(-1/alpha * (density / self.critical_density)**alpha)
