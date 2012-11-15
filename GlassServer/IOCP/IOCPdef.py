#!/usr/bin/env python
# ----------------------------------------------------------
# IOCP Load Definitions 
# ----------------------------------------------------------
import logging
#Constants
from types import FunctionType
import setup.radios as radios
import setup.airspeed as airspeed
import setup.altitude as altitude
import setup.position as position
import setup.heading as heading

def setup(comm, variables):
    
        def add_IOCP(var_num, var_name, read = True, write= False):
            v = variables.byName(var_name)
            if v!=None:
                comm.add_IOCP(var_num,v, read, write)
            else:
                logging.warning("IOCPdef: Couldn't add IOCP var, variable name %s not found", var_name)
                
            
          
        
        #Airspeed
        #airspeed.setup(add_var)
        #Altitude
        #altitude.setup(add_var)
        #Radios
        radios.setup(add_IOCP)
        #Position
        #position.setup(add_IOCP)
        #HEading
        #heading.setup(add_var)


def setup_events(sevent, variables):        
    
        pass
