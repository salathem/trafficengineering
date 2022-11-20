import numpy as np


class Simulation:
    def __init__(self, net, start_time=0, duration=5000 / 3600, step_time=10 / 3600, scenario_file=None):
        """
      Network: net [Network]
      Start Time [h]
      Duration [h]
      Time of a Step [h]
      """
        self.net = net
        self.duration = duration
        self.start_time = start_time
        self.end_time = start_time + duration
        self.time = start_time
        self.step_time = step_time
        self.all_steps = np.arange(start_time, start_time + duration, step_time)
        self.stepindex = 0
        self.k = 0
        # self.records = []

    def cflcheck(self):
        for cell in self.net.cells:
            if self.step_time <= cell.length / cell.free_flow_speed:
                print("CFL check of cell " + str(cell.index) + " OK.")
            else:
                print("CFL check " + str(cell.index) + " not OK.")

    def setdemand(self, t):
        """
       Update Flow [Veh]
       Needs: Demand Graph (Aufgabenstellung)
       Gives: net.q[k], cell.r[k]
       """
        for cell in self.net.cells:
            if cell.index == 0:
                self.calculatestartdemand(t)
            self.calculateonrampdemand(cell, t)
            # self.calculateonrampflow(cell, t)

    def calculatestartdemand(self, t):
        t_s = t * 3600
        if t_s < 450:
            self.net.q.append(self.net.demand * t_s / 450)
        elif 450 <= t_s <= 3150:
            self.net.q.append(self.net.demand)
        elif 3150 < t_s < 3600:
            self.net.q.append(self.net.demand - self.net.demand * (t_s - 3150) / 450)
        else:
            self.net.q.append(0)

    def calculateonrampdemand(self, cell, t):
        t_s = t * 3600
        if t_s < 900:
            cell.x.append(cell.x_in / 900 * t_s)
        elif 900 <= t_s <= 2700:
            cell.x.append(cell.x_in)
        elif 2700 < t_s < 3600:
            cell.x.append(cell.x_in - cell.x_in / 900 * (t_s - 2700))
        else:
            cell.x.append(0)

    def updatedensity(self, k):
        """
      Update Flow [Veh]
      Needs: cell.n[k], cell.length
      Gives: cell.p[k]
      """
        for cell in self.net.cells:
            density = cell.n[k] / cell.length
            cell.p.append(density)

    def updateflow(self, k):
        """
       Update Flow [Veh]
       Needs: cell.p[k]
       Gives: cell.q[k]
       """
        for cell in self.net.cells:
            t = self.step_time
            q = self.minflow(cell=cell, k=k)
            r = cell.x[k] + cell.onrampqueue[k] / t
            if True:  # cell.index == len(self.net.cells) - 1:
                cell.q.append(q)
                cell.r.append(r)
                queue = cell.onrampqueue[k] + (cell.x[k] - r) * t
                cell.onrampqueue.append(queue)
            else:
                if q + r <= 12.5 * (180 - self.net.getfollowingscell(cell).p[
                    k]):  # self.net.getfollowingscell(cell).fundamentaldiagram.congestion_wave_speed * (self.net.getfollowingscell(cell).jam_density - self.net.getfollowingscell(cell).p[k]):
                    print("No Queue")
                    cell.q.append(q)
                    cell.r.append(r)
                    queue = cell.onrampqueue[k] + (cell.x[k] - r) * t
                    cell.onrampqueue.append(queue)
                else:
                    print("Queue")
                    flow = q / (q + r) * self.net.getfollowingscell(cell).fundamentaldiagram.congestion_wave_speed * (
                                self.net.getfollowingscell(cell).jam_density - self.net.getfollowingscell(cell).p[k])
                    cell.q.append(flow)
                    onrampflow = r / (q + r) * self.net.getfollowingscell(
                        cell).fundamentaldiagram.congestion_wave_speed * (self.net.getfollowingscell(cell).jam_density -
                                                                          self.net.getfollowingscell(cell).p[k])
                    cell.r.append(onrampflow)
                    queue = cell.onrampqueue[k] + (cell.x[k] - r) * t
                    cell.onrampqueue.append(queue)

    def updatevolume(self, k):
        # n_i(k+1)=n_i(k)+T[q_i-1(k)+r_i(k)-q_i(k)-s_i(k)]
        """
      Update Cell Volume [Veh]
      Needs: cell.q[k], cell.n[k], cell.r[k]
      Gives: cell.n[k+1]
      """
        for cell in self.net.cells:
            if len(self.all_steps) > len(cell.n):
                if cell.index == 0:
                    n = cell.n[k] - self.step_time * (cell.q[k] / (1 - cell.b_out) - self.net.q[k])
                else:
                    previous_cell = self.net.getpreviouscell(cell)
                    n = cell.n[k] - self.step_time * (cell.q[k] / (1 - cell.b_out) - previous_cell.q[k] - cell.r[k])
                cell.n.append(n)

    def updateoutflow(self, k):
        for cell in self.net.cells:
            cell.s.append(cell.b_out / (1 - cell.b_out) * cell.q[k])

    def updatespeed(self, k):
        for cell in self.net.cells:
            if cell.p[k] > 0:
                speed = cell.q[k] / cell.p[k]
            else:
                speed = 0
            cell.v.append(speed)

    def minflow(self, cell, k):
        if cell.index == len(self.net.cells) - 1:
            return min((1 - cell.b_out) * cell.free_flow_speed * cell.p[k], cell.flow_capacity)
        else:
            return min((1 - cell.b_out) * cell.free_flow_speed * cell.p[k],
                       self.net.getfollowingscell(cell).congestion_wave_speed *
                       (self.net.getfollowingscell(cell).jam_density - self.net.getfollowingscell(cell).p[k]),
                       cell.flow_capacity)
