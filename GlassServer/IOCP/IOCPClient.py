#!/usr/bin/env python
# ----------------------------------------------------------
# Testing for IOCPClient
# ----------------------------------------------------------
# This module handels communication with a IOCPServer
#
# 
# ---------------------------------------------------------------

import threading 
import time
import struct
#import config
#from socket import *
import socket
#Constants

        
class IOCP_Client_c(threading.Thread):
    
       
    def __init__(self, ip, port):
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
        print "IOCP Send: ", pre+data
        
    def send_typeserver(self, name):
        data = 'TipoSer:'+ name + ':'
        self.send(data)
        
    def send_live(self):
        self.send('Vivo:')
        
    def send_response(self, response_l):
        data = 'Resp:'
        for i in response_l:
            data+='%d=%d:' %(i[0],i[1])
            
        if len(data) >0 :
            self.send(data)
            
    def send_initiation(self, init_l):
        data = 'Inicio:'
        for i in init_l:
            data += '%d:' %i 
        
        if len(data) >0 :
            self.send(data)
        
    def connect(self, addr, port):
    #Attempts to connect to FSX.
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(5.0)
        succeed = False
        try:
            self.s.connect((addr, port))
        
            #Send connection header
            self.send('TipoSer:GlassServer:')
            
            succeed = True
        except socket.error:
            print "Could Not Connect"
        
        return succeed    

    def close(self):
        try: 
            self.s.close()
        except AttributeError:
            print "Can't close Socket, Socket doesn't exist."

    def quit(self):
        print "QUITTING IOCP Client"
        self.go = False
        
        
    def run(self):
        
        def reset_timer():
            #used to reset the kill timer.
            #Called from RJGlass to reset timer, if timer isn't reset then thread will die.
            self.kill_timer = 0 #currently not used
        
            
        def decode_recieve(data_in):
            #Used to look for and read anydata that is coming in.
            #Split by Arn.
            pass
        
            #print self.packet_data
        #Begin self.receive()
        
        def recieve():
            try:
                r = self.s.recv(1024)
            except socket.timeout:
                r = ''
                #if self.go:
                #    print "SERVER TIMED OUT (Will ReTry)"
                    
            except: #Unknown error so shutdown server.
                r = ''
                self.connected = False
                    
            return r
                    
        #Starst of run loop
        self.go = True
        
        while self.go:
            #I connected run
            if self.connected:
                r = recieve()    
                
                self.read_buffer = r
                if len(r) > 0:
                    print "IOCP Recv: %r" %r
                
            else: #Try to reconnect
                if self.connect(self.ip, self.port) == True:
                    self.connected = True
                    print "Connected to IOCP Server"
                else:
                    print "Connect to IOCP Server failed %s:%d" %(self.ip,self.port)
                    time.sleep(5)
        #End of while self.go
        self.close()
        print "End IOCP Thread"
        
        
class IOCPComm(object):
        
        def __init__(self, config):
            self.active = int(config['active'])
            self.ip = config['ip']
            self.port = int(config['port'])
            
        
            self.client = IOCP_Client_c(self.ip, self.port)
            if self.active: 
                self.client.start()
                
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