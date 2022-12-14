import numpy as np
from cell import Cell as Mastercell


class Cell(Mastercell):
    def __init__(self, length, lanes, delta_time, fd, beta=0, on_ramp_demand=0, flow=0, vehicles=0, tao=22, ny=15, kappa=10, delta=1.4, alinea=None):
        super(Cell, self).__init__(length, lanes, delta_time, fd, alinea, flow, vehicles, beta, on_ramp_demand)

        self.time_step = 0
        self.r = 0

        # calculations
        self.critical_density = self.maximum_flow / (self.freeflow_speed * np.exp(-1/2))
        self.congestion_wave_speed = self.maximum_flow / (self.jam_density - self.critical_density)  # ð¤ð = ðð/(ðjam,ð - ðcr,i)

        # model parameters metanet
        self.tao = tao / 3600
        self.ny = ny
        self.kappa = kappa
        self.delta = delta
        self.lambdai = self.lanes
        
    # update parameters
    def update(self, timestep):
        self.time_step = timestep

        if self.has_on_ramp:
            self.r = self.on_ramp.outflow

        self.flow_update()
        self.density_update()
        self.speed_update()

    def flow_update(self):
        # for cell 1 to (n-1)
        if self.next_cell:
            self.outflow = min(self.density * self.speed, self.maximum_flow, self.next_cell.congestion_wave_speed * (self.next_cell.jam_density - self.next_cell.density))  # ð¤ð+1(ðÌð+1 â ðð+1(ð))
            if self.next_cell.has_on_ramp:  # with alinea
                if self.next_cell.on_ramp.alinea.is_applied:
                    self.next_cell.on_ramp.outflow_alinea(self.time_step, self.next_cell.critical_density, self.next_cell.density)
                else:   # without alinea
                    temp_outflow_cell = self.outflow
                    temp_outflow_on_ramp = self.next_cell.on_ramp.temp_outflow(self.time_step)
                    if (temp_outflow_on_ramp + temp_outflow_cell) <= self.downstream_supply():
                        self.outflow = temp_outflow_cell
                        self.next_cell.on_ramp.update_outflow_reduced(temp_outflow_on_ramp)
                    else:
                        self.outflow = temp_outflow_cell / (temp_outflow_cell + temp_outflow_on_ramp) * self.downstream_supply()
                        self.next_cell.on_ramp.update_outflow_reduced(temp_outflow_on_ramp / (temp_outflow_cell + temp_outflow_on_ramp) * self.downstream_supply())
        # for cell n (last cell)
        if not self.next_cell:
            self.outflow = min(self.density * self.speed, self.maximum_flow)

        self.flow = self.outflow
      
    def density_update(self):
        if self.previous_cell:
            self.density = self.density + self.delta_time / (self.length * self.lambdai) * (self.previous_cell.outflow - self.outflow + self.r)     # ð(ð+1)=ði(ð)+ ð â (ði-1(ð) â ði(ð)+ði(ð)âð i(ð))
            if self.density > self.jam_density:
                print("Error Overflow")

    def speed_update(self):
        # ð£ð(ð+1) = ð£ð(ð) + ð/ð â (ð(ðð(ð)) â ð£ð(ð)) + ð/Lð â ð£ð(ð) â (ð£ðâ1(ð) â ð£ð(ð)) â ð£*ð/(ð*Lð) * (ði+1(ð)âði(ð)) / (ðð(ð) + ð¾) -  (ð¿ð*ði(ð)*ð£i(ð)) / (Îððð ðð(ð) + ð¾)
        # for cell 1 to (n-1)
        if self.previous_cell and self.next_cell:
            self.speed = self.speed + self.delta_time / self.tao * (self.get_speed(self.density) - self.speed) \
                         + (self.delta_time / self.length) * self.speed * (self.previous_cell.speed - self.speed) \
                         - (self.ny * self.delta_time) / (self.tao * self.length) * (
                                     self.next_cell.density - self.density) / (self.density + self.kappa) \
                         - (self.delta * self.delta_time) / (self.length * self.lambdai) * (self.r * self.speed) / (
                                     self.density + self.kappa)
        # for cell n (last cell)
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
        return self.freeflow_speed * np.exp(-1/alpha * (density / self.critical_density)**alpha)    # ð(ðð(ð)) = ð£ð,ð ^ (-1/ð â (ð(k)/ððð,ð))^ð
