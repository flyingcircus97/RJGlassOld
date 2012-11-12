#glassclient.py
#***********************************************
#Client program for RJGlass to display guages
#***********************************************

import display, time
import pyglet
import gauge
import client
#from variable import variables_c

#variables = variables_c()

display = display.display_c('view.xml')
c = client.client_c()
#window = windows[0]


#g_window = gauge.window_c(display.display)




pyglet.app.run()

c.stop()