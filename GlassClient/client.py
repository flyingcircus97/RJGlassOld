# client.py  -- 
# Runs in thread and communicates with the Glass Server.
import threading
import socket
import config
import time
import struct
import logging

import GlassProtocol

from variable import variables

class client_c(object):
    #Overall client class
    
    def __init__(self):
        
       #Read Config file for port and host of GlassServer to connect to.
        self.port = int(config.client.config['GlassServer']['port'])
        self.host = config.client.config['GlassServer']['ip']
        self.client_thread = threading.Thread(target = self.run)
        self.go = True
        
        self.rx_count =0
        self.VD_recv = False
    def stop(self):
        self.go=False    
    
    def start(self):
        self.client_thread.start()
       
    def run(self):
        self.init_client()
        count = 10
        while self.go:
            #Check to see if connected, if not try to connect to Glass Server
            if not self.connected:
                self.try_connect()
            else:
                if not self.AVsent: #If no AV sent then send add variables
                    self.AVsend(variables.list())
                                    
                #Check send buffer
                #self.send_data()
                #self.parse_data(self)
                GlassProtocol.sendrecv(self, self.sock)
            
                if self.go:
                    GlassProtocol.parse_data(self)
                #Check for server ping
                if (time.time() - self.lastRXtime) > 10:
                    self.reset_connect()
            
            #Time delay for know for testing
            #print count
            #count = count -1
            #time.sleep(0.01)
         
        logging.info("Client Thread Ended %s", self.client_thread.name)
            
    def init_client(self):
        self.commands = ["PI","VD"]
        self.connected = False
        self.AVsent = False
        self.send_buffer = ""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        GlassProtocol.initialize(self)
        
        
    def try_connect(self):
        success = False
        try:
            self.sock.connect((self.host,self.port))
            success = True
        except socket.error, e:
            if e[0]==111: #Connection refused
                pass
            else: #Something is wrong True Error occured
                logging.warning("Client: Socket Error %r", e)
                self.go = False #Quit connection
        if success: 
            self.connected= True
            logging.info("Client: Connected %r:%r",self.host,self.port)
            self.lastRXtime = time.time()
            self.sock.setblocking(0)
        else: 
            time.sleep(3)
        
    def reset_connect(self):
        #Reset connection if no ping recieved
        logging.warning("Client: Resetting Connection No Data Received")
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        time.sleep(1)
    
    def add_to_send(self, response):
        #Takes data to send in list form
        
        for id, data, desc in response: #Cycle through all data that needs to be sent.
            length = len(data)
            send_s = id + struct.pack("H",length) + data
            self.send_buffer += send_s
            
    def send_data(self):
        if len(self.send_buffer) > 0:
            #try:
                self.sock.send(self.send_buffer)
                logging.debug("Client: Send send_buffer %r" ,self.send_buffer)
                self.send_buffer = "" #Empty send buffer
            #except:
            
            
    def AVsend(self, list):
        data_out = ""
        if list and len(list)>0:
            for i in list:
                data_out+=struct.pack("H",i)
            if data_out != "":
                self.add_to_send([["AV",data_out,"Add variables"]])
                self.AVsent = True
                
    def process_data(self, command_byte, command_data):
        #print "Byte = %r  Data = %r" %(command_byte, command_data)
        data_len = len(command_data)
        desc = "UNKNOWN"
        
        if command_byte == "PI":
            desc = "Ping from Server "
            #No actions taken
            logging.debug("Client: Ping for Server Received")
        elif command_byte == "VD":
            i=0
            self.rx_count = self.rx_count + 1
            self.VD_recv = True
            logging.debug("Client: VD Recieved rx_count %r" , self.rx_count)
            while i<data_len: #Loop through till data runs out.
                #Get addr
                addr = struct.unpack("H",command_data[i:i+2])[0]
                i+=2
                #Determine size of data value.
                #Make sure it exists.
                if variables.exists(addr):
                    #Get variable
                    var = variables.dict[addr]
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
                    format = "%" + var.format_s
                    value = format %v
                    desc = "Client Set Variable 0x%04X to " %(addr) + value
                    #print desc
                    logging.debug(desc)
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
            
        #self.log_comm('TX', command_byte, command_data, desc)
