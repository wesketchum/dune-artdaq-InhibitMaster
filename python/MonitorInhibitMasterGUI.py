#!/usr/bin/env python
import zmq
import InhibitMaster
import sys
import Tkinter

def print_usage():
    print "Usage:\n\tMonitorInhibitMasterGUI.py <InhibitMaster_pub_node>"

if len(sys.argv)!=2 or str(sys.argv[1])=="-h" or str(sys.argv[1])=="--help":
    print_usage()
    sys.exit()

context = zmq.Context()
subscriber = InhibitMaster.InhibitSUBNode(context)
subscriber.connect(str(sys.argv[1]))

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Quit',command=self.quit)
        self.quitButton.grid()

app = Application()
app.master.title('Sample application')
app.mainloop()

#while True:
#    msg = subscriber.recv_status_msg_timeout()
#    print msg
