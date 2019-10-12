# This file contains a list of functions or logic that serves as interactions.
# with the comm. module. The comm. module will handle the actual communication with the SAT.

from groundstation.comm import send
from commands import *


def ping(socket):
	""" Create a Ping command and send it to the socket.
		- socket (Simulator) : A Simulator instance
	"""
	ping = Ping(name=1, timeout=1200, size=10)
	return send(socket, ping.getTuple())


def get_hk(socket):
	""" Create a Get HK command and send it to the socket.
	"""
	return ""