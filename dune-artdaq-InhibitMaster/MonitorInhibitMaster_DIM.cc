#define TRACE_NAME "MonitorInhibitMasterDIM"
//#include "artdaq/DAQdata/Globals.hh"
#include "trace.h"

#include <unistd.h>
#include <dim/dis.hxx>

#include <iostream>
#include <string>
#include <vector>
#include <boost/algorithm/string.hpp>

#include "InhibitMasterDefinitions.h"

enum {
  TERROR=0,
  TWARNING=1,
  TINFO=2,
  TDEBUG=3,
};

int main(int argc, char* argv[])
{

  if(argc!=3){
    std::cout << "Usage:  MonitorInhibitMaster_DIM InhitbitMaster_HostName InhibitMaster_Port" << std::endl;
    return 1;
  }

  char ih_zmq_port[256];
  char dim_service_detail_name[256];
  char dim_service_name[256];
  char dim_server_name[256];

  sprintf(ih_zmq_port,"tcp://%s:%s",argv[1],argv[2]);
  sprintf(dim_service_name,"Artdaq/InhibitMaster%s/monitoring/status",argv[2]);
  sprintf(dim_service_detail_name,"Artdaq/InhibitMaster%s/monitoring/status_detail",argv[2]);
  sprintf(dim_server_name,"InhibitMaster%s",argv[2]);

  TRACEN(TRACE_NAME,TINFO,"InhibitMaster ZMQ port = %s",ih_zmq_port);
  TRACEN(TRACE_NAME,TINFO,"DIM Service Name, status: %s",dim_service_name);
  TRACEN(TRACE_NAME,TINFO,"DIM Service Name, status detail: %s",dim_service_detail_name);
  TRACEN(TRACE_NAME,TINFO,"DIM Server Name: %s",dim_server_name);

  //ZeroMQ Setup
  //  Prepare our context and publisher
  void *context = zmq_ctx_new ();
  void *subscriber = zmq_socket (context, ZMQ_SUB);
  int rc = zmq_connect (subscriber,ih_zmq_port);
  
  const int hwm=1;
  rc = zmq_setsockopt (subscriber,
		       ZMQ_SUBSCRIBE,
		       INHIBIT_MSG_MARKER,
		       strlen (INHIBIT_MSG_MARKER));
  rc = zmq_setsockopt(subscriber,ZMQ_RCVHWM,&hwm,sizeof(int));

  //printf("Everything is set up...%d\n",rc);
  TRACEN(TRACE_NAME,TINFO,"ZMQ receiver setup with return code %d",rc);
  
  struct timeval timenow;
  char recv_buf[256];
  int  status_code=-1;
  std::string recv_str;
  std::vector<std::string> split_strings;

  DimService _dim_service(dim_service_name,status_code);
  DimService _dim_service_detail(dim_service_detail_name,recv_buf);
  DimServer  _dim_server;
  _dim_server.setDnsNode("np04-srv-010.cern.ch",2505);    
  _dim_server.start(dim_server_name);
    
  while(true){

    int msg_size = zmq_recv(subscriber,recv_buf,256,ZMQ_DONTWAIT);
    gettimeofday(&timenow,NULL);

    if(msg_size<0){
      usleep(100000);
      TRACEN(TRACE_NAME,TDEBUG,"No message received. Sleep 100 ms.");
    }

    else{
      TRACEN(TRACE_NAME,TDEBUG,
	       "%s received at %ld seconds and %ld microseconds",
	       recv_buf,timenow.tv_sec,timenow.tv_usec);
      _dim_service_detail.updateService(recv_buf);
      
      recv_str = std::string(recv_buf);
      boost::split(split_strings,recv_str,boost::is_any_of("_"));
      if(split_strings.size() < 3)
	TRACEN(TRACE_NAME,TERROR,"Poorly formatted IH message! %s",recv_str.c_str());
      else{
	if(split_strings[1]=="XON")
	  status_code=0;
	else
	  status_code=1;
	TRACEN(TRACE_NAME,TDEBUG,"Updating status code to value %d (%s)",
		 status_code,split_strings[1].c_str());
	_dim_service.updateService(status_code);	
      }

    }
  }

  zmq_close (subscriber);
  zmq_ctx_destroy (context);
  return 0;


}
