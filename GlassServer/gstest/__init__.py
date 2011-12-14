#!/usr/bin/env python
# ----------------------------------------------------------
# Tests - Glass Server
# ----------------------------------------------------------
# Folder where all Tests are held for glass server.
#
# This init.py file
# 

# ---------------------------------------------------------------
import os, sys

extension = '.py'

def scan_folders(extension):
    #Scan through all folders within modules looking for _mod.py files.
    #And also variable.txt files.
    ext_len = len(extension)
    test_py_files = []
    for root, dirs, files in os.walk(__name__+ os.sep + 'tests'):
        #print root, dirs, files
        for f in files:
            #Scan through files, find ones with correct extension.
            if f!= "__init__.py":
                if f[-ext_len:] == extension:
                    test_py_files.append(os.path.join(root, f))
                    
          
                
    return test_py_files
    
def import_test_files(test_files):
    #print mod_files
    list = []
    for f in test_files:
        test_name = f[:-3].replace(os.sep,'.')
        print test_name
        try:
           exec('import ' + test_name)
        except ImportError:
           print "IMPORT ERROR"
           print os.path.split(sys.path[0])[0] + '\\test'
           sys.path.append(os.path.split(sys.path[0])[0])
           exec('import ' + 'test.' + test_name)
        exec('list.append(%s)' %test_name)
        
    return list

def run_test():
    for i in test_list:
        #try:
            i.thetest.step()
        #except:
        #    print "ERROR RUNNING TEST" ,i
        
def AJAX_list(active_list):
    out = []
    count = 0
    for test in test_list:
        t = test.thetest        
        #Set active state of tests, from active_list from webpage.
        if active_list != None: #If webpage doesn't have what's active then don't change anything.
            if count in active_list:
                t.active = True
            else:
                t.active = False
        out.append([t.active, t.name, t.filename, t.message])
        count +=1
        
    return out
        
#Main program
test_files = scan_folders(extension)
print test_files
test_list = import_test_files(test_files)

#import Main.airspeed_mod

