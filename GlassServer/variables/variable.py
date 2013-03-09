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
import logging
import inspect, os, time
import variables.valid_check as valid_check #classes to check validity of variables.
from FlightSim.FSX.PySimConnect import data_obj
from IOCP.IOCPClient import IOCP_data_obj

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
        self.valid_check = valid_check.check_c() #Valid check set to return value, (can be changed if desired.)
        self.pack_format = pack_format #Either "f" - float, "i" - int, "I" - for unsigned int.
        self.pack_size = struct.calcsize(pack_format) #Calculates size in bytes.
        self.change_count = 0 #This is incremented everytime value changed. Used for change detect.
        self.read_func = None #Func to convert sim value to variable value.
        self.write_func = None #Func to convert variable value to sim value. (Set by FSX or X-Plane connect modules)
        #IOCP Functions
        self.IOCP = IOCP_data_obj(self)
        if 's' in pack_format: #if string.
            self.data = data_obj('') #Create dataobj.
        else:
            self.data = data_obj(0) #Create dataobj.
        self.prev_data = self.data.value


    def change_check(self):
        #Increment change cound of variable, everytime it changes.
        #--Used by GlassServer, and IOCP, to see when variable has changed.
        if self.prev_data!= self.data.value:
            self.prev_data = self.data.value
            self.change_count +=1
            
    def unpack(self, value):
        #print self.pack_format, "%r" %value
        return struct.unpack(self.pack_format, value)[0]
    
    def set_writeable(self, func):
        self.writeable = func
        
    def set_valid_check(self, func):
        self.valid_check = func
    
    def add_test(self, obj):
        self.valid_check.add_test(obj)
    
    def setvalue_string(self, value):
        #Set value by passing in string.
        #Used for Webserver and variable XML parsing.
        pack_format = self.pack_format
        if pack_format == 'f':
            try:
                value = float(value)
            except ValueError:
                value = None
            #If integer, then make integer
        elif pack_format == 'i':
            try:
                value = int(value)
            except ValueError:
                value = None

        if value!=None:
            return self.setvalue(value)
        else:
            return None
    
    def setvalue(self, value):
        #Check for valid number and correct it if needed.
        logging.debug("Variable: Setting Value: %04X %r %r", self.addr, self.name, value)
        result = self.valid_check.test(value)
                    
        if result != None: #If valid check return False (Don't write)
        #Check for custom write function in self.writable.
        #If write_func is True, means variable is writable but no write_func
        #If write_func is False, means variable not writeable.
            if inspect.ismethod(self.writeable):
                #self.writeable(self.unpack(value))
                #logging.debug("Varibale: Writeable Func")
                self.writeable(result)
            elif self.writeable == True:
                #self.data.set_value(self.unpack(value))
                self.data.set_value(result)
            else:
                logging.debug("Variable: Variable %04X not WRITEABLE",self.addr)
                result = None
            
        else: #if result == False
            logging.warning("Variable: Value %r - Failed valid check for Variable %04X", value, self.addr)
        return result
            
    def getvalue(self):
        return self.data.value
    
    def client_setvalue(self, value):
        self.data.value = self.unpack(value)
        
    def client_set(self,value):
        self.data.set_value(value)
    
class variable_c(object):
    
    
    def __init__(self):
        #self.aircraft = aircraft
        #Creating dict containing all variables
        #print "VARIABLE INIT"
        self.dict = {} #Holds all varibles keyed by address.
        self.valid_check = valid_check
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
                
    def byAddr(self, addr):
        '''
        Returns variable object by name. (Should be unique so only one is returned.)
        Returns None if not found.
        '''
        r = None
        if addr in self.dict:
            r = self.dict[addr]
        
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
            logging.warning("Variable: Variable Addr %04X Not valid", addr)
            return None
    
    def get_string(self,addr):
        v = self.get(addr)
        if v == None:
            return None
        else:
            format = "%" + v.format_s
            s = format %v.data.value
            return s
    
    def add_test(self, test, var):
        #Add validity check / test to list of var byName.
        for v in var:
            i = self.byName(v)
            if i != None:
                i.add_test(test)
                
    
    def set(self, addr, value):
        #Sets variable, if settible.
        if addr in self.dict.keys():
            v = self.dict[addr]
            
            ok = v.setvalue(value)
            return ok
        else:
            logging.warning("Variable: Variable Addr %04X Not valid Can Not Write to", addr)
            return None
    
    def set_string(self, addr, value):
        #Sets variable, if settible. (By convert string to correct type.)
        if addr in self.dict.keys():
            v = self.dict[addr]
            
            ok = v.setvalue_string(value)
            return ok
        else:
            logging.warning("Variable: Variable Addr %04X Not valid Can Not Write to", addr)
            return None
    
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
            initial = None
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
                elif tag == 'initial':
                    initial = value
                #addr = int('0x'+data[0],16)
            #Add Variable to list
            new_var = self.add_var(addr, name, type, desc, unit, format)
            if initial != None:
                new_var.setvalue_string(initial)
            ret_list.append(new_var)
            
                
            #print addr, name, type, desc, unit, format
            #time.sleep(0.5)
        return ret_list
    
    def add_vargroup(self, var_file, var_list):
        #Split
        #print "VAR_LIST", var_list
        l = var_file.split(os.sep)
        l.pop(0)  #Take out first (modules)
        l.pop()   #Take out last 'variable.txt'
        group = self.var_groups
        
        for name in l:
            last_group = group
            if name not in group:
                group[name] = {}
            group = group[name]
        last_group[name] = var_list
            
        
        #print self.var_groups
        
    def get_varAJAX(self, name, values_only = False):
        #If values_only then will return just values not entire AJAX table.
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
        #print name
        #Check to see if var_group found.
        if type(var_group) == list:
            for i in var_group:
                #Uppercase type F, I etc.
                var_type = i.pack_format.upper()
                #Format variable
                format = "%" + i.format_s
                value = format %i.data.value
                #Check if string then convert from null terminated, and add space if blank.
                if type(i.data.value) == str:
                    value = i.data.value.rstrip("\0")
                    if value == '': value = ' '
                if values_only:
                    out_list.append(['value', value])
                else:
                    if i.writeable == False:
                        w = False
                    else:
                        w = True
                    out_list.append([w, hex(i.addr).upper()[2:], i.name, i.pack_format.upper(), value, check_none(i.unit), check_none(i.desc)])
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
            elif type == 'STRING':
                type_s = '8s'
            else:
                type_s = 'f' #If not specifies just make float.
            return type_s
          
        #Upper case type
        type = type.upper()
        #Check for unique address.
        if self.exists(address):
            logging.warning("Variable: Address 0x%X already exists in Variable dict.", address)
        #Check for unique name
        elif self.byName(name) != None:
            logging.warning("Variable: Name %s already exists in Variable dict.", name)
        else:
            self.dict[address] = var_obj(address, name, convert_type(type), desc, unit,format)
            
            return self.dict[address]
        
    def create_var_file(self, file_name):
        '''
        Creates a text file, of all variables.
        -- Can be used by clients to translate / lookup variables.
        -- Updated everytime GlassServer is run.
        '''
        def f_write(var):
            s = "0%X,%s,%s,%s,%s" %(var.addr, var.name, var.pack_format, var.desc, var.unit)
            s += '\n'
            return s
        
        #open file
        f = open(file_name,'w')
        #sort by address
        keys = self.dict.keys()
        keys.sort()
        for k in keys:
            d = self.dict[k]
            f.write(f_write(d))
            
        f.close()
        
    def reset_vars(self):
        for i in self.dict:
            self.dict[i].data.reset()

        
variables = variable_c()