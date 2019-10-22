from groundstation.backend_api.models import Commands, FlightSchedules, FlightScheduleCommands
from groundstation import db

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

def add_command(command_name, num_arguments):
		command = Commands(command_name=command_name, num_arguments=num_arguments)
		db.session.add(command)
		db.session.commit()
		return command

def add_flight_schedule(creation_date, upload_date):
	flightschedule = FlightSchedules(creation_date=creation_date, upload_date=upload_date)
	db.session.add(flightschedule)
	db.session.commit()
	return flightschedule

def add_command_to_flightschedule(timestamp, flightschedule_id, command_id):
	flightschedule_commands = FlightScheduleCommands(
								timestamp=timestamp, 
								flightschedule_id=flightschedule_id, 
								command_id=command_id
							)
	db.session.add(flightschedule_commands)
	db.session.commit()
	return flightschedule_commands
