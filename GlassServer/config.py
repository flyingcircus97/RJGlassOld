#config.py 
# Config file for PyGlass
#
#This imported by PyGlass via  import config
#
#CONSTANTS
TEST = 1 #run test routine (will not recieve any data from Flight Sim program)
FSXSP0 = 2 #Recieve data from test routine
FSXSP1 = 3
FSXSP2 = 4
ESP = 5
CLIENT = 6
#Flight Director Constant type
Vshape = 0
LINES = 1


#Set Mode of program
# TEST = run test routine (will not recieve any data from Flight Sim program)
# FSXSP0 or FSXSP1 or FSXSP2 = Recieve data from FSX Using PySimConnect.py
#mode = ESP #Note: case sensitive
#mode = TEST
#mode = CLIENT
#mode = FSXSP2
mode = ESP
#FSX Sim Connect (Config) See README on how to configure SimConnect.xml file.
#server_only if set to true, no guages will be drawn (no graphics)
# use this when running on the same computer as FSX.
server_only = False
addr = '192.168.1.43'  #IP Address of computer running FSX.
port = 1500
server_port = 39547
timeout = 5.0  #Number of seconds before Connection to FSX will timeout
