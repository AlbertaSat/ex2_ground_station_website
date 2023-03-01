"""
The Communications Module is responsible for sending and retrieving data
with the satellite (or the simulator).
"""

import time
import json
import signal
import sys
import os
import subprocess
from enum import Enum
from datetime import datetime, timezone

from groundstation.backend_api.flightschedule import FlightScheduleList, Flightschedule
from groundstation.backend_api.communications import CommunicationList, Communication
from groundstation.backend_api.ftp import FTPUploadAPI

from groundstation.backend_api.housekeeping import HousekeepingLogList
from groundstation.tests.utils import fake_housekeeping_as_dict, fake_adcs_hk_as_dict, \
    fake_athena_hk_as_dict, fake_eps_hk_as_dict, fake_eps_startup_hk_as_dict, \
    fake_uhf_hk_as_dict, fake_sband_hk_as_dict, fake_hyperion_hk_as_dict, \
    fake_charon_hk_as_dict, fake_dfgm_hk_as_dict, \
    fake_northern_spirit_hk_as_dict, fake_iris_hk_as_dict


class Connection(Enum):
    SIMULATOR = 1
    SATELLITE = 2


class FSStatus(Enum):
    QUEUED = 1
    DRAFT = 2
    UPLOADED = 3


# Global variables
mode = None
communication_list = CommunicationList()
communication_patch = Communication()
flightschedule_list = FlightScheduleList()
flightschedule_patch = Flightschedule()
housekeeping_post = HousekeepingLogList()
ftp_uploads = FTPUploadAPI()


# Handle the sig alarm
def handler(signum, frame):
    exit()


def change_fs_status(fs_id, new_status, execution_time=None, error=0):
    """
    Given a flightschedule, change its status

    :param fs_id: The id of the flightschedule to change
    :param new_status: The new status of the flightschedule.
    :param execution_time: The execution time of the flightschedule.
    :param error: The error code returned after upload (0 means success).

    :returns: A dict representing the newly patched flightschedule
    """
    if execution_time is None:
        fs = flightschedule_patch.get(fs_id)
        execution_time = fs[0]['data']['execution_time']
    patch_data = {
        'status': new_status,
        'execution_time': execution_time,
        'commands': [],
        'error': error
    }
    return flightschedule_patch.patch(
        fs_id, local_data=json.dumps(patch_data))[0]['data']


def get_queued_fs():
    """
    Fetches a queued flightschedule.

    The website's API logic only allowes for one flightschedule to be queued
    at any given time.

    :returns: A dict representing the queued flightschedule object
    """
    local_args = {'limit': 1, 'queued': 1}
    fs = flightschedule_list.get(local_args=local_args)

    if len(fs[0]['data']['flightschedules']) >= 1:
        return fs[0]['data']['flightschedules'][0]

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
            change_fs_status(
                prev_fs['flightschedule_id'],
                FSStatus.DRAFT.value,
                prev_fs['execution_time']
            )


def format_date_time(dt_str):
    """Generates a datetime object from a string.

    :param str dt_str: A date-time string to convert

    :returns: A datetime object representing the time passed in from string.
    :rtype: datetime
    """
    try:
        exec_time = (datetime
                     .strptime(dt_str, '%Y-%m-%d %H:%M:%S.%f')
                     .replace(tzinfo=timezone.utc))
    except ValueError:  # Sometimes the date format is off for some reason
        exec_time = (datetime
                     .strptime(dt_str, '%Y-%m-%d %H:%M:%S')
                     .replace(tzinfo=timezone.utc))
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
            command_string = ('{}({})'.format(command_name, ','.join(args)))

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


def send_flightschedules(gs):
    queued_fs = get_queued_fs()
    if queued_fs is not None:
        if mode == Connection.SIMULATOR:
            resp = send_to_simulator(queued_fs)
        elif mode == Connection.SATELLITE:
            file_path = generate_fs_file(queued_fs)
            resp = send_to_satellite(
                gs, 'ex2.scheduler.replace_schedule({})'.format(file_path))
            save_response('Flight Schedule Successful! (ID = {}): {}'.format(
                queued_fs['flightschedule_id'], repr(resp)))
            if resp['err'] == 0:
                change_fs_status(
                    queued_fs['flightschedule_id'],
                    FSStatus.UPLOADED.value,
                    queued_fs['execution_time']
                )
                reset_fs_status_except_uploaded(queued_fs['flightschedule_id'])
            else:
                change_fs_status(
                    queued_fs['flightschedule_id'],
                    FSStatus.DRAFT.value,
                    queued_fs['execution_time'],
                    resp['err']
                )


def log_housekeeping(response):
    """
    Parses housekeeping data from the HOUSEKEEPING.GET_HK command and creates
    a database entry for each housekeeping entry.
    """
    for log in response:
        if log['err'] != 0:
            save_response(
                'Failed to log housekeeping! (error: {})'.format(log['err']))
            continue

        # Form baseline schema for the post data
        hk = fake_housekeeping_as_dict(
            timestamp=datetime.fromtimestamp(log['UNIXtimestamp']).isoformat(),
            data_position=log['dataPosition']
        )
        hk['adcs'] = fake_adcs_hk_as_dict()
        hk['athena'] = fake_athena_hk_as_dict()
        hk['eps'] = fake_eps_hk_as_dict()
        hk['eps_startup'] = fake_eps_startup_hk_as_dict()
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
            'eps_startup',
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

        # Log HK transaction
        save_response('Logged housekeeping!\nTimestamp: {}\nData Position: {}'.format(
            hk['timestamp'], hk['data_position']))


def upload_ftp():
    request_data = {'uploaded': False}
    files = ftp_uploads.get(local_data=request_data)[0]
    if (len(files['data']['uploads']) > 0):
        for f in files['data']['uploads']:
            subprocess.Popen([
                'python3',
                'comm_ftp.py',
                '-I',
                'dummy',  # TODO: make this flexible later
                '-p',
                str(f['filepath']),
                '--file-id',
                str(f['id'])
            ])


def send_to_simulator(msg):
    try:
        return antenna.send(json.dumps(msg))
    except Exception as e:
        print('Unexpected error occured:', e)


def send_to_satellite(gs, msg):
    try:
        transactObj = gs.interactive.getTransactionObject(
            msg, gs.networkManager)
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


def communication_loop(gs=None):
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
        # Upload any queued flight schedules
        if mode == Connection.SATELLITE:
            send_flightschedules(gs)
            upload_ftp()

        # Get queued communications
        messages = communication_list.get(local_data=request_data)[0]

        # If we have queued messages addressed to comm send them to the satellite
        if len(messages['data']['messages']) > 0:
            for message in messages['data']['messages']:
                if message['message']:
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
                        if 'housekeeping.get_hk' in msg or 'housekeeping.get_instant_hk' in msg:
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
        sys.path.append(os.path.join(
            sys.path[0], 'ex2_ground_station_software', 'src'))
        from groundStation import GroundStation
        from options import optionsFactory
    else:
        if input('Would like to communicate with the satellite simulator (if not, the program '
                 'will attempt to communicate with the satellite) [Y/n]: ').strip() in ('Y', 'y'):
            mode = Connection.SIMULATOR
            import satellite_simulator.antenna as antenna
        else:
            mode = Connection.SATELLITE
            sys.path.append(os.path.join(
                sys.path[0], 'ex2_ground_station_software', 'src'))
            from groundStation import GroundStation
            from options import optionsFactory

    main()
