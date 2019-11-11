# The Communications Module. Responsible for sending and retrieving data with the satellite.
# (or the simulator)
import groundstation.satellite_simulator.antenna as antenna

def send(socket, data):
	""" Pipes the incoming data (probably a Command tuple) to the socket (probably the Simulator)
		- socket (something that implements .send(data) interface):
		- data (str) : Message string
	"""
	return socket.send(data)

def example():
    telecommands = ['ping', 'get-hk', 'turn-on gps', 'ping', 'get-hk']
    for telecommand in telecommands:
        resp = send(antenna, telecommand)
        print(resp)


if __name__=='__main__':
    example()
