import sys
import unittest
from datetime import datetime, timedelta
import json
import click

from flask.cli import FlaskGroup

from groundstation import create_app, db
from groundstation.backend_api.models import User, Housekeeping, Telecommands
from groundstation.tests.utils import fakeHousekeepingAsDict
from groundstation.backend_api.housekeeping import HousekeepingLogList
from groundstation.backend_api.utils import add_telecommand, \
add_flight_schedule, add_command_to_flightschedule, add_user, \
add_arg_to_flightschedulecommand, add_message_to_communications, \
add_passover

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('recreate_db')
def recreate_db():
    """Recreate the database"""
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command()
@click.argument('path', required=False)
def test(path=None):
    """Runs all tests in tests folder"""
    if path is None:
        tests = unittest.TestLoader().discover('groundstation/tests', pattern='test*.py')
    else:
        tests = unittest.TestLoader().loadTestsFromName(f'groundstation.tests.{path}')
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
        'upload-fs': (0, False)
    }

    for name, (num_args, is_danger) in commands.items():
        c = add_telecommand(command_name=name, num_arguments=num_args, is_dangerous=is_danger)

    command = Telecommands.query.filter_by(command_name='ping').first()
    flightschedule = add_flight_schedule(creation_date=timestamp, upload_date=timestamp, status=2, execution_time=timestamp)
    flightschedule_commands = add_command_to_flightschedule(
                                timestamp=timestamp,
                                flightschedule_id=flightschedule.id,
                                command_id=command.id
                            )

    add_user(username='Admin_user', password='Admin_user', is_admin=True)
    add_user(username='user1', password='user1', is_admin=False)
    add_user(username='user2', password='user2', is_admin=False)
    command = Telecommands.query.filter_by(command_name='turn-on').first()
    flightschedule_commands = add_command_to_flightschedule(
                                timestamp=timestamp,
                                flightschedule_id=flightschedule.id,
                                command_id=command.id
                            )

    flightschedulecommand_arg = add_arg_to_flightschedulecommand(
                                index=0,
                                argument='5',
                                flightschedule_command_id=flightschedule_commands.id
                            )

    message = add_message_to_communications(
                    timestamp=timestamp,
                    message='ping',
                    sender='user',
                    receiver='comm'
                )

    now = datetime.utcnow()
    add_passover(timestamp=now - timedelta(seconds=10))
    for i in range(5):
        add_passover(timestamp=now + timedelta(minutes=i*2))






if __name__ == '__main__':
    cli()
