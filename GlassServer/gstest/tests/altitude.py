import gstest.test_mod as test_mod
import variables.variable as variable


class thetest_c(test_mod.Test_c):
    
    def __init__(self):
        test_mod.Test_c.__init__(self, __name__)
        self.bank = variable.variables.byName("PLANE_BANK")
        self.pitch = variable.variables.byName("PLANE_PITCH")
        self.name = "Bank/Pitch Test"
        
    def inc_alt(self):
        self.bank.data.value += .5
        self.pitch.data.value += .1
        if self.pitch.data.value > 30:
            self.pitch.data.value = -30.0
        if self.bank.data.value >180.0:
            self.bank.data.value = -180.0
        
        #print "YYOYOYOYO"
        
        
    
thetest = thetest_c()
thetest.add_func(thetest.inc_alt)