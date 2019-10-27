from flask import has_app_context
from groundstation import create_app
from groundstation.backend_api.models import Telecommands, FlightSchedules, FlightScheduleCommands
from groundstation import db


# a decorator to handle cases where backend api calls have no app context
# namely for when locally using the api, db session must be initiated
# in order to access models and database operation
def create_context(function):
    def decorate(*args, **kwargs):
        if not has_app_context():
            app = create_app()

            with app.app_context():
                return function(*args, **kwargs)

        else:
             return function(*args, **kwargs)

    return decorate

def add_telecommand(command_name, num_arguments):
		command = Telecommands(command_name=command_name, num_arguments=num_arguments)
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
