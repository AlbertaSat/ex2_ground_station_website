import sys
import unittest
from datetime import datetime
import json

from flask.cli import FlaskGroup

from groundstation import create_app, db
from groundstation.backend_api.models import User, Housekeeping
from groundstation.tests.utils import fakeHousekeepingAsDict
from groundstation.backend_api.housekeeping import HousekeepingLogList
from groundstation.backend_api.utils import add_command, add_flight_schedule, add_command_to_flightschedule

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

    command = add_command(command_name='ping', num_arguments=0)
    flightschedule = add_flight_schedule(creation_date=timestamp)
    flightschedule_commands = add_command_to_flightschedule(
                                timestamp=timestamp,
                                flightschedule_id=flightschedule.id,
                                command_id=command.id
                            )

    print(flightschedule.to_json())


if __name__ == '__main__':
    cli()
