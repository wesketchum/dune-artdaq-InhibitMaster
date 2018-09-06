#!/usr/bin/env python
import zmq
import InhibitMaster
import sys

def print_usage():
    print "Usage:\n\tMonitorFrontEnds.py <status_publisher_node_list>"

if len(sys.argv)!=2 or str(sys.argv[1])=="-h" or str(sys.argv[1])=="--help":
    print_usage()
    sys.exit()

context = zmq.Context()
subscriber = InhibitMaster.StatusSUBNode(context)

node_list_file = open(sys.argv[1],"r")
for line in node_list_file:
    myline = line.split(" ")
    print "Adding status publisher %s with socket %s" % (myline[0],myline[1])
    subscriber.connect(myline[1])

while True:
    msg = subscriber.recv_status_msg_timeout()
    if msg!="TIMEOUT":
        print msg
