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
