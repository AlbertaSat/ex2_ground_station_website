import helpers
import random
import json
import time

class Environment:

    def __init__(self, connection_strength, connection_stability, packet_drop_probability):
        """
        params:
            - connection_strength (int) : value between [1 (weak), 10 (strong)]
            - connection_stability (int) : value between [1 (weak), 10 (strong)]
            - packet_drop_probability (float) : probability that the command won't reach the satellite
        """
        self.connection_strength = connection_strength
        self.connection_stability = connection_stability
        self.packet_drop_probability = packet_drop_probability

    def step(self):
        """Moves the environment one time step, change environment state in here
        """
        pass

class SatelliteComponent:

    def __init__(self, name, effects_when_on, effects_when_off):
        """
        params:
            - name (string) : name of the component
            - effects_when_on (list of 2 valued tuples)
                * where each tuple is of form (attr, effect_func)
                * effect_func is a function reference that has one parameter and returns one value
                    * the satellite attribute corresponding to attr will be passed into
                    the effect_func, effect_func will calculate and return the new_value.
            - effects_when_off (list of 2 valued tupled), same concept as effects_when_on
        """
        self.name = name
        self.effects_when_on = effects_when_on
        self.effects_when_off = effects_when_off
        self.is_on = False

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False


class Satellite:

    sat_modes =  ['Danger', 'Critical', 'Passive', 'Active Mission']

    def __init__(self, components, satelliteMode=sat_modes[2], batteryVoltage=4,
        currentIn=0.3, currentOut=0.3, noMCUResets=0,
        lastBeaconTime=None, currentTime=0, beaconInterval=20):

        # model attributes
        self.satelliteMode = satelliteMode
        self.batteryVoltage = batteryVoltage
        self.currentIn = currentIn
        self.currentOut = currentOut
        self.noMCUResets = noMCUResets
        self.lastBeaconTime = lastBeaconTime

        self.currentTime = currentTime
        self.time_till_next_beacon = beaconInterval
        # a dict, {component_name:component_object}

        # convert list of components to dict for easier searching
        self.components = {c.name:c for c in components}

        # beacons will be 'broadcast' to this file every beacon interval
        self.BEACON_BROADCAST_FILE = 'beacons.txt'
        self.BEACON_INTERVAL = beaconInterval


    def step(self):
        """Moves the satellite one time step, change satellite state here
        """
        self.currentTime += 1
        self.time_till_next_beacon  -= 1

        self._apply_component_effects_on_satellite_state()

        if self.time_till_next_beacon == 0:
            self._broadcast_beacon()
            self.time_till_next_beacon = self.BEACON_INTERVAL


    def _apply_component_effects_on_satellite_state(self):
        for component_name, component in self.components.items():
            effects = component.effects_when_on if component.is_on else component.effects_when_off

            for effect in effects:
                attr, effect_function = effect
                new_val = effect_function(getattr(self, attr))
                setattr(self, attr, new_val)


    def _turn_on_component(self, component_name):

        # NOTE: Not sure if I should catch exceptions if component does not exist
        component = self.components[component_name]
        component.turn_on()


    def _turn_off_component(self, component_name):
        component = self.components[component_name]
        component.turn_off()


    def _get_hk_as_dict(self):
        lb = self.lastBeaconTime if self.lastBeaconTime is not None else ''
        return {
            'satelliteMode':self.satelliteMode,
            'batteryVoltage':self.batteryVoltage,
            'currentIn':self.currentIn,
            'currentOut':self.currentOut,
            'noMCUResets':self.noMCUResets,
            'lastBeaconTime':lb
        }


    def _broadcast_beacon(self):
        self.lastBeaconTime = self.currentTime
        with open(self.BEACON_BROADCAST_FILE, 'a+') as f_ptr:
            hk_json = json.dumps(self._get_hk_as_dict(), indent=4)
            f_ptr.write(hk_json)


    def send(self, data, environment):
        """Send data to the satellite via here
        params:
            - data (tuple) : a 2 valued tuple, eg.) (command_name, [arg1, ..., argn])
        return:
            - depends, idk, probably always a string for now
        """
        command_name, args = data
        response = ''

        # determine if we will drop the request (based on connection)
        if random.random() <= environment.packet_drop_probability:
            # drop packet
            return 'NO-RESPONSE'

        if command_name == 'PING':
            response = 'PING-RESPONSE'
        elif command_name == 'GET-HK':
            response = json.dumps(self._get_hk_as_dict())
        elif command_name == 'TURN-ON':
            # expecting one string in args, 'component_name' to turn on
            self._turn_on_component(args[0])
            response = '200 OK'
        elif command_name == 'TURN-OFF':
            # expecting one string in args, 'component_name' to turn off
            self._turn_off_component(args[0])
            response = '200 OK'
        else:
            response = 'UNRECOGNIZED-COMMAND'

        response_latency = helpers.calculate_semi_random_latency(environment.connection_strength, environment.connection_stability)
        time.sleep(response_latency)
        # TODO: separate incoming dropped packets with outgoing dropped packets
        #       i.e.) packets sent to satellite might not even reach it (essentially what we have rn)
        #           * but there is also the case where sat recieves, telecommand, executes, but we dont get its response (we need to add this)
        return response

class Simulator:

    def __init__(self, environment, satellite):
        self.environment = environment
        self.satellite = satellite

    def send_to_sat(self, data):
        sat_resp = self.satellite.send(data, self.environment)
        return sat_resp

    def step(self):
        """Step environment and satellite one step
        """
        self.environment.step()
        self.satellite.step()


def minimal_example():

    environment = Environment(connection_strength=10, connection_stability=10,
        packet_drop_probability=0.05)
    satellite = Satellite(components=[])

    simulator = Simulator(environment, satellite)
    del environment, satellite

    data = ('PING', [])
    resp = simulator.send_to_sat(data)
    print(resp)


def example_usage():

    environment = Environment(connection_strength=7, connection_stability=7,
        packet_drop_probability=0.05)

    def effect_of_gps_on(old_value):
        new_value = old_value - 0.01
        return new_value

    satellite_components = [
        SatelliteComponent('GPS', [('batteryVoltage', effect_of_gps_on)], []),
        ]
    satellite = Satellite(satellite_components)
    simulator = Simulator(environment, satellite)
    del environment, satellite

    data = ('GET-HK', [])
    resp = simulator.send_to_sat(data)
    print(resp)

    data = ('TURN-ON', ['GPS'])
    resp = simulator.send_to_sat(data)
    print(resp)

    for i in range(50):
        simulator.step()

    data = ('GET-HK', [])
    resp = simulator.send_to_sat(data)
    print(resp)


def run_interactively():

    from ast import literal_eval as make_tuple

    print('--- ENTER DATA TO SEND, enter \'Q\' to quit ---')

    environment = Environment(10, 10, 0.05)

    def effect_of_gps_on(old_value):
        new_value = old_value - 0.01
        return new_value

    satellite_components = [SatelliteComponent('GPS', [('batteryVoltage', effect_of_gps_on)], [])]
    satellite = Satellite(satellite_components)
    simulator = Simulator(environment, satellite)
    del environment, satellite

    while 1:
        inp = input('> ')
        if inp == 'Q':
            break
        resp = simulator.send_to_sat(make_tuple(inp))
        print('response: {}'.format(resp))

        simulator.step()



def main():

    minimal_example()




if __name__=="__main__":
    main()
