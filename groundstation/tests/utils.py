def fakeHousekeepingAsDict(timestamp):
	housekeepingData = {
        'satellite_mode' : 'Passive',
        'battery_voltage': 1.7,
        'current_in': 1.2,
        'current_out': 1.1,
        'no_MCU_resets': 14,
        'last_beacon_time': timestamp,

        'watchdog_1': 6000,     # Watchdog counts
        'watchdog_2': 5,
        'watchdog_3': 0,
        'panel_1_current': 1.0, # Solar panel currents
        'panel_2_current': 1.0,
        'panel_3_current': 1.0,
        'panel_4_current': 1.0,
        'panel_5_current': 1.0,
        'panel_6_current': 1.0,
        'temp_1': 11,           # Temperatures
        'temp_2': 11,
        'temp_3': 14,
        'temp_4': 12,
        'temp_5': 11,
        'temp_6': 10,
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