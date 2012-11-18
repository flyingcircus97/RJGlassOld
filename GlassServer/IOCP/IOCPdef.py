#!/usr/bin/env python
# ----------------------------------------------------------
# IOCP Load Definitions 
# ----------------------------------------------------------
import logging
#Constants
from types import FunctionType

import setupIOCP.radios
import setupIOCP.CRJ700.indications

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
        setupIOCP.radios.setup(add_IOCP)
        #Position
        #position.setup(add_IOCP)
        #HEading
        #heading.setup(add_var)
        #CRJ700
            #Indications
        setupIOCP.CRJ700.indications.setup(add_IOCP)


def setup_events(sevent, variables):        
    
        pass
