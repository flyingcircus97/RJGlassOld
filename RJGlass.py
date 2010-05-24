#!/usr/bin/env python
# ----------------------------------------------------------
# RJGlass Main Program  version 0.2 8/1/07
# ----------------------------------------------------------
# Copyright 2007 Michael LaBrie
#
#    This file is part of RJGlass.
#
#    RJGlass is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.

#   RJGlass is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ---------------------------------------------------------------
import sys, os, time

#Load the modules needed for RJGlass.
	
	
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

#pygame needed for sound in server_only (so load either way)
import pygame
from pygame.locals import *
from pygame import image
	
from guage import * #All add on guage functions colors etc. 

#This is code to import config file (config.py)
try:
	import config
except ImportError:
	# We're in a py2exe, so we'll append an element to the (one element) 
	# sys.path which points to Library.zip, to the directory that contains 
	# Library.zip, allowing us to import config.py
	# Adds one level up from the Library.zip directory to the path, so import will go forward
	sys.path.append(os.path.split(sys.path[0])[0])
	import config


class screen_c(object):
	#This controls what is in each screen.
	def __init__(self, x, guage_list=[]):
		self.guage_list = [] #list of guages to cycle through.
		self.guage_index = 0
		self.x = x
		self.y = 0
		self.width = 512
		self.heigth = 768
		self.add_guage_list(guage_list)
		
	def add_guage_list(self,glist):
		for g in glist:
			self.append_guage(guage_dict[g])
		
	def append_guage(self,guage):
		self.guage_list.append(guage)
		
	def cycle(self):
		self.guage_index +=1
		if self.guage_index >= len(self.guage_list):
			self.guage_index =0
			
	def cycle_reverse(self):
		self.guage_index -=1
		if self.guage_index <0:
			self.guage_index = len(self.guage_list) -1
			
	def active_guage(self):
		return self.guage_list[self.guage_index]			
	
	#this is a static function not specificaly for the screen.
	#the eventhandlers have references to the screens so it is easier to
	#get the guage references by name through this object.
	def gauge_by_name(self,name):
		return guage_dict[name]
			
	def draw(self, aircraft):
		self.guage_active = self.guage_list[self.guage_index]
		self.guage_active.draw(aircraft, self.x, self.y)


def InitPyGame():
	glutInit(())
	pygame.init()
	if config.full_screen:
		s = pygame.display.set_mode((1024,768), DOUBLEBUF|OPENGL|FULLSCREEN)
	else:
		s = pygame.display.set_mode((1024,768), DOUBLEBUF|OPENGL)
	return s
		
def InitView(smooth, width, heigth):
	global x_s, y_s, scissor
	
	glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) 
	glLoadIdentity()
	glOrtho(0,width,0.0,heigth,-1.0,1.0)
	
	x_s = width/1024.0
	y_s = heigth/768.0

	glScalef(x_s, y_s, 1.0)
	scissor.x_s = x_s
	scissor.y_s = y_s
	if smooth:
		#Enable Smoothing Antianalising
		glEnable(GL_LINE_SMOOTH)
		glEnable(GL_BLEND)
		#glBlendFunc(GL_SRC_ALPHA, GL_ZERO)
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
		glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
		#glDisable(GL_DEPTH_TEST)
	#Clear Screen
	#glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
	
	
def DisplaySplash(filename, delay, window_x, window_y):
	#Display needs to be initialized first.
	i = image.load(filename)
	splash_image = bitmap_image(i)
	#Determine the x and y coords to put in center of screen.
	splash_x = (window_x / 2) - (splash_image.w/2)
	splash_y = (window_y /2) - (splash_image.h/2)
	glRasterPos3f(splash_x,splash_y,0)
	glDrawPixels(splash_image.w, splash_image.h, GL_RGBA, GL_UNSIGNED_BYTE, splash_image.tostring)
	pygame.display.flip()
	time.sleep(delay)
	

	

def DrawWindow(left_screen, right_screen):
	
	def divider(): #Dividing vertical white line between instruments
		glColor(white)
		glLineWidth(2.0)
		glBegin(GL_LINES)
		glVertex2f(512.0, 0.0)
		glVertex2f(512.0, 768.0)
		glEnd()
		
	def draw_nodata(x,y): #Draw no data text on screen.
		glColor(red)
		glLineWidth(5.0)
		glPushMatrix()
		glTranslatef(x,y,0)
		glScalef(0.4,0.4,1.0)
		glText("NO SIM DATA", 100)
		glPopMatrix()
		
	global count
	divider()
	#PFD.draw(aircraft_data,250,445)
	left_screen.draw(aircraft_data)
	#ND.draw(aircraft_data,512+256, 400)
	#FMS.draw(aircraft_data,512+256, 0)
	right_screen.draw(aircraft_data)
	glDisable(GL_SCISSOR_TEST) #Disable any scissoring.
	draw_FPS(20,740, aircraft_data.frame_time)
	#If Nodata is coming from Flight Sim, show on screen
	if aircraft_data.nodata:
		draw_nodata(50,500)
	
	
	count = count +1 #Used for FPS calc
	
def MainLoop(mode, server_only):
	#global window
	global starttime
	global count
	global mode_func, left_screen, right_screen, eventhandler
	# Start Event Processing Engine	
	starttime = time.time() # Used for FPS (Frame Per Second) Calculation
	
	if (server_only):
		#Set up correct function for selected mode
		mode_func = aircraft_data.get_mode_func(mode)
	else:	
		left_screen = screen_c(256,config.left_screen)
		right_screen = screen_c(512+256,config.right_screen)
	#	left_screen.add_guage_list(config.left_screen)
	#	right_screen.add_guage_list(config.right_screen)
		#Set up correct function for selected mode
		mode_func = aircraft_data.get_mode_func(mode, left_screen, right_screen)
	
	#Setup Keyboard
	#keys.setup_lists(aircraft_data)
	#Inititalize View
	#left_screen = screen_c(256, [PFD, ND, FMS])
	
		eventhandler = event_handler.event_handler_c(aircraft_data,FMS, right_screen, left_screen)
	
		#Load textures, and guages that use them
		FMS.load_texture()
		EICAS1.load_texture()
		EICAS2.load_texture()
		RADIO.load_texture()
	
	if server_only:
		server_loop()
	else:
		graphic_loop()

def graphic_loop():
	#This is the loop for the non server mode. Gauges drawn.
	while not (aircraft_data.quit_flag):
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #Clear Screen	
		#Update globaltime
		aircraft_data.globaltime = time.time()
		globaltime.update(time.time())
		DrawWindow(left_screen, right_screen)
		pygame.display.flip() #Update screen
		mode_func() #Run aircraft mode function, to do all teh calaculations etc.
		
		# Check for keypresses
		eventhandler.check_events(pygame.event.get(), globaltime.value)		
def server_loop():
	#This is the loop for the server only mode. No Guages Drawn
	while not (aircraft_data.quit_flag):
		#Update globaltime
		aircraft_data.globaltime = time.time()
		globaltime.update(time.time())
		mode_func() #Run aircraft mode function, to do all teh calaculations etc.
		time.sleep(0.01) #Throw in some time delay, since no guages are being drawn.
		
		# Check for keypresses
		#eventhandler.check_events(pygame.event.get(), globaltime.value)		
	
	


def Init_Graphics(x,y):
	InitPyGame()
	InitView(True, x,y)
	
def Initialize(server_only):
	#if server_only True then server will just be run, No Graphics
	#Initialize count for FPS calc
	global count
	count = 0
	if (not server_only):
		Init_Graphics(config.window_x, config.window_y)
		#Draw Splash Screen
		if config.splash:
			DisplaySplash(config.splash_filename, config.splash_delay, config.window_x, config.window_y)


	
	
def ShutDown(mode, server_only):
	#Close LogFile
	datafile.close()
	#Close pygame mixer
	pygame.mixer.quit()
	#Print average Frames per second on shutdown
	print "FPS ", count / (time.time() - starttime)
	#Try to kill the thread if it exists. Closes it down on exit				
	aircraft_data.AP.quit() #only here to close debugging files if present.
	if ((mode != config.TEST) & (mode != config.CLIENT)): #If simconnected connected, kill the thread.
		aircraft_data.kill_SimConnect()

def CheckArg(arg, mode, server_only, addr):
	if 'server' in arg:
		server_only = True
	elif 'guage' in arg:	
		server_only = False
		
	if 'client' in arg:
		mode = config.CLIENT
	elif 'test' in arg:
		mode = config.TEST
	
	for a in arg:
		if 'addr' in a:
			addr = a.split('=')[1]
				
	return mode, server_only, addr
	

#===========================================================================
#Main program starts here
#===========================================================================
#Check arguments first, and get mode and server_only flags
mode, server_only, addr = CheckArg(sys.argv, config.mode, config.server_only, config.addr)
#config.addr = addr
#print addr
Initialize(server_only)
#Import guage files.
import aircraft #Does all of the aircraft_data
import event_handler #Handles all keyboard commands
import variable
	
if (not server_only):
	import PFD_mod
	import ND_mod
	import EICAS1_mod
	import EICAS2_mod
	import FMS_guage
	import radio_mod

#Create Guages

aircraft_data = aircraft.data()
variables = variable.variable_c(aircraft_data)

if (not server_only):
	PFD = PFD_mod.PFD_Guage()
	ND = ND_mod.ND_Guage()
	FMS = FMS_guage.FMS_guage_c()
	EICAS1 = EICAS1_mod.EICAS1_guage()
	EICAS2 = EICAS2_mod.EICAS2_guage()
	ND.initialize(aircraft_data)
	RADIO = radio_mod.radio_guage()
	
	guage_dict= { "RADIO":RADIO,"PFD":PFD,"ND":ND,"FMS":FMS,
		"EICAS1":EICAS1,"EICAS2":EICAS2 }
		

print "Main Loop"
#Run main, and get window size and operation mode from config file. config.py
MainLoop(mode, server_only)
#===================
# Shuting Down
#===================
ShutDown(mode, server_only)	
