#Speed Tape Gauge
# 
#
# -- Currently Missing
#  
#   -- Mach text
#   -- Fine location and positioning
#   -- Connection with GlassServer


import pyglet
from pyglet.gl import *
from gauge import gauge_parent
import common
import variable
import math, time
import text


class Vspeed_c(object):
    #Hold all data on VSpeed Class
        def __init__(self, name, y_pos, value, visible):
            self.name = name
            self.y_pos = y_pos
            self.value = value
            self.visible = visible
        
        def draw_indicator(self, loc):
            if self.y_pos + loc > -165:    
                glPushMatrix()
                glTranslatef(-35.0, self.y_pos + loc, 0.0)
                glScalef(0.15,0.15,1.0)
                if self.visible.value: 
                    text.write("%s %3d" %(self.name, self.value.value))
                else:
                    text.write("%s" %(self.name))
                glPopMatrix()
                
        def draw_selected(self, loc):
                #Always draw located below airspeed tape
                glPushMatrix()
                glTranslatef(-35.0, loc, 0.0)
                glScalef(0.15,0.15,1.0)
                if self.visible.value:
                    text.write("%s %3d" %(self.name, self.value.value))
                else:
                    text.write("%s ---" %(self.name))
                glPopMatrix()
        
        def draw_bug(self, airspeed, knot_unit):
            if self.visible.value:
                diff = (self.value.value- airspeed) * knot_unit
                noshow = 168 #If out of this range then don't show
                if abs(diff) <= noshow:
                    glPushMatrix()
                    glTranslatef(17.5, diff, 0.0) #Move to point of V speed bug
                    #Draw Line
                    glBegin(GL_LINES)
                    glVertex2f(-35.0,0.0)
                    glVertex2f(-7.5,0.0)
                    glEnd()
                    #Draw Text next to line 1,2,R,T
                    
                    glScalef(0.12,0.12,1.0)
                    text.write(self.name[1]) #Only do 2nd character
                    glPopMatrix()
        
        def draw(self,loc, airspeed, knot_unit):
            self.draw_indicator(loc)
            self.draw_bug(airspeed, knot_unit)
        
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
        self.IAS = variable.variables.load(0x100,'4F')
        self.OnGround = variable.variables.load(0x127)
        self.Mach = variable.variables.load(0x103,'4F')
        self.V1 = variable.variables.load(0x1100)
        self.V1_visible = variable.variables.load(0x1101)
        self.VR = variable.variables.load(0x1102)
        self.VR_visible = variable.variables.load(0x1103)
        self.V2 = variable.variables.load(0x1104)
        self.V2_visible = variable.variables.load(0x1105)
        self.VT = variable.variables.load(0x1106)
        self.VT_visible = variable.variables.load(0x1107)
        self.MaxCue = variable.variables.load(0x1110)
        #Cpt / FO Specific
        if self.parent.side == 'CPT':
            self.VSpeed_Selected = variable.variables.load(0x1108)
        else: #parent.side =='FO'
            self.VSpeed_Selected = variable.variables.load(0x1109)            
            
        self.Vinput = 0 #Vspeed that is selected. (0-4) 0=V1 1=VR 2=V2 3=VT
        self.a = 0.0
        # Init Vspeeds  
        y_space = 30
        y_offset = 5
        self.Vspeed_l = [Vspeed_c('V1', y_offset, self.V1, self.V1_visible),Vspeed_c('VR', y_space+y_offset, self.VR, self.VR_visible),
            Vspeed_c('V2', 2*y_space+y_offset, self.V2, self.V2_visible), Vspeed_c('VT', 3*y_space+y_offset, self.VT, self.VT_visible)]
        # Init speed tending line variables
        self.IAS_speeds = [[40.0, time.time()]] * 60
        self.IAS_trend = 0.0
        self.Mach_visible = False
        
        
    def comp(self):
            self.time = time.time()
            self.comp_IAS_accel()
            self.comp_Mach_disp()
            
    def comp_Mach_disp(self):
        self.Mach_ind = self.Mach.value
        if self.Mach_visible:
            if self.Mach_ind < 0.4: self.Mach_visible = False
        else:
            if self.Mach_ind > 0.45: self.Mach_visible = True
            
    def comp_IAS_accel(self):
        self.IAS_speeds.append([self.airspeed,self.time])
        self.IAS_speeds.pop(0)
        
        avg = []
        for i in range(0,60,6):
            first = self.IAS_speeds[i]
            last = self.IAS_speeds[i+5]
            if (last[1]-first[1])!=0.0:
                avg.append((last[0]-first[0]) / (last[1]-first[1]))
            
        if len(avg) == 0:
            new_trend = 0
        else:
            new_trend = sum(avg) / len(avg) * 10.0
            
        self.IAS_trend += (new_trend - self.IAS_trend) * 0.10 #Limit change to 10% for smoothing
        #Limit trending to 50 knots.
        if self.IAS_trend>50: self.IAS_trend = 50
        elif self.IAS_trend<-50: self.IAS_trend = -50
            
            
    def load_batch(self):
        self.arrow_shape = self.center_arrow_b()
        self.top_black_shape = self.black_blocks_b(True)
        self.bottom_black_shape = self.black_blocks_b(False)
        self.speedbug_shape = self.speedbug_b()
        self.barberup_shape = self.barberpole_b(1)
        self.barberdown_shape = self.barberpole_b(-1)
    
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
        
    def speedbug_b(self):
        
        v1 = common.vertex.lines()
        v1.add([0,0,10,8,10,15,0,15,0,-15,10,-15,10,-8,0,0])
        batch = pyglet.graphics.Batch()
        b1 = batch.add(v1.num_points, GL_LINES, None, ('v2f', v1.points),('c3f',common.color.purple*v1.num_points))
        
        return batch
    
    def barberpole_b(self, dir):
    
        step = 12 #Determine step between
        x1 = 2
        x2 = 14
        vp = common.vertex.lines()
        vl = common.vertex.lines()
        loc = 0
        i =0
        num = 2
        d = step* dir
        
        #Draw polygon
        vp.add([x1,0,x2,0])
        loc+=d
        vp.add([x2,loc,x1,loc, x1,0])
        loc+=d
        #Draw lines
        vl.add([x1,0,x1,loc])
        vl.reset()
        vl.add([x2,0,x2,loc])

        batch = pyglet.graphics.Batch()
        b1 = batch.add(vp.num_points, GL_POLYGON, None, ('v2f', vp.points),('c3f', common.color.red*vp.num_points))
        b2 = batch.add(vl.num_points, GL_LINES, None, ('v2f', vl.points),('c3f', common.color.red*vl.num_points))
        
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
    
    def airspeed_diff(self, difference):
            #Pink Line above or below arrow that shoes accel or decel rate. Forcast 5 seconds ahead??
            if abs(difference) > 1: #If forcasted not difference is less than 2 knots then down't show
                y1 = 0
                y2 = y1 + difference * self.knot_unit
                x1 = 18
                x2 = x1 + 12.0
                glLineWidth(2.0)
                common.color.set(common.color.purple)
                glBegin(GL_LINE_STRIP)
                glVertex2f(x1, y2)
                glVertex2f(x2, y2)
                glVertex2f(x2, y1)
                glEnd()
    
    def speedbug_draw(self, x=0,y=0):
        
        diff = 100 - self.indicated_IAS()
        diff = diff*self.knot_unit
        if abs(diff)<168:
            glPushMatrix()
            glTranslatef(0,diff,0)
            self.speedbug_shape.draw()
            glPopMatrix()
            
    def speedbugind_draw(self, x=0,y=0):
        
            common.color.set(common.color.purple)
            glPushMatrix()
            glTranslatef(x,y,0)
            self.speedbug_shape.draw()
            glTranslatef(30,0,0)
            glScalef(0.15,0.15,1.0)
            text.write("%3d" %(100))
            glPopMatrix()        
        
    def Vspeeds(self, start_loc, start_tick_ten):
        #Draw Vspeeds
        
                    
        #First calculate location of each of the Vspeeds (V1,VR,V2,VT)
        loc = start_loc - (start_tick_ten *10 * self.knot_unit)
        common.color.set(common.color.cyan)
        for speed in self.Vspeed_l:
            speed.draw(loc, self.airspeed, self.knot_unit)
            
    def Vspeed_selected(self, loc):
        
        if self.VSpeed_Selected.value >0: #If 0 don't draw Vspeed window
            common.color.set(common.color.cyan)
            self.Vspeed_l[self.VSpeed_Selected.value-1].draw_selected(loc) #Subtract one to account for zero (No Vspeed selected)
                    
    def tick_marks(self, x=0, y=0):

            #Draw the tick mark

            unit_apart = self.knot_unit
            center = 0.0
            y_center = 0
            #air_spd is class of speed, will use IAS, Mach, and V Speeds, possibly Ground Speed
            airspeed = self.indicated_IAS()
            self.a+=0.1
            #airspeed = self.a
            
            common.color.set(common.color.white) #White
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
                
    def speed_cues(self):
        
        def lowspeedcue(y):
            x1 = -17.5
            x2 = 22.5
            common.color.set(common.color.green)
            glLineWidth(2.0)
            glBegin(GL_LINES)
            glVertex2f(x1,y)
            glVertex2f(x2,y)
            glEnd()
        
        def barberpole(y, dir):
            glPushMatrix()
            noshow = 168
            
            if dir==1:
                if y < -noshow: #If outside of range draw bar entire length
                    num = 14
                    y = -noshow + (y % 24)
                else:
                    num = int(((noshow - y) / 24) + 1)
                    
                glTranslatef(0,y,0)
                for i in range(num):
                    self.barberup_shape.draw()
                    glTranslatef(0,24,0)
            else:
                if y > noshow: #If outside of range draw bar entire length
                    num = 14
                    y = noshow + (y % 24)
                else:
                    num = int(((noshow + y) / 24) + 1)
               
                glTranslatef(0,y,0)
                for i in range(num):
                    self.barberdown_shape.draw()
                    glTranslatef(0,-24,0)
            glPopMatrix()
        
        #Lowspeed cue
        y = self.calc_show(60)
        if y: lowspeedcue(y)
        #Barber Pole Lower
        y = self.calc_show(120, False)
        #barberpole(y,-1)  ##Disable Lower Barber Pole for now.
        #Barber Pole Upper
        y = self.calc_show(self.MaxCue.value, False)
        barberpole(y,1)
        
    def airspeed_mach_text(self, value, x=0, y=0): # Text on top

            common.color.set(common.color.white)
            #Draw Text Part
            glPushMatrix()
            glTranslatef(x, y, 0.0)
            glScalef(0.13,0.13,1.0)
            text.write("M", 100)
            text.write(("%3.3f" %value)[1:], 90)
            glPopMatrix()
        
        
    def calc_show(self, speed, return_none = True):
        #Calculate on speed tape if item should be visible and where.
        diff = (speed - self.airspeed) * self.knot_unit
        noshow = 168
        if (abs(diff) <= noshow) or (not return_none):
            return diff
        else:
            return None
    
    def indicated_IAS(self):
        indicated = self.IAS.value
        if indicated <40: indicated =40
        elif indicated > 500: indicated = 500
        
        return indicated
    
    def draw(self):
        #self.glLineWidth(2.0)
        #Limit Airspeed
        self.airspeed = self.indicated_IAS()
        
        self.comp()
        glLineWidth(2.0)
        
        start_loc, start_tick_ten = self.tick_marks()
        self.tick_numbers(start_loc, start_tick_ten)    
        self.speedbug_draw()
        self.Vspeeds(start_loc, start_tick_ten)
        self.speed_cues()
        #Airspeed pink trending line, only draw if inflight.
        if not self.OnGround.value: self.airspeed_diff(self.IAS_trend)
        self.arrow_shape.draw()
        self.top_black_shape.draw()
        self.bottom_black_shape.draw()
        self.speedbugind_draw(-40,-170)
        self.Vspeed_selected(-200)
        if self.Mach_visible: self.airspeed_mach_text(self.Mach.value, -38, 170)