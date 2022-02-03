"""
The Communications Module is responsible for sending and retrieving data 
with the satellite (or the simulator).
"""

from multiprocessing import connection
import time
import json
import signal
from enum import Enum
from groundstation.backend_api import communications


from groundstation.backend_api.communications import CommunicationList
from groundstation.backend_api.communications import Communication
from gs_commands import GsCommands


class Connection(Enum):
    SIMULATOR = 1
    SATELLITE = 2


# some global variables
mode = None
communication_list = CommunicationList()
communication_patch = Communication()
gs_commands_obj = GsCommands()
gs_commands_dict = gs_commands_obj.get_gs_commands_dict()


def simulator_use_example():
    telecommands = ['ping', 'get-hk', 'turn-on 0', 'ping', 'get-hk']
    for telecommand in telecommands:
        print(send_to_simulator(telecommand))


# handle the sig alarm
def handler(signum, frame):
    exit()


# handle message in communication table
def handle_message(message):
    """
    Messages sent to comm will pass through this function, essentially acting 
    as a decorator. Refer to gs_commands module

    :param str message: The incoming message to comm

    :returns: Return is dependent on the handler function triggered
    :rtype: Optional
    """
    # TODO this needs to be implmented to support flight schedule functionality
    handle = gs_commands_dict.get(message)
    if handle:
        return handle()
    else:
        return message


def send_to_simulator(msg):
    try:
        return antenna.send(msg)
    except Exception as e:
        print('Unexpected error occured:', e)


def send_to_satellite(sock, csp, msg):
    try:
        to_send, server, port = csp.getInput(inVal=msg)
        csp.send(server, port, to_send)
        return csp.receive(sock)
    except Exception as e:
        print('Unexpected error occured:', e)


def communication_loop(sock, csp=None):
    """
    Main communication loop which polls for messages that are queued and addressed to comm 
    (i.e. messages it needs to send to satellite). This should be run when a passover is
    expected to occur.

    :param Csp csp: The Csp instance. See groundStation.py
    """
    if mode == Connection.SATELLITE and csp is None:
        raise Exception('Csp instance must be specified if sending to satellite')

    request_data = {'is_queued': True, 'receiver': 'comm'}

    # Continuously check communication table every minute
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
                    msg = message['message'].replace(" ", ".")
                    print('Sent:', msg)
                    if mode == Connection.SIMULATOR:
                        response = send_to_simulator(msg)
                    elif mode == Connection.SATELLITE:
                        response = send_to_satellite(sock, csp, msg)

                    if response:
                        if isinstance(response, list):
                            print('Received:', response)
                            for item in response:
                                # Save the satellite response as a comm log
                                message = {
                                    'message': str(item),
                                    'sender': 'comm',
                                    'receiver': 'logs',
                                    'is_queued': False
                                }
                                message = json.dumps(message)
                                communication_list.post(local_data=message)
                        
                        communication_patch.patch(
                            message['message_id'], 
                            local_data=json.dumps({'is_queued': False}))
        
        time.sleep(60)


def main():
    # Terminate after 10 minutes
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(10 * 60)

    if mode == Connection.SIMULATOR:
        import satellite_simulator.antenna as antenna
        communication_loop()
    elif mode == Connection.SATELLITE:
        import ex2_ground_station_software.src.groundstation as gs_software
        import libcsp.build.libcsp_py3 as libcsp
        # TODO clean up by putting in a function in gs_software
        opts = gs_software.getOptions()
        csp = gs_software.Csp(opts)
        sock = libcsp.socket()
        libcsp.bind(sock, libcsp.CSP_ANY)
        communication_loop(sock, csp)


if __name__ == '__main__':
    if input('Would like to communicate with the satellite simulator (if not, the program ' 
        'will attempt to communicate with the satellite) [Y/n]: ').strip() in ('Y', 'y'):
        mode = Connection.SIMULATOR
    else:
        mode = Connection.SATELLITE

    main()
