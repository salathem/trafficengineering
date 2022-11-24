import numpy as np


class Source:
    def __init__(self, timestep, demand_points, demand_values, alinea=False, alinea_k=0.5, id=0):
        self.id = id
        self.demand_points = demand_points
        self.demand_values = demand_values
        self.current_demand = 0
        self.queue = 0
        self.vehicles = 0
        self.timestep = 0
        self.outflow = 0
        self.speed = 0
        self.time_step = 0
        self.timestep_hour = timestep
        self.alinea = alinea
        self.alinea_k = alinea_k

        # objects
        self.next_cell = None

    def update(self, timestep):
        self.current_demand = self.demand_function(timestep)
        self.outflow = min(self.current_demand + self.queue / self.timestep_hour, self.next_cell.maximum_flow, self.next_cell.congestion_wave_speed * (self.next_cell.jam_density - self.next_cell.density))

        self.queue += (self.current_demand - self.outflow) * self.timestep_hour
        self.time_step = timestep

    def demand_function(self, timestep):
        current_timestep = timestep * self.timestep_hour
        return np.interp(current_timestep, self.demand_points, self.demand_values)

    def on_ramp_temp_outflow(self, timestep):
        self.current_demand = self.demand_function(timestep)
        self.time_step = timestep
        return min(self.current_demand + self.queue / self.timestep_hour, self.next_cell.maximum_flow, self.next_cell.congestion_wave_speed * (self.next_cell.jam_density - self.next_cell.density))

    def on_ramp_update(self, outflow_reduced):
        self.outflow = outflow_reduced
        self.queue = self.queue + (self.current_demand - outflow_reduced) * self.timestep_hour

    def on_ramp_outflow_alinea(self, timestep, downstream_crit_density, downstream_density):
        self.current_demand = self.demand_function(timestep)
        self.time_step = timestep
        self.outflow = min(self.outflow + self.alinea_k * (downstream_crit_density - downstream_density), self.current_demand + self.queue / self.timestep_hour)
        self.queue += (self.current_demand - self.outflow) * self.timestep_hour
        return self.outflow
    
    def performance_calculation(self):
        return 0, (self.queue * self.timestep_hour)

