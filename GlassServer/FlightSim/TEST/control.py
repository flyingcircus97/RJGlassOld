#!/usr/bin/env python
# ----------------------------------------------------------
# Controller File for TEST mode
# ----------------------------------------------------------

import time
#This is code to import config file (config.py)
try:
    import config
except ImportError:
    # We're in a py2exe, so we'll append an element to the (one element) 
    # sys.path which points to Library.zip, to the directory that contains 
    # Library.zip, allowing us to import config.py
    # Adds one level up from the Library.zip directory to the path, so import will go forward
    sys.path.append(os.path.split(sys.path[0])[0])
    import config

class control_c(object):
    #Class to read and write data to FSX.
    def __init__(self, variables, mod_data):
        self.connected = True
        self.variables = variables
        self.mod_data = mod_data
            
        time.sleep(0.4)
        
    
    def quit(self):
        self.connected = False
      
        
        
   
    def process(self):
        if self.connected: self.mod_data.test()
        
    def calc_status_message(self):
        
        if self.connected:
            return ("Connected")
        else:
            return ("Disconnected")

