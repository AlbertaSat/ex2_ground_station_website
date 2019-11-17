from groundstation.backend_api.communications import CommunicationList
from groundstation.backend_api.passover import PassoverList
from datetime import datetime
import json
import subprocess

def main():
    sender = CommunicationList()
    passover = PassoverList()

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

    # the automation will also handle queuing passover times
    passovers = passover.get(local_args={'limit': 1, 'next-only' : 'true'})
    print(passovers)

    if passovers[1] == 200:
        passover_data = passovers[0]['data']['passovers']
        for passover in passover_data:
            time_obj = datetime.strptime(passover['timestamp'], '%Y-%m-%d %H:%M:%S.%f')
            f_time_min = time_obj.strftime('%H:%M')
            f_time_date = time_obj.strftime('%m/%d/%Y')

            subprocess.run(['at', f_time_min, f_time_date, '-f', 'test.sh'])











main()