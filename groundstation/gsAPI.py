#This file contains a list of functions or logic that serves as interactions
from testcomm import send 
import satelliteSimulator.satSim

def ping(socket):
	ping = Ping(1,1200,10)
	return send(socket, Ping.getCommand())






