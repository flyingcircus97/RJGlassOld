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
    
    def string256(self, s): #Takes a string and returns it padded to 256
        return s.ljust(256, chr(0))
    
    def __init__(self):
        self.clock = time.time()
        self.count = 0
        self.kill_timer = 0
        threading.Thread.__init__(self) 
        self.read_buffer = ''
        self.packet_data = []
        self.go = True
        
        
    def send(self, data):
        #Send the data, will add header, type is type of command
        self.count += 1 #just a incramental counter
        out = 'Arn.' + data
        print "Send: ", out
        out += '\r\n'
        #Send data to socket
        self.s.send(out)
        
    
        
    def connect(self, addr, port):
    #Attempts to connect to FSX.
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(5.0)
        succeed = False
        try:
            self.s.connect((addr, port))
        
        #Send connection header
            self.send('TipoSer:GlassServer:')
            self.send('Inicio:5:')
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
        if self.recieve: #Kill Thread
            self.go = False
        else:
            self.close() #No thread to kill, just close socket.
        
    def run(self):
        
        def reset_timer():
            #used to reset the kill timer.
            #Called from RJGlass to reset timer, if timer isn't reset then thread will die.
            self.kill_timer = 0
        def decode_header(s):
                #Decode 1st 12 bytes for the header
                #out[0] length of packet out[1] protocol out[2] type of recieve packet
                t = s[:HEADER_len]
                #print "%r" %t
                out = struct.unpack('<III', t)
                #print "Decode Header", out
                return out    
            
        def decode_data(length, packet_type):
            #Used to look for and read anydata that is coming in.
            #Take data from buffer minus header
            data = self.read_buffer[12:length]
            self.read_buffer = self.read_buffer[length:]
            #print "%r" %data
            self.packet_data.append([packet_type, data]) 
            #print "PD", self.packet_data
            return len(self.packet_data)
        
            #print self.packet_data
        #Begin self.receive()
        self.go = True
        print "Py SIMCONNECT SERVER STARTING"
        while self.go:
        #print time.time()-self.clock
            #print self.app_name, "RECIEVE"
            
            try:
                r = self.s.recv(1024)
            except socket.timeout:
                r = ''
                if self.go:
                    print "SERVER TIMED OUT (Will ReTry)"
                    self.go = False
            except: #Unknown error so shutdown server.
                r = ''
                self.go = False
        
         
            self.read_buffer = r
            print "Recived Bytes", len(r)
            print "%r" %r
        #End of while self.go
        #self.s.close()
        #print "Closing Socket"
        
    
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