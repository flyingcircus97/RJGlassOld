#config.py 
# Config file for PyGlass Client
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
modes = {'Test':1,'FSXSP0':2,'FSXSP1':3,'FSXSP2':4,'ESP':5}
modes_list = ['Test','FSXSP0','FSXSP1','FSXSP2','ESP']

class general_c(object):
    def __init__(self, filename):
        self.config = ConfigObj(filename)
 #       self.glassserver_port = int(self.config['GlassServer']['port'])
 #       self.webserver_port = int(self.config['WebServer']['port'])
        
 



client = general_c('config.cfg')