"""The Automation Module allows operators to execute commands automatically at the next pass.
"""
from groundstation.backend_api.communications import CommunicationList
from groundstation.backend_api.passover import PassoverList
from datetime import datetime, timezone
import json
import subprocess
import time

def automate_communication():
    """Reads from a pre-defined script file called 'automation.txt' which contains messages
    separated by newlines. The Automation module will open this file and send each message to the comm module,
    which will then interpret and pass the message along to the satellite. The 'automation.txt' essentially mimicks a human
    user entering commands through the 'live commands' portal.
    """
    sender = CommunicationList()

    with open('automation.txt', 'r') as f:
        for line in f:
            line = line.strip("\n")

            message = {
                'message': line,
                'sender': 'automation',
                'receiver': 'comm'
            }

            message = json.dumps(message)
            sender.post(local_data=message)

def automate_passovers():
    """Before Automation terminates, this function is run to set a 'wake up' timer for the next passover, so that it will
    be automatically run again during the next pass.
    """
    passover = PassoverList()

    # the automation will also handle queuing passover times
    passovers = passover.get(local_args={'limit': 1, 'next' : 'true'})

    if passovers[1] == 200:
        passover_data = passovers[0]['data']['next_passovers']
        for passover in passover_data:
            time_obj = datetime.strptime(passover['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            time_obj = time_obj.replace(tzinfo=timezone.utc).astimezone(tz=None)
            f_time_min = time_obj.strftime('%H:%M')
            f_time_date = time_obj.strftime('%m/%d/%Y')

            subprocess.run(['at', f_time_min, f_time_date, '-f', 'automate.sh'])


def main():
    """Main function called when automation is run, calls automate_communication(), sleeps for a bit, and then calls automate_passovers().
    """
    automate_communication()
    time.sleep(60)
    automate_passovers()


if __name__ == '__main__':
    main()
