#!/usr/bin/env python

import sys
import time
import zmq
import InhibitMaster

def print_usage():
    print "Usage:\n\tFakeSpillInhibitor.py <cmd_pub_node>"

if len(sys.argv)!=2 or str(sys.argv[1])=="-h" or str(sys.argv[1])=="--help":
    print_usage()
    sys.exit()

cmd_node = sys.argv[1]
print "Running FakeSpillInhibitor status publisher, listening to commands from node %s" % cmd_node

frontend_name = "FakeSpillInhibitor"

context = zmq.Context()

pub_socket = context.socket(zmq.PUB)

cmd_socket = context.socket(zmq.SUB)
cmd_socket.connect(cmd_node)
cmd_socket.setsockopt(zmq.SUBSCRIBE, "CTRL")
 
# Initialize poll set
cmd_poller = zmq.Poller()
cmd_poller.register(cmd_socket, zmq.POLLIN)

next_msg_good = True
allow_time = 10.0
inhibit_time = 10.0
poll_time_ms = None
pubnode="tcp://*:6555"
            
while True:
    try:
        ready_sockets = dict(cmd_poller.poll(poll_time_ms))
    except KeyboardInterrupt:
        print "\n\nKeyboardInterrupt detected."
        mystr = InhibitMaster.CreateStatusMsg(frontend_name,"EndingFakeSpills",InhibitMaster.STATUS_GOOD)
        pub_socket.send_string(mystr)
        print "Sent string %s" % mystr
        sys.exit()

    if cmd_socket in ready_sockets:
        msg = cmd_socket.recv_string()

        if msg=="CTRL KILL" or msg=="CTRL QUIT" or msg=="CTRL EXIT":
            print "\n\nReceived exit command. Exiting..."
            mystr = InhibitMaster.CreateStatusMsg(frontend_name,"EndingFakeSpills",InhibitMaster.STATUS_GOOD)
            pub_socket.send_string(mystr)
            print "Sent string %s" % mystr
            sys.exit()
        elif "CTRL CONFIG" in msg:
            msg_list = msg.split(" ")
            if len(msg_list) != 5:
                print "\n\nReceived init message '%s', but it is malformed." % msg
                print "\nMessage format: 'CTRL CONFIG ALLOWTIME INHIBITTIME PUBPORT'"
            else:
                allow_time = float(msg_list[2])
                inhibit_time = float(msg_list[3])
                pubnode = "tcp://*:%d" % int(msg_list[4])
                print "\n\nConfigured FakeSpillInhibitor on pubnode=%s:" % pubnode
                print "Will allow triggers for %f seconds, and then interrupt for %f seconds." % (allow_time,inhibit_time)
            continue
        elif msg=="CTRL START":
            pub_socket.bind(pubnode)
            time.sleep(0.25)
            print "Starting FakeSpillInhibitor status publisher on node %s" % pubnode
            next_msg_good = False
            poll_time_ms = allow_time*1000.
            mystr = InhibitMaster.CreateStatusMsg(frontend_name,"SpillStart",InhibitMaster.STATUS_GOOD)
            pub_socket.send_string(mystr)
            print "Sent string %s" % mystr
            continue
        elif msg=="CTRL STOP":
            print "Stopping fake spill structure."
            next_msg_good = True
            poll_time_ms = None
            mystr = InhibitMaster.CreateStatusMsg(frontend_name,"StoppingFakeSpills",InhibitMaster.STATUS_GOOD)
            pub_socket.send_string(mystr)
            print "Sent string %s" % mystr
            pub_socket.unbind(pubnode)
            continue
        else:
            print "\n\nUnrecognized command '%s'" % msg
            continue

    else:
        if next_msg_good:
            next_msg_good = False
            poll_time_ms = allow_time*1000.
            mystr = InhibitMaster.CreateStatusMsg(frontend_name,"SpillBegin",InhibitMaster.STATUS_GOOD)
            pub_socket.send_string(mystr)
            print "Sent string %s" % mystr
            continue
        else:
            next_msg_good = True
            poll_time_ms = inhibit_time*1000.
            mystr = InhibitMaster.CreateStatusMsg(frontend_name,"SpillEnd",InhibitMaster.STATUS_BAD)
            pub_socket.send_string(mystr)
            print "Sent string %s" % mystr
            continue
