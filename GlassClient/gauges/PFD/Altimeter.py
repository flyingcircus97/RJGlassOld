#Altimeter Gauge
# 

import pyglet
from pyglet.gl import *
from gauge import gauge_parent
import common
import variable
import math, time
import text
        
        
class MDADH_c(object):
    #Decision Heigth Class used for to house and compute DH data
    
    def __init__(self, bug, active):
        self.bug = variable.variables.load(bug)
        self.active = variable.variables.load(active)
        self.notify = False #Set to true when below 
        self.flash = 0 #Increments to cause flashing 1 second cycle if needed
        self.flash_time = 0.0
        self.visible = False
        
    def comp(self, alt, OnGround, dt=0.0):
        
        if ((self.active.value) and (alt <= self.bug.value) and (not OnGround)):
            self.notify = True
            self.flash_time += dt
            if self.flash_time >= 0.4:
                self.flash +=1
                self.flash_time -=0.4
                if self.flash>28: self.flash = 28 #Causes to only flash for 14 times for 11 seconds per Jeff
                if self.flash%2==0: #Visible used only for MDA with flashing
                    self.visible = True
                else:
                    self.visible = False
            
        else:
            self.notify = False
            self.visible = False
            self.flash_time = 0.0
            self.flash = 0
            
            

    
    
class gauge_c(gauge_parent):
        
    def __init__(self, *args, **kwds):
        
        super(gauge_c, self).__init__(*args, **kwds)
        
        self.x = 100
        self.y = 300
        self.set_native_size(self.x, self.y)
        
        
        self.load_batch()
        
        #Init Constants
        self.units_apart = 13.0
        self.pixel_per_foot = 13.0/20.0
        self.thoupixel_per_foot = 13.0/100.0
        #Init Variables
        self.rad_alt = variable.variables.load(0x112)
        self.OnGround = variable.variables.load(0x127)
        self.alt_bug_var = variable.variables.load(0x150)
         #Cpt / FO Specific
        if self.parent.side == 'CPT':
            self.ind_alt = variable.variables.load(0x1130)
            self.alt_setting = variable.variables.load(0x112C)
            self.DH = MDADH_c(0x1120,0x1121)
            self.MDA = MDADH_c(0x1128,0x1129)
        else: #parent.side =='FO'
            self.ind_alt = variable.variables.load(0x1131)
            self.alt_setting = variable.variables.load(0x112E)
            self.DH = MDADH_c(0x1122,0x1123)
            self.MDA = MDADH_c(0x112A,0x112B)
        self.count = 0
        self.dt = 0.0
    
        
    def load_batch(self):
        self.smticks_shape = self.small_ticks_b()
        self.thousand_shape, self.fivehund_shape = self.thousand_lines_b()
        self.thousandodd_shape = self.thousand_ticks_b(1)
        self.thousandeven_shape = self.thousand_ticks_b(0)
        self.rollingblack_shape = self.rollingblack_b()
        self.rollingblackhalf_shape = self.rollingblack_b(True)
        self.rollingblacksmall_shape = self.rollingblack_b(small=True)
        self.altitudebg_shape = self.altitudebg_b()
        self.blackbox_shape = self.blackbox_b()
        self.altitudebug_shape = self.altitudebug_b()
        self.altitudethoubug_shape = self.altitudebug_b(True)
        self.DHbug_shape = self.DH_b()
        self.MDAbug_shape = self.MDA_b()
     
    def DH_b(self):
        w1,w2 = 5,20
        h = 10
        rect = common.vertex.lines()
        rect.add([0,h,w1,h,w1,-h,0,-h])
        
        line = common.vertex.lines()
        line.add([w1,0,w2,0])
        
        batch = pyglet.graphics.Batch()
        top = pyglet.graphics.OrderedGroup(0)
        bottom = pyglet.graphics.OrderedGroup(1)
        
        b1 = batch.add(rect.num_points, GL_POLYGON, top, ('v2f', rect.points),('c3f',common.color.cyan*rect.num_points))
        b2 = batch.add(line.num_points, GL_LINES, bottom, ('v2f', line.points),('c3f',common.color.cyan*line.num_points))
        
        return batch
    
    def MDA_b(self):
        w1,w2 = -8,40
        h = 14
                
        line = common.vertex.lines()
        line.add([0,0,w1,-h,w1,h,0,0])
        line.add([w2,0])
        
        
        batch = pyglet.graphics.Batch()
        
        b1 = batch.add(line.num_points, GL_LINES, None, ('v2f', line.points),('c3f',common.color.cyan*line.num_points))
        
        return batch
        
        
    def rollingblack_b(self, half=False, small=False):
        #Used to conver up rolling digits and thousands tick marks as they go through center.
        #Normal covers up upper and lower digit
        #Half covers up lower half digit
        #Small covers up just thousands tick marks as the move through center.
        
        x1 = 0
        x2 = 38
        black_l = 29.0
        black_h = 57.0
        if small:
            black_h = 30.0
            black_l = 22.0
        vp = common.vertex.lines()
        vp2 = common.vertex.lines()
        vp.add([x1,black_l,x2,black_l,x2,black_h,x1,black_h,x1,black_l])
        if half:
            black_h = 44.0
        vp2.add([x1,-black_l,x2,-black_l,x2,-black_h,x1,-black_h,x1,-black_l])
        
        batch = pyglet.graphics.Batch()
        top = pyglet.graphics.OrderedGroup(0)
        bottom = pyglet.graphics.OrderedGroup(1)
        
        b1 = batch.add(vp.num_points, GL_POLYGON, top, ('v2f', vp.points),('c3f',common.color.black*vp.num_points))
        b2 = batch.add(vp2.num_points, GL_POLYGON, bottom, ('v2f', vp2.points),('c3f',common.color.black*vp2.num_points))
         
        return batch
    
    def blackbox_b(self):
        #Used to conver up top and bottom of altitude tape for scissoring
     
        x1 = 0
        x2 = 100
        black_l = 150.0
        black_h = 200.0
        
        vp = common.vertex.lines()
        vp2 = common.vertex.lines()
        vp.add([x1,black_l,x2,black_l,x2,black_h,x1,black_h,x1,black_l])
        vp2.add([x1,-black_l,x2,-black_l,x2,-black_h,x1,-black_h,x1,-black_l])
        
        batch = pyglet.graphics.Batch()
        top = pyglet.graphics.OrderedGroup(0)
        bottom = pyglet.graphics.OrderedGroup(1)
        
        b1 = batch.add(vp.num_points, GL_POLYGON, top, ('v2f', vp.points),('c3f',common.color.black*vp.num_points))
        b2 = batch.add(vp2.num_points, GL_POLYGON, bottom, ('v2f', vp2.points),('c3f',common.color.black*vp2.num_points))
         
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
        
        #Tick itself
        if (tick % 2): #If odd then 500 foot mark make smaller, if even then make larger 1000 foot mark
            x1 = 29
        else:
            x1 = 21

        y1 = loc-3
        y2 = loc+3
        vl.add([x1, y1, x2, y1, x2, y2, x1,y2, x1,y1]) 
        vl.reset()
                
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
        x2 = -1
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
        
    def altitudebg_b(self):
        vl = common.vertex.lines()
        # Background with white outline
        h2 = 30
        h1 = 18
        vl.add([20.0, h2])
        vl.add([35.0, h2])
        vl.add([42.0, h1])
        vl.add([100, h1])
        vl.reset()
        vl.add([20.0, -h2])
        vl.add([35.0, -h2])
        vl.add([42.0, -h1])
        vl.add([100, -h1])
        
        batch = pyglet.graphics.Batch()
        b1 = batch.add(vl.num_points, GL_LINES, None, ('v2f', vl.points),('c3f',common.color.white*vl.num_points))
        
        return batch
   
    #Draws putple lines for bug
    def altitudebug_b(self, thou=False):
        vl = common.vertex.lines()
        if thou: 
            y=0;x1=21;x2=37
         
            vl.add([x1,y,x2,y])
                
        else: 
            y1=16; y2=19; x1=52; x2=94
            for y in [-y1,-y2,y1,y2]:
                vl.add([x1,y,x2,y])
                vl.reset()
        
        batch = pyglet.graphics.Batch()
        b1 = batch.add(vl.num_points, GL_LINES, None, ('v2f', vl.points),('c3f',common.color.purple*vl.num_points))
        
        return batch
   
    
    def tick_marks(self, altitude):
            
            
            #Draw the tick mark
            #Every 20 ft is 13 units apart

            
            #altitude = aircraft.altitude
            #glColor3f(1.0, 1.0, 1.0)
            #glLineWidth(2.0)
            start_tick_ten = (altitude / 20) - 13
            tick_ten = start_tick_ten
            start_loc = -((altitude - (tick_ten * 20)) * self.pixel_per_foot)
            #Small ticks
            loc = start_loc
            glPushMatrix()
            glTranslatef(0,loc,0)
            self.smticks_shape.draw()
            glPopMatrix()
            
            loc = start_loc
            tick_ten = start_tick_ten
            #glLineWidth(2.0)
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
                    #glLineWidth(2.0)
                    glScalef(0.15,0.15,1) #Scale text, also done in else statement below.
                    
                    s = str(temp) + "00"
                    text.write(s)
                    glPopMatrix()

                tick_ten = tick_ten +1
                loc = loc + 13.0
                
    def thousand_tick_marks(self, altitude):
            alt = altitude % 1000 #Only need the hundreds feet part because it repeats
            #Draw the tick marks
            #Every 100 ft is 13 units apart
           
            
            #altitude = aircraft.altitude
            
            #glLineWidth(2.0)
            tick = ((alt-250) / 500) - 1
            loc = -((alt - (tick * 500)) * self.thoupixel_per_foot) #Some how need to fit 5 in there.

            #Thousand ticks
            glPushMatrix()
            glTranslatef(0,loc,0)
            for i in range(5):
                if abs(loc)>27:
                    if (tick % 2):
                        self.thousandodd_shape.draw()
                    else:
                        self.thousandeven_shape.draw()
                tick=tick+1
                glTranslatef(0,65,0)
                loc+=65
            glPopMatrix()
            
            #Draw black plygon over area, therefore these ticks need to be done first, eaiser then doing multiple scissor boxes	
            #self.centerblack_shape.draw()
            #common.color.set(common.color.purple)
            #glBegin(GL_POLYGON)
            #glVertex2f(20.0, black_l)
            #glVertex2f(38.0, black_l)
            #glVertex2f(38.0, black_h)
            #glVertex2f(20.0, black_h)
            #glEnd()
            
    def altitude_disp(self, altitude, x=0, y=0):
            #altitude = aircraft.altitude
            def thousands():  # This does the thousands and ten thousands digit
                alt = altitude
                thou = (alt // 1000)
                roll=False
                
                def text_out(d, blank_zero = False): #Just output the text.
                    if ((d>0) or (not blank_zero)):
                        glScalef(0.20, 0.22, 1.0)                        
                        text.write("%2d" %d)
                    
                def altdigit_draw(value,y_nextdigit,y_digit, x, blank_zero = False):
                    #Next digit if rolling
                    if y_nextdigit:
                        glPushMatrix()
                        glTranslatef(x, 45.0-y_nextdigit, 0.0)
                        text_out((value+1)%10, blank_zero)
                        glPopMatrix()
                    #Current digit
                    glPushMatrix()
                    glTranslatef(x, -y_digit, 0.0)
                    text_out(value, blank_zero)
                    glPopMatrix()
                    
                    
                #Check to see if near change in thousand above 900 feet
                alt_1000 = alt % 1000  
                glPushMatrix()
                if thou <0: #negative number no rolling
                #Display yellow NEG in place of number
                    self.rollingblacksmall_shape.draw()
                    common.color.set(common.color.yellow)
                    #glDisable(GL_SCISSOR_TEST) #Turn off so text will show up
                    glTranslatef(28.0, 12.0, 0.0)
                    glScalef(0.10, 0.10, 1.0)
                    text.write("N")
                    glTranslatef(-85.0, -120.0, 0.0)
                    text.write("E")
                    glTranslatef(-85.0, -120.0, 0.0)
                    text.write("G")
                    
                #Bottom digit starts moving and top digit appears at 900.
                #--Top digit goes twice as fast about as lower digit. 
                #--Digits hit at 950, then bottom digit goes twice as fast as top digit.
                else: #Altitude positive.
                    if (alt_1000 >= 900): # Close to change in thousand will roll digits
                        roll=True
                        thou_diff = 1000- alt_1000 
                        diff100 = 100-thou_diff
                        if thou_diff <=50:
                            diff50 = 50-thou_diff
                        else:
                            diff50 = 0
                            
                        rate = 0.3   #pixel per foot for movement of digits
                        y_digit = (diff100+diff50) * rate  #y position of current lower digit
                        y_nextdigit = (2*diff100-diff50) * rate#y position of next upper digit
                    else: 
                        #No rolling <900
                        y_digit=0
                        y_nextdigit= 0 
                    #1's thounsands digit
                    altdigit_draw(thou%10, y_nextdigit, y_digit, 12)
                    #10's thousand digit
                    if thou%10 != 9: #Don't roll it
                        y_nextdigit=0 
                        y_digit =0 
                    altdigit_draw(thou//10, y_nextdigit, y_digit, -6, True)    
                    #Draw black box to conver up rolling numbers
                    if roll:
                        if thou_diff<=30:#used to gradually cover up lower digit, without covering thousands tick marks.
                            self.rollingblack_shape.draw()
                        else:
                            self.rollingblackhalf_shape.draw()
                    else:
                        self.rollingblacksmall_shape.draw()
                        
                glPopMatrix()
            #glEnable(GL_SCISSOR_TEST)
            #scissor(x-10, y-15, 80, 30)
            #Draw thousands digits
            thousands()
            self.altitudebg_shape.draw()
            
    def hundred_alt_bug(self, altitude, bug):
            #Draws putple lines for bug    
            diff = altitude- bug
            if abs(diff) <= 260: #If farther than that away no need to draw it.
                loc = -diff * self.pixel_per_foot
                glPushMatrix()
                glTranslatef(0,loc,0)
                self.altitudebug_shape.draw()
                glPopMatrix()
    
    def thousand_alt_bug(self, altitude, bug):
            #Cant use batch drawing due to rolling digits
            def draw_line(loc):
                if abs(loc)>31:
                    self.altitudethoubug_shape.draw()
                    
            diff = altitude- bug
            if abs(diff) <= 1400: #If farther than that away no need to draw it.
                loc = -diff * self.thoupixel_per_foot
                #Draw two purple lines above and below loc
                loc+=11
                glPushMatrix()
                glTranslatef(0,loc,0)
                draw_line(loc)
                for i in [-4,-14,-4]:
                    glTranslatef(0,i,0)
                    loc+=i
                    draw_line(loc)
                glPopMatrix()
                
                
    
    def alt_bug(self,altitude,bug):
        self.thousand_alt_bug(altitude,bug)
        self.hundred_alt_bug(altitude,bug)
        
    def radar_alt(self, aag): # Puts mark on tape that show ground.
                    
            def foreground(aag): #Draw the correct white lines for foreground
                    common.color.set(common.color.white)
                    glLineWidth(2.0)
                    glBegin(GL_LINES)
                    if aag > 1020:
                        h = 30
                    else:
                        h = 12
                        glVertex2f(-10,0)
                        glVertex2f(0,0)
                    
                    glVertex2f(0, h)
                    glVertex2f(20, h)
                    glVertex2f(0, -h)
                    glVertex2f(20, -h)
                    
                    glEnd()
            
            
            def radar_scale(aag):
                
                
                def tick_line(w,loc): #Just draw the tick line
                    glBegin(GL_LINES)
                    glVertex2f(0.0, loc)
                    glVertex2f(w, loc)
                    glEnd()
                    
                    
                start_tick = (aag // 100) - 3
                start_loc = -((aag - (start_tick * 100.0)) * self.pixel_per_foot)

                loc = start_loc
                tick = int(start_tick) - 1 #Makes sure tick is integer for glText1 command below
                w = 6
                fifty_offset = 50 * self.pixel_per_foot #The fifty foot offset
                if self.DH.notify:#If DH notifer is on, change color to yellow, insted of default green
                    common.color.set(common.color.yellow)
                else: 
                    common.color.set(common.color.green)
                    
                glLineWidth(2.0)
                fifty_flag=True
                loc -= fifty_offset
                for i in range(14):
                    if abs(loc) <=160:
                        if  (10 > tick >=0):
                            tick_line(w,loc) #Draw tick at 100'
                     #       tick_line(w, loc - fifty_offset) # Draw tick at 50' mark below it.
                            if not fifty_flag and tick: 
                                glPushMatrix()
                                glTranslatef(w + 7, loc, 0.0)
                                glScalef(0.13,0.13,1.0)
                                text.write("%d" %tick) #Ok since number will only be 1-9
                                glPopMatrix()
                        #elif tick == 10: #Special case to add the 950' mark
                        #    tick_line(w, loc - fifty_offset)
                    if fifty_flag:
                        fifty_flag=False
                        tick+=1
                    else:
                        fifty_flag=True
                    
                    loc += fifty_offset
                
            def ground_mark(aag):
                loc =-((aag) * self.pixel_per_foot) #Ever 20 feet is 13 units (pixels)
                num = ((230-aag) // 20) + 1
                common.color.set(common.color.yellow)
                glLineWidth(2.0)
                glBegin(GL_LINE_STRIP)
                w = 20.0 #width of yellow cross hatch
                bot_loc = -150 #loc - (225 * self.pixel_per_foot)
                glVertex2f(1.0, bot_loc)
                glVertex2f(1.0, loc) #Draw horizontal top line
                glVertex2f(w, loc)
                glVertex2f(w, bot_loc)
                glEnd()
                glBegin(GL_LINES)
                for i in range(num): #Draw angled verticle lines
                    glVertex2f(1.0, loc)
                    glVertex2f(w, loc - 13)
                    loc -= 13.0
                glEnd()
                
            def DH_bug_draw(diff):
                loc = - diff * self.pixel_per_foot
            #    common.color.set(common.color.cyan)
                #glLineWidth(2.0)
                glPushMatrix()
                glTranslatef(0,loc,0)
                self.DHbug_shape.draw()
                glPopMatrix()
                
            def MDA_bug_draw(diff):
                loc = - diff * self.pixel_per_foot
                glPushMatrix()
                glTranslatef(54,loc,0)
                self.MDAbug_shape.draw()
                glPopMatrix()
#                
#            def DH_Notifier(x,y):
#                glDisable(GL_SCISSOR_TEST)
#                glPushMatrix()
#                glTranslate(x,y, 0)
#                glColor(yellow)
#                glScalef(0.2,0.2, 1.0)
#                glLineWidth(2.0)
#                glText("DH", 100)
#                glPopMatrix()
#                glEnable(GL_SCISSOR_TEST)
                
            if 1: #config.RA_scale: #If RA_scale enabled
                if aag<1300:
                    radar_scale(aag)
                    if aag<=230:
                        ground_mark(aag)
                
                foreground(aag)
            #Draw DH if active and within 250 ft of RA
            if self.DH.active.value:
                diff = self.rad_alt.value-self.DH.bug.value
                if (self.DH.flash %2==0):
                    if abs(diff)<250: DH_bug_draw(diff)
            #Flash MDA if 
            if self.MDA.active.value:
                diff = self.ind_alt.value -self.MDA.bug.value
                if (self.MDA.flash %2==0):
                    if abs(diff)<300: MDA_bug_draw(diff)
                        
            

    def alt_bug_text(self, bug):
            common.color.set(common.color.purple)
            #glLineWidth(2.0)
            glPushMatrix()
            glTranslatef(36, 200, 0.0) #Move to start of digits
            glScalef(0.16,0.16,1.0)
            text.write("%2d" %(bug // 1000))
            glScalef(0.80,0.80,1.0) #Scale digits 85%
            glTranslatef(0,-13,0)
            text.write("%03d" %(bug % 1000))
            glPopMatrix()
            
    def alt_setting_disp(self, setting):
            common.color.set(common.color.cyan)
            glPushMatrix()
            glTranslatef(15,-165,0)
            #Text out setting
            glPushMatrix()
            glScalef(0.14,0.15,0)
            
            if setting >2000: #Must be inches of HG if under 35
                text.write("%5.2f" %(setting/100.0), 90) #Round it to 2 places after decimal point 0.01 is slight correction. (Rouding Error?)
            else:
                text.write("%4d" %setting, 90)
            glPopMatrix() #Text 29.92
            #Display IN
            if setting>2000: #Must by HG if under 35 HPA if not.
                glTranslatef(58,-1,0) #move for In display
                glScalef(0.12,0.12,0)
                text.write("I N",40)
            else: #Must be HPA
                glTranslatef(53, -1,0)
                glScalef(0.12,0.12,0)
                text.write("HPA",90)
                
            glPopMatrix()
            
    def comp(self):
        self.DH.comp(self.rad_alt.value, self.OnGround.value, self.dt)
        self.MDA.comp(self.alt, self.OnGround.value, self.dt)
        self.parent.DH_notify = self.DH.notify
        
    def draw(self):
        common.color.set(common.color.white)
        glPushMatrix()
        self.alt = self.ind_alt.value
        #Compute Necessary Data
        self.comp()
        
        #self.glLineWidth(2.0)
        glLineWidth(2.5)
        glTranslatef(-50.0,0,0)
        self.tick_marks(self.alt)
        self.thousand_tick_marks(self.alt)
        self.altitude_disp(self.alt)
        
        self.alt_bug(self.alt, self.alt_bug_var.value)
        
        self.radar_alt(self.rad_alt.value)
        self.blackbox_shape.draw()
        glLineWidth(2.5)
        self.alt_bug_text(self.alt_bug_var.value)
        self.alt_setting_disp(self.alt_setting.value)
        glPopMatrix()