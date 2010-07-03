#!/usr/bin/env python
# ----------------------------------------------------------
# variable MODULE for GlassCockpit procject RJGlass
# ----------------------------------------------------------
# This module will take the keys that are pressed on the keyboard and take appropriate action.
#
# Copyright 2009 Michael LaBrie
#
#    This file is part of RJGlass.
#
#    RJGlass is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.

#   RJGlass is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ---------------------------------------------------------------

#This modules creates, assigns, and processes the variables for the Glass Protocol.
#This module is used for both the server and clinet.
#import PySimConnect
import struct
import inspect, os, time

class data_obj(object):
    #Used to make a object for Definition to link to
    def __init__(self, value):
        self.value = value
        self.adjusted = value #Used incase value needs to be adjusted from data inputed from FSX.
        self.sim_event = None
        self.inhibit = 0 #Used to postpone reading of data value from sim, when data is written too.
        
    def set_value(self, value):
        self.value = value
        if self.sim_event != None:
            self.sim_event.send()
            self.inhibit = 4


class var_obj(object):
    #This is the a Glass Protocol variable object, similar to data_obj that holds are information
    #about each variable. Used only to communicate between instances of RJGlass. Not FSX
    def __init__(self, addr, name, pack_format, desc, unit, format_s): 
        self.addr = addr #Address of variable
        self.name = name #Name of variable, used for lookup.
        self.desc = desc #Description, used for Web interface.
        self.unit = unit #Unit of variable, used for Web interface.
        self.format_s = format_s #Format of variable, used for Web interface.
        self.writeable = True #Set to True, will be set to False if applicable.
        self.valid = False #Where valid check func goes if desired.
        self.pack_format = pack_format #Either "f" - float, "i" - int, "I" - for unsigned int.
        self.pack_size = struct.calcsize(pack_format) #Calculates size in bytes.
        self.change_count = 0 #This is incremented everytime value changed. Used for change detect.
        self.read_func = None #Func to convert sim value to variable value.
        self.write_func = None #Func to convert variable value to sim value. (Set by FSX or X-Plane connect modules)
        self.data = data_obj(0) #Create dataobj.
        self.prev_data = self.data.value
    def change_check(self):
        
        if self.prev_data!= self.data.value:
            self.prev_data = self.data.value
            self.change_count +=1
            
    def unpack(self, value):
        print self.pack_format, "%r" %value
        return struct.unpack(self.pack_format, value)[0]
    
    
    
    def set_writeable(self, func):
        self.writeable = func
        
    def set_valid_check(self, func):
        self.valid = func
    
    def setvalue(self, value):
        #Check for valid number.
        result = True
        if inspect.ismethod(self.valid): #Check if valid check exists.
            result = self.valid(value)
            if ((result != True) or (result != False)): #If not true or flase then change value to result (different value)
                value = result 
        if result != False: #If valid check return False (Don't write)
        #Check for custom write function in self.writable.
        #If write_func is True, means variable is writable but no write_func
        #If write_func is False, means variable not writeable.
            if inspect.ismethod(self.writeable):
                #self.writeable(self.unpack(value))
                print "WRITEABLE FUNC"
                self.writeable(value)
            elif self.writeable == True:
                #self.data.set_value(self.unpack(value))
                self.data.set_value(value)
            else:
                print "Variable %04X not WRITEABLE" %self.addr
        else: #if result == False
            print "Value %r - Failed valid check for Variable %04X" %(value, self.addr)
            
    def client_setvalue(self, value):
        self.data.value = self.unpack(value)
    
class variable_c(object):
    
    
    def __init__(self):
        #self.aircraft = aircraft
        #Creating dict containing all variables
        self.dict = {} #Holds all varibles keyed by address.
        #Get Element Tree setup for parsing of variable XML files.
        from xml.etree.ElementTree import ElementTree
        self.tree = ElementTree()
    
    def byName(self, name):
        '''
        Returns variable object by name. (Should be unique so only one is returned.)
        Returns None if not found.
        '''
        r = None
        for var in self.dict.itervalues():
            if var.name == name: #If name match return variable object
                r = var
        return r    
                
                    
    def exists(self, addr):
        #Will check if addr exists.
        if addr in self.dict.keys():
            return True
        else:
            return False
    
    def size(self, addr):
        if addr in self.dict.keys():
            return self.dict[addr].pack_size
        
    def writeable(self, addr):
        if self.dict[addr].writable:
            return True
        else:
            return False
        
    def get(self, addr):
        if addr in self.dict.keys():
            return self.dict[addr]
        else:
            print "Error: Variable Addr %04X Not valid" %addr
            return None
    
    def get_string(self,addr):
        v = self.get(addr)
        if v == None:
            return None
        else:
            format = "%" + v.format_s
            s = format %v.data.value
            return s
    
    def set(self, addr, value):
        #Sets variable, if settible.
        if addr in self.dict.keys():
            v = self.dict[addr]
            
            v.setvalue(value)
            return v.data.value
        else:
            print "Error: Variable Addr %04X Not valid Can Not Write to" %addr    
            return False
        
    def change_check(self):#Is called when SV is recieved.
        #Go through all variables and check to see if they have changed.
        dict = self.dict
        for v in dict:
            dict[v].change_check()
    
    def parse_variable_file(self, file_name):
        delimeter = ','
        columns = 3
        ret_list = []
        #Parse file
        var_list =  self.tree.parse(file_name)
        #Loop thourgh lines
        for v in var_list:
            #Get all children.
            children = v.getchildren()
            #Setup defaults
            type = 'float'
            unit = None
            format = '5.2f'
            desc = None
            #Go through each child.
            for c in children:
                tag = c.tag
                value = c.text
                #If else
                if tag == 'name':
                    name = value
                elif tag == 'addr':
                    addr = int('0x'+value,16)
                elif tag == 'type':
                    type = value
                elif tag == 'desc':
                    desc = value
                elif tag == 'unit':
                    unit = value
                elif tag == 'format':
                    format = value
                #addr = int('0x'+data[0],16)
            #Add Variable to list
            ret_list.append(self.add_var(addr, name, type, desc, unit, format))
            print addr, name, type, desc, unit, format
            #time.sleep(0.5)
        return ret_list
    
    def add_vargroup(self, var_file, var_list):
        #Split
        #print "VAR_LIST", var_list
        l = var_file.split(os.sep)
        l.pop(0)  #Take out first (modules)
        l.pop()   #Take out last 'variable.txt'
        group = self.var_groups
        print l
        for name in l:
            last_group = group
            if name not in group:
                group[name] = {}
            group = group[name]
        last_group[name] = var_list
            
        
        print self.var_groups
        
    def get_varAJAX(self, name):
        
        def check_none(value):
            if value == None:
                return ''
            else:
                return value
        
        out_list = []
        
        name_list = name.split('.')
        var_group = self.var_groups
        #Drill down to dictonary.
        for n in name_list:
            if n in var_group:
                var_group = var_group[n]
            else:
                var_group = []
        print name
        #Check to see if var_group found.
        if type(var_group) == list:
            for i in var_group:
                #Uppercase type F, I etc.
                var_type = i.pack_format.upper()
                #Format variable
                format = "%" + i.format_s
                value = format %i.data.value
                              
                out_list.append([i.addr, i.name, i.pack_format.upper(), value, check_none(i.unit), check_none(i.desc)])
                #print "***I", i
        if len(out_list) > 0:
                out_list.insert(0,[name])
        return out_list
            
                
        
    
    def parse_variable_files(self, var_files):
        #Used to handle multiple variable files to parse.
        self.var_groups = {}
        for f in var_files:
            var_list = self.parse_variable_file(f)
            self.add_vargroup(f, var_list)
            
            
            
    def add_var(self, address, name, type, desc, unit, format):
        '''
        Adds varible object to servers variable dictionary.
        -- Checks to make sure name and address are both unique.
        '''
        def convert_type(type):
            if type == 'FLOAT':
                type_s = 'f'
            elif type == 'INT':
                type_s = 'i'
            else:
                type_s = 'f' #If not specifies just make float.
            return type_s
          
        #Upper case type
        type = type.upper()
        #Check for unique address.
        if self.exists(address):
            print "Warning: Address 0x%X already exists in Variable dict." %addr
        #Check for unique name
        elif self.byName(name) != None:
            print "Warning: Name %s already exists in Variable dict." %name
        else:
            self.dict[address] = var_obj(address, name, convert_type(type), desc, unit,format)
            
            return self.dict[address]
#def __init__(self):
    #print "LET's GO"
variables = variable_c()
        #Load up dictinary with all variables.
    #    aircraft = self.aircraft
        #Speed
    #    add_var(0x0100, "f", aircraft.airspeed.IAS)
    #    add_var(0x0101, "f", aircraft.airspeed.Mach)
    #    add_var(0x0102, "f", aircraft.airspeed.GS)
    #    add_var(0x0103, "f", aircraft.airspeed.bug)
        #Artifical Horizon
    #    add_var(0x0200, "f", aircraft.attitude.pitch)
    #    add_var(0x0201, "f", aircraft.attitude.bank)
    #    add_var(0x0202, "h", aircraft.attitude.FD_active)
    #    add_var(0x0203, "f", aircraft.attitude.FD_pitch)
    #    add_var(0x0204, "f", aircraft.attitude.FD_bank)
    #    add_var(0x0205, "i", aircraft.attitude.turn_coord)
    #    add_var(0x0206, "i", aircraft.attitude.marker)
        #Altimeter
    #    add_var(0x0300, "i", aircraft.altimeter.indicated)
    #    add_var(0x0301, "i", aircraft.altimeter.absolute)
#        add_var(0x0302, "H", aircraft.altimeter.bug)
#        add_var(0x0303, "H", aircraft.onground)
#        #HSI
#        add_var(0x0400, "f", aircraft.HSI.Mag_Heading)
#        add_var(0x0401, "f", aircraft.HSI.Mag_Variation)
#        add_var(0x0402, "f", aircraft.HSI.Mag_Track)
#        add_var(0x0403, "f", aircraft.HSI.Heading_Bug)
#        
#        #VSI
#        add_var(0x0500, "i", aircraft.VSI)
#        
#        #COM and NAV Radio Freq
#        add_var(0x0600, "f", aircraft.Com_1.Active)
#        add_var(0x0601, "f", aircraft.Com_1.Standby)
#        add_var(0x0602, "f", aircraft.Com_2.Active)
#        add_var(0x0603, "f", aircraft.Com_2.Standby)
#        add_var(0x0604, "f", aircraft.Nav_1.Active)
#        add_var(0x0605, "f", aircraft.Nav_1.Standby)
#        add_var(0x0606, "f", aircraft.Nav_2.Active)
#        add_var(0x0607, "f", aircraft.Nav_2.Standby)
#        
#        #Test data
#        add_var(0x0A00, "i", aircraft.TEST, True)
#        
#        return dict