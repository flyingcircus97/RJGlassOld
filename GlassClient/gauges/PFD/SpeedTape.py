#Speed Tape Gauge

import pyglet
from pyglet.gl import *
from gauge import gauge_parent
import common
import variable
import math, time
import text


class gauge_c(gauge_parent):
    
    def __init__(self, *args, **kwds):
        
        super(gauge_c, self).__init__(*args, **kwds)
        
        self.x = 90
        self.y = 300
        self.set_native_size(self.x, self.y)
        
        self.earth = (0.69, 0.4, 0.0) #The ground color on attitude indicator
        self.sky = (0.0, 0.6, 0.8) 
        self.pixel_per_degree = 7.5
        
        self.load_batch()
        
        #Init Constants
        self.knot_unit = 3.5 #Number of units per knot
        self.knot_text = ['%3d' %(i*10) for i in range(0,56,2)]
        
        #Init Variables
        self.IAS = variable.variables.load(0x100)
        self.a = 0.0
        
        
    def load_batch(self):
        self.arrow_shape = self.center_arrow_b()
        self.top_black_shape = self.black_blocks_b(True)
        self.bottom_black_shape = self.black_blocks_b(False)
    
    def black_blocks_b(self, top):
        #Black blocks on top and bottom of speed tape. To hide numbers that spill over.
        # -- Used insted of scissoring.
        
            x1 = -45
            x2 = 10
            y1 = 150
            y2 = 200
            if top:
                y1=-y1
                y2=-y2
            v1 = common.vertex.lines()
            v1.add([x1,y1,-x1,y1,-x1,y2,x1,y2])
            batch = pyglet.graphics.Batch()
            b1 = batch.add(v1.num_points, GL_POLYGON, None, ('v2f', v1.points),('c3f',common.color.black*v1.num_points))
         
            return batch
            
    def center_arrow_b(self):
            
            #Center White Arrow 
            y = 0 #self.y_center
            w = 18.0
            h = 10.0
            point = 0.0 #Point of arrow's X cord
            
            v1 = common.vertex.lines()
            v1.add([point,y])
            v1.add([point+w, y-h])
            v1.add([point+w, y+h])
            v1.add([point,y])
            
            v2 = common.vertex.lines()
            v2.add([point+w,y])
            v2.add([point+w + 12.0, y])
            
            batch = pyglet.graphics.Batch()
            b1 = batch.add(v1.num_points, GL_LINES, None, ('v2f', v1.points),('c3f',common.color.white*v1.num_points))
            b2 = batch.add(v2.num_points, GL_LINES, None, ('v2f', v2.points),('c3f',common.color.white*v2.num_points))
        
            return batch
    
    def tick_marks(self, x=0, y=0):

            #Draw the tick mark

            unit_apart = self.knot_unit
            center = 0.0
            y_center = 0
            #air_spd is class of speed, will use IAS, Mach, and V Speeds, possibly Ground Speed
            airspeed = self.indicated_IAS()
            self.a+=0.1
            #airspeed = self.a
            
            glColor3f(1.0, 1.0, 1.0) #White
            #glLineWidth(2.0)
            start_tick_ten = (int(airspeed) / 10) - 4
            tick_ten = start_tick_ten
            start_loc = y_center - ((airspeed - (tick_ten * 10)) * unit_apart)
            loc = start_loc
            glBegin(GL_LINES)
            vert_line_bottom = -150
            for i in range(10):
            #Tick itself
                if tick_ten == 4:
                    vert_line_bottom = loc
                if tick_ten >=4: #This causes nothing below 40 to be displyed
                    glVertex2f(center - 10.0, loc)
                    glVertex2f(center, loc)
                    if tick_ten <20: #If its under 200 knots add a 5 knot mork
                        mid_loc = loc + (unit_apart * 5) # This is equivelent of 5 knots higher
                        glVertex2f(center - 5.0, mid_loc)
                        glVertex2f(center, mid_loc)
                tick_ten = tick_ten +1
                loc = loc + (unit_apart * 10)	
            #Draw verticle Line of airspeed tape
            glVertex2f(center, vert_line_bottom)
            glVertex2f(center, 150.0)
            glEnd()
    
            return start_loc, start_tick_ten
        
    def tick_numbers(self, start_loc, start_tick_ten):    
            loc = start_loc
            tick_ten = start_tick_ten
            unit_apart = self.knot_unit
#            glLineWidth(2.0)
            for i in range(10):
            # Put in numbers
                if (tick_ten >=4) & (tick_ten % 2 == 0): #Must be multiple of 20 and above 0 knots
                #Print out number print
                    glPushMatrix()
                    #if tick_ten >=10:
                    #    glTranslatef(8.0, loc - 6.0, 0.0)
                    #    glScalef(0.13,0.13,1) #Scale text, also done in else statement below.
                        #c = (tick_ten / 10) + 48
                        #glutStrokeCharacter(GLUT_STROKE_ROMAN, c)
                    #    text.write(self.knot_text[tick_ten/2])
                    #else:
                    #    glTranslatef(18.0, loc - 6.0, 0.0) #Move over since no hundreds digit
                    #    glScalef(0.13,0.13,1) #Don't forget to scale text
                    #c = (tick_ten % 10) + 48
                    #glutStrokeCharacter(GLUT_STROKE_ROMAN, c) #Tens digit
                    #glutStrokeCharacter(GLUT_STROKE_ROMAN, 48) # Ones Digit
                    glTranslatef(-40.0, loc, 0.0)
                    glScalef(0.13,0.13,1.0)
                    text.write(self.knot_text[tick_ten/2])
                    glPopMatrix()
                elif (tick_ten == 3): #Put in V Speed Text
                    #self.V_Speeds(air_spd, loc - 12.0)
                    pass
                tick_ten = tick_ten +1
                loc = loc + (unit_apart * 10)
                
    def indicated_IAS(self):
        indicated = self.a
        if indicated <40: indicated =40
        elif indicated > 500: indicated = 500
        
        return indicated
    
    def draw(self):
        #self.glLineWidth(2.0)
        #Limit Airspeed
        glLineWidth(2.0)
        self.arrow_shape.draw()
        start_loc, start_tick_ten = self.tick_marks()
        self.tick_numbers(start_loc, start_tick_ten)    
        self.top_black_shape.draw()
        self.bottom_black_shape.draw()
        