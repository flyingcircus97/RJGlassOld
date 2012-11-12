#config.py 
# Config file for PyGlass
from configobj import ConfigObj
#This imported by PyGlass via  import config
#
#CONSTANTS
TEST = 1 #run test routine (will not recieve any data from Flight Sim program)
FSXSP0 = 2 #Recieve data from test routine
FSXSP1 = 3
FSXSP2 = 4
ESP = 5
CLIENT = 6
modes = {'Test':1,'FSXSP0':2,'FSXSP1':3,'FSXSP2':4,'ESP':5,'XPLANE':6}
modes_list = ['Test','FSXSP0','FSXSP1','FSXSP2','ESP','XPLANE']

class general_c(object):
    def __init__(self, filename):
        self.config = ConfigObj(filename)
        self.glassserver_port = int(self.config['GlassServer']['port'])
        self.webserver_port = int(self.config['WebServer']['port'])
        
        
#load connection config file.
class connection_c(object):
    def __init__(self, filename):
        self.config = ConfigObj(filename)
        self.active = None
        self.active_num = 0
        #See if any of the connections are set as deafult.
        if 'active' in self.config:
            self.set_active(self.config['active'])
            
    def set_active(self, num):
        key = 'connection' + str(num)#self.config['active']
        if key in self.config:
            self.active = self.config[key]
            self.active_num = num
            #self.mode = modes[self.active['mode']]
            #self.addr = self.active['IP']
            #self.port = self.active['port']
            self.config['active'] = num
            self.config.write()
        else:
            print "Connection Config - Active not found."
            
    def connection_data(self):
        #Return all the connection data in dictionary format for AJAX request.
        config_list = []
        for i in self.config.keys():
            if 'connection' in i:
                config_list.append(self.config[i])
        return self.active_num, config_list
    
    def num_connections(self):
        num = 0
        for i in self.config.keys():
            if 'connection' in i:
                conn_num = int(i.split('connection')[1])
                if conn_num > num: 
                    num = conn_num
        return num
    
    def save(self, index, name, mode, ip, port):
        key = 'connection' + str(index)
        if key in self.config:
            self.config[key]['name'] = name
            self.config[key]['mode'] = mode
            self.config[key]['IP'] = ip
            self.config[key]['port'] = port
            self.config.write()
            
    def new(self):
        #Create new connection config.
        self.selected = self.num_connections()+1
        key = 'connection' + str(self.selected)
        self.config[key] = {}
        self.config[key]['name'] = 'New'
        self.config[key]['mode'] = 'Test'
        self.config[key]['IP'] = ''
        self.config[key]['port'] = ''
        self.config.write()
        return str(self.selected)
    
    def delete(self, index): 
        #Delete index connection config.
        num = self.num_connections()
        
        if (index == num):
            key = 'connection' + str(index)
            del self.config[key]
        else:
            for i in range(index, num):
                key = 'connection' + str(i)
                key_next = 'connection' + str(i+1)
                self.config[key] = self.config[key_next]
                print key, ' = ', key_next
            key = 'connection' + str(index)
            del self.config[key_next]
            print 'delete ', key_next
        self.config.write()
        
        return str(0)
        
        
#Set Mode of program
# TEST = run test routine (will not recieve any data from Flight Sim program)
# FSXSP0 or FSXSP1 or FSXSP2 = Recieve data from FSX Using PySimConnect.py
#mode = ESP #Note: case sensitive
#mode = TEST
#mode = CLIENT
#mode = FSXSP2
#FSX Sim Connect (Config) See README on how to configure SimConnect.xml file.
#server_only if set to true, no guages will be drawn (no graphics)
# use this when running on the same computer as FSX.
server_only = False
#addr = '192.168.1.45'  #IP Address of computer running FSX.
#port = 1500
server_port = 39550
timeout = 5.0  #Number of seconds before Connection to FSX will timeout

connection = connection_c('connections.cfg')
general = general_c('config.cfg')