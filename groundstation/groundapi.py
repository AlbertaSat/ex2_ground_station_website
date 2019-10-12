# This file contains a list of functions or logic that serves as interactions.
# with the comm. module. The comm. module will handle the actual communication with the SAT.

from groundstation.comm import send 

def ping(socket):
	ping = Ping(1,1200,10)
	return send(socket, Ping.getCommand())
	