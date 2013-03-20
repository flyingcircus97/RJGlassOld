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
        self.obs_circle_shape = self.obs_circle_b()
        self.nav_needle_shape = self.nav_needle_b()
        self.bearing_shape = self.bearing_b()
        
    def bottom_b(self):
        #Bottom black polygon for scissoring
        w = 150
       
        y2 = (self.y/-2) -10
        
        y1 = y2 + 60
        
        v1 = common.vertex.lines()
        v1.add([-w,y1,w,y1,w,y2,-w,y2,-w,y1])
        
        batch = pyglet.graphics.Batch()
        b1 = batch.add(v1.num_points, GL_POLYGON, None, ('v2f', v1.points),('c3f',common.color.black*v1.num_points))
            
        return batch
            
        
    def obs_circle_b(self):
        
        v1 = common.vertex.lines()
        
        #Draw 4 circles
        x, r, seg = 33, 4, 9
        for i in [-2*x,-x,x,2*x]:
            v1.add(common.draw.List_Circle(r,seg,offset_x=i))
            v1.reset()
        #Done with 4 circles
        batch = pyglet.graphics.Batch()
        b1 = batch.add(v1.num_points, GL_LINES, None, ('v2f', v1.points),('c3f',common.color.white*v1.num_points))
        
        return batch
        
    def nav_needle_b(self):
        #The top part with arrow, and bottom part. Line will be draw without batch.
        v1 = common.vertex.lines()
        
        radius = 140
        arrow_w = 10
        h = 70
        offset = 6
        arrow_bot = radius - offset - h/2 - 5
        #Draw Top arrow
        v1.add([0,radius - offset,-arrow_w, arrow_bot, arrow_w, arrow_bot, 0,radius-offset])
        v1.reset()
        #Draw top line
        v1.add([0,arrow_bot,0,radius-offset-h])
        v1.reset()
        #Draw bottom line
        v1.add([0,-radius+offset, 0, -radius+offset+h])
        
        #Draw needle seprate batch so it can be moved.
        gap = 3
        v2 = common.vertex.lines()
        v2.add([0,radius-offset-(h+gap),0,-radius+offset+(h+gap)])
        
        #To/From Indicator
        v3 = common.vertex.lines() #top arrow
        v4 = common.vertex.lines() #bottom arrow
        
        offset, w, h = 60, 7, 15
        
        #Draw To Arrow
        v3.add([0,offset,-w,offset-h,w,offset-h,0,offset])
        v4.add([0,offset-h, -w, offset,w,offset,0,offset-h])
        
                     
        b_dic = {}
        
        for c in [common.color.white, common.color.green, common.color.yellow, common.color.cyan]:
            #Load needle for each color
            batch = pyglet.graphics.Batch()
            b1 = batch.add(v1.num_points, GL_LINES, None, ('v2f', v1.points),('c3f',c*v1.num_points))
            batch2 = pyglet.graphics.Batch()
            b2 = batch2.add(v2.num_points, GL_LINES, None, ('v2f', v2.points),('c3f',c*v2.num_points))
            to_batch = pyglet.graphics.Batch()
            b1 = to_batch.add(v3.num_points, GL_LINES, None, ('v2f', v3.points),('c3f',c*v3.num_points))
            from_batch = pyglet.graphics.Batch()
            b2 = from_batch.add(v4.num_points, GL_LINES, None, ('v2f', v4.points),('c3f',c*v4.num_points))
                        
            b_dic[c] = {'arrow': batch, 'needle': batch2, 'to': to_batch, 'from':from_batch}
            
        return b_dic
    
           
    def bearing_b(self):
        #ADF/NAV Bearing Needles 
        
        
        def needle(num, color): 
        
            def double():
                y3 = arrow_y-8
                v1.add([w,y3,w,y2])
                v1.reset()
                v1.add([-w,y3,-w,y2])
                v1.reset()
                v1.add([0,arrow_y,0,y1])
                v1.reset()
            v1 = common.vertex.lines()
            #Calculate batch for num of lines and color
            radius = 145
            w = 8
            offset= 40 #Radius from center not to draw bearing line
            arrow_point = 72 #Point at which to draw_arrow
            arrow_w = 15
            arrow_h = 15
            
            #Top Part
            y1 = radius-10
            y2 = offset
            arrow_y = arrow_point+10
            if num==1: #Single Line
                v1.add([0,y1,0,y2])
            else: #Double Line
                double()
            v1.reset()
            v1.add([-15,arrow_y-15,0,arrow_y,15,arrow_y-15])
            v1.reset()
            #Bottom Part
            y1 = -radius+10
            y2 = -offset
            arrow_y = -arrow_point
            if num==1: #Single Line
                v1.add([0,y1,0,y2])
            else: #Double Line
                double()
            v1.reset()
            v1.add([-15,arrow_y-15,0,arrow_y,15,arrow_y-15])
                            
            batch = pyglet.graphics.Batch()
            b1 = batch.add(v1.num_points, GL_LINES, None, ('v2f', v1.points),('c3f',color*v1.num_points))
            
            return batch
        
        r_dict={}
        r_dict[1]=needle(1,common.color.purple)
        r_dict[2]=needle(1,common.color.cyan)
            
        return r_dict

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
                glTranslatef(0,135,0)
                self.mag_track_shape.draw()
                glPopMatrix()
                
    #NAV guage    
    def nav(self, hdg):
            #Draw OBS
            diff = hdg - 40
            if diff <0: diff+=360 #Make sure diff is between 0 and 360
            glPushMatrix()
            glRotatef(diff, 0,0, 1)
            #Color
            glLineWidth(2.0)
            self.obs_circle_shape.draw()
            #Draw Needle
            c = common.color.green
            #Top Arrow and Bottom line
            self.nav_needle_shape[c]['arrow'].draw()
            
         #   if NAV.hasNav.value:   
            #To/From Indicator
            self.nav_needle_shape[c]['from'].draw()
            #Draw CDI Line
            #cdi_x = NAV.CDI.value / 127.0 * (x* 2 + r) #x*2+r is max difflection = to outmost point of outer circle             
            cdi_x = 10
            glTranslatef(cdi_x,0,0)
            self.nav_needle_shape[c]['needle'].draw()
         
            glPopMatrix()
            
    def bearing(self, hdg):
        diff = hdg-140
        glPushMatrix()
        glRotatef(diff, 0,0, 1)
        #Color
        glLineWidth(2.0)
        
        #Draw Needle
        self.bearing_shape[1].draw()
         
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
        self.nav(self.hdgmag.value)
        self.bearing(self.hdgmag.value)
        self.magnetic_track(self.hdgmag.value, self.magtrack.value)
        self.heading_bug(self.hdgmag.value,self.hdgbug.value)
        
        glPopMatrix()
        self.bottom_polygon.draw() #Used to cut off bottom of HSI
        
        