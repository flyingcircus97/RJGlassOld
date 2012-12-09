import time, struct, socket
import logging

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
                self.lastRXtime = time.time() 

                length = struct.unpack("H", data[2:4])[0]
                #Check if buffer is long enough for all data.
                if buffer_length >= length + 4: 
                    #Parse data
                    command_data = data[4:length+4]
                    #print "Command %r %r" %(command_id, command_data)
                    self.process_data(command_id, command_data)
                    #Delete from recv buffer all data before end point
                    self.recv_buffer = data = data[length+4:]
                    #print "AFTER %r -- %r" %(self.recv_buffer, data)
                    if len(data) > 0: #If more data then check next data
                        go = True
                    #print self.recv_buffer, i_start, i_end
            else:
                logging.warning("GlassProtocol: Command %s Not Valid" ,command_id)
                self.recv_buffer = ''
                
                
def sendrecv(self, conn):
        #Send and recieve data
        time.sleep(0.01)
        temp_time = time.time()
        
        #Send data if available
        if len(self.send_buffer)>=1:
            conn.send(self.send_buffer)
            logging.debug("GlassProtocol: Sending %r" ,self.send_buffer)
            self.send_buffer = '' #Clear buffer after it has been sent.
            self.time_lastTX = temp_time
        elif temp_time - self.time_lastTX > 3:
            self.add_to_send([['PI','','Ping from Server']])
            
        #Try to recieve data
        try:
            data = conn.recv(1024)
            #print "DATA %r" %data
            self.RX_bytes += len(data)
            self.recv_buffer += data
        except socket.error, e:
            if e[0]==11 or e[0]==10035: #Standard error if no data to receieve
                #print "Not Blocking"
                pass
            else: #Something is wrong True Error occured
                logging.warning("GlassProtocol: Socket Error %r", e)
                self.go = False #Quit connection
                
def initialize(self):
    self.send_buffer = ''
    self.recv_buffer = ''
    self.time_lastTX = 0
    self.RX_bytes = 0
    self.TX_bytes = 0
    
    
    