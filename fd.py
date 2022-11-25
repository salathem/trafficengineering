class Fundamentaldiagram:
    def __init__(self, freeflow_speed=100, jam_density=180, maximum_flow=2000,):
        # init
        self.freeflow_speed = freeflow_speed
        self.jam_density = jam_density
        self.maximum_flow = maximum_flow

        # calculations
        self.critical_density = maximum_flow / freeflow_speed
        self.congestion_wave_speed = abs(maximum_flow / (self.critical_density - jam_density))
