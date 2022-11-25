import numpy as np


class Alinea:
    def __init__(self, k=0.5, is_applied=False):
        self.k = k
        self.is_applied = is_applied

    def optimize(self, net, precision):

        vht_min = None
        self.fd = net.fd
        self.scenario = net.scenario
        self.method = net.method

        start = precision
        end = 1-precision
        step = 0.1
        precision /= 10

        while step != precision:
            for k in np.arange(start, end, step):
                net.set_scenario(self.fd, self.scenario, self.method, self.is_applied, k)
                vkt = 0
                vht = 0
                for sim_step in range(net.nr_of_steps):

                    # update network demand
                    net.demand.update(sim_step)
                    for cell in net.cells:
                        # calculate cell
                        cell.update(sim_step)

                        # update performance parameters
                        temp_vkt, temp_vht = cell.performance_calculation()
                        vkt += temp_vkt
                        vht += temp_vht

                    # advance simulation
                    sim_step += 1

                if vht_min:
                    if vht_min > vht:
                        vht_min = vht
                        self.k = k
                else:
                    vht_min = vht
                    self.k = k


            print("Zyklus")
            print(start)
            print(end)
            print(step)
            print(self.k)
            start = max(precision, self.k-step)
            end = min(1-precision, self.k+step)
            step = max(precision, step/10)



        print(vht_min)
        print(round(self.k, len(str(precision))))
