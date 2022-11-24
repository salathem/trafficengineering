from source import Source


class Network:
    def __init__(self, method):
        self.method = method
        self.cells = []
        self.demand = None

    def set_scenario(self, fd, delta_time, index, method, alinea=None, alinea_k=None):
        if method == "ctm":
            from cell import Cell

        elif method == "metanet":
            from cell_metanet import Cell

        delta_length = 0.5

        if index == 1:
            # initialize all cells
            cells = [
                Cell(delta_length, 3, fd, delta_time),
                Cell(delta_length, 3, fd, delta_time),
                Cell(delta_length, 3, fd, delta_time, on_ramp_demand=2000),
                Cell(delta_length, 3, fd, delta_time),
                Cell(delta_length, 3, fd, delta_time),
                Cell(delta_length, 3, fd, delta_time),
            ]
            self.demand = 4000

        elif index == 2:
            # initialize all cells
            cells = [
                Cell(delta_length, 3, fd, delta_time),
                Cell(delta_length, 3, fd, delta_time),
                Cell(delta_length, 3, fd, delta_time, on_ramp_demand=2500),
                Cell(delta_length, 3, fd, delta_time),
                Cell(delta_length, 3, fd, delta_time),
                Cell(delta_length, 3, fd, delta_time),
            ]
            self.demand = 4000

        else:
            # initialize all cells
            cells = [
                Cell(delta_length, 3, fd, delta_time),
                Cell(delta_length, 3, fd, delta_time),
                Cell(delta_length, 3, fd, delta_time, on_ramp_demand=1500),
                Cell(delta_length, 3, fd, delta_time),
                Cell(delta_length, 1, fd, delta_time),
                Cell(delta_length, 3, fd, delta_time),
            ]
            self.demand = 1500

        if method == "metanet":
            for cell in cells:
                if cell.on_ramp_demand and alinea and alinea_k:
                    cell.add_on_ramp(alinea, alinea_k)


        # define upstream demand
        demand_upstream_points = [0, 450 / 3600, 3150 / 3600, 3600 / 3600, 5000 / 3600]
        demand_upstream_values = [0, self.demand, self.demand, 0, 0]

        # initialize Network Demand
        self.demand = Source(delta_time, demand_upstream_points, demand_upstream_values)

        self.cells = cells
        self.set_id()
        self.set_neighbours()


    # link neighbours and network demand
    def set_neighbours(self):
        self.demand.next_cell = self.cells[0]
        self.cells[0].previous_cell = self.demand
        for index in range(len(self.cells)-1):
            self.cells[index].next_cell = self.cells[index+1]
            self.cells[index+1].previous_cell = self.cells[index]

    # set cell id's
    def set_id(self):
        id = 1
        for cell in self.cells:
            cell.id = id
            id += 1





