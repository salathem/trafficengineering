import numpy as np
from source import Source

class Cell:
    def __init__(self, length, lanes, fd, delta_time, id=0, beta=0, on_ramp_demand=0, flow=0, vehicles=0, tao=22, ny=15, kappa=10, delta=1.4, alinea=False, alinea_k=0.5):
        self.id = id
        self.vehicles = vehicles
        self.length = length
        self.flow = 0
        self.outflow = flow
        if on_ramp_demand:
            self.has_on_ramp = True
        else:
            self.has_on_ramp = False
        if beta:
            self.has_off_ramp = True
        else:
            self.has_off_ramp = False
        self.lanes = lanes
        self.on_ramp_demand = on_ramp_demand
        self.delta_time = delta_time
        self.beta = beta
        self.speed = 100
        self.time_step = 0
        self.r = 0
        self.density = 0

        #objects
        self.fd = fd
        if self.has_on_ramp:
            self.add_on_ramp(alinea, alinea_k)
        else:
            self.on_ramp = None
        self.previous_cell = None
        self.next_cell = None


        # calculations
        self.freeflow_speed = fd.freeflow_speed
        self.jam_density = fd.jam_density * lanes
        self.maximum_flow = fd.maximum_flow * lanes

        self.critical_density = self.maximum_flow / (self.freeflow_speed * np.exp(-1/2))
        self.congestion_wave_speed = self.maximum_flow / (self.jam_density - self.critical_density)


        #model parameters
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
        

    def speed_update(self):
        if self.previous_cell and self.next_cell:
#            self.speed = self.speed + self.delta_time / self.tao * (self.fd.get_speed(self.density) - self.speed) \
            self.speed = self.speed + self.delta_time / self.tao * (self.get_speed(self.density) - self.speed) \
                         + (self.delta_time / self.length) * self.speed * (self.previous_cell.speed - self.speed) \
                         - (self.ny * self.delta_time) / (self.tao * self.length) * (self.next_cell.density - self.density) / (self.density + self.kappa) \
                         - (self.delta * self.delta_time) / (self.length * self.lambdai) * (self.r * self.speed) / (self.density + self.kappa)
                 
        if not self.next_cell:
#            self.speed = self.speed + self.delta_time / self.tao * (self.fd.get_speed(self.density) - self.speed) \
            self.speed = self.speed + self.delta_time / self.tao * (self.get_speed(self.density) - self.speed) \
                         + self.delta_time / self.length * self.speed * (self.previous_cell.speed - self.speed) \
                         - (self.delta * self.delta_time) / (self.length * self.lambdai) * (self.r * self.speed) / (self.density + self.kappa)
                
        if self.speed < 0:
            self.speed = 0
            
    def flow_update(self):
        self.outflow = min(self.density * self.speed, self.maximum_flow)
        if self.next_cell:
            self.outflow = min(self.density * self.speed, self.maximum_flow, self.next_cell.congestion_wave_speed * (self.next_cell.jam_density - self.next_cell.density))
            if self.next_cell.has_on_ramp:
                if self.next_cell.on_ramp.alinea:
                    self.next_cell.on_ramp.on_ramp_outflow_alinea(self.time_step, self.next_cell.critical_density, self.next_cell.density)
                else:
                    temp_outflow_cell = self.outflow
                    temp_outflow_on_ramp = self.next_cell.on_ramp.on_ramp_temp_outflow(self.time_step)
                    downstream_supply = self.next_cell.congestion_wave_speed * (self.next_cell.jam_density - self.next_cell.density)
                    if (temp_outflow_on_ramp + temp_outflow_cell) <= downstream_supply:
                        self.outflow = temp_outflow_cell
                        self.next_cell.on_ramp.on_ramp_update(temp_outflow_on_ramp)
                    else:
                        self.outflow = temp_outflow_cell / (temp_outflow_cell + temp_outflow_on_ramp) * downstream_supply
                        self.next_cell.on_ramp.on_ramp_update(temp_outflow_on_ramp / (temp_outflow_cell + temp_outflow_on_ramp) * downstream_supply)
        self.flow = self.outflow
      
    def density_update(self):
        if self.previous_cell:
            self.density = self.density + self.delta_time / (self.length * self.lambdai) * (self.previous_cell.outflow - self.outflow + self.r)
            if self.density > self.jam_density:
                print(self.time_step, 'alarm', self.id, self.density)

    def dump_data(self, flow=[], density=[], speed=[],):
        flow[self.id-1, self.time_step] = self.outflow
        density[self.id-1, self.time_step] = self.density
        speed[self.id-1, self.time_step] = self.speed

    def performance_calculation(self):
        cell_vkt = self.delta_time * self.outflow * self.length
        cell_vht = self.delta_time * self.density * self.length

        if self.has_on_ramp:
            cell_vht += self.on_ramp.queue * self.delta_time

        return cell_vkt, cell_vht

    def get_speed(self, density):
        if density > self.jam_density:
            return 0
        return self.freeflow_speed * np.exp(-1/2 * (density / self.critical_density)**2)

    def add_on_ramp(self, alinea, alinea_k):
        demand_onramp_points = [0, 900 / 3600, 2700 / 3600, 3600 / 3600, 5000 / 3600]
        demand_onramp_values = [0, self.on_ramp_demand, self.on_ramp_demand, 0, 0]
        # initialize on-ramp cell
        on_ramp = Source(self.delta_time, demand_onramp_points, demand_onramp_values, alinea, alinea_k)
        on_ramp.next_cell = self
        self.on_ramp = on_ramp

    def check_cfl(self):
        if self.delta_time < (self.length/self.freeflow_speed):
            print("CFL Condition OK for Cell "+str(self.id)+".")
        else:
            print("CFL Condition Not OK for Cell "+str(self.id)+"!!!")


