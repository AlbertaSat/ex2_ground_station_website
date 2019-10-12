# This is a demo for how to interface with the API.
# The API will subsequently use the comm. module to send and receive data from the satellite.
# For now, the "satellite" is just the simulator.

import groundstation.groundapi

def main():
	# We could do an input loop or something here, but instead I'll just do an example
	print("Pinging satellite for a stable connection...")
	# TODO: call connect() or smth from API
	pass

if __name__ == '__main__':
    # Script is being run directly
	main()
else:
	# we're being imported...
	pass



# from groundstation.satelliteSimulator.satSim import Environment, Satellite, Simulator

# def setSimulator(conn_strength, conn_stability, packet_drop_prob):
# 	environment = Environment(connection_strength=conn_strength, connection_stability=conn_stability,
#         packet_drop_probability=packet_drop_prob)

# 	satellite = Satellite(components=[])
# 	return Simulator(environment, satellite)

# def main():
# 	socket = setSimulator(10,10,.05)

# 	print(ping(socket))

# main()
