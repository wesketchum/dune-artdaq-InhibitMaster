#!/usr/bin/env python
import zmq
import InhibitMaster
import sys

def print_usage():
    print "Usage:\n\tRunInhibitMaster.py <InhibitMaster_pub_node> <status_publisher_node_list>"

if len(sys.argv)!=3 or str(sys.argv[1])=="-h" or str(sys.argv[1])=="--help":
    print_usage()
    sys.exit()

pubnode="tcp://*:%s" % str(sys.argv[1])
print "Running InhibitMaster publisher on node %s" % pubnode

context = zmq.Context()
publisher = InhibitMaster.InhibitPUBNode(context,pubnode)

subscriber = InhibitMaster.StatusSUBNode(context)

node_list_file = open(sys.argv[2],"r")
for line in node_list_file:
    myline = line.split(" ")
    print "Adding status publisher %s with socket %s" % (myline[0],myline[1])
    subscriber.connect(myline[1])

im = InhibitMaster.InhibitMaster(0.5)

im.run(subscriber,publisher)
