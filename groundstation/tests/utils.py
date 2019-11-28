import datetime

def fakeHousekeepingAsDict(timestamp):
    housekeepingData = {
        'satellite_mode' : 'Passive',
        'battery_voltage': 1.7,
        'current_in': 1.2,
        'current_out': 1.1,
        'no_MCU_resets': 14,
        'last_beacon_time': timestamp,

        'watchdog_1': 6000,     # Watchdog counts
        'watchdog_2': 11,
        'watchdog_3': 0,
        'panel_1_current': 1.1, # Solar panel currents
        'panel_2_current': 1.0,
        'panel_3_current': 1.2,
        'panel_4_current': 1.0,
        'panel_5_current': 1.0,
        'panel_6_current': 1.0,

        'temp_1': 11.0,           # Temperatures
        'temp_2': 11.0,
        'temp_3': 14.0,
        'temp_4': 12.0,
        'temp_5': 11.0,
        'temp_6': 10.0,

        'channels': [],
    }

    return housekeepingData

def fake_power_channel_as_dict(channel_no):
    power_channel = {
        'channel_no': channel_no,
        'enabled': True,
        'current': 0.0
    }

    return power_channel


def fake_flight_schedule_as_dict(status=2, commands=[], execution_time=None):
    flightschedule = {
        'status':status,
        'commands':commands,
        'execution_time': execution_time
    }
    return flightschedule

def fake_passover_as_dict(timestamps):
    """Create mock passovers as a dictionary
    
    :param list(datetime.datetime) timestamps: The passover timestamps to use
    """
    return {
        'passovers':[{'timestamp':str(timestamp)} for timestamp in timestamps]
    }

def fake_message_as_dict(message='test', sender='tester', receiver='tester2'):
    fake_message = {
        'message': message,
        'sender': sender,
        'receiver': receiver,
        'timestamp':datetime.datetime.now(datetime.timezone.utc)
    }

    return fake_message

def fake_patch_update_as_dict(timestamp):
    return {'status': 2,
            'execution_time': str(timestamp),
            'commands': [
                {'op': 'replace',
                'flightschedule_command_id': 1,
                'timestamp': str(timestamp),
                'args' : [],
                'command': {'command_id': 2}},
                {'op': 'add', 'timestamp': str(timestamp), 'args' : [], 'command': {'command_id': 1}}
            ]
        }

def fake_user_as_dict(username, password):
    return {
        'username':username,
        'password':password
    }
def fake_telecommand_as_dict(command_name='test', num_arguments='0', is_dangerous=False):
    return {'command_name':command_name,
            'num_arguments':num_arguments,
            'is_dangerous':is_dangerous
    }
