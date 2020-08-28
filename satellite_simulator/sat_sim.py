from . import helpers
import random
import json
import time
from ast import literal_eval as make_tuple
import os
import datetime
from collections import defaultdict

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
        self.current_time = datetime.datetime.now(datetime.timezone.utc)

    def get_current_time(self):
        return self.current_time

    def step(self):
        """Moves the environment one time step, change environment state in here
        """
        self.current_time = datetime.datetime.now(datetime.timezone.utc)

class SatelliteComponent:

    def __init__(self, name, channel, effects_when_on=[], effects_when_off=[]):
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
        self.channel = channel
        self.effects_when_on = effects_when_on
        self.effects_when_off = effects_when_off
        self.is_on = False

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False


class Satellite:

    sat_modes =  ['Danger', 'Critical', 'Passive', 'Active Mission']

    def __init__(self, components, satellite_mode=sat_modes[2], battery_voltage=16,
        current_in=0.3, current_out=0.3, no_MCU_resets=0,
        last_beacon_time=None, beacon_interval=10):
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
        self.watchdogs = [90*60] * 3
        self.panel_currents = [2] * 6
        self.temps = [8] * 6
        self.power_channels = [{'enabled':False, 'current':0.5} for _ in range(24)]

        self.last_step_time = None
        self.time_till_next_beacon = beacon_interval
        self.flight_schedule = None
        # convert list of components to dict for easier searching
        self.components = defaultdict(list)
        for c in components:
            self.components[c.channel].append(c)

        # beacons will be 'broadcast' to this file every beacon interval
        self.BEACON_BROADCAST_FILE = os.path.join(os.path.dirname(__file__), 'beacons.json')
        with open(self.BEACON_BROADCAST_FILE, 'w') as fptr:
            json.dump([], fptr)
        self.BEACON_INTERVAL = beacon_interval


    def step(self, environment):
        """Moves the satellite one time step, change satellite state here
        """
        current_time = environment.get_current_time()
        self.time_till_next_beacon -= 0 if self.last_step_time is None else (current_time - self.last_step_time).total_seconds()
        self._apply_component_effects_on_satellite_state(current_time)

        # TODO: Maybe re-implement executing fs commands but not priority

        if self.time_till_next_beacon <= 0:
            self._broadcast_beacon(current_time)
            self.time_till_next_beacon = self.BEACON_INTERVAL

        self.last_step_time = current_time


    def _apply_component_effects_on_satellite_state(self, current_time):
        if self.last_step_time is None:
            return
        time_since_last_step = (current_time - self.last_step_time).total_seconds()
        for component_list in list(self.components.values()):
            for component in component_list:
                effects = component.effects_when_on if component.is_on else component.effects_when_off

                for effect in effects:
                    attr, effect_function = effect
                    new_val = effect_function(getattr(self, attr), time_since_last_step)
                    setattr(self, attr, new_val)


    def _pet_watchdog(self, watchdog_index, new_value):
        self.watchdogs[watchdog_index] = new_value


    def _turn_on_channel(self, channel_index):
        self.power_channels[channel_index]['enabled'] = True
        for component in self.components[channel_index]:
            component.turn_on()


    def _turn_off_channel(self, channel_index):
        self.power_channels[channel_index]['enabled'] = False
        for component in self.components[channel_index]:
            component.turn_off()


    def _get_hk_as_dict(self):
        """Return a JSON serializable dict of the current housekeeping data
        """
        lb = str(self.last_beacon_time) if self.last_beacon_time is not None else ''
        return {
            'satellite_mode':self.satellite_mode,
            'battery_voltage':self.battery_voltage,
            'current_in':self.current_in,
            'current_out':self.current_out,
            'no_MCU_resets':self.no_MCU_resets,
            'last_beacon_time':lb,
            'watchdogs':self.watchdogs,
            'panel_currents':self.panel_currents,
            'temps':self.temps,
            'power_channels':self.power_channels,
        }


    def _broadcast_beacon(self, current_time):
        self.last_beacon_time = current_time
        with open(self.BEACON_BROADCAST_FILE, 'r') as fptr:
            beacons_list = json.load(fptr)
            beacons_list.append(self._get_hk_as_dict())

        with open(self.BEACON_BROADCAST_FILE, 'w') as fptr:
            json.dump(beacons_list, fptr, indent=4)


    # TODO: Needs updating if we want this feature
    # def _get_fs_command_for_current_time(self):
    #     pass


    def _execute_telecommand(self, telecommand_name, args):
        telecommand_name = telecommand_name.upper()
        if telecommand_name == 'PING':
            response = 'PING-RESPONSE'
        elif telecommand_name == 'GET-HK':
            response = json.dumps(self._get_hk_as_dict())
        elif telecommand_name == 'TURN-ON':
            self._turn_on_channel(int(args[0]))
            response = '200 OK'
        elif telecommand_name == 'TURN-OFF':
            self._turn_off_channel(int(args[0]))
            response = '200 OK'
        elif telecommand_name == 'PET-WATCHDOG':
            # expecting 2 args, 1.) watchdog timer index, 2.) new value
            self._pet_watchdog(int(args[0]), int(args[1]))
            response = '200 OK'
        elif telecommand_name == 'UPLOAD-FS':
            response = '200 OK'
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
        return response


class Simulator:

    def __init__(self, environment, satellite):
        self.environment = environment
        self.satellite = satellite
        self._log_file_path = os.path.join(os.path.dirname(__file__), 'log.txt')

    def send_to_sat(self, data):
        self._step()
        self._add_to_log('groundstation', 'satellite', data)
        sat_resp = self.satellite.send(data, self.environment)
        self._add_to_log('satellite', 'groundstation', sat_resp)
        return sat_resp

    def _step(self):
        """Step environment and satellite one step
        """
        self.environment.step()
        self.satellite.step(self.environment)

    def _add_to_log(self, sender, recipient, message):

        log_message = '---- LOG ENTRY ----\n'
        log_message += f'sender: {sender}\n'
        log_message += f'recipient: {recipient}\n'
        log_message += f'message: {message}\n\n'

        with open(self._log_file_path, 'a+') as fptr:
            fptr.write(log_message + '\n')
