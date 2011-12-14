#!/usr/bin/env python
# ----------------------------------------------------------
# Controller File for FSX
# ----------------------------------------------------------
from PySimConnect import SimConnect, DataDefinition
import FSXdef
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
    def __init__(self, variables, mod_data, sim):
        self.mod_data = mod_data
        self.connected = False
        self.desire_connect = True
        self.variables = variables
        self.last_connect_attempt = 0
        self.nodata = True
        self.nodata_time = 0
        self.mode = config.modes[sim['mode']]
        #self.s = SimConnect('GlassServer', self.mode, True)
        #self.sevent = SimConnect('GlassServer Event', self.mode, False)
        
        #self.addr = '192.168.1.46'
        self.addr = sim['IP']
        #self.port = 1500
        self.port = int(sim['port'])
              #Add definition's
        #self.s.definition_0 = self.s.create_DataDefinition(2)   
        #self.connect()    
        time.sleep(0.4)
        
    def init_comm(self):
        #Before connecting initialize SimConnect connections
        self.s = SimConnect('GlassServer', self.mode, True)
        self.sevent = SimConnect('GlassServer Event', self.mode, False)
        
    def close_comm(self):
        #Shutdown both sockets.
        self.s.quit()
        self.sevent.quit()
        self.connected = False
        
    def quit(self):
        self.desire_connect = False
        self.last_connect_attempt = time.time()
        self.close_comm()
        
    def connect(self):
        self.init_comm()
        self.connected = True
        self.desire_connect = True
        print 'Connect:' , self.addr, self.port
        if not self.s.connect(self.addr, self.port, True):
            self.connected = False
        if not self.sevent.connect(self.addr, self.port, False):
            self.connected = False
        self.last_connect_attempt = time.time()
        if self.connected == True:        
           FSXdef.setup(self.s,self.variables)
           FSXdef.setup_events(self.sevent, self.variables) 
           self.request_data()
           print "Connection to FSX Succeded"
        else:
            print "Connection to FSX Failed"
        
            
    def request_data(self):
        self.s.definition_0.request(4, DataDefinition.USER, DataDefinition.ONCE, interval = 0, flag = 0)
    
    def decode_input(self, data_in):
        if self.s.definition_0.id in data_in: #Define ID is high priority data, if received then compute, and request another.
            #start_time = 0.0
            self.request_data()
            #self.comp() # Main computation loop
            self.nodata = False #Rest no data boolean    
            self.nodata_time = time.time()
        else:
            diff = time.time() - self.nodata_time
            #if diff > 5.0: #If no data for more than 5 seconds, stop socket.
                #self.s.client.go = False 
            if diff > 2.0: #If no data for 2 seconds.
            #Request data
                self.nodata = True
            
                #Request more data from FSX (This was causing multiple requests removed for now)
            #    self.request_data()
            #    self.nodata_time +=2 #Reset timer so request again in 2 seconds.
            
    def calc_status_message(self):
        if self.connected:
            return ("Connected")
        elif self.desire_connect: #Not connected, but wanting to be connected
            return ("Connecting")
        else:   #Disconnecting.
            return ("Disconnected")
        
            
            
    def process(self):
        if self.connected:
            if ((self.s.connected() == False) or (self.sevent.connected() == False)): #Probably with socket, socket has shutdown.
                self.close_comm() #Reset comm, to try a reconnect.
            else:
                self.decode_input(self.s.receive())
                self.mod_data.comp()
            
        elif self.desire_connect == True: #not connected
            if (time.time() - self.nodata_time) > 5.0: #Wait 5 sec to reconnect
                if (time.time() - self.last_connect_attempt) > 10.0: #Wait 10 sec between attempts.
                    self.connect()
                
        #Create Status message
        #self.status_message = self.calc_status_message()
        pass        