#!/usr/bin/env python
import zmq
import InhibitMaster
import sys

def print_usage():
    print "Usage:\n\tMonitorInhibitMaster.py <InhibitMaster_pub_node>"

if len(sys.argv)!=2 or str(sys.argv[1])=="-h" or str(sys.argv[1])=="--help":
    print_usage()
    sys.exit()

context = zmq.Context()
subscriber = InhibitMaster.InhibitSUBNode(context)
subscriber.connect(str(sys.argv[1]))

while True:
    msg = subscriber.recv_status_msg_timeout()
    print msg
