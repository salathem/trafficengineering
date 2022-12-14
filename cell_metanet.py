import numpy as np
from cell import Cell as Mastercell


class Cell(Mastercell):
    def __init__(self, length, lanes, delta_time, fd, beta=0, on_ramp_demand=0, flow=0, vehicles=0, tao=22, ny=15, kappa=10, delta=1.4, alinea=None):
        super(Cell, self).__init__(length, lanes, delta_time, fd, alinea, flow, vehicles, beta, on_ramp_demand)

        self.time_step = 0
        self.r = 0

        # calculations
        self.critical_density = self.maximum_flow / (self.freeflow_speed * np.exp(-1/2))
        self.congestion_wave_speed = self.maximum_flow / (self.jam_density - self.critical_density)  # 𝑤𝑖 = 𝑄𝑖/(𝜌jam,𝑖 - 𝜌cr,i)

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
            self.outflow = min(self.density * self.speed, self.maximum_flow, self.next_cell.congestion_wave_speed * (self.next_cell.jam_density - self.next_cell.density))  # 𝑤𝑖+1(𝜌̅𝑖+1 − 𝜌𝑖+1(𝑘))
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
            self.density = self.density + self.delta_time / (self.length * self.lambdai) * (self.previous_cell.outflow - self.outflow + self.r)     # 𝜌(𝑘+1)=𝜌i(𝑘)+ 𝑇 ∗ (𝑞i-1(𝑘) − 𝑞i(𝑘)+𝑟i(𝑘)−𝑠i(𝑘))
            if self.density > self.jam_density:
                print("Error Overflow")

    def speed_update(self):
        # 𝑣𝑖(𝑘+1) = 𝑣𝑖(𝑘) + 𝑇/𝜏 ∗ (𝑉(𝜌𝑖(𝑘)) − 𝑣𝑖(𝑘)) + 𝑇/L𝑖 ∗ 𝑣𝑖(𝑘) ∗ (𝑣𝑖−1(𝑘) − 𝑣𝑖(𝑘)) − 𝑣*𝑇/(𝜏*L𝑖) * (𝜌i+1(𝑘)−𝜌i(𝑘)) / (𝜌𝑖(𝑘) + 𝐾) -  (𝛿𝑇*𝑟i(𝑘)*𝑣i(𝑘)) / (Δ𝑖𝜆𝑖 𝜌𝑖(𝑘) + 𝐾)
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
        return self.freeflow_speed * np.exp(-1/alpha * (density / self.critical_density)**alpha)    # 𝑉(𝜌𝑖(𝑘)) = 𝑣𝑓,𝑖 ^ (-1/𝑎 ∗ (𝜌(k)/𝜌𝑐𝑟,𝑖))^𝑎
