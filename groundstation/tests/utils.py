def fakeHousekeepingAsDict(timestamp):
	housekeepingData = {
						'satelliteMode' : 'Passive',
						'batteryVoltage': 1.7,
						'currentIn': 1.2,
						'currentOut': 1.1,
						'noMCUResets': 14,
						'lastBeaconTime': timestamp
					}

	return housekeepingData

def fake_flight_schedule_as_dict(is_queued=False, commands=[]):
    flightschedule = {
        'is_queued':is_queued,
        'commands':commands
    }
    return flightschedule
