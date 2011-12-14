#!/usr/bin/env python
import socket, time, struct

#Sample code on how a client would connect to a Glass Server
def decode_data(buffer):
        #Decode the data
        #Look for VD
        print "DD - %r" %buffer
        if buffer[:2] == 'VD':
            #Get overall length
            length = struct.unpack("H", buffer[2:4])[0]
            data = buffer[4:4+length]
            process_VD(data)
        #self.input_buffer = '' #Temporary	
    
def process_VD(data):
    print "PROCESS VD %r" %data
    while len(data)>0:
                     
        #Get ID
        addr = struct.unpack("H", data[:2])[0]
        print "  ADDR 0x%x" %addr
        
        #In this example we are only decoding floats. 
        #You need to know what type each variable is int, float,
        #  so you can determine the length of the data, and to decode is correctly.
        # Again this is little endian.
        length = 4 #
        value_bytes = data[2:2+length]
        #var.setvalue(value_bytes)
        value = struct.unpack("f", value_bytes)[0]
        print value
        data = data[2+length:]
        #print "  DATA %r" % data
def form_data(command, data):
        l = len(data)
        a = command + struct.pack("H", l) + data
        print "%r" %a
        return a
        
def AVtest():
    a = "AV" + struct.pack("H", 4) + struct.pack("H",0x0441) + struct.pack("H",0x0440)
    time.sleep(1)
    sock.send(a)
    time.sleep(1)
    #Now sit in loop receiveing data
#    h=sock.recv(1024)
#    decode_data(h)
    #SVtest()
    
#    for i in range(20):
#        h=sock.recv(1024)
#        decode_data(h)
        
def SVtest():
    time.sleep(1)
    data = struct.pack("H", 0x0A00) + struct.pack("i", 12345)
    sock.send(form_data("SV", data))
    time.sleep(5)
    
def SEtest():
    time.sleep(1)
    data = struct.pack("H", 0xA100) + struct.pack("i", 2)
    sock.send(form_data("SE", data))
    time.sleep(5)
    sock.send(form_data("SE", data))
    time.sleep(5)
    
def IAS_bug_test():
    time.sleep(1)
    data = struct.pack("H", 0xA104) + struct.pack("i", 102)
    sock.send(form_data("SE", data))
    time.sleep(5)
    sock.send(form_data("SE", data))
    time.sleep(5)

def SendName(name):
    time.sleep(0.5)
    sock.send(form_data("SN", name))
    time.sleep(0.5)
    
def NAV_COM_test():
    time.sleep(1)
    #list = [[0xA600, 123.45],[0xA601, 120.75],[0XA602, 122.8],[0xA603, 120.0] \
    #,[0XA604, 110.0],[0XA605, 111.35],[0XA606, 113.00],[0XA607, 108.6]]
    #list = [[0xA600, 120.0],[0xA601, 121.8],[0XA602, 122.5],[0xA603, 123.15] \
    #,[0XA604, 111.1],[0XA605, 111.20],[0XA606, 111.25],[0XA607, 111.3]]
    list = [[0x420, 110.0],[0x421, 108.6],[0x430, 113.1],[0x431, 114.2] \
    ,[0x400, 128.375],[0x401, 123.4],[0x410, 125.9],[0x411, 132.35],[0x440, 305.5] \
    ,[0x441,1042.0]]
    
    #list = [[0xA604, 110.8],[0xA605, 109.9]]
    for i in range(10):
        
        for i in list:
            if i[0] == 0x940: #Transponder
                data = struct.pack("H", i[0]) + struct.pack("i", i[1])
                i[1]+=1111
            else:
                data = struct.pack("H", i[0]) + struct.pack("f", i[1])
                i[1]+= .025
            sock.send(form_data("SV", data))
            
        
        print "%r" %sock.recv(1024)    
        #list[0][1] += 1.05
        time.sleep(1.51)
    #sock.send(form_data("SE", data))
    time.sleep(5)    
    
#Make connection
HOST = '127.0.0.1'
PORT = 32276
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))
#After connection send list of variables you want to follow.
#Uses little endian for all numbers.
#Format --  AV length var1 var2 var3 
#length (2bytes) is the length of the message after that length bytes
#var1 (2bytes) is the addr of variable 1
#var2 (2bytes) is the addr of variable 2
#var3 (2bytes) is the addr of variable 3
#length therefore in this case will be 6. 2+2+2
#SVtest()
SendName("Co-Pilot PFD")
AVtest()
#SEtest()
#IAS_bug_test()
NAV_COM_test()
#sock.send("TEST123")
time.sleep(4)
print "Client Test Closing"
sock.close()