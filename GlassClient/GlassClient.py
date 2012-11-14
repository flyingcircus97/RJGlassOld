#glassclient.py
#***********************************************
#Client program for RJGlass to display guages
#***********************************************
import time, sys
import logging

def init_log():
    level = logging.INFO
    if '-debug' in sys.argv:
        level = logging.DEBUG
    logging.basicConfig(level=level, format='%(asctime)s.%(msecs)d %(levelname)s:%(message)s', datefmt='%H:%M:%S')
    #Set up File log
    logger = logging.getLogger()
    handler = logging.FileHandler('GlassClient.log', mode='w')
    #handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(asctime)s.%(msecs)d %(levelname)s:%(message)s', '%H:%M:%S'))
    logger.addHandler(handler)

#Initalize logging
init_log()
#Finish Imports
import display
import pyglet
import gauge
import client

#Start GlassClient program
display = display.display_c('view.xml')
c = client.client_c()

pyglet.app.run()

#Stop Client
c.stop()