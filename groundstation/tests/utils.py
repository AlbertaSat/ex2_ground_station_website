from groundstation.backend_api.models import PowerChannels

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
        'channels': []          # 24 power channels
    }
    # Create channels. Operator can't create HK, so it's just hardcoded
    for i in range(1, 25):
        p = PowerChannels()
        p.hk_id = 1
        p.channel_no = i
        p.enabled = True
        p.current = 0.0
        housekeepingData['channels'].append(p)

    return housekeepingData

def fake_flight_schedule_as_dict(status=2, commands=[]):
    flightschedule = {
        'status':status,
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
    return {'status': 2,
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
