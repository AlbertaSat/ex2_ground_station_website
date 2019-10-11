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