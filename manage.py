import sys
import unittest
from datetime import datetime
import json

from flask.cli import FlaskGroup

from groundstation import create_app, db
from groundstation.backend_api.models import User, Housekeeping, Telecommands
from groundstation.tests.utils import fakeHousekeepingAsDict
from groundstation.backend_api.housekeeping import HousekeepingLogList
from groundstation.backend_api.utils import add_telecommand, add_flight_schedule, add_command_to_flightschedule

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('recreate_db')
def recreate_db():
    """Recreate the database"""
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
def test():
    """Runs all tests in tests folder"""
    tests = unittest.TestLoader().discover('groundstation/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)

@cli.command('seed_db')
def seed_db():
    timestamp = datetime.fromtimestamp(1570749472)
    housekeepingData = fakeHousekeepingAsDict(timestamp)

    housekeeping = Housekeeping(**housekeepingData)
    db.session.add(housekeeping)
    db.session.commit()

    commands = {
        'ping': (0,False),
        'get-hk':(0,False),
        'turn-on':(1,True),
        'turn-off':(1,True),
        'set-fs':(1,True),
    }

    for name, (num_args, is_danger) in commands.items():
        c = add_telecommand(command_name=name, num_arguments=num_args, is_dangerous=is_danger)

    command = Telecommands.query.filter_by(command_name='ping').first()
    flightschedule = add_flight_schedule(creation_date=timestamp, upload_date=timestamp)
    flightschedule_commands = add_command_to_flightschedule(
                                timestamp=timestamp,
                                flightschedule_id=flightschedule.id,
                                command_id=command.id
                            )


if __name__ == '__main__':
    cli()
