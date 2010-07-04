#!/usr/bin/env python
# ----------------------------------------------------------
# Glass Server
# ----------------------------------------------------------
# 
#
# use nc localhost 5004 in linux to test

# ---------------------------------------------------------------

import threading 
import time
import struct
import sys, os
try:
    import config
except ImportError:
    print "PY2EXE"
    # We're in a py2exe, so we'll append an element to the (one element) 
    # sys.path which points to Library.zip, to the directory that contains 
    # Library.zip, allowing us to import config.py
    # Adds one level up from the Library.zip directory to the path, so import will go forward
    sys.path.append(os.path.split(sys.path[0])[0])
    import config
#from socket import *
import socket, select
import pickle
import string
#import FMS_control
#import aircraft
#Constants


import SocketServer


class VariableWatch_c(object):
    #Class to keep track of variables that are being watched
    def __init__(self, v):
        self.var = v
        self.addr = v.addr
        self.change_count = -1 #This makes it so variable will be sent first time.
        
    def check_change(self):
        
        if self.change_count != self.var.change_count:
            self.change_count = self.var.change_count
            return True
        else:
            return False
        
class VariableWatch_list(object):
    def __init__(self, variables):
        self.list = []
        self.addr_list = []
        self.variables = variables #Reference to variable module
        
    def update_addr_list(self):
        self.addr_list = []
        for v in self.list:
            self.addr_list.append(v.addr)
            
    def add(self, addr):
        if addr in self.addr_list:
            print "Warning: Address %04X allready in watch list. Not Added" %addr
        else:
            v = self.variables.get(addr)
            if v!=None:
                self.list.append(VariableWatch_c(v))
                self.update_addr_list()
                print "Added Variable %04X to watch list." %addr
                
    def check(self):
        change_list = []
        for v in self.list:
            if v.check_change():
                change_list.append(v)
        
        return change_list
        
    
class GlassConnection(object):
    #This keeps track of all the data in the glass connection.
    #Variables that need to be watched .... 
    #This does all the communicating with the aircraft module
    def __init__(self, variables):
        #self.aircraft = aircraft
        self.response = None
        self.variables = variables #Reference to variable module
        #self.events = events
        #List to watch variables
        self.var_watch = VariableWatch_list(variables) #List of variables watched 
    
    def getsend(self): #Checks and returns any data that needs to be sent.
        response = []
        #Check for varible changes to send
        var_change = self.var_watch.check()
        
        if len(var_change)>0:
            r = ''
            for v in var_change:
                r+= struct.pack("H", v.addr) + struct.pack(v.var.pack_format, v.var.data.value)
            response.append(['VD',r]) #Response is command_id, then data
            
        return response
        

        
    def AddVariable(self, addr):  #This adds a variable to watch
        self.var_watch.add(addr)
    
    def SetVariable(self, addr, value):
        #Set the value of the variable
        self.variables.set(addr,value)
    

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    
    #def __init__(self, request, client_address, server):
#        print "MICHAEL", request, client_address, server
    #    SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        
    #    return

    
    #def __init__(self, aircraft):
    #    self.aircraft = aircraft
    #    print aircraft
    def setup(self):
        self.connection = GlassConnection(self.server.variables)
        self.commands = ["AV","SV","SE"]
        print self.client_address, 'connected!'
        #self.request.send('hi ' + str(self.client_address) + '\n')
        #self.socket.settimeout(10)
        self.request.setblocking(0)
        self.variables = self.connection.variables
        #self.events = self.connection.events
        #Time of last transmission of data. 
        #  -- Used so data is always sent to client, to make sure client hasn't disconnected.
        self.time_lastTX = 0

    
    def process_data(self, command_byte, command_data):
        print "Byte = %r  Data = %r" %(command_byte, command_data)
        data_len = len(command_data)
        
        if command_byte == "AV":
            for i in range(0,data_len, 2): #Decode addr every 2 char.
                addr = struct.unpack("H",command_data[i:i+2])[0]
                self.connection.AddVariable(addr)
        elif command_byte == "SV":
            i=0
            while i<data_len: #Loop through till data runs out.
                #Get addr
                addr = struct.unpack("H",command_data[i:i+2])[0]
                i+=2
                #Determine size of data value.
                #Make sure it exists.
                if self.variables.exists(addr):
                    #Get variable
                    var = self.variables.dict[addr]
                    #Determine size
                    size = var.pack_size
                    value_s = command_data[i:i+size]
                    i+= size
                    #Try to write to it, if var is not writable will get error.
                    #print addr, "%r" %value_s
                    v = struct.unpack(var.pack_format,value_s)[0]
                    #print "V= ",v, var.pack_format
                    var.setvalue(v)
                    #self.connection.SetVariable(addr,value_s)
        elif command_byte == "SE": #Send Event
            #Events don't repeat.. so certian events can be passed through server,
            #with server not needing to know of them.
            #If events repeat then server needs to know size of data of each event, 
            #for it to parse it correctly.
            
            addr = struct.unpack("H", command_data[:2])[0]
            data = command_data[2:] #Data is all data after addr.
            #Send addr, and data to event obj on server.
            #self.events.process(addr,data)
            #To see if server is aware of event and needs to process it.
            
            #Automatically forward event to all clients.
            #*** STILL NEED TO DO  ****
            
        
    
    def parse_data(self):
        #Go through data and find command and end codes to parse recv buffer
        data = self.recv_buffer
        buffer_length = len(data)
        if buffer_length>0: 
            go=True
        else:
            go=False
            
        while go:
            go=False #If data is found then go will be set to true
            #1st two byte command code
            command_id = data[:2]
            if command_id in self.commands: #Check to make sure it is command code
                #Now get length two bytes
                length = struct.unpack("H", data[2:4])[0]
                #Check if buffer is long enough for all data.
                if buffer_length >= length + 4: 
                    #Parse data
                    command_data = data[4:length+4]
                    print "Command %r %r" %(command_id, command_data)
                    self.process_data(command_id, command_data)
                    #Delete from recv buffer all data before end point
                    self.recv_buffer = data = data[length+4:]
                    #print "AFTER %r -- %r" %(self.recv_buffer, data)
                    if len(data) > 0: #If more data then check next data
                        go = True
                    #print self.recv_buffer, i_start, i_end
            else:
                print "ERROR: Command %s Not Valid" %command_id
                self.recv_buffer = ''
    def sendrecv(self):
        #Send and recieve data
        time.sleep(0.01)
        temp_time = time.time()
        
        #Send data if available
        if len(self.send_buffer)>=1:
            self.request.send(self.send_buffer)
            print "SENDING %r" %self.send_buffer
            self.send_buffer = '' #Clear buffer after it has been sent.
            self.time_lastTX = temp_time
        elif temp_time - self.time_lastTX > 3:
            self.add_to_send([['PI','']])
            
        #Try to recieve data
        try:
            data = self.request.recv(1024)
            #print "DATA %r" %data
            self.recv_buffer += data
        except socket.error, e:
            if e[0]==11: #Standard error if no data to receieve
                pass 
            else: #Something is wrong True Error occured
                print "Error", e
                self.go = False #Quit connection

    def add_to_send(self, response):
        #Takes data to send in list form
        for id, data in response: #Cycle through all data that needs to be sent.
            length = len(data)
            self.send_buffer += id + struct.pack("H",length) + data
            #print id, length, "%r" %data

    def handle(self):
        self.connected = False
        self.initial_sent = False
        self.recv_buffer = ''
        self.send_buffer = ''
        self.go = True
        while self.go:
            self.add_to_send(self.connection.getsend()) #Sees if any response is needed
            self.sendrecv()
            if self.go:
                self.parse_data()


    def finish(self):
        print self.client_address, 'disconnected!'
        self.request.send('bye ' + str(self.client_address) + '\n')

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    
    #Threads will close if main program stops.
    daemon_threads = True

    #Allows server to reuse addresses, if sockets don't shutdown correctly.
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass, variables):
        SocketServer.TCPServer.__init__(self, server_address, RequestHandlerClass)
        #self.aircraft = aircraft_data #This is so the handler can access the aircraft data.
        self.variables = variables
        #self.events = events

class Glass_Server_c():
    
    def __init__(self, variables):
    
        server = ThreadedTCPServer(('localhost', 39547), ThreadedTCPRequestHandler, variables)
    
        print server.server_address
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.setDaemon(True)
        server_thread.start()
    
        print "Glass Server running in thread:", server_thread.getName()

class mod_data_c(object):
    def __init__(self, mod_list, variables):
        #Go through mod_list and make list of data objects.
        #Used to run test, comp, or comp_second on all modules.
        self.mod_data = []
        for mod in mod_list:
            self.mod_data.append(mod.data(variables))
            
    def test(self):    
        #print "MOD DATA TEST"
        for mod_data in self.mod_data:
            mod_data.test()
    
    def comp(self):
        #print "MOD DATA COMP"
        for mod_data in self.mod_data:
            mod_data.comp()

class Glass_Controller_c(object):
    
        
    def setup_Modules(self):    
        import variables.variable as variable
        import modules
#        try:
#            import modules
#        except ImportError:
#            print "IMPORT ERROR - GlassServer.py Modules"
#            sys.path.append(os.path.split(sys.path[0])[0])
#            import config

        
        #self.variables = variable.variable_c()
        self.variables = variable.variables
        self.variables.parse_variable_files(modules.variable_files)
        self.mod_data = mod_data_c(modules.mod_list, self.variables)
    
    def setup_FSComm(self, variables):
        import FlightSim.comm
        self.FS_Comm = FlightSim.comm.FS_Comm
        self.FS_Comm.setup_sim(config.mode, self.mod_data)
    
    def __init__(self):
        self.setup_Modules()
        self.setup_FSComm(self.variables)        
        self.server = Glass_Server_c(self.variables)
        print "SERVER is RUNNING"
    
    def comp(self):
        self.mod_data.comp()
    
            
    def quit(self):
        self.FS_Comm.quit()
                           
            
if __name__ == '__main__':
    from WebServer.WebServer import GlassWebServer_c
    
    print "Press Ctrl-C to Quit"
    try:
        webserver = GlassWebServer_c()
        controller = Glass_Controller_c()
        
        mike = controller.variables.byName("ADF1_ACTIVE").data
        mike2 = controller.variables.byName("ADF1_STANDBY").data
        
        while 1:
            time.sleep(.3)
            #print mike.value, mike2.value
            controller.FS_Comm.process()
            #controller.comp()
            controller.variables.change_check()
    except KeyboardInterrupt:
        print "KEY INT"
        #Shot down server
        try:
            controller.quit()
        except NameError:
            print "No Controller Exists to Kill"
        
        
    #import variable, aircraft, event
#    import variable
#    import modules
    #aircraft_data = aircraft.data()
#    variables = variable.variable_c()
#    variables.parse_variable_files(modules.variable_files)
#    print modules.variable_files
    #print modules.list #list of modules to go through
#    mod_data = mod_data_c(modules.mod_list, variables)
#    mike = variables.byName('IAS').data
    #events = event.event_c(aircraft_data)
#    glass = Glass_Server_c(variables)
#    print "SERVER is RUNNING"
#    for i in range(10):
#        time.sleep(2)
#        mod_data.test() #Here loop through all modules calling test method.
#        print mike.value
    #input("enter to quit")
#    print variables.dict
