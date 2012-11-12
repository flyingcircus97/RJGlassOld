import config
import SocketServer, socket
import threading, time, struct

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
        self.name = "Undefined"
    
    def getsend(self): #Checks and returns any data that needs to be sent.
        response = []
        #Check for varible changes to send
        var_change = self.var_watch.check()
        
        if len(var_change)>0:
            r = ''
            desc = 'Var Change:'
            for v in var_change:
                r+= struct.pack("H", v.addr) + struct.pack(v.var.pack_format, v.var.data.value)
                s_value = str(v.var.data.value)
                format = "%" + v.var.format_s
                value = format %v.var.data.value
                desc+= '0x%04X' %v.addr + '=' + value + ','
            response.append(['VD',r, desc]) #Response is command_id, then data
            
        return response
        

        
    def AddVariable(self, addr):  #This adds a variable to watch
        self.var_watch.add(addr)
    
    def SetVariable(self, addr, value):
        #Set the value of the variable
        self.variables.set(addr,value)
        
    def SetName(self, name):
        #Set the name of the connection. (i.e. Co-Pilot PFD, RTU, etc.)
        self.name = name
    

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    
    #def __init__(self, request, client_address, server):
#        print "MICHAEL", request, client_address, server
    #    SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        
    #    return
    
    def log_comm(self, dir, command_byte, command_data, desc):
        #Keeps log of last 50 transmissions in both direction for each connection.
        command_data_s = ""
        for byte in command_data:
            command_data_s += "%02X " %ord(byte)
        time_stamp = "%7.2f" %(time.time() - self.start_time)
        self.log.insert(0,[dir,time_stamp,command_byte,command_data_s, desc, ])
        if len(self.log) > 50:
            self.log.pop()
            
            
    #def __init__(self, aircraft):
    #    self.aircraft = aircraft
    #    print aircraft
    def setup(self):
        self.connection = GlassConnection(self.server.variables)
        self.TX_bytes = 0
        self.RX_bytes = 0
        self.start_time = time.time()
        self.log = []
        connections.add(self)
        self.commands = ["AV","SV","SE","SN"]
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
        desc = "UNKNOWN"
        
        if command_byte == "AV":
            desc = "Add Variables to Watch "
            for i in range(0,data_len, 2): #Decode addr every 2 char.
                addr = struct.unpack("H",command_data[i:i+2])[0]
                self.connection.AddVariable(addr)
                desc += " %04X" %addr
        elif command_byte == "SN":
            self.connection.SetName(command_data)
            desc = "Set Connection Name to %s" %command_data
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
                    format = "%" + var.format_s
                    value = format %v
                    desc = "Set Variable 0x%04X %s to " %(addr,var.name) + value
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
            
        self.log_comm('TX', command_byte, command_data, desc)
    
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
            self.add_to_send([['PI','','Ping from Server']])
            
        #Try to recieve data
        try:
            data = self.request.recv(1024)
            #print "DATA %r" %data
            self.RX_bytes += len(data)
            self.recv_buffer += data
        except socket.error, e:
            if e[0]==11 or e[0]==10035: #Standard error if no data to receieve
                pass 
            else: #Something is wrong True Error occured
                print "Error", e
                self.go = False #Quit connection

    def add_to_send(self, response):
        #Takes data to send in list form
        for id, data, desc in response: #Cycle through all data that needs to be sent.
            length = len(data)
            send_s = id + struct.pack("H",length) + data
            self.send_buffer += send_s
            self.TX_bytes += len(send_s)
            self.log_comm('RX', id, data, desc)
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
        #self.request.send('bye ' + str(self.client_address) + '\n')
        del(self)


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
    
    def __init__(self, variables, port):
    
        self.port = port
        self.server = ThreadedTCPServer(('localhost', self.port), ThreadedTCPRequestHandler, variables)
    
        print self.server.server_address
        self.go = True
        server_thread = threading.Thread(target=self.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.setDaemon(True)
        server_thread.start()
    
        print "Glass Server running in thread:", server_thread.getName()

    def serve_forever(self):
        self.server.timeout = 3.0
        while self.go:
            self.server.handle_request()
                        
    def shutdown(self):
        #self.server.shutdown()
        self.go = False


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

class Glass_Connections_c(object):
    def __init__(self):
        self.list = {}
        self.count = 0

    def add(self, connection):
        self.list[self.count] =  connection
        self.count += 1
             
        
    def AJAX_list(self):
        out = []
        for key in self.list:
            conn = self.list[key]
            out.append([conn.go, key, conn.connection.name, conn.client_address[0], conn.client_address[1], conn.TX_bytes, conn.RX_bytes])
        return out
    
    def AJAX_log(self, index):
        if index in self.list.keys():
            
            return self.list[index].log
        else:
            return [["Key not found", "YO"]]
        
    
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
        #create var file
        self.variables.create_var_file('variables/var.txt')
        #self.tests = test.Test_c(variable.variables)
        import gstest
        self.gstest = gstest
    
    def setup_FSComm(self, variables):
        import FlightSim.comm
        #Load module data
        FlightSim.comm.FS_Comm.load_mod_data(self.mod_data)
        self.FS_Comm = FlightSim.comm.FS_Comm
        self.FS_Comm.setup_sim(config.connection.active)
    
    def __init__(self):
        print "CONTROLLER INIT"
        self.setup_Modules()
        self.setup_FSComm(self.variables)        
        self.init_server()
        
    def init_server(self):
        self.Glass_Server = Glass_Server_c(self.variables, config.general.glassserver_port)
        print "SERVER is RUNNING"
    
    def comp(self):
        #print "COMP"
        self.mod_data.comp()
        self.gstest.run_test()
            
    def quit(self):
        print "Controller Quit"
        self.FS_Comm.quit()
        self.Glass_Server.shutdown()
        
controller = Glass_Controller_c()                      
connections = Glass_Connections_c()
