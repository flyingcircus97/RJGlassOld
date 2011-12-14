import gstest.test_mod as test_mod
import variables.variable as variable


class thetest_c(test_mod.Test_c):
    
    def __init__(self):
        test_mod.Test_c.__init__(self, __name__)
        self.alt = variable.variables.byName("IND_ALT")
        self.name = "Increase Altitude"
        
    def inc_alt(self):
        self.alt.data.value += 1
        self.message = "Alt: %d" %self.alt.data.value
        
    
thetest = thetest_c()
thetest.add_func(thetest.inc_alt)