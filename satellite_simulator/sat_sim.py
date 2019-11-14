import sys
from . import helpers
import random
import json
import time
from ast import literal_eval as make_tuple
import os

class Environment:

    def __init__(self, connection_strength, connection_stability, packet_drop_probability, no_delay=False):
        """
        params:
            - connection_strength (int) : value between [1 (weak), 10 (strong)]
            - connection_stability (int) : value between [1 (weak), 10 (strong)]
            - packet_drop_probability (float) : probability that the command won't reach the satellite
            - no_delay (bool) : if this is true, responses will be instant regardless of strength/stability
        """
        self.connection_strength = connection_strength
        self.connection_stability = connection_stability
        self.packet_drop_probability = packet_drop_probability
        self.no_delay = no_delay

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

    def __init__(self, components, satellite_mode=sat_modes[2], battery_voltage=4,
        current_in=0.3, current_out=0.3, no_MCU_resets=0,
        last_beacon_time=None, current_time=helpers.get_unix_time(), beacon_interval=20):
        """
        Attributes:
            - flight_schedule (string) : a path to the flight schedule file.
                * assumes each timestep in the fs is unique
        """

        # model attributes
        self.satellite_mode = satellite_mode
        self.battery_voltage = battery_voltage
        self.current_in = current_in
        self.current_out = current_out
        self.no_MCU_resets = no_MCU_resets
        self.last_beacon_time = last_beacon_time

        self.current_time = current_time
        self.time_till_next_beacon = beacon_interval
        self.flight_schedule = None

        # convert list of components to dict for easier searching
        self.components = {c.name:c for c in components}

        # beacons will be 'broadcast' to this file every beacon interval
        self.BEACON_BROADCAST_FILE = os.path.join(os.path.dirname(__file__), 'beacons.json')
        with open(self.BEACON_BROADCAST_FILE, 'w') as fptr:
            json.dump([], fptr)
        self.BEACON_INTERVAL = beacon_interval


    def step(self):
        """Moves the satellite one time step, change satellite state here
        """
        self.current_time += 1
        self.time_till_next_beacon  -= 1

        self._apply_component_effects_on_satellite_state()
        fs_command = self._get_fs_command_for_current_time()
        if fs_command is not None:
            response = self._execute_telecommand(fs_command[0], fs_command[1])
            print('Executed FS command, resp = ', response)

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
        lb = self.last_beacon_time if self.last_beacon_time is not None else ''
        return {
            'satellite_mode':self.satellite_mode,
            'battery_voltage':self.battery_voltage,
            'current_in':self.current_in,
            'current_out':self.current_out,
            'no_MCU_resets':self.no_MCU_resets,
            'last_beacon_time':lb
        }


    def _broadcast_beacon(self):
        self.last_beacon_time = self.current_time
        with open(self.BEACON_BROADCAST_FILE, 'r') as fptr:
            beacons_list = json.load(fptr)
            beacons_list.append(self._get_hk_as_dict())

        with open(self.BEACON_BROADCAST_FILE, 'w') as fptr:
            json.dump(beacons_list, fptr, indent=4)


    def _get_fs_command_for_current_time(self):
        """
        returns:
            - command (tuple?)
        """
        if self.flight_schedule is not None:
            with open(self.flight_schedule) as fptr:
                for row in fptr:
                    row = (row.strip()).split(',', 1)
                    if int(row[0]) == self.current_time:
                        return make_tuple(row[1])


    def _execute_telecommand(self, telecommand_name, args):
        telecommand_name = telecommand_name.upper()
        if telecommand_name == 'PING':
            response = 'PING-RESPONSE'
        elif telecommand_name == 'GET-HK':
            response = json.dumps(self._get_hk_as_dict())
        elif telecommand_name == 'TURN-ON':
            self._turn_on_component(args[0])
            response = '200 OK'
        elif telecommand_name == 'TURN-OFF':
            self._turn_off_component(args[0])
            response = '200 OK'
        elif telecommand_name == 'SET-FS':
            # expecting string path to the flight schedule
            self.flight_schedule = args[0]
            response = '201 Created'
        else:
            response = 'UNRECOGNIZED-COMMAND'

        return response


    def send(self, data, environment):
        """Send data to the satellite via here
        params:
            - data (tuple) : a 2 valued tuple, eg.) (command_name, [arg1, ..., argn])
        return:
            - depends, idk, probably always a string for now
        """
        telecommand_name, args = data

        # determine if we will drop the request (based on connection)
        if random.random() <= environment.packet_drop_probability:
            # drop packet
            return 'NO-RESPONSE'

        response = self._execute_telecommand(telecommand_name, args)
        if not environment.no_delay:
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
        self._log_file_path = os.path.join(os.path.dirname(__file__), 'log.txt')

    def send_to_sat(self, data):
        self._add_to_log('groundstation', 'satellite', data)
        sat_resp = self.satellite.send(data, self.environment)
        self._add_to_log('satellite', 'groundstation', sat_resp)
        return sat_resp

    def step(self):
        """Step environment and satellite one step
        """
        self.environment.step()
        self.satellite.step()

    def get_current_satellite_time(self):
        return self.satellite.current_time

    def _add_to_log(self, sender, recipient, message):

        log_message = '---- LOG ENTRY ----\n'
        log_message += f'sender: {sender}\n'
        log_message += f'recipient: {recipient}\n'
        log_message += f'message: {message}\n\n'

        with open(self._log_file_path, 'a+') as fptr:
            fptr.write(log_message + '\n')



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

    environment = Environment(connection_strength=10, connection_stability=10,
        packet_drop_probability=0.02)

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

    # doing this so I dont have to keep creating it for each example
    return simulator


def flight_schedule_example():
    # WARNING: This wont work now that time is referenced by current unix time
    # just use it as visual reference

    simulator = example_usage()

    data = ('SET-FS', ['groundstation/satellite_simulator/test_flight_schedule1.txt'])
    resp = simulator.send_to_sat(data)
    print(resp)

    for i in range(50):
        simulator.step()

    data = ('GET-HK', [])
    resp = simulator.send_to_sat(data)
    print(resp)
    assert not simulator.satellite.components['GPS'].is_on, 'GPS is still on!'




def run_interactively():

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

    example_usage()




if __name__=="__main__":
    main()
