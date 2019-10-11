# from .satelliteSimulator import satSim 
#import gsAPI
from groundstation.gsAPI import ping 
#from satelliteSimulator.satSim import satSim

from groundstation.satelliteSimulator.satSim import Environment, Satellite, Simulator

def setSimulator(conn_strength, conn_stability, packet_drop_prob):
	environment = Environment(connection_strength=conn_strength, connection_stability=conn_stability,
        packet_drop_probability=packet_drop_prob)

	satellite = Satellite(components=[])
	return Simulator(environment, satellite)

def main():
	socket = setSimulator(10,10,.05)

	print(ping(socket))

main()
