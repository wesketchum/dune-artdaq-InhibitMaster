#ifndef INHIBITMASTERDEFINITIONS
#define INHIBITMASTERDEFINITIONS 1

#include "zmq.h"
#include "string.h"
#include <sys/time.h>
#include <unistd.h>

extern const char* STATUS_MSG_MARKER;//  = "STATUSMSG";
extern const char* INHIBIT_MSG_MARKER;// = "INHIBITMSG";

extern const char* STATUS_BAD;//  = "BAD";
extern const char* STATUS_GOOD;// = "GOOD";

#endif
