#!/usr/bin/env python

import sys
import time
import zmq
import InhibitMaster

def print_usage():
    print "Usage:\n\tTestFrontEnd.py <status_pub_node>"

if len(sys.argv)!=2 or str(sys.argv[1])=="-h" or str(sys.argv[1])=="--help":
    print_usage()
    sys.exit()

pubnode="tcp://*:%s" % str(sys.argv[1])
print "Running TestFrontEnd status publisher on node %s" % pubnode

frontend_name = "TestFrontEnd"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(pubnode)

counter = 0
while True:
    status = InhibitMaster.STATUS_GOOD
    if counter%10==0:
        status = InhibitMaster.STATUS_BAD
    mystr = InhibitMaster.CreateStatusMsg(frontend_name,"*",status)
    socket.send_string(mystr)
    print "Sent string %s" % mystr
    counter+=1
    time.sleep(1)
