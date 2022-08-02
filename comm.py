"""
The Communications Module is responsible for sending and retrieving data
with the satellite (or the simulator).
"""

import time
import json
import signal
import sys
import os
from enum import Enum
from datetime import datetime

from groundstation.backend_api.flightschedule import FlightScheduleList, Flightschedule
from groundstation.backend_api.communications import CommunicationList, Communication

from groundstation.backend_api.housekeeping import HousekeepingLogList
from groundstation.tests.utils import fake_housekeeping_as_dict, fake_adcs_hk_as_dict, \
    fake_athena_hk_as_dict, fake_eps_hk_as_dict, fake_uhf_hk_as_dict, \
    fake_sband_hk_as_dict, fake_hyperion_hk_as_dict, fake_charon_hk_as_dict, \
    fake_dfgm_hk_as_dict, fake_northern_spirit_hk_as_dict, fake_iris_hk_as_dict


class Connection(Enum):
    SIMULATOR = 1
    SATELLITE = 2


# Global variables
mode = None
communication_list = CommunicationList()
communication_patch = Communication()
flightschedule_list = FlightScheduleList()
flightschedule_patch = Flightschedule()
housekeeping_post = HousekeepingLogList()


# Handle the sig alarm
def handler(signum, frame):
    exit()


def handle_message(message):
    """
    Messages sent to comm will pass through this function, essentially acting
    as a decorator.

    TODO: this needs to be implmented to support flight schedule functionality.

    :param str message: The incoming message to comm

    :returns: Return is dependent on the handler function triggered
    :rtype: Optional
    """
    # Groundstation functions with additional capabilities rather than just sending a string
    gs_commands = {
        'upload-fs': upload_fs
    }

    handle = gs_commands.get(message)

    if handle:
        return handle()
    else:
        return message


def upload_fs():
    """
    If there is no queued flightschedule log it, otherwise, set its status
    to uploaded and send something to the flight schedule (this may be handled
    differently right now we are blindly trusting that a sent flightschedule
    is uploaded) and no data of the flight schedule is actually sent at the
    moment.

    TODO: this needs to be implemented properly.
    """
    local_args = {'limit': 1, 'queued': True}
    fs = flightschedule_list.get(local_args=local_args)

    if len(fs[0]['data']['flightschedules']) < 1:
        save_response('A queued flight schedule does not exist.')
        return None
    else:
        fs_id = fs[0]['data']['flightschedules'][0]['flightschedule_id']
        fs_ex = fs[0]['data']['flightschedules'][0]['execution_time']
        local_data = {'status': 3, 'execution_time': fs_ex, 'commands': []}

        flightschedule_patch.patch(
            fs_id, local_data=json.dumps(local_data))

        return 'upload-fs'


def log_housekeeping(response):
    """
    Parses housekeeping data from the HOUSEKEEPING.GET_HK command and creates
    a database entry for each housekeeping entry.
    """
    for log in response:
        # Form baseline schema for the post data
        hk = fake_housekeeping_as_dict(
            timestamp=datetime.fromtimestamp(log['UNIXtimestamp']).isoformat(),
            data_position=log['dataPosition']
        )
        hk['adcs'] = fake_adcs_hk_as_dict()
        hk['athena'] = fake_athena_hk_as_dict()
        hk['eps'] = fake_eps_hk_as_dict()
        hk['uhf'] = fake_uhf_hk_as_dict()
        hk['sband'] = fake_sband_hk_as_dict()
        hk['hyperion'] = fake_hyperion_hk_as_dict()
        hk['charon'] = fake_charon_hk_as_dict()
        hk['dfgm'] = fake_dfgm_hk_as_dict()
        hk['northern_spirit'] = fake_northern_spirit_hk_as_dict()
        hk['iris'] = fake_iris_hk_as_dict()

        # Strip the subsystem title from response data
        for key in list(log):
            if '#' in key:
                log[key.split('\r\n')[-1]] = log.pop(key)

        # Copy over response data to post data
        subsystems = [
            'adcs',
            'athena',
            'eps',
            'uhf',
            'sband',
            'hyperion',
            'charon',
            'dfgm',
            'northern_spirit',
            'iris'
        ]
        for subsystem in subsystems:
            for key in hk[subsystem]:
                hk[subsystem][key] = log[key]

        # Post HK data
        post_data = json.dumps(hk)
        housekeeping_post.post(local_data=post_data)


def send_to_simulator(msg):
    try:
        return antenna.send(msg)
    except Exception as e:
        print('Unexpected error occured:', e)


def send_to_satellite(gs, msg):
    try:
        transactObj = gs.interactive.getTransactionObject(msg, gs.networkManager)
        return transactObj.execute()
    except Exception as e:
        print('Unexpected error occured:', e)
        return 'Unexpected error occured: {}'.format(e)


# Save the satellite response as a comm log
def save_response(message):
    print('Received:', message)
    message = {
        'message': str(message),
        'sender': 'comm',
        'receiver': 'logs',
        'is_queued': False
    }
    message = json.dumps(message)
    communication_list.post(local_data=message)


def communication_loop(gs=None, cli_gs=None):
    """
    Main communication loop which polls for messages that are queued and addressed to comm
    (i.e. messages it needs to send to satellite). This should be run when a passover is
    expected to occur.

    :param Csp csp: The Csp instance. See groundStation.py
    """
    if mode == Connection.SATELLITE and gs is None:
        raise Exception(
            'Ground station instance must be specified if sending to satellite')

    request_data = {'is_queued': True,
                    'receiver': 'comm', 'newest-first': False}

    # Check communication table every minute
    while True:
        # Get queued communications
        messages = communication_list.get(local_data=request_data)[0]

        # If we have queued messages addressed to comm send them to the satellite
        if len(messages['data']['messages']) > 0:
            for message in messages['data']['messages']:
                if message['message']:
                    # TODO may need to handle flight schedule stuff here using handle_message

                    # Send the message to the satellite
                    response = None
                    msg = message['message']
                    print('Sent:', msg)
                    if mode == Connection.SIMULATOR:
                        msg = message['message'].replace(" ", ".")
                        response = send_to_simulator(msg)
                    elif mode == Connection.SATELLITE:
                        response = send_to_satellite(gs, msg)

                    if response:
                        if 'housekeeping.get_hk' in msg:
                            save_response('Housekeeping logged')
                            log_housekeeping(response)
                        elif isinstance(response, list):
                            for item in response:
                                save_response(item)
                        else:
                            save_response(response)

                        # Denote that the message has been executed if successful
                        communication_patch.patch(
                            message['message_id'],
                            local_data=json.dumps({'is_queued': False}))

        time.sleep(5)


def main():
    # Terminate after 10 minutes
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(10 * 60)

    if mode == Connection.SIMULATOR:
        communication_loop()
    elif mode == Connection.SATELLITE:
        opts = optionsFactory("basic")
        gs = GroundStation(opts.getOptions())

        communication_loop(gs)


if __name__ == '__main__':
    if input('Would like to communicate with the satellite simulator (if not, the program '
             'will attempt to communicate with the satellite) [Y/n]: ').strip() in ('Y', 'y'):
        mode = Connection.SIMULATOR
        import satellite_simulator.antenna as antenna
    else:
        mode = Connection.SATELLITE
        # Really jank path workaround that prevents messing up a lot of imports
        # in ex2_ground_station_software for non-website users
        sys.path.append(os.path.join(sys.path[0], 'ex2_ground_station_software', 'src'))
        from groundStation import GroundStation
        from options import optionsFactory

    main()
