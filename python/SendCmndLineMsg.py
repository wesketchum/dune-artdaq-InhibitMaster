#!/usr/bin/env python

import sys
import time
import zmq
import InhibitMaster

def print_usage():
    print "Usage:\n\tSendCmndLineMessage.py <status_pub_node> <status> <marker>"

if len(sys.argv)!=4 or str(sys.argv[1])=="-h" or str(sys.argv[1])=="--help":
    print_usage()
    sys.exit()

pubnode="tcp://*:%s" % str(sys.argv[1])
print "Running SendCmndLineMsg status publisher on node %s" % pubnode

frontend_name = "SendCmndLineMsg"

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(pubnode)

time.sleep(0.5)

print "Socket bound. Will now send message"

mystr = InhibitMaster.CreateStatusMsg(frontend_name,sys.argv[3],sys.argv[2])
socket.send_string(mystr)
print "Sent string %s" % mystr
sys.exit()
