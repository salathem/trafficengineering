import numpy as np


class Alinea:
    def __init__(self, k=0.5, is_applied=False, optimise_k=False):
        self.k = k
        self.is_applied = is_applied
        self.optimise_k = optimise_k

    def optimize(self, net, precision):
        print("K-Value Optimizer is running ...")
        vht_min = None
        self.fd = net.fd
        self.scenario = net.scenario
        self.method = net.method

        start = precision
        end = 1-precision
        step = 0.1
        precision /= 10
        optimal_k = self.k
        counter = 1
        while step != precision:
            for k in np.arange(start, end, step):
                self.k = k
                net.set_scenario(self.fd, self.scenario, self.method, self)
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
                        optimal_k = k
                else:
                    vht_min = vht
                    optimal_k = k

            start = max(precision, optimal_k-step)
            end = min(1-precision, optimal_k+step)
            step = max(precision, step/10)
            counter += 1

        self.k = optimal_k

        print("Optimised K-Value: "+str(round(self.k, len(str(round(1/precision))))))
        print("Value found in "+str(counter)+" Iterations with a Precision of: "+str(precision))
