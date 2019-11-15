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
        'temp_1': 11,           # Temperatures
        'temp_2': 11,
        'temp_3': 14,
        'temp_4': 12,
        'temp_5': 11,
        'temp_6': 10,
        'channels': [           # 24 power channels
            # {'id':1, 'hk_id':1, 'channel_no':1, 'enabled': True, 'current': 3.0},
            # {'id':2, 'hk_id':1, 'channel_no':2, 'enabled': True, 'current': 0.0},
            # {'id':3, 'hk_id':1, 'channel_no':3, 'enabled': True, 'current': 0.0},
            # {'id':4, 'hk_id':1, 'channel_no':4, 'enabled': True, 'current': 0.0},
            # {'id':5, 'hk_id':1, 'channel_no':5, 'enabled': True, 'current': 1.0},
            # {'id':6, 'hk_id':1, 'channel_no':6, 'enabled': True, 'current': 0.0},
            # {'id':7, 'hk_id':1, 'channel_no':7, 'enabled': True, 'current': 0.0},
            # {'id':8, 'hk_id':1, 'channel_no':8, 'enabled': True, 'current': 0.0},
            # {'id':9, 'hk_id':1, 'channel_no':9, 'enabled': True, 'current': 60.0},
            # {'id':10, 'hk_id':1, 'channel_no':10, 'enabled': True, 'current': 0.0},
            # {'id':11, 'hk_id':1, 'channel_no':11, 'enabled': True, 'current': 0.0},
            # {'id':12, 'hk_id':1, 'channel_no':12, 'enabled': True, 'current': 0.0},
            # {'id':13, 'hk_id':1, 'channel_no':13, 'enabled': True, 'current': 6.0},
            # {'id':14, 'hk_id':1, 'channel_no':14, 'enabled': True, 'current': 0.0},
            # {'id':15, 'hk_id':1, 'channel_no':15, 'enabled': True, 'current': 0.0},
            # {'id':16, 'hk_id':1, 'channel_no':16, 'enabled': True, 'current': 0.0},
            # {'id':17, 'hk_id':1, 'channel_no':17, 'enabled': True, 'current': 0.0},
            # {'id':18, 'hk_id':1, 'channel_no':18, 'enabled': True, 'current': 0.0},
            # {'id':19, 'hk_id':1, 'channel_no':19, 'enabled': True, 'current': 0.0},
            # {'id':20, 'hk_id':1, 'channel_no':20, 'enabled': True, 'current': 0.0},
            # {'id':21, 'hk_id':1, 'channel_no':21, 'enabled': True, 'current': 127.0},
            # {'id':22, 'hk_id':1, 'channel_no':22, 'enabled': True, 'current': 0.0},
            # {'id':23, 'hk_id':1, 'channel_no':23, 'enabled': True, 'current': 0.0},
            # {'id':24, 'hk_id':1, 'channel_no':24, 'enabled': True, 'current': 0.0}
        ]
    }
    # Append 24 power channels
    for i in range(1, 25):
        p = PowerChannels()
        p.hk_id = 1
        p.channel_no = i
        p.enabled = True
        p.current = 0.0
        housekeepingData['channels'].append(p)

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