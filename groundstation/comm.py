# The Communications Module. Responsible for sending and retrieving data with the satellite.
# (or the simulator)


# def setSimulator(conn_strength, conn_stability, packet_drop_prob):
# 	environment = Environment(connection_strength=conn_strength, connection_stability=conn_stability,
#         packet_drop_probability=packet_drop_prob)

# 	satellite = Satellite(components=[])
# 	return Simulator(environment, satellite)


def send(socket, data):

	return socket.send_to_sat(data)