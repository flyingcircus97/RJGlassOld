#!/usr/bin/env python
# ----------------------------------------------------------
# FSX Definitions 
# ----------------------------------------------------------
#Constants
from PySimConnect import event_obj, data_obj
import setup.radios as radios
import setup.airspeed as airspeed
import setup.altitude as altitude
 

def setup(s, variables):
    
        def add_var(desc, unit, type, var_name, func = None):
            s.definition_0.add(desc, unit, type, variables.byName(var_name).data, func)
            variables.byName(var_name).writeable = False #For FSX set writeable to False
        
        s.definition_0 = s.create_DataDefinition(2)
        #Data definition ID 2, is the high priority data, that needs to have no delay.
       
        
        #Airspeed
        airspeed.setup(add_var)
        #Altitude
        altitude.setup(add_var)
        #Radios
        radios.setup(add_var)


def setup_events(sevent, variables):        
    
        def add_event(FSX_event, var_name, send_func=None):
            #Used to reduce amount of repative code, when adding events
            var = variables.byName(var_name)
            if send_func == None:
                sevent.eventlist.add(FSX_event, var.data)
            else:
                sevent.eventlist.add(FSX_event, var.data, send_func)
            var.set_writeable(var.data.set_value)
            
        sevent.eventlist = sevent.create_EventList()
        #Setup Events, (For FSX variables that can only be written this way.)
        #Radio Events
        radios.setup_events(add_event)
        #Altitude Events
        altitude.setup_events(add_event)