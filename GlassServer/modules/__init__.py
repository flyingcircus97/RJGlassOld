#!/usr/bin/env python
# ----------------------------------------------------------
# Modules - Glass Server
# ----------------------------------------------------------
# Folder where all Modules are held for glass server.
#
# This init.py file, will load in all modules found within
# 

# ---------------------------------------------------------------
import os, sys

extension = '_mod.py'
variable_name = 'variable.xml'

def scan_folders(extension, variable_name):
    #Scan through all folders within modules looking for _mod.py files.
    #And also variable.txt files.
    ext_len = len(extension)
    mod_py_files = []
    variable_txt_files = []
    for root, dirs, files in os.walk(__name__):
        #print root, dirs, files
        for f in files:
            #Scan through files, find ones with correct extension.
            if f[-ext_len:] == extension:
                mod_py_files.append(os.path.join(root, f))
            if f == variable_name:
                variable_txt_files.append(os.path.join(root,f))
                
    return mod_py_files, variable_txt_files
    
def import_mod_files(mod_files):
    #print mod_files
    list = []
    for f in mod_files:
        mod_name = f[:-3].replace(os.sep,'.')
        print mod_name
        try:
           exec('import ' + mod_name)
        except ImportError:
           print "IMPORT ERROR"
           print os.path.split(sys.path[0])[0] + '\\modules'
           sys.path.append(os.path.split(sys.path[0])[0])
           exec('import ' + 'modules.' + mod_name)
        exec('list.append(%s)' %mod_name)
    return list

#Main program
mod_files, variable_files = scan_folders(extension, variable_name)
mod_list = import_mod_files(mod_files)
#import Main.airspeed_mod

