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
    satellite = Satellite(satellite_components, 'Passive', 16)
    simulator = Simulator(environment, satellite)
    del environment, satellite

    # Now we can try the API
    print("Pinging satellite for a stable connection...")
    
    # Just as a throwaway example
    # This particular example with the loop might also go in groundapi...
    i = 0
    a = 0
    while i < 5:
        time.sleep(0.5)
        response = ping(simulator)
        a += 1
        print(response)
        if response != "PING-RESPONSE":
            i = 0 # Retry...
        else:
            i+=1

        if a >= 50:
            # Currently lacking functionality to fix connection issues.
            print("Satellite is experiencing connection issues.")
            a = 0

    print("Recieved 5 responses, it's probably safe to continue...")

    # After which we run through the housekeeping and startup checks.
    housekeeping = simulator.send_to_sat(('GET-HK'))
    if housekeeping['satelliteMode'] == 'Danger' or 'Critical':
        print("Satellite is experiencing an emergency!")
        # We'll want to send out emails to the admins here.

    if housekeeping['batteryVoltage'] < 15.3:
        print("Battery voltage critical. Shutting down all components.")
        for component in satellite_components:
            simulator.send_to_sat(('TURN-OFF', component.name))
    elif housekeeping['batteryVoltage'] < 15.6:
        # Shutdown components based on some kind of priority system?
        print("Battery voltage low. Shutting down low priority components.")
        simulator.send_to_sat(('TURN-OFF', satellite_components[0].name))

    if housekeeping['currentIn'] >= 0.4:
        # Missing current channels functionality.
        # Tied to different components, so turn them off then on again?
        print("Over-current detected.")
        simulator.send_to_sat(('TURN-OFF', satellite_components[0].name))
        time.sleep(5)
        simulator.send_to_sat(('TURN-ON', satellite_components[0].name))

    log = HousekeepingLogList()
    log.post(housekeeping)
    time.sleep(2)

    # That's housekeeping taken care of, so next is watchdogs. 
    # ... Which is currently not finished in groundapi.py and isn't in satSim.py
    print("Petting Watch Dog timers.")
    time.sleep(2)

    # Update clock/gps
    simulator.send_to_sat(('TURN-ON', 'GPS'))
    # Missing functionality. 
    print('Syncronized Satellite to: ', time.localtime())



if __name__ == '__main__':
    # Script is being run directly
    main()
else:
    # we're being imported...
    pass
