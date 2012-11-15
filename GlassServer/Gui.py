from Tkinter import *
import tkFont, tkMessageBox
import GlassServer
import threading
import webbrowser
import time, socket
import logging


class GlassServerApp(threading.Thread):
    def __init__(self):
        self.mainloop = GlassServer.mainloop
        threading.Thread.__init__(self)
    
    def run(self):
        self.mainloop.run()
    
    def quit(self):
        self.mainloop.quit()
    
    def restart(self):
        self.mainloop.restart()
class GlassServer_Status(object):
    def __init__(self, parent, ip, webport):
        self.frame = Frame(parent)
        
        self.label = Label(self.frame)
        
        self.label["text"] = "GlassServer: IP: %s   Port: %d" %(ip,webport)
        
        
    
    def pack(self):
        self.label.pack(side=LEFT)
      
        self.frame.pack(fill=X,padx=10)
   
        
class WebServer_Status(object):
    def __init__(self, parent, webport):
        self.frame = Frame(parent)
        
        self.label = Label(self.frame)
        
        self.label["text"] = "WebServer:"
        self.label2 = Label(self.frame)
        self.label2["text"] = "Running on Port:  %d" %webport
        self.link = Label(self.frame, fg="#00d")
        self.link["text"] = "http://localhost:%d/WebServer" %webport
        self.link["font"] = tkFont.Font(underline = 1, size = 10)
        self.link["cursor"] = "hand2"
        self.link.bind("<Button-1>", self.weblink)
        
    def pack(self):
        self.label.pack(side=LEFT)
        self.label2.pack(side=LEFT)
        self.link.pack(side=LEFT)
        self.frame.pack(fill=X, padx=10)
    def weblink(self, event):
        webbrowser.open(self.link["text"])

class Application(Frame):
    
    def createWidgets(self, webport, serverport, ip):
        photo = PhotoImage(file="rjglass.GIF")
        self.img = Label(self, image=photo)
        self.img.photo = photo
        self.img.pack()
        self.gs = GlassServer_Status(self, ip, serverport)
        self.ws = WebServer_Status(self, webport)
       # self.ws2 = WebServer_Status(self)
        self.gs.pack()
        self.ws.pack()
        #self.ws2.pack()
        self.QUIT = Button(self)
        self.QUIT["text"] = "Quit / Shutdown all Servers"
        self.QUIT["fg"]   = "black"
        self.QUIT["command"] =  self.comm_quit
        self.QUIT.pack(pady = 10, fill=X, padx = 40)
      #  self.restart = Button(self)
      #  self.restart["text"] = "RESTART"
      #  self.restart["command"] =  self.comm_restart
      #  self.restart.pack()

    
    def __init__(self, master=None, glassserverapp = None):
        Frame.__init__(self, master)
        self.glassclass = glassserverapp
        self.glassserver = glassserverapp()
        self.glassserver.start()
        webport = self.glassserver.mainloop.webserver.port
        serverport = self.glassserver.mainloop.controller.Glass_Server.port
        ip = socket.gethostbyname(socket.gethostname())
        self.pack()

        self.createWidgets(webport, serverport, ip)
        
        
    def comm_quit(self):
        logging.info("Gui - Communication Quit")
        self.glassserver.quit()
        logging.info("Gui - Quite Gui")
        self.quit()
        
    #def comm_restart(self):
    #    print "COMMRESTART"
    #    self.glassserver.restart()
       
    
def callback():
    if tkMessageBox.askokcancel("Quit Shutdown Servers", "Do you really wish to quit and shutdown all servers?"):
        app.glassserver.quit()
        time.sleep(.71)
        root.destroy()

root = Tk()
root.title("Glass Server")
#root.wm_iconbitmap('D:/Python26/DLLs/py.ico') #Create new icon.
root.protocol("WM_DELETE_WINDOW", callback)

app = Application(master=root, glassserverapp=GlassServerApp)
#glassserver.start()
app.mainloop()
#root.destroy()

#root.after(2000,task)
#root.mainloop()