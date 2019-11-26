"""The Communications Module is responsible for sending and retrieving data with the satellite (or the simulator).
"""
import satellite_simulator.antenna as antenna
from groundstation.backend_api.communications import CommunicationList
from groundstation.backend_api.flightschedule import FlightScheduleList, Flightschedule
import time
import json
import signal

# some global variables
communication_list = CommunicationList()

def send(socket, data):
    """Pipes the incoming data (probably a Command tuple) to the socket (probably the Simulator)

    :param int socket: The socket for sending data into
    :param str data: the data to send

    :returns: response from the socket
    :rtype: str
    """
    return socket.send(data)

# probably handle errors in the post, if not 200 OK
def handle_response(data):
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

def upload_fs():
    local_args = {'limit': 1, 'queued': True}

    flightschedule_list = FlightScheduleList()
    flightschedule_patch = Flightschedule()
    fs = flightschedule_list.get(local_args=local_args)

    # if there is no queued flightschedule, log it
    # if there is a queued flightschedule, set its status to uploaded and
    # send something to the flight schedule (this may be handled differently
    # right now we are blindly trusting that a sent flightschedule is uploaded)
    # and no data of the flight schedule is actually sent at the moment
    if len(fs[0]['data']['flightschedules']) < 1:
        handle_response('A queued flight schedule does not exist.')
        return None
    else:
        fs_id = fs[0]['data']['flightschedules'][0]['flightschedule_id']
        local_data = {'status': 3, 'commands': []}

        flightschedule_patch.patch(fs_id, local_data=json.dumps(local_data))

        return 'upload-fs'

# groundstation functions with additional capabilities rather than just sending a string
# are handled here
gs_commands = {
    'upload-fs': upload_fs
}

# handle message in communication table
def handle_message(message):
    """Messages sent to comm will pass through this function, essentially acting as a decorator.
    You can implement message-interpreting and message-triggered functionality here.

    :param str message: The incoming message to comm

    :returns: Return is dependent on the handler function triggered
    :rtype: Optional
    """
    handle = gs_commands.get(message)
    if handle:
        return handle()
    else:
        return message




def communication_loop():
    """Main communication loop which polls for messages addressed to comm (i.e. messages it needs to send to satellite)
    """

    request_data = {'last_id': 0, 'receiver': 'comm'}
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
                if message['message']:
                    data = handle_message(message['message'])

                    if data:
                        resp = send(antenna, data)
                        handle_response(resp)

            request_data['last_id'] = messages['data']['messages'][-1]['message_id']

        time.sleep(1)

def main():
    # set a sigalarm so the comm module will close after a specified amount of time
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)
    communication_loop()


if __name__=='__main__':
    main()
