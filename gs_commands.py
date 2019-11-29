from groundstation.backend_api.flightschedule import FlightScheduleList, Flightschedule
from groundstation.backend_api.communications import CommunicationList
import json

class GsCommands:
    """
    This file is mainly for decorating additional functionality on top of commands
    By default the behaviour for interpreting commands is to send the command as a string
    This class allows for additonal functionality when the comm module reads the string of the command
    the return value of the fuction should be what is sent to the satellite
    if nothing should be sent, return None
    An example below is upload_fs
    To include decorator commands, store then in thr gs_commands dict,
    With the command string as the key and the function as the value
    """

    def __init__(self):
        self.communication_list = CommunicationList()


    def upload_fs(self):
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
            self.handle_response('A queued flight schedule does not exist.')
            return None
        else:
            fs_id = fs[0]['data']['flightschedules'][0]['flightschedule_id']
            fs_ex = fs[0]['data']['flightschedules'][0]['execution_time']
            local_data = {'status': 3, 'execution_time':fs_ex, 'commands': []}

            flightschedule_patch.patch(fs_id, local_data=json.dumps(local_data))

            return 'upload-fs'

    # probably handle errors in the post, if not 200 OK
    def handle_response(self, data):
        logged_data = {'message': data, 'receiver': 'all', 'sender': 'comm'}
        resp = self.communication_list.post(local_data=json.dumps(logged_data))

    # groundstation functions with additional capabilities rather than just sending a string
    # are handled here
    def get_gs_commands_dict(self):
        gs_commands = {
            'upload-fs': self.upload_fs
        }

        return gs_commands
