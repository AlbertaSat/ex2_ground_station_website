# This is a demo for how to interface with the API.
# The API will subsequently use the comm. module to send and receive data from the satellite.
# For now, the "satellite" is just the simulator.

import time
import json
from datetime import datetime
from groundstation.groundapi import ping
from groundstation.satelliteSimulator.satSim import Environment, Satellite, SatelliteComponent, Simulator
from groundstation.backend_api.housekeeping import HousekeepingLogList
from groundstation.tests.utils import fakeHousekeepingAsDict


def main():

    # At the beginning of the demo, we start the simulator (for lack of a real satellite)
    print("Starting satellite simulator...")
    environment = Environment(connection_strength=7, connection_stability=7, packet_drop_probability=0.05)
    def effect_of_gps_on(old_value):
        new_value = old_value - 0.01
        return new_value
    satellite_components = [SatelliteComponent('GPS', [('batteryVoltage', effect_of_gps_on)], []),]
    satellite = Satellite(satellite_components)
    simulator = Simulator(environment, satellite)
    del environment, satellite

    # Now we can try the API
    print("Pinging satellite for a stable connection...")
    
    # Just as a throwaway example
    # This particular example with the loop might also go in groundapi...
    i = 0
    while i < 5:
        time.sleep(0.5)
        response = ping(simulator)
        print(response)
        if response != "PING-RESPONSE":
            i = 0 # Retry...
        else:
            i+=1
    print("Recieved 5 responses, it's probably safe to continue...")


if __name__ == '__main__':
    # Script is being run directly
    main()
else:
    # we're being imported...
    pass
