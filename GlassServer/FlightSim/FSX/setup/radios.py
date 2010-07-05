#!/usr/bin/env python
# ----------------------------------------------------------
# FSX Definitions 
# ----------------------------------------------------------
from common import *#DataTypes

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


def setup(add_var):
        #Radios freq
        add_var("NAV ACTIVE FREQUENCY:1", "MHZ", FLOAT32,  'NAV1_ACTIVE')
        add_var("NAV STANDBY FREQUENCY:1", "MHZ", FLOAT32,  'NAV1_STANDBY')
        add_var("NAV ACTIVE FREQUENCY:2", "MHZ", FLOAT32,  'NAV2_ACTIVE')
        add_var("NAV STANDBY FREQUENCY:2", "MHZ", FLOAT32,  'NAV2_STANDBY')
        add_var("COM ACTIVE FREQUENCY:1", "MHZ", FLOAT32,  'COM1_ACTIVE')
        add_var("COM STANDBY FREQUENCY:1", "MHZ", FLOAT32,  'COM1_STANDBY')
        add_var("COM ACTIVE FREQUENCY:2", "MHZ", FLOAT32,  'COM2_ACTIVE')
        add_var("COM STANDBY FREQUENCY:2", "MHZ", FLOAT32,  'COM2_STANDBY')
        add_var("ADF ACTIVE FREQUENCY:1", "KHZ", FLOAT32,  'ADF1_ACTIVE')
        add_var("ADF STANDBY FREQUENCY:1", "KHZ", FLOAT32,  'ADF1_STANDBY')
        add_var("ADF ACTIVE FREQUENCY:2", "KHZ", FLOAT32,  'ADF2_ACTIVE')
        add_var("ADF STANDBY FREQUENCY:2", "KHZ", FLOAT32,  'ADF2_STANDBY')
        #Transponder
        add_var("TRANSPONDER CODE:1", "", INT32,  'XPDR')
        #Nav1
        add_var("Nav OBS:1", "degrees", INT32,  'NAV1_OBS')
        add_var("Nav Radial:1", "degrees", FLOAT32,  'NAV1_RADIAL')
        add_var("Nav CDI:1", "number", INT32,  'NAV1_CDI')
        add_var("Nav GSI:1", "number", INT32,  'NAV1_GSI')
        add_var("Nav has Nav:1", "bool", INT32,  'NAV1_hasNAV', converttoBool)
        add_var("Nav has Localizer:1", "bool", INT32,  'NAV1_hasLOC', converttoBool)
        add_var("Nav has Glide Slope:1", "bool", INT32,  'NAV1_hasGS', converttoBool)
        add_var("Nav DME:1", "Nautical Miles", FLOAT32,  'NAV1_DME')
        add_var("NAV TOFROM:1", "Enum", INT32,  'NAV1_TOFROM')
        add_var("Nav Ident:1", "", STRING8,  'NAV1_ID')
        #Nav2
        add_var("Nav OBS:2", "degrees", INT32,  'NAV2_OBS')
        add_var("Nav Radial:2", "degrees", FLOAT32,  'NAV2_RADIAL')
        add_var("Nav CDI:2", "number", INT32,  'NAV2_CDI')
        add_var("Nav GSI:2", "number", INT32,  'NAV2_GSI')
        add_var("Nav has Nav:2", "bool", INT32,  'NAV2_hasNAV', converttoBool)
        add_var("Nav has Localizer:2", "bool", INT32,  'NAV2_hasLOC', converttoBool)
        add_var("Nav has Glide Slope:2", "bool", INT32,  'NAV2_hasGS', converttoBool)
        add_var("Nav DME:2", "Nautical Miles", FLOAT32,  'NAV2_DME')
        add_var("NAV TOFROM:2", "Enum", INT32,  'NAV2_TOFROM')
        add_var("Nav Ident:2", "", STRING8,  'NAV2_ID')
        #Adfs
        add_var("ADF Radial:1", "degrees", INT32,  'ADF1_RADIAL')
        add_var("ADF Radial:2", "degrees", INT32,  'ADF2_RADIAL')
        add_var("ADF Signal:1", "number", INT32,  'ADF1_hasNAV', converttoBool)
        add_var("ADF Signal:2", "number", INT32,  'ADF2_hasNAV', converttoBool)
        #Markers
        add_var("MARKER BEACON STATE", "", INT32,  'MARKERS')
        
def setup_events(add_event):        
    
        
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
        add_event('VOR1_SET','NAV1_OBS')
        add_event('VOR2_SET','NAV2_OBS')
