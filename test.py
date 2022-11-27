path_flow = 'plots/flow ' + self.method + ' scenario ' + self.scenario
if not os.path.exists(path_flow):
    os.mkdir(path_flow)
path_density = 'plots/density ' + self.method + ' scenario ' + self.scenario
os.mkdir(path_density)
path_speed = 'plots/speed ' + self.method + ' scenario ' + self.scenario
os.mkdir(path_speed)