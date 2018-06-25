# basic source code CMakeLists.txt

INCLUDE_DIRECTORIES($ENV{ZEROMQ_INC})
LINK_DIRECTORIES($ENV{ZEROMQ_LIB})
INCLUDE_DIRECTORIES($ENV{DIM_INC})
LINK_DIRECTORIES($ENV{DIM_LIB})

cet_make_exec( TriggerManager
	       SOURCE TriggerManager.C
	       LIBRARIES zmq)

cet_make_exec( MonitorInhibitMaster_DIM
	       SOURCE MonitorInhibitMaster_DIM.cc
	       LIBRARIES zmq
	       		 dim pthread )

cet_make_library( LIBRARY_NAME InhibitMaster_CommonTools
		  SOURCE StatusPublisher.cc
		  LIBRARIES zmq
			    ${FHICLCPP}
  			    ${CETLIB}
  			    ${CETLIB_EXCEPT}
                )

install_headers()
install_source()
install_fhicl()
