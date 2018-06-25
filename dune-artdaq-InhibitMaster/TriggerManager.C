#include "zmq.h"
#include "string.h"
#include <sys/time.h>
#include <unistd.h>

#include "InhibitMasterDefinitions.h"

int main(){

  //  Prepare our context and publisher
  void *context = zmq_ctx_new ();
  void *subscriber = zmq_socket (context, ZMQ_SUB);
  int rc = zmq_connect (subscriber, "tcp://localhost:5556");
  
  const int hwm=1;
  rc = zmq_setsockopt (subscriber,
		       ZMQ_SUBSCRIBE,
		       INHIBIT_MSG_MARKER,
		       strlen (INHIBIT_MSG_MARKER));
  rc = zmq_setsockopt(subscriber,ZMQ_RCVHWM,&hwm,sizeof(int));

  printf("Everything is set up...%d\n",rc);
  
  struct timeval timenow;
  char recv_buf[256];

  while(true){

    int msg_size = zmq_recv(subscriber,recv_buf,256,ZMQ_DONTWAIT);
    gettimeofday(&timenow,NULL);

    if(msg_size<0)
      usleep(100000);

    else
      printf("%s received at %ld seconds and %ld microseconds\n",recv_buf,timenow.tv_sec,timenow.tv_usec);    
  }

  zmq_close (subscriber);
  zmq_ctx_destroy (context);
  return 0;
     
}
