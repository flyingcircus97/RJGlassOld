#!/usr/bin/env python
# ----------------------------------------------------------
# FlightSim Comm 
# ----------------------------------------------------------
import variables.variable as variable
import config
class FS_Comm_c(object):
    #Common class to read and write data to Flight Sim app.
    def __init__(self):
        self.variables = variable.variables
        self.sim = None
        self.controller = None
       
      #  if sim !=None:
      #      self.setup_sim(sim)
            
            
    def setup_sim(self, sim, mod_data):
        #Setup sim to new sim.
        self.sim = sim
        #self.mod_data = mod_data
        if (config.FSXSP0 <= sim <= config.ESP):
            import FlightSim.FSX.control 
            self.controller = FlightSim.FSX.control.control_c(self.variables, mod_data)
        elif sim == config.TEST:
            import FlightSim.TEST.control
            self.controller = FlightSim.TEST.control.control_c(self.variables, mod_data)
        else:
            print "ERROR: Sim ID Not Found"    
    
    def disconnect(self):
        if self.controller != None:
            self.controller.quit()
    def connect(self):
         if self.sim != None:
            self.setup_sim(self.sim)
            #self.controller.connect()
            
    def process(self):
        self.controller.process()
        
    def quit(self):
        self.controller.quit()
            
FS_Comm = FS_Comm_c()            