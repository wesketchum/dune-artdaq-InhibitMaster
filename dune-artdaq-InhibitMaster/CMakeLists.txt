# basic source code CMakeLists.txt

INCLUDE_DIRECTORIES($ENV{ZEROMQ_INC})
LINK_DIRECTORIES($ENV{ZEROMQ_LIB})
INCLUDE_DIRECTORIES($ENV{DIM_INC})
LINK_DIRECTORIES($ENV{DIM_LIB})

cet_make_library( LIBRARY_NAME InhibitMaster_CommonTools
		  SOURCE StatusPublisher.cc InhibitMasterDefinitions.C
		  LIBRARIES zmq
			    ${FHICLCPP}
  			    ${CETLIB}
  			    ${CETLIB_EXCEPT}
                )

cet_make_exec( TriggerManager
	       SOURCE TriggerManager.C
	       LIBRARIES zmq InhibitMaster_CommonTools )

cet_make_exec( MonitorInhibitMaster_DIM
	       SOURCE MonitorInhibitMaster_DIM.cc
	       LIBRARIES zmq
	       		 dim pthread InhibitMaster_CommonTools)

install_headers()
install_source()
install_fhicl()
