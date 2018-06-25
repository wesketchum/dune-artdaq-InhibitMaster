#include "trace.h"

#include "StatusPublisher.hh"
#include "fhiclcpp/ParameterSet.h"
#include <sstream>

artdaq::StatusPublisher::StatusPublisher(fhicl::ParameterSet const& ps) :
  StatusPublisher(ps.get<std::string>("IHProcessName",""),
		  ps.get<std::string>("IHPublisherAddress",""),
		  ps.get<uint8_t>("IHTRACELVL",60))
{
}

artdaq::StatusPublisher::StatusPublisher(std::string name,
					 fhicl::ParameterSet const& ps) :
  StatusPublisher(name,
		  ps.get<std::string>("IHPublisherAddress",""),
		  ps.get<uint8_t>("IHTRACELVL",60))
{
}
artdaq::StatusPublisher::StatusPublisher(std::string name,
					 std::string address,
					 uint8_t tracelvl) :
  fProcessName(name),
  fPublisherAddress(address),
  fTRACELVL(tracelvl),
  fDisable(fPublisherAddress.size()==0)
{
  if(fDisable) return;

  sprintf(fTRACE_NAME,"%s",fProcessName.c_str());

  fZMQContextPtr = zmq_ctx_new ();
  fZMQPublisherPtr = zmq_socket (fZMQContextPtr, ZMQ_PUB);

  TRACEN(fTRACE_NAME,fTRACELVL,
	 "Instantiated StatusPublisher: %s at %s",
	 fProcessName.c_str(),fPublisherAddress.c_str());
}

artdaq::StatusPublisher::~StatusPublisher()
{
  if(fDisable) return;

  zmq_close(fZMQPublisherPtr);
  zmq_ctx_destroy(fZMQContextPtr);
  TRACEN(fTRACE_NAME,fTRACELVL,"StatusPublisher %s destroyed",fProcessName.c_str());
}

int artdaq::StatusPublisher::BindPublisher()
{
  if(fDisable) return -999;

  int rc = zmq_bind(fZMQPublisherPtr,fPublisherAddress.c_str());

  TRACEN(fTRACE_NAME,fTRACELVL,"StatusPublisher %s bound at %s (error code=%d)",
	 fProcessName.c_str(),fPublisherAddress.c_str(),rc);

  return rc;
}

void artdaq::StatusPublisher::PublishStatus(const char* status,
					    std::string marker)
{
  if(fDisable) return;

  gettimeofday(&fTimeStamp,NULL);
  std::stringstream ss;
  ss << STATUS_MSG_MARKER << "_" 
     << fProcessName << "_"
     << marker.c_str() << "_"
     << status << "_"
     << fTimeStamp.tv_sec << "." << fTimeStamp.tv_usec;

  TRACEN(fTRACE_NAME,fTRACELVL,
	 "StatusPublisher %s sending: %s",
	 fProcessName.c_str(),ss.str().c_str());

  zmq_send(fZMQPublisherPtr,ss.str().c_str(),ss.str().size(),0);
}

void artdaq::StatusPublisher::PublishBadStatus(std::string marker)
{
  PublishStatus(STATUS_BAD,marker);
}
void artdaq::StatusPublisher::PublishGoodStatus(std::string marker)
{
  PublishStatus(STATUS_GOOD,marker);
}
