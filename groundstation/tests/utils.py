def fakeHousekeepingAsDict(timestamp):
	housekeepingData = {
						'satellite_Mode' : 'Passive',
						'battery_Voltage': 1.7,
						'current_In': 1.2,
						'current_Out': 1.1,
						'no_MCU_Resets': 14,
						'last_Beacon_Time': timestamp
					}

	return housekeepingData
