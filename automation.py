from groundstation.backend_api.communications import CommunicationList
from groundstation.backend_api.passover import PassoverList
from datetime import datetime, timezone
import json
import subprocess
import time

def automate_communication():
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
    automate_communication()
    time.sleep(60)
    automate_passovers()


if __name__ == '__main__':
    main()