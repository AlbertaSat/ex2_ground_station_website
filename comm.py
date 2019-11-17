# The Communications Module. Responsible for sending and retrieving data with the satellite.
# (or the simulator)
import satellite_simulator.antenna as antenna
from groundstation.backend_api.communications import CommunicationList
import time
import json
import signal

def send(socket, data):
    """ Pipes the incoming data (probably a Command tuple) to the socket (probably the Simulator)
        - socket (something that implements .send(data) interface):
        - data (str) : Message string
    """
    return socket.send(data)

# probably handle errors in the post, if not 200 OK
def handle_response(data, communication_list):
    logged_data = {'message': data, 'receiver': 'all', 'sender': 'comm'}
    resp = communication_list.post(json.dumps(logged_data))

def example():
    telecommands = ['ping', 'get-hk', 'turn-on 0', 'ping', 'get-hk']
    for telecommand in telecommands:
        resp = send(antenna, telecommand)
        print(resp)

# handle the sig alarm
def handler(signum, frame):
    exit()

def communication_loop():
    request_data = {'last_id': 0, 'receiver': 'comm'}

    communication_list = CommunicationList()
    # get the id of the last entry in the communication list
    # so we dont send anything before that
    # for our request arguments include max to get the entry with the max id
    comm_last_id = communication_list.get(local_data={'max' : True})[0]
    request_data['last_id'] = comm_last_id['data']['messages'][0]['message_id']

    # loop to continuously check communication table
    # if we have messages address to comm greater than the last id
    # send them to the satellite
    # possibly change polling to select on a named pipe, probably the easiest
    # for the server to notify the comm module on new data
    # or polling might be just fine
    while True:
        messages = communication_list.get(local_data=request_data)[0]

        if len(messages['data']['messages']) > 0:
            for message in messages['data']['messages']:
                resp = send(antenna, message['message'])
                handle_response(resp, communication_list)

            request_data['last_id'] = messages['data']['messages'][-1]['message_id']

        time.sleep(1)

if __name__=='__main__':
    # set a sigalarm so the comm module will close after a specified amount of time
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)
    communication_loop()
