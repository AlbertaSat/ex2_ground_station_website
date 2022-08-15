"""The Automation Module allows operators to execute commands automatically at the next pass.
"""
from groundstation.backend_api.communications import CommunicationList, Communication
from groundstation.backend_api.automatedcommand import AutomatedCommandList
from groundstation.backend_api.housekeeping import HousekeepingLogList
from groundstation.backend_api.passover import PassoverList
from groundstation.backend_api.utils import add_passover
from groundstation.backend_api.user import UserList
from datetime import datetime, timezone
from pyorbital.orbital import Orbital
import os
import slack
import json
import subprocess
import time


def automate_communication():
    """Reads from the automated commands table in the database and creates communications objects
    to be sent to the comm module, which will then interpret and pass the command messages along to the satellite
    This essentially mimicks a human user entering commands through the 'live commands' portal. Also supports
    sending commands by reading from a pre-defined script called 'automation.txt', although the website should be
    the preferred method of setting up the automated command sequence.
    """
    sender = CommunicationList()
    automatedcommand_list = AutomatedCommandList()

    with open('automation.txt', 'r') as f:
        for line in f:
            line = line.strip("\n")

            message = {
                'message': line,
                'sender': 'automation',
                'receiver': 'comm',
                'is_queued': True
            }

            message = json.dumps(message)
            sender.post(local_data=message)

    automatedcommands = automatedcommand_list.get(local_args={'limit': 1000})[
        0]['data']['automatedcommands']
    for command in automatedcommands:
        args = []
        # might need to sort args by index, not sure if db keeps order from original post req
        for arg in command['args']:
            args.append(arg['argument'])
        msg = command['command']['command_name'] + '(' + ' '.join(args) + ')'
        message = {
            'message': msg,
            'sender': 'automation',
            'receiver': 'comm',
            'is_queued': True
        }

        message = json.dumps(message)
        sender.post(local_data=message)

    timestamp = str(datetime.utcnow())
    message = 'An Ex-Alta 2 passover is beginning now! The timestamp for this passover is {0}'.format(
        timestamp)
    send_slack_notifs(message)


def automate_passovers():
    """Before Automation terminates, this function is run to set a 'wake up' timer for the next passover, so that it will
    be automatically run again during the next pass.
    """
    passover = PassoverList()
    housekeeping = HousekeepingLogList()

    # the automation will also handle queuing passover times
    passovers = passover.get(local_args={'limit': 1, 'next': 'true'})

    if passovers[1] == 200 and len(passovers[0]['data']['next_passovers']) > 0:
        passover_data = passovers[0]['data']['next_passovers']
        for ps in passover_data:
            time_obj = datetime.strptime(
                ps['aos_timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            time_obj = time_obj.replace(
                tzinfo=timezone.utc).astimezone(tz=None)
            f_time_min = time_obj.strftime('%H:%M')
            f_time_date = time_obj.strftime('%m/%d/%Y')

            subprocess.run(
                ['at', f_time_min, f_time_date, '-f', 'automate.sh'])
            print("Scheduled to automate at the next passover.")
    else:
        print("AUTOMATION: no more passovers found.")
        # calculate new passovers for the next 24 hours using current TLE data

        hk = housekeeping.get(local_args={'limit': 1, 'newest-first': 'true'})

        tle = hk[0]['data']['logs'][0]['tle']
        lines = tle.split('\n')

        orb = Orbital('ex-alta 2', line1=lines[0], line2=lines[1])
        dtobj = datetime.utcnow()
        # edmonton coordinates and elevation
        passes = orb.get_next_passes(dtobj, 24, -113.4938, 53.5461, 0.645)
        ps_data = {'passovers': [{'aos_timestamp': str(
            ps[0]), 'los_timestamp': str(ps[1])} for ps in passes]}

        passover.post(local_data=json.dumps(ps_data))


def send_slack_notifs(message):
    """Sends out a Slack message to all subscribed users.

    :param str message: Message to be sent to users on Slack.
    """
    # api call to get all users
    user_list = UserList()

    users = user_list.get(local_args={'limit': 1000, 'no_admin': True})[
        0]['data']['users']

    slack_token = os.getenv('SLACK_TOKEN')
    if slack_token is not None:
        client = slack.WebClient(token=slack_token)
        for user in users:
            print(user)
            if user['subscribed_to_slack'] and user['slack_id'] is not None:
                try:
                    client.chat_postMessage(
                        channel=user['slack_id'], text=message)
                except:
                    print('Error: slack id "{0}" is invalid.'.format(
                        user['slack_id']))
    else:
        print('Error: SLACK_TOKEN environemnt variable not set!')


def main():
    """Main function called when automation is run, calls automate_communication(), sleeps for a bit, and then calls automate_passovers().
    """
    automate_communication()
    time.sleep(60)
    automate_passovers()


if __name__ == '__main__':
    main()
