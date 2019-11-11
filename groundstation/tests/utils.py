def fakeHousekeepingAsDict(timestamp):
	housekeepingData = {
						'satellite_mode' : 'Passive',
						'battery_voltage': 1.7,
						'current_in': 1.2,
						'current_out': 1.1,
						'no_MCU_resets': 14,
						'last_beacon_time': timestamp
					}

	return housekeepingData

def fake_flight_schedule_as_dict(is_queued=False, commands=[]):
    flightschedule = {
        'is_queued':is_queued,
        'commands':commands
    }
    return flightschedule

def fake_passover_as_dict(timestamps):
    """
    params:
        @timestamps : [datetime.datetime.utcnow()] : (a list of datetime objects)
    """
    return {
        'passovers':[{'timestamp':str(timestamp)} for timestamp in timestamps]
    }

def fake_message_as_dict(message='test', sender='tester', receiver='tester2'):
    fake_message = {
        'message': message,
        'sender': sender,
        'receiver': receiver
    }

    return fake_message

def fake_patch_update_as_dict(timestamp):
    return {'is_queued': False,
            'commands': [
                {'op': 'replace',
                'flightschedule_command_id': 1,
                'timestamp': str(timestamp),
                'args' : [],
                'command': {'command_id': 2}},
                {'op': 'add', 'timestamp': str(timestamp), 'args' : [], 'command': {'command_id': 1}}
            ]
        }

def fake_telecommand_as_dict(command_name='test', num_arguments='0', is_dangerous=False):
    return {'command_name':command_name,
            'num_arguments':num_arguments,
            'is_dangerous':is_dangerous
    }
