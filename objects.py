
class FundamentalDiagram:
   def __init__(self, flow_capacity=2000, jam_density=180, free_flow_speed=100):

      critical_density = flow_capacity / free_flow_speed
      congestion_wave_speed = flow_capacity / (jam_density - critical_density)
      self.flow_capacity = flow_capacity                                         #flow capacity (veh/h/lane)
      self.critical_density = critical_density                                   #Criticaltical density (veh/km/lane)
      self.jam_density = jam_density                                             #Jam density (veh/km/lane)
      self.free_flow_speed = free_flow_speed                                     #Free Flow Speed (km/h)
      self.congestion_wave_speed = congestion_wave_speed                         #Congestion Wave Speed (km/h)

   def print(self):
      print("Flow Capacity: ", self.flow_capacity)
      print("Critical Density: ", self.critical_density)
      print("Jam Density: ", self.jam_density)
      print("Free Flow Speed: ", self.free_flow_speed)
      print("Congestion Wave Speed: ", self.congestion_wave_speed)


class Cell:
   def __init__(self, fundamentaldiagram, lanes=3, length=0.5, x_in=0, b_out=0):

      self.fundamentaldiagram = fundamentaldiagram
      self.lanes = lanes                                                   #Lanes [-]
      self.length = length                                                 #Length[km]
      self.flow_capacity = lanes * fundamentaldiagram.flow_capacity
      self.critical_density = lanes * fundamentaldiagram.critical_density
      self.jam_density = lanes * fundamentaldiagram.jam_density
      self.x_in = x_in           #Max Onramp Demand [veh/h]
      self.b_out = b_out         #Off ramp Split Ration [-]
      self.n = [0]               #Anzahl Veh in cell [veh]
      self.p = []                #Dichte Veh in cell [veh/km]
      self.q = []                #Flow aus Zelle [veh/h]
      self.x = []                #Onramp Demand [veh/h]
      self.r = []                #Wirklicher Onramp Flow [veh/h]
      self.s = []
      self.free_flow_speed = fundamentaldiagram.free_flow_speed
      self.onrampqueue = [0]

   def setindex(self, index):
      self.index = index

   def appendflow(self, flow):
      self.q.append(flow)

   def appenddensity(self, density):
      self.p.append(density)

   def setvolume(self, volume):
      self.volume = volume

   def readattribute(self, attribute):
      if attribute == "n":
         return self.n
      elif attribute == "p":
         return self.p
      elif attribute == "q":
         return self.q
      elif attribute == "x":
         return self.x
      elif attribute == "r":
         return self.r
      elif attribute == "s":
         return self.s
      else:
         print("Cell attribute could not be read. No valid Attribute give.")

   def print(self):
      try:
         print("Index: ", self.index)
      except:
         print("No index set.")
      print("Anzahl Linien: ", self.lanes)
      print("Länge: ", self.length)
      print("Demand Onramp In: ", self.x_in)
      print("Ratio Onramp Out: ", self.b_out)


class Network:

   def __init__(self, method):
      self.cells = []
      self.method = method
      self.q = []

   def add_cell(self, cell):
      cell.setindex(len(self.cells))
      self.cells.append(cell)

   def rm_cell(self, cellname):
      self.cells.remove(cellname)
      index = 0
      for cell in self.cells:
         cell.index = index
         index += 1

   def getpreviouscell(self, cell):
      if cell.index > 0:
         return self.cells[cell.index-1]
      else:
         print("No Previous Cell")
         return None

   def getfollowingscell(self, cell):
      if cell.index < len(self.cells)-1:
         return self.cells[cell.index+1]
      else:
         print("No Following Cell")
         return None

   def setparameters(self, fundamentaldiagram):
      self.fundamentaldiagram = fundamentaldiagram

   def setdemand(self, demand):
      self.demand = demand

   def print(self):
      try:
         self.fundamentaldiagram.print()
      except:
         print("Fundamental Diagram not properly Set")
      print()
      for cell in self.cells:
         cell.print()
         print()

   def setscenario(self, fundamentaldiagram, index):
      # cell = Cell(lanes, length, d_in, d_out, x_in, B_out)
      if index == 1:
         # Scenario a)
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 0, 0))
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 0, 0))
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 2000, 0))
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 0, 0))
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 0, 0))
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 0, 0))
      if index == 2:
         # Scenario b)
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 0, 0))
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 0, 0))
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 2500, 0))
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 0, 0))
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 0, 0))
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 0, 0))
      if index == 3:
         # Scenario c)
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 0, 0))
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 0, 0))
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 1500, 0))
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 0, 0))
         self.add_cell(Cell(fundamentaldiagram, 1, 0.5, 0, 0))
         self.add_cell(Cell(fundamentaldiagram, 3, 0.5, 0, 0))
