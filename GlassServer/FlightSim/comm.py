#!/usr/bin/env python
# ----------------------------------------------------------
# FlightSim Comm 
# ----------------------------------------------------------
import logging
import variables.variable as variable
import config
class FS_Comm_c(object):
    #Common class to read and write data to Flight Sim app.
    def __init__(self):
        self.variables = variable.variables
        self.sim = None
        self.controller = None
        self.status_message = 'Unknown'
        
       
      #  if sim !=None:
      #      self.setup_sim(sim)
    def load_mod_data(self, mod_data):
        self.mod_data = mod_data
            
    def setup_sim(self, sim):
        #Setup sim to new sim.
        self.sim = sim
        #self.mod_data = mod_data
        if (sim['mode'] == 'ESP'):
            import FlightSim.FSX.control 
            self.sim_name = 'ESP'
            self.controller = FlightSim.FSX.control.control_c(self.variables, self.mod_data, sim)
            self.status_message = "Connecting"
            
        elif sim['mode'] == 'FSXSP2':
            import FlightSim.FSX.control 
            self.sim_name = 'FSXSP2'
            self.controller = FlightSim.FSX.control.control_c(self.variables, self.mod_data, sim)
            self.status_message = "Connecting"
            
        elif sim['mode'] == 'XPLANE':
            import FlightSim.XPLANE.control
            self.sim_name = 'XPLANE'
            self.controller = FlightSim.XPLANE.control.control_c(self.variables, self.mod_data, sim)
            self.status_message = "Connecting"
        
        elif sim['mode'] == 'Test':
            self.sim_name = 'TEST'
            import FlightSim.TEST.control
            self.controller = FlightSim.TEST.control.control_c(self.variables, self.mod_data)
            
        else:
            logging.warning("ERROR: Sim ID Not Found %r -- Fallingback to Test Mode Disconnected", sim)
            self.sim_name = 'TEST'
            import FlightSim.TEST.control
            self.controller = FlightSim.TEST.control.control_c(self.variables, self.mod_data)
            self.controller.quit()
            #Defaults
    
    def disconnect(self):
        logging.info('FlightSim Controller - Disconnect')
        if self.controller != None:
            self.controller.quit()
    def connect(self):
        logging.info('FlightSim Controller - Connect')
        if self.sim != None:
            self.status_message = "Connecting"
            self.setup_sim(self.sim)
            #self.controller.connect()
            
    def process(self):
        self.controller.process()
        self.status_message = self.controller.calc_status_message()
    def quit(self):
        logging.info('FlightSim Controller - Quitting')
        self.controller.quit()
            
FS_Comm = FS_Comm_c()            