#!/usr/bin/env python
# ----------------------------------------------------------
# Testing for IOCPClient
# ----------------------------------------------------------
# This module handels communication with a IOCPServer
# ---------------------------------------------------------------

import threading 
import logging
import time
#import config
#from socket import *
import socket

import variables.variable
import IOCPdef
#Constants
class IOCP_data_obj(object):
    #Data object used by variables to hold IOCP data.
    def __init__(self, var_obj, read = None, write = None):
        self.var = var_obj #Parent variable object (var_obj)
        self.read = read
        self.write = write
        self.change_count = self.var.change_count
        
    def var_read(self, value):
        if self.read: #Check for function
            self.var.setvalue(value)
            
    def var_changed(self): 
        #Scans variable if writeable sees if changed, then sends to IOCP
        
        if self.write: #If variable not to be written to IOCP stop here
            if self.var.change_count != self.change_count: #see if variable has changed
                self.change_count = self.var.change_count
                return self.var.getvalue()
            else: 
                return None
        else:
            return None
        
class IOCP_Client_c(threading.Thread):
    
       
    def __init__(self, parent, ip, port):
        self.IOCPComm = parent
        self.ip = ip
        self.port = port
        self.clock = time.time()
        self.count = 0
        self.kill_timer = 0
        threading.Thread.__init__(self) 
        self.read_buffer = ''
        self.packet_data = []
        self.go = True
        self.connected = False
        
        
    def send(self, data):
        #Send the data, will add header, type is type of command
        self.count += 1 #just a incramental counter
        pre = 'Arn.'
        out = pre + data + '\r\n'
        #Send data to socket
        self.s.send(out)
        logging.debug("IOCPClient: IOCP Send: %s", pre+data)
        
    def send_typeserver(self, name):
        data = 'TipoSer:'+ name + ':'
        self.send(data)
        
    def send_live(self):
        self.send('Vivo:')
        
    def send_response(self, response_l):
        command = 'Resp:'
        data = ''
        for i in response_l:
            if i[1]!=None:
                data+='%d=%d:' %(i[0],i[1])
            
        if len(data) >0 :
            self.send(command+data)
            
    def send_initiation(self, init_l):
        data = 'Inicio:'
        for i in init_l:
            data += '%d:' %i 
        
        if len(data) >0 :
            self.send(data)
        
    def connect(self, addr, port):
    #Attempts to connect to IOCP Server
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(5.0)
        
        
        succeed = False
        try:
            self.s.connect((addr, port))
            self.s.setblocking(0)
        #Send connection header
            self.send_typeserver('GlassServer')
            succeed = True
            
        except socket.error, e:
             if e[0]!=10035: #Non blocking error
                succeed = False
                

        
        return succeed    

    def close(self):
        try: 
            self.s.close()
        except AttributeError:
            logging.warning("IOCPClient: Can't close Socket, Socket doesn't exist.")

    def quit(self):
        logging.info("IOCPClient: Qutitting IOCP Client")
        self.go = False
        
        
    def connect_init(self):
        #Set variables that need to be monitor, know if they change.        
        self.send_initiation(self.IOCPComm.keys())
        self.connected = True
        
    def process_resp(self, args):
        for arg in args:
            l = arg.split('=')
            if len(l) == 2:
                var_num = int(l[0])
                value = int(l[1])
                self.IOCPComm.response(var_num, value)
                
    
        
    def run(self):
        
        def reset_timer():
            #used to reset the kill timer.
            #Called from RJGlass to reset timer, if timer isn't reset then thread will die.
            self.kill_timer = 0 #currently not used
        
        def process_packet(packet):
            
            command = packet[0]
            args = packet[1:-1] #Remove command, and CRLF at end.
            #print "IOCP Packet Recieved", command, args
            
            if command == 'Vivo':
                self.send_live()
            elif command == 'Resp':
                self.process_resp(args)
        
        def check_var():
            self.IOCPComm.check_var()
            
        def decode_receive(data_in):
            #Used to look for and read anydata that is coming in.
            #All data starts with Arn.
            #Split by Arn.
            packets = data_in.split('Arn.')
            for packet in packets:
                if len(packet)>0:
                    process_packet(packet.split(':'))
                
        
            #print self.packet_data
        #Begin self.receive()
        
        def receive():
            
            r = ''
            try:
                r = self.s.recv(1024)
                
            except socket.error, e:
                
                if e[0] != 10035:
                   logging.warning("IOCP Client: IOCP Server socket error", e)
                   self.connected = False
                
            except socket.timeout:
                pass
                #if self.go:
                #    print "SERVER TIMED OUT (Will ReTry)"
                    
            except: #Unknown error so shutdown server.
                
                self.connected = False
                    
            return r
                    
        #Starst of run loop
        self.go = True
        self.live_count = 0
        while self.go:
            #I connected run
            time.sleep(0.1)
            if self.connected:
                #Receive data
                r = receive()    
                self.read_buffer = r
                if len(r) > 0:
                    logging.debug("IOCPClient: IOCP Recv: %r", r)
                    decode_receive(self.read_buffer)
                #Send data Response if needed
                self.send_response(self.IOCPComm.check_var())
                #Send live if needed
                self.live_count +=1
                if self.live_count > 40:
                    self.send_live()
                    self.live_count = 0
                
            else: #Try to reconnect
                if self.connect(self.ip, self.port) == True:
                    self.connect_init()
                    logging.info("IOCPClient: Connected to IOCP Server %s:%d", self.ip,self.port)
                else:
                    logging.warning("IOCPClient: Connect to IOCP Server failed %s:%d",self.ip,self.port)
                    time.sleep(5)
        #End of while self.go
        self.close()
        logging.info("IOCPClient: IOCP Thread Ended")
        
        
class IOCPComm(object):
        
        def __init__(self, config):
            self.variables = variables.variable.variables
            self.active = int(config['active'])
            self.ip = config['ip']
            self.port = int(config['port'])
            self.client = IOCP_Client_c(self, self.ip, self.port)
            self.var_dict = {}
            IOCPdef.setup(self, self.variables)
            self.var_keys = self.var_dict.keys()
            if self.active: 
                self.client.start()
                
        def keys(self):
            return self.var_keys
            
        def add_IOCP(self, var_num, var, read, write):
                self.var_dict[var_num] = IOCP_data_obj(var, read, write)
                
        def response(self, var_num, value):
                if var_num in self.var_keys:
                    self.var_dict[var_num].var_read(value)
                    
        def check_var(self):
                #Look for changes
                l = []
                for var_num in self.var_keys:
                    l.append([var_num, self.var_dict[var_num].var_changed()])
                    
                return l
                
                
        def quit(self):
            self.client.go = False
         
if __name__ == '__main__':
    c = IOCP_Client_c()
    c.connect('127.0.0.1', 8092)
    for i in range(100):
        print "COUNT", i
        
        c.run()
        c.send('Resp:1=%d:' %i)
        if i==3:
            c.send('Vivo:')
        time.sleep(1)
    
    c.close()