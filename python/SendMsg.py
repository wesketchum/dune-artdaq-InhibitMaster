#!/usr/bin/env python

import sys
import time
import zmq
import InhibitMaster

def print_usage():
    print "Usage:\n\tSendMsg.py <status_pub_node> <msg>"

if len(sys.argv)!=3 or str(sys.argv[1])=="-h" or str(sys.argv[1])=="--help":
    print_usage()
    sys.exit()

pubnode="tcp://*:%s" % str(sys.argv[1])

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(pubnode)

time.sleep(0.5)
msg = str(sys.argv[2])
socket.send_string(msg)
print "Sent string  '%s'" % msg
sys.exit()
