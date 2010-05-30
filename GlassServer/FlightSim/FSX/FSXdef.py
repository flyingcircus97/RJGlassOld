#!/usr/bin/env python
# ----------------------------------------------------------
# FSX Definitions 
# ----------------------------------------------------------
#Constants
from PySimConnect import event_obj, data_obj
#DataTypes
INT32 = 1
INT64 = 2
FLOAT32 = 3
FLOAT64 = 4
STRING8 = 5
STRING32 = 6
STRING64 = 7
STRING128 = 8
STRING256 = 9

def freqtoBCD(freq):
    #freq is a float.
    #Returns BCD value as int. Needed for FSX Event to set it.
    #freq = 123.45
    temp = int(round(freq * 1000)) #round to 1/1000th place.
    temp = temp / 10 #truncate to 1/100th place.
    temp = temp % 10000 #nock off hundred place of freq
       
    #temp = 2345
    bcd = 0
    for i in range(4):
        bcd = bcd * 16
        bcd+= temp / 1000
        temp = temp % 1000  * 10
    return bcd

def xpdrtoBCD(freq):
    bcd = 0
    temp = int(freq)
    for i in range(4):
        bcd = bcd * 16
        bcd+= temp / 1000
        temp = temp % 1000  * 10
    print bcd
    return bcd

def adftoBCD(freq):
    
    bcd = 0
    temp = int(freq * 10)
    for i in range(5):
        print bcd,temp, temp / 10000
        bcd = bcd * 16
        bcd+= temp / 10000
        temp = temp % 10000 * 10
    #print bcd * 16^4
    #return 50679808
    return bcd * 16**3
    

def setup(s, variables):
        s.definition_0 = s.create_DataDefinition(2)
        #Data definition ID 2, is the high priority data, that needs to have no delay.
        s.definition_0.add("Airspeed Indicated", "knots", FLOAT32, variables.byName('IAS').data)
        s.definition_0.add("GROUND VELOCITY", "knots", FLOAT32, variables.byName('GS').data)
        #Radios
        s.definition_0.add("NAV ACTIVE FREQUENCY:1", "MHZ", FLOAT32, variables.byName('NAV1_ACTIVE').data)
        s.definition_0.add("NAV STANDBY FREQUENCY:1", "MHZ", FLOAT32, variables.byName('NAV1_STANDBY').data)
        s.definition_0.add("NAV ACTIVE FREQUENCY:2", "MHZ", FLOAT32, variables.byName('NAV2_ACTIVE').data)
        s.definition_0.add("NAV STANDBY FREQUENCY:2", "MHZ", FLOAT32, variables.byName('NAV2_STANDBY').data)
        s.definition_0.add("COM ACTIVE FREQUENCY:1", "MHZ", FLOAT32, variables.byName('COM1_ACTIVE').data)
        s.definition_0.add("COM STANDBY FREQUENCY:1", "MHZ", FLOAT32, variables.byName('COM1_STANDBY').data)
        s.definition_0.add("COM ACTIVE FREQUENCY:2", "MHZ", FLOAT32, variables.byName('COM2_ACTIVE').data)
        s.definition_0.add("COM STANDBY FREQUENCY:2", "MHZ", FLOAT32, variables.byName('COM2_STANDBY').data)
        s.definition_0.add("ADF ACTIVE FREQUENCY:1", "KHZ", FLOAT32, variables.byName('ADF1_ACTIVE').data)
        s.definition_0.add("ADF STANDBY FREQUENCY:1", "KHZ", FLOAT32, variables.byName('ADF1_STANDBY').data)
        s.definition_0.add("ADF ACTIVE FREQUENCY:2", "KHZ", FLOAT32, variables.byName('ADF2_ACTIVE').data)
        s.definition_0.add("ADF STANDBY FREQUENCY:2", "KHZ", FLOAT32, variables.byName('ADF2_STANDBY').data)
        
        s.definition_0.add("TRANSPONDER CODE:1", "", INT32, variables.byName('XPDR').data)

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
        add_event('NAV1_RADIO_SET', 'NAV1_ACTIVE', freqtoBCD)
        add_event('NAV1_STBY_SET', 'NAV1_STANDBY', freqtoBCD)
        add_event('NAV2_RADIO_SET', 'NAV2_ACTIVE', freqtoBCD)
        add_event('NAV2_STBY_SET', 'NAV2_STANDBY', freqtoBCD)
        add_event('COM_RADIO_SET', 'COM1_ACTIVE',  freqtoBCD)
        add_event('COM_STBY_RADIO_SET', 'COM1_STANDBY', freqtoBCD)
        add_event('COM2_RADIO_SET', 'COM2_ACTIVE', freqtoBCD)
        add_event('COM2_STBY_RADIO_SET', 'COM2_STANDBY', freqtoBCD)
        add_event('XPNDR_SET','XPDR', xpdrtoBCD)
        add_event('ADF_COMPLETE_SET','ADF1_ACTIVE', adftoBCD)
        add_event('ADF2_COMPLETE_SET','ADF2_ACTIVE', adftoBCD)
        #COM2_STBY_RADIO_SET
        #print type(Nav1_Active.set_value)
#Nav1_Active = data_obj(0)      
