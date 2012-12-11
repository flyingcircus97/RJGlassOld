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


class myEventLoop(pyglet.app.EventLoop):

    def __init__(self):
        super(myEventLoop, self).__init__()
        self.FPS_clock = pyglet.clock.Clock()
        self.fps_display = pyglet.clock.ClockDisplay(clock=self.FPS_clock)
        
    def idle(self):
        t = time.time()
        pyglet.clock.tick(poll=True)
#        display.win.dispatch_event('on_draw')
#        display.win.flip()
   #     #print "IDLE"
   #     #print pyglet.clock.get_sleep_time(sleep_idle=True)
        #time.sleep(0.01)
        #print time.time()-t
        #time.sleep((1/30.0)-t)
        return pyglet.clock.get_sleep_time(sleep_idle=True)
        
    def myDraw(self, dt):
        self.FPS_clock.tick(poll=True)
        display.win.dispatch_event('on_draw')
        #Draw FPS Display
        self.fps_display.draw()
        display.win.flip()



def myDraw(dt):
    #if c.VD_recv:
    #   c.VD_recv = False
    #display.myDraw(dt)
    pass
    #print rx_count
    #print c.rx_count
        
event_loop = myEventLoop()
#Start GlassClient program
c = client.client_c()
display = display.display_c('view.xml')

c.start()
pyglet.clock.schedule_interval(event_loop.myDraw, 1/30.0)
#pyglet.app.run()
#pyglet.clock.schedule_interval(myDraw, 1.0/60.0)
event_loop.run()

#Stop Client
c.stop()