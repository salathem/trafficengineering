def setscenario(index):
    #cell = Cell(lanes, length, q_in, q_out, d_in, d_out)
    #Scenario a)
    cell1 = Cell(3, 500, 4000, 4000, 0, 0)
    cell2 = Cell(3, 500, 4000, 4000, 0, 0)
    cell3 = Cell(3, 500, 4000, 6000, 2000, 0)
    cell4 = Cell(3, 500, 6500, 6000, 0, 0)
    cell5 = Cell(3, 500, 6500, 6000, 0, 0)
    cell6 = Cell(3, 500, 6500, 6000, 0, 0)

    # Scenario b)
    cell1 = Cell(3, 500, 4000, 4000, 0, 0)
    cell2 = Cell(3, 500, 4000, 4000, 0, 0)
    cell3 = Cell(3, 500, 4000, 6500, 2500, 0)
    cell4 = Cell(3, 500, 6500, 6500, 0, 0)
    cell5 = Cell(3, 500, 6500, 6500, 0, 0)
    cell6 = Cell(3, 500, 6500, 6500, 0, 0)

    # Scenario c)
    cell1 = Cell(3, 500, 1500, 1500, 0, 0)
    cell2 = Cell(3, 500, 1500, 1500, 0, 0)
    cell3 = Cell(3, 500, 1500, 3000, 1500, 0)
    cell4 = Cell(3, 500, 3000, 3000, 0, 0)
    cell5 = Cell(1, 500, 3000, 3000, 0, 0)
    cell6 = Cell(3, 500, 3000, 3000, 0, 0)

#Assumptions and Precalculations
t_1 = 10               #ime Intervall in seconds
t_end1 = 5000          #Duration of Simulation (5000 sec)
t = t_1/3600           #Time Intervall in hours
t_end = t_end1/3600    #Duration of Simulation (in hours)

#range(Start, End-1, Intervall)

# cell.q[i] = cell.p[i] * cell.v[i]

def calculatestartdemand(self, t):
    if t <= 450:
        self.q.append(self.demand * t / 450)
    elif 450 < t <= 3150:
        self.q.append(self.demand)
    elif 3150 < t < 3600:
        self.q.append(self.demand - self.demand * (t - 3150) / 450)
    else:
        self.q.append(0)


def calculateonrampdemand(self, t):
    for cell in self.cells:
        if t <= 900:
            cell.r.append(cell.x_in / 900 * t)
        elif 900 < t < 2700:
            cell.r.append(cell.x_in)
        elif 2700 < t < 3600:
            cell.r.append(cell.x_in - cell.x_in / 900 * (t - 2700))
        else:
            cell.r.append(0)