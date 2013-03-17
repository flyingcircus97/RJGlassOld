#HSI
#-- Part of PFD
#

import pyglet
from pyglet.gl import *
from gauge import gauge_parent
import common
import variable
import math, time
import text



        
class gauge_c(gauge_parent):
    #HSI
     
    
    def __init__(self, *args, **kwds):
        
        super(gauge_c, self).__init__(*args, **kwds)
        
        self.x = 500
        self.y = 312
        self.set_native_size(self.x, self.y)
        
               
        self.load_batch()
        
        #Init Constants
        
        #Init Variables
        self.a = 0
        self.dt_count = 0
        self.prev_bug = 0
        #Init Sim Variables
        self.hdgmag = variable.variables.load(0x130,'4F')
        self.hdgbug = variable.variables.load(0x151)
        self.magtrack = variable.variables.load(0x132,'4F')
        
        self.hdgbug_timer = 5 #5 second delay to show hdg bug value and dashed line
      
        
        
    def comp(self, dt):
            self.dt_count += dt
            
            if self.prev_bug != self.hdgbug.value:
                self.dt_count = 0
                self.prev_bug = self.hdgbug.value
                
            
            
            
            
    def load_batch(self):
        self.plane_shape = self.plane_figure_b()
        self.ticks_shape = self.ticks_b()
        self.triangle_marks = self.marks_b()
        self.hdgbug_shape = self.hdgbug_b()
        self.hdgbugline_shape = [self.hdgbugline_b(6), self.hdgbugline_b(5)]
        self.bottom_polygon = self.bottom_b()
        self.mag_track_shape = self.mag_track_b()
        
    def bottom_b(self):
        #Bottom black polygon for scissoring
        w = 150
       
        y2 = (self.y/-2)
        y1 = y2 + 50
        
        v1 = common.vertex.lines()
        v1.add([-w,y1,w,y1,w,y2,-w,y2,-w,y1])
        
        batch = pyglet.graphics.Batch()
        b1 = batch.add(v1.num_points, GL_POLYGON, None, ('v2f', v1.points),('c3f',common.color.black*v1.num_points))
            
        return batch
            
        
            
        
    def marks_b(self):
        
            def triangle_l(radius, w, h, angle):
                def rot(xy, angle):
                    rad = math.radians(-angle)
                    s = math.sin(rad)
                    c = math.cos(rad)
                    return [xy[0]*c-xy[1]*s, xy[0]*s+xy[1]*c]
                #Radius traingle is away from center, width, heigth, rotation angle
                #Returns list of points for batch
                l = []
                l.extend(rot([0,radius], angle))
                l.extend(rot([w,radius+h], angle))
                l.extend(rot([w,radius+h], angle))
                l.extend(rot([-w,radius+h], angle))
                l.extend(rot([-w,radius+h], angle))
                l.extend(rot([0,radius], angle))
                
                return l
            
            radius = 150
            
            
            v1 = common.vertex.lines()
            v1.add(triangle_l(radius - 2, 9, 15,0.0))
            v1.reset()
            v1.add(triangle_l(radius , 5, 8, 45))
            v1.reset()
            v1.add(triangle_l(radius , 5, 8, -45))
            v1.reset()
            v1.add([radius-2, 0, radius+15, 0]) #Right line
            v1.reset()
            v1.add([-(radius-2), 0, -(radius+15), 0]) #Left line
            
            batch = pyglet.graphics.Batch()
            b1 = batch.add(v1.num_points, GL_LINES, None, ('v2f', v1.points),('c3f',common.color.white*v1.num_points))
            
            return batch
            
    def plane_figure_b(self):
        
            
            v1 = common.vertex.lines()
            #Fuesalage
            v1.add([0,12,0,-35])
            v1.reset()
            #Wing (Note: Wing is located slightly below center (3pixels))
            v1.add([-25,-1,25,-1])
            v1.reset()
            #Tail
            v1.add([-13,-28,13,-28])
            
            batch = pyglet.graphics.Batch()
            b1 = batch.add(v1.num_points, GL_LINES, None, ('v2f', v1.points),('c3f',common.color.white*v1.num_points))
         
            return batch
        
    def mag_track_b(self):
            v1 = common.vertex.lines()
            v1.add(common.draw.List_Circle(6,10))
            
            batch = pyglet.graphics.Batch()
            b1 = batch.add(v1.num_points, GL_LINES, None, ('v2f', v1.points),('c3f',common.color.green*v1.num_points))
            
            return batch
        
        
    def hdgbug_b(self):
        
                   
            v1 = common.vertex.lines()
            v1.add([0,0,10,8,10,15,0,15,0,-15,10,-15,10,-8,0,0])
            
            batch = pyglet.graphics.Batch()
            b1 = batch.add(v1.num_points, GL_LINES, None, ('v2f', v1.points),('c3f',common.color.purple*v1.num_points))
            
            return batch
    
    def hdgbugline_b(self, dashes):
            v1 = common.vertex.lines()
            #Calculate line dashes
            start = 15.0
            step = (145-start) / 12
            for i in range(dashes):
                v1.add([start, 0.0])
                start += step
                v1.add([start, 0.0])
                start += step
                v1.reset()
                        
            batch = pyglet.graphics.Batch()
            b1 = batch.add(v1.num_points, GL_LINES, None, ('v2f', v1.points),('c3f',common.color.purple*v1.num_points))
            
            return batch
    
        
    def ticks_b(self):
        
            radius = 145
            sm_tick = 15
            lg_tick = 20
            v1 = common.vertex.lines()
            deg = -130
            end_deg = deg*-1
            count = 0
            while deg <= end_deg:
                rad = math.radians(deg)
                sin = math.sin(rad)
                cos = math.cos(rad)
                v1.add([radius*sin, radius*cos])
                if count%2 == 0:
                    #Lg Tick
                    v1.add([(radius-lg_tick)*sin,(radius-lg_tick)*cos])
                else:
                    #Sm Tick
                    v1.add([(radius-sm_tick)*sin, (radius-sm_tick)*cos])
                v1.reset()
                deg +=5
                count +=1
            
            
            batch = pyglet.graphics.Batch()
            b1 = batch.add(v1.num_points, GL_LINES, None, ('v2f', v1.points),('c3f',common.color.white*v1.num_points))
         
            return batch
    
        
    def heading_ticks(self,radius, heading):
                
                def HSI_Text(i): #Returns text equivelent of tick mark
                    if i == 0:
                        return "N"
                    elif i== 9:
                        return "E"
                    elif i== 18:
                        return "S"
                    elif i== 27:
                        return "W"
                    else:
                        return str(i)
                    
                
                glPushMatrix()
                glRotatef(heading %10, 0.0, 0.0, 1.0)
                glLineWidth(2.0)
                common.color.set(common.color.white)
               
                self.ticks_shape.draw()
                #Draw Numbers / Letters
                #glRotatef(150,0,0,1) #Rotate -150 to start
                start = int(heading // 10)
                for i in range(0,36): #Draw tick ever 10 degrees
                    #Draw Number
                    if (start % 3) == 0: #Check to see if multiple of 3
                        glPushMatrix()
                        c = HSI_Text(start)
                        if len(c) == 2: #Two digits
                            glTranslatef(-6.0, 0.0, 0.0)
                        glTranslatef(-0.0, radius -30.0, 0.0)
                        glScalef(0.15, 0.15, 1.0)
                        text.write(HSI_Text(start))
                        glPopMatrix()
                    glRotatef(-10.0, 0.0, 0.0, 1.0) #Rotate 5 degrees
                    start = start + 1
                    if start == 36:start =0
                glPopMatrix()    
        
    def heading_bug(self, mag, bug):
            #radius = radius of guage, mag = mag heading of plane bug = heading bug value
            #draw_line True if you want purple line drawn from center to bug, (Used when bug's value is changed)
               
                def bug_text(x,y, bug):
                    glPushMatrix()
                    glTranslatef(x,y,0)
                    glScalef(0.15,0.15,1)
                    text.write("HDG %03d" %bug, 90)
                    glPopMatrix()
                
                common.color.set(common.color.purple)
                radius = 145
                diff = mag - bug
                if diff <0: diff+=360 #Make sure diff is between 0 and 360
                glPushMatrix()
                glRotatef(diff + 90, 0, 0, 1) #90 degree offset is since bug_polygon above is rotated
                #Check for 5 second delay
                if (self.hdgbug_timer <= self.dt_count): #Enable drawing of line
                    draw_line=False
                else:
                    draw_line=True
                
                draw_flag = (draw_line) or (120 < diff <240)
                #Draw dotted line from center to heading bug
                if draw_flag:
                    if (150 <diff < 210):
                        self.hdgbugline_shape[1].draw()
                    else:
                        self.hdgbugline_shape[0].draw()
                        
                #Draw bug_polygon
                glLineWidth(2.0)
                glTranslatef(radius, 0.0, 0.0)
                if not (138< diff < 222): self.hdgbug_shape.draw()
                glPopMatrix()
                if draw_flag: bug_text(-150,157,bug)
                
    def magnetic_track(self, hdgmag, magtrack):
                diff = hdgmag - magtrack
                glPushMatrix()
                glRotatef(diff,0,0,1.0)
                glTranslatef(0,138,0)
                self.mag_track_shape.draw()
                glPopMatrix()
        
        
      
    def draw(self):
        
        self.comp(self.dt)
        glLineWidth(2.0)
        #Move down
        glPushMatrix()
        glTranslatef(0,-30,0)
        self.plane_shape.draw()
        self.heading_ticks(145,self.hdgmag.value)
        self.triangle_marks.draw()
        self.heading_bug(self.hdgmag.value,self.hdgbug.value)
        self.magnetic_track(self.hdgmag.value, self.magtrack.value)
        glPopMatrix()
        self.bottom_polygon.draw() #Used to cut off bottom of HSI
        
        