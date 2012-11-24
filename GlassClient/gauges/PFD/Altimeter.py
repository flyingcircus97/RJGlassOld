#Altimeter Gauge
# 
#


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
        
        
        self.load_batch()
        
        #Init Constants
        self.knot_unit = 3.5 #Number of units per knot
        self.knot_text = ['%3d' %(i*10) for i in range(0,56,2)]
        
        #Init Variables
        self.a = 1000
    
        
    def load_batch(self):
        self.smticks_shape = self.small_ticks_b()
        self.thousand_shape, self.fivehund_shape = self.thousand_lines_b()
        self.thousandodd_shape = self.thousand_ticks_b(1)
        self.thousandeven_shape = self.thousand_ticks_b(0)
        self.centerblack_shape = self.centerblack_b()
        
    
    def centerblack_b(self):
        x1 = 20
        x2 = 38
        black_l = -30.0
        black_h = 30.0
        vp = common.vertex.lines()
        vp.add([x1,black_l,x2,black_l,x2,black_h,x1,black_h,x1,black_l])
        
        batch = pyglet.graphics.Batch()
        b1 = batch.add(vp.num_points, GL_POLYGON, None, ('v2f', vp.points),('c3f',common.color.black*vp.num_points))
         
        return batch
            
    
    def small_ticks_b(self):
        
        vl = common.vertex.lines()
        loc = 0
        for i in range(28):
        #Tick itself
            vl.add([42.0,loc])
            vl.add([50.0,loc])
            vl.reset()
            loc = loc + 13.0	
        
        batch = pyglet.graphics.Batch()
        b1 = batch.add(vl.num_points, GL_LINES, None, ('v2f', vl.points),('c3f',common.color.white*vl.num_points))
         
        return batch
    
    def thousand_ticks_b(self, tick):
        vl = common.vertex.lines()
        loc = 0
        x2 = 37
        
        for i in range(5):
            #Tick itself
                if (tick % 2): #If odd then 500 foot mark make smaller, if even then make larger 1000 foot mark
                    x1 = 29
                else:
                    x1 = 21
       
                y1 = loc-3
                y2 = loc+3
                vl.add([x1, y1, x2, y1, x2, y2, x1,y2, x1,y1]) 
                vl.reset()
                tick = tick +1
                loc = loc + 65	
                
        batch = pyglet.graphics.Batch()
        b1 = batch.add(vl.num_points, GL_LINES, None, ('v2f', vl.points),('c3f',common.color.white*vl.num_points))
         
        return batch
    
    def thousand_lines_b(self):
        #1000' lines
        vl = common.vertex.lines()
        h = 16
        w = 42
        vl.add([0.0, h])
        vl.add([w, h])
        vl.reset()
        vl.add([0.0, -h])
        vl.add([w, -h])
        #500' lines
        v5 = common.vertex.lines()
        v5.add([0.0, h])
        v5.add([w/2, h])
        v5.reset()
        v5.add([0.0, -h])
        v5.add([w/2, -h])
        #White solid square
        vp = common.vertex.lines()
        x1 = -10
        x2 = -4
        y1 = -3
        y2 = 3
        vp.add([x1,y1,x2,y1,x2,y2,x1,y2,x1,y1])
        
        thousand_batch = pyglet.graphics.Batch()
        b1 = thousand_batch.add(vl.num_points, GL_LINES, None, ('v2f', vl.points),('c3f',common.color.white*vl.num_points))
        b2 = thousand_batch.add(vp.num_points, GL_POLYGON, None, ('v2f', vp.points),('c3f',common.color.white*vp.num_points)) 
        fivehund_batch = pyglet.graphics.Batch()
        b5 = fivehund_batch.add(v5.num_points, GL_LINES, None, ('v2f', v5.points),('c3f', common.color.white*v5.num_points))
        b2 = fivehund_batch.add(vp.num_points, GL_POLYGON, None, ('v2f', vp.points),('c3f',common.color.white*vp.num_points)) 
        return thousand_batch, fivehund_batch
        
        
    def tick_marks(self, altitude):
            
            def white_square():
                glLineWidth(2.0)
                glBegin(GL_POLYGON)
                glVertex2f(-10.0, -3)
                glVertex2f(-4.0, -3)
                glVertex2f(-4.0, 3)
                glVertex2f(-10.0, 3)
                glEnd()
            
            #Draw the tick mark
            #Every 20 ft is 13 units apart
            units_apart = 13.0
            y_center = 0.0
            #altitude = aircraft.altitude
            glColor3f(1.0, 1.0, 1.0)
            glLineWidth(2.0)
            start_tick_ten = (altitude / 20) - 13
            tick_ten = start_tick_ten
            start_loc = y_center - ((altitude - (tick_ten * 20)) * units_apart/ 20)
            #Small ticks
            loc = start_loc
            glPushMatrix()
            glTranslatef(0,loc,0)
            self.smticks_shape.draw()
            glPopMatrix()
            
            loc = start_loc
            tick_ten = start_tick_ten
            glLineWidth(1.0)
            for i in range(28):
            # Put in numbers
                if (tick_ten >=-50) & (tick_ten % 5 == 0): #Must be multiple of 200 and above 0 feet
                #Print out number print
                    glPushMatrix()
                    temp = abs(tick_ten / 5 ) % 10
                    #if tick_ten<0: temp = 10 - temp
                    h = 16.0
                    if temp ==0: #Need to be lines above and below altitude
                        glPushMatrix()
                        glTranslatef(52.0, loc, 0.0)
                        self.thousand_shape.draw()
                        glPopMatrix()
                    elif temp ==5: #Need lines above and below 500' marks also
                        glPushMatrix()
                        glTranslatef(52.0, loc, 0.0)
                        self.fivehund_shape.draw()
                        glPopMatrix()
                        
                    glTranslatef(58.0, loc , 0.0)
                    glLineWidth(2.0)
                    glScalef(0.15,0.15,1) #Scale text, also done in else statement below.
                    
                    s = str(temp) + "00"
                    text.write(s)
                    glPopMatrix()

                tick_ten = tick_ten +1
                loc = loc + 13.0
                
    def thousand_tick_marks(self, altitude, y_center=0):
            alt = altitude % 1000 #Only need the hundreds feet part because it repeats
            #Draw the tick marks
            #Every 100 ft is 13 units apart
            units_apart = 0.13 #13.0 / 100
            
            #altitude = aircraft.altitude
            
            glLineWidth(2.0)
            tick = ((alt-250) / 500) - 1
            loc = y_center - ((alt - (tick * 500)) * units_apart) #Some how need to fit 5 in there.

            #Thousand ticks
            glPushMatrix()
            glTranslatef(0,loc,0)
            if (tick % 2):
                self.thousandodd_shape.draw()
            else:
                self.thousandeven_shape.draw()
            glPopMatrix()
            
            #Draw black plygon over area, therefore these ticks need to be done first, eaiser then doing multiple scissor boxes	
            self.centerblack_shape.draw()
            #common.color.set(common.color.purple)
            #glBegin(GL_POLYGON)
            #glVertex2f(20.0, black_l)
            #glVertex2f(38.0, black_l)
            #glVertex2f(38.0, black_h)
            #glVertex2f(20.0, black_h)
            #glEnd()
    
    def draw(self):
        #self.glLineWidth(2.0)
        glLineWidth(2.0)
        self.tick_marks(self.a)
        self.thousand_tick_marks(self.a)
        self.a = self.a + 1
        