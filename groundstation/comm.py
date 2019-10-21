# The Communications Module. Responsible for sending and retrieving data with the satellite.
# (or the simulator)


def send(socket, data):
	""" Pipes the incoming data (probably a Command tuple) to the socket (probably the Simulator)
		- socket (Simulator) : A Simulator instance
		- data (Tuple) : The collection of data to send to the socket.
	"""
	# This is where you should send information, data, or commands to the satellite or server.
	# (for now it's just the simulator)
	# eg of the tuple: 	('PING', [])
	return socket.send_to_sat(data)