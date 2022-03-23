"""
The Communications Module is responsible for sending and retrieving data
with the satellite (or the simulator).
"""

import time
import json
import signal
from enum import Enum

from groundstation.backend_api.flightschedule import FlightScheduleList, Flightschedule
from groundstation.backend_api.communications import CommunicationList, Communication


class Connection(Enum):
    SIMULATOR = 1
    SATELLITE = 2


# Global variables
mode = None
communication_list = CommunicationList()
communication_patch = Communication()
flightschedule_list = FlightScheduleList()
flightschedule_patch = Flightschedule()


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


def send_to_simulator(msg):
    try:
        return antenna.send(msg)
    except Exception as e:
        print('Unexpected error occured:', e)

def convert_command_syntax(cmd):
    """
    Takes in a website command and converts it to ground station software's
    syntax.

    Currently, the website's command syntax is:
        `command.name arg1 arg2 ...`
    but ground station software's command syntax is:
        `command.name(arg1 arg2 ...)`

    TODO: Change the "Live Commands" syntax on the website
          to match ground station software's for consistency (Issue #64).

    :param str cmd: A command entered from the website.
    :returns: The same command but in ground station software's syntax.
    :rtype: str
    """
    tokens = cmd.split()
    return tokens[0] + '(' + ' '.join(tokens[1:]) + ')'

def send_to_satellite(csp, msg):
    try:
        command = csp.getInput(inVal=msg)
        if command is None:
            return "INVALID COMMAND"
        server, port, toSend = command
        return csp.transaction(server, port, toSend)
    except Exception as e:
        print('Unexpected error occured:', e)


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


def communication_loop(csp=None):
    """
    Main communication loop which polls for messages that are queued and addressed to comm
    (i.e. messages it needs to send to satellite). This should be run when a passover is
    expected to occur.

    :param Csp csp: The Csp instance. See groundStation.py
    """
    if mode == Connection.SATELLITE and csp is None:
        raise Exception('Csp instance must be specified if sending to satellite')

    request_data = {'is_queued': True, 'receiver': 'comm', 'newest-first': False}

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
                        msg = convert_command_syntax(msg)
                        response = send_to_satellite(csp, msg)

                    if response:
                        if isinstance(response, list):
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
        # TODO maybe clean up by putting in a function in gs_software
        opts = gs_software.groundStation.options()
        csp = gs_software.groundStation.groundStation(opts.getOptions())

        communication_loop(csp)


if __name__ == '__main__':
    if input('Would like to communicate with the satellite simulator (if not, the program '
        'will attempt to communicate with the satellite) [Y/n]: ').strip() in ('Y', 'y'):
        mode = Connection.SIMULATOR
        import satellite_simulator.antenna as antenna
    else:
        mode = Connection.SATELLITE
        import ex2_ground_station_software.src.groundStation as gs_software

    main()
