#!/usr/bin/env python

import sys
import time
import zmq
import InhibitMaster

def print_usage():
    print "Usage:\n\tFakeSpillInhibitor_CmdLine.py <status_pub_node> <allow_time_s> <inhibit_time_s>"

if len(sys.argv)!=4 or str(sys.argv[1])=="-h" or str(sys.argv[1])=="--help":
    print_usage()
    sys.exit()

pubnode="tcp://*:%s" % str(sys.argv[1])
print "Running FakeSpillInhibitor_CmdLine status publisher on node %s" % pubnode

allow_sleep = float(sys.argv[2])
inhibit_sleep = float(sys.argv[3])

print "\n\nWill allow triggers for %f seconds, and then interrupt for %f seconds." % (allow_sleep,inhibit_sleep)
print "To quit cleanly, do Ctrl-C, and the inhibit will be left in the allow state.\n"

frontend_name = "FakeSpillInhibitor_CmdLine"

context = zmq.Context()
pub_socket = context.socket(zmq.PUB)
pub_socket.bind(pubnode)

while True:
    try:
        mystr = InhibitMaster.CreateStatusMsg(frontend_name,"SpillStart",InhibitMaster.STATUS_GOOD)
        pub_socket.send_string(mystr)
        print "Sent string %s" % mystr
        time.sleep(allow_sleep)

        mystr = InhibitMaster.CreateStatusMsg(frontend_name,"SpillEnd",InhibitMaster.STATUS_BAD)
        pub_socket.send_string(mystr)
        print "Sent string %s" % mystr
        time.sleep(inhibit_sleep)

    except KeyboardInterrupt:
        print "\n\nKeyboardInterrupt detected."
        mystr = InhibitMaster.CreateStatusMsg(frontend_name,"EndingFakeSpills",InhibitMaster.STATUS_GOOD)
        pub_socket.send_string(mystr)
        print "Sent string %s" % mystr
        sys.exit()

