"""
The Communications Module is responsible for sending and retrieving data
with the satellite (or the simulator).
"""

from ast import Import
import time
import json
import signal
import sys
import os
import datetime
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
    local_args = {'limit': 1, 'queued': 1}
    fs = flightschedule_list.get(local_args=local_args)

    if len(fs[0]['data']['flightschedules']) >= 1:
        fs_id = fs[0]['data']['flightschedules'][0]['flightschedule_id']
        fs_ex = fs[0]['data']['flightschedules'][0]['execution_time']
        local_data = {'status': 3, 'execution_time': fs_ex, 'commands': []}

        return flightschedule_patch.patch(
            fs_id, local_data=json.dumps(local_data))[0]['data']

    return None


def reset_fs_status_except_uploaded(uploadedID):
    """
    Resets all previously uploaded flightschedules to 'draft' status when
    a new flightschedule is uploaded.

    :param uploadedID: The ID of the most recently uploaded flightschedule.
    :type uploadedID: int
    """
    local_args = {'limit': 5, 'queued': 3}
    prev_uploaded = flightschedule_list.get(local_args=local_args)

    for prev_fs in prev_uploaded[0]['data']['flightschedules']:
        if prev_fs['flightschedule_id'] != uploadedID:
            patch_data = {
                'status': 2,
                'execution_time': prev_fs['execution_time'],
                'commands': []
            }
            flightschedule_patch.patch(
                prev_fs['flightschedule_id'],
                local_data=json.dumps(patch_data)
            )


def format_date_time(dt_str):
    """Generates a datetime object from a string.

    :param str dt_str: A date-time string to convert

    :returns: A datetime object representing the time passed in from string.
    :rtype: datetime
    """
    try:
        exec_time = (datetime.datetime
                     .strptime(dt_str, '%Y-%m-%d %H:%M:%S.%f')
                     .replace(tzinfo=datetime.timezone.utc))
    except ValueError:  # Sometimes the date format is off for some reason
        exec_time = (datetime.datetime
                     .strptime(dt_str, '%Y-%m-%d %H:%M:%S')
                     .replace(tzinfo=datetime.timezone.utc))
    return exec_time


def generate_fs_file(fs):
    """Generates a flight schdeule file for upload.

    :param dict fs: A flight schedule object fetched from db.
    :return: Path to the flight schedule file.
    :rtype: str
    """
    file_name = 'flightschedules/fs_{}.txt'.format(fs['flightschedule_id'])
    with open(file_name, "w+") as file:
        for command in fs['commands']:
            # Format the command string from fs
            command_name = command['command']['command_name']
            args = [arg['argument'] for arg in command['args']]
            command_string = ('{}({})'.format(command_name, ' '.join(args)))

            # Format the date/time from fs
            exec_time = format_date_time(command['timestamp'])
            time_fields = {
                'ms': '*' if command['repeats']['repeat_ms']
                    else int(exec_time.microsecond / 1000),
                'second': '*' if command['repeats']['repeat_sec']
                    else exec_time.second,
                'minute': '*' if command['repeats']['repeat_min']
                    else exec_time.minute,
                'hour': '*' if command['repeats']['repeat_hr']
                    else exec_time.hour,
                'day': '*' if command['repeats']['repeat_day']
                    else exec_time.day,
                'month': '*' if command['repeats']['repeat_month']
                    else exec_time.month,
                'year': '*' if command['repeats']['repeat_year']
                    else exec_time.year - 1970  # Offset from 1970
            }
            time_str = ('{ms} {second} {minute} {hour} 0 {day} {month} {year}'
                        .format(**time_fields))

            # Write fs commands to file
            print(time_str, command_string, file=file)

    return file_name


def send_to_simulator(msg):
    try:
        return antenna.send(json.dumps(msg))
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
        raise Exception('Ground station instance must be specified if sending to satellite')

    request_data = {'is_queued': True,
                    'receiver': 'comm', 'newest-first': False}

    # Check communication table every minute
    while True:
        # Upload any queued flight schedules
        queued_fs = get_queued_fs()
        if queued_fs is not None:
            if mode == Connection.SIMULATOR:
                resp = send_to_simulator(queued_fs)
            elif mode == Connection.SATELLITE:
                fs_file_path = generate_fs_file(queued_fs)
                # TODO: Upload fs file to satellite via ground station
                # and handle acknowledgement
                resp = fs_file_path
                save_response("Generated: " + resp)
                reset_fs_status_except_uploaded(queued_fs['flightschedule_id'])

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
        opts = optionsFactory("basic")
        gs = GroundStation(opts.getOptions())

        communication_loop(gs)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print('Detected CLI arguments for Ground Station Software!')
        print('Automatically setting mode to satellite...')
        mode = Connection.SATELLITE
        sys.path.append(os.path.join(sys.path[0], 'ex2_ground_station_software', 'src'))
        from groundStation import GroundStation
        from options import optionsFactory
    else:
        if input('Would like to communicate with the satellite simulator (if not, the program '
                 'will attempt to communicate with the satellite) [Y/n]: ').strip() in ('Y', 'y'):
            mode = Connection.SIMULATOR
            import satellite_simulator.antenna as antenna
        else:
            mode = Connection.SATELLITE
            sys.path.append(os.path.join(sys.path[0], 'ex2_ground_station_software', 'src'))
            from groundStation import GroundStation
            from options import optionsFactory

    main()
