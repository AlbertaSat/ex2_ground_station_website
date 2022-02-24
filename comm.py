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


def get_queued_fs():
    """
    If there is no queued flightschedule log it, otherwise, set its status
    to uploaded and send something to the flight schedule (this may be handled
    differently right now we are blindly trusting that a sent flightschedule
    is uploaded) and no data of the flight schedule is actually sent at the
    moment.

    TODO: this needs to be implemented properly.

    :returns: A dict representing the flight schedule object
    """
    local_args = {'limit': 1, 'queued': True}
    fs = flightschedule_list.get(local_args=local_args)


    if len(fs[0]['data']['flightschedules']) >= 1:
        fs_id = fs[0]['data']['flightschedules'][0]['flightschedule_id']
        fs_ex = fs[0]['data']['flightschedules'][0]['execution_time']
        local_data = {'status': 3, 'execution_time': fs_ex, 'commands': []}

        return flightschedule_patch.patch(
            fs_id, local_data=json.dumps(local_data))[0]['data']

    return None


def send_to_simulator(msg):
    try:
        return antenna.send(json.dumps(msg))
    except Exception as e:
        print('Unexpected error occured:', e)


def send_to_satellite(sock, csp, msg):
    try:
        server, port, toSend = csp.getInput(inVal=msg)
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


def communication_loop(sock=None, csp=None):
    """
    Main communication loop which polls for messages that are queued and addressed to comm
    (i.e. messages it needs to send to satellite). This should be run when a passover is
    expected to occur.

    :param Csp csp: The Csp instance. See groundStation.py
    """
    if mode == Connection.SATELLITE and (sock is None or csp is None):
        raise Exception('Csp instance must be specified if sending to satellite')

    request_data = {'is_queued': True, 'receiver': 'comm', 'newest-first': False}

    # Check communication table every minute
    while True:
        # Upload any queued flight schedules
        queued_fs = get_queued_fs()
        if queued_fs is not None:
            resp = send_to_simulator(queued_fs)
            save_response(resp)

        # Get queued communications
        messages = communication_list.get(local_data=request_data)[0]

        # If we have queued messages addressed to comm send them to the satellite
        if len(messages['data']['messages']) > 0:
            for message in messages['data']['messages']:
                if message['message']:
                    # TODO may need to handle flight schedule stuff here using handle_message

                    # Send the message to the satellite
                    response = None
                    msg = message['message'].replace(" ", ".")
                    print('Sent:', msg)
                    if mode == Connection.SIMULATOR:
                        response = send_to_simulator(msg)
                    elif mode == Connection.SATELLITE:
                        response = send_to_satellite(sock, csp, msg)

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

        # Fetch any flight schedule command responses
        # TODO: How would fs work with gs_software/obc?
        # TODO: Find an efficient way to continually listen for any kind of message from sat
        #       since right now, comm.py is a client and must continuously request from sat_server
        if mode == Connection.SIMULATOR:
            resp = send_to_simulator('fetch-fs')
            if resp != 'null':
                resp = json.loads(resp)
                for item in resp:
                    save_response(item)

        time.sleep(5)


def main():
    # Terminate after 10 minutes
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(60 * 60)

    if mode == Connection.SIMULATOR:
        communication_loop()
    elif mode == Connection.SATELLITE:
        # TODO maybe clean up by putting in a function in gs_software
        opts = gs_software.groundStation.options()
        csp = gs_software.groundStation.groundStation(opts.getOptions())

        # Not sure if this socket is needed here as gs_software already manages it.
        sock = libcsp.socket()
        libcsp.bind(sock, libcsp.CSP_ANY)

        communication_loop(sock, csp)


if __name__ == '__main__':
    if input('Would like to communicate with the satellite simulator (if not, the program '
        'will attempt to communicate with the satellite) [Y/n]: ').strip() in ('Y', 'y'):
        mode = Connection.SIMULATOR
        import satellite_simulator.antenna as antenna
    else:
        mode = Connection.SATELLITE
        import ex2_ground_station_software.src.groundStation as gs_software

        # Not sure if this is still needed as gs_software already imports it
        import libcsp.build.libcsp_py3 as libcsp

    main()
