"""
The Manage Module is how you can run the flask application through the command
line. It also allows you to define your own command line functions
that can be called as:

    python3 manage.py <command_line_command>

As is you can also run tests by specifying the module path like so:

    python3 manage.py test test_api.TestHousekeepingService

or:

    python3 manage.py test test_api.TestHousekeepingService.test_get_housekeeping

"""
import sys
import unittest
from datetime import datetime, timedelta
import json
import click
import re
import subprocess
import os

from flask.cli import FlaskGroup
from sqlalchemy import false

from groundstation import create_app, db
from groundstation.backend_api.models import User, Housekeeping, Telecommands, PowerChannels
from groundstation.tests.utils import fakeHousekeepingAsDict, fake_power_channel_as_dict
from groundstation.backend_api.housekeeping import HousekeepingLogList
from groundstation.backend_api.utils import add_telecommand, \
    add_flight_schedule, add_command_to_flightschedule, add_user, \
    add_arg_to_flightschedulecommand, add_message_to_communications, \
    add_passover

from ex2_ground_station_software.src.groundStation.system import SystemValues
server_prefixes = SystemValues().APP_DICT.keys()

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    """Drops and recreates the database (with no initial data)
    """
    db.drop_all()
    db.create_all()
    db.session.commit()

    now = datetime.utcnow()
    add_passover(aos_timestamp=now - timedelta(seconds=60), los_timestamp=now)
    print("Database has been dropped and recreated.")


@cli.command()
@click.argument('path', required=False)
def test(path=None):
    """Runs all tests in tests folder
    """
    if path is None:
        tests = unittest.TestLoader().discover(
            'groundstation/tests', pattern='test*.py')
    else:
        tests = unittest.TestLoader().loadTestsFromName(
            f'groundstation.tests.{path}')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    sys.exit(result)


@cli.command('seed_db')
@click.pass_context
def seed_db(ctx):
    """Imports commands and adds admin and non-admin user.
    """
    ctx.invoke(import_commands) # no telecommands added if import fails

    add_user(username='Admin_user', password='Admin_user', is_admin=True)
    add_user(username='albert', password='albert', is_admin=False)


@cli.command('seed_db_example')
@click.pass_context
def seed_db_example(ctx):
    """Imports commands, adds users and example data.
    """
    # generate timestamps for flightschedule commands
    timestamp = datetime.fromtimestamp(1570749472)
    for x in range(20):
        # 20 days
        for y in range(3):
            # 3 entries per day
            housekeepingData = fakeHousekeepingAsDict(
                timestamp + timedelta(days=x, minutes=y*15))
            if (x+y) % 10 == 0:
                housekeepingData['satellite_mode'] = 'Danger'

            housekeeping = Housekeeping(**housekeepingData)

            for i in range(1, 25):
                channel = fake_power_channel_as_dict(i)
                p = PowerChannels(**channel)
                housekeeping.channels.append(p)

            db.session.add(housekeeping)
    db.session.commit()

    ctx.invoke(import_commands) # no telecommands added if import fails

    flightschedule = add_flight_schedule(
        creation_date=timestamp, upload_date=timestamp, status=2, execution_time=timestamp)

    # add a few commands to flightschedule
    commands = Telecommands.query.all()

    for i in range(0, min(len(commands), 2)):
        command = commands[i]
        flightschedule_commands = add_command_to_flightschedule(
            timestamp=timestamp,
            flightschedule_id=flightschedule.id,
            command_id=command.id
        )

    add_user(username='Admin_user', password='Admin_user', is_admin=True)
    add_user(username='albert', password='albert', is_admin=False)

    message = add_message_to_communications(
        timestamp=timestamp,
        message='ping',
        sender='user',
        receiver='comm',
        is_queued=False
    )

    now = datetime.utcnow()
    add_passover(aos_timestamp=now - timedelta(seconds=20), los_timestamp=now)
    for i in range(1, 20):
        p = add_passover(aos_timestamp=now + timedelta(minutes=i*5), los_timestamp=now + timedelta(minutes=i*5 + 1))
    print("Database has been seeded.")


@cli.command('demo_db')
def demo_db():
    db.drop_all()
    db.create_all()

    timestamp = datetime.fromtimestamp(1570749472)
    time2 = datetime.fromisoformat('2019-11-04 00:05:23.283+00:00')
    #time3 = datetime.fromisoformat('2019-11-05 00:08:43.203+00:00')
    #time4 = datetime.fromisoformat('2019-11-05 00:15:20.118+00:00')

    housekeepingData = fakeHousekeepingAsDict(timestamp)
    hkd2 = fakeHousekeepingAsDict(time2)
    #hkd3 = fakeHousekeepingAsDict(time3)
    #hkd4 = fakeHousekeepingAsDict(time4)

    housekeeping = Housekeeping(**housekeepingData)
    hk2 = Housekeeping(**hkd2)
    #hk3 = Housekeeping(**hkd3)
    #hk4 = Housekeeping(**hkd4)

    db.session.add(housekeeping)
    db.session.add(hk2)
    # db.session.add(hk3)
    # db.session.add(hk4)

    db.session.commit()

    add_user(username='Ex-Alta-Master', password='master88', is_admin=True)
    add_user(username='Ex-Alta-Safety', password='totalRecall', is_admin=True)
    add_user(username='Manny1996', password='valientHearts', is_admin=False)
    add_user(username='Impeach45', password='russia45', is_admin=False)
    add_user(username='StarFinder', password='spaceForce', is_admin=False)
    add_user(username='JojoBagins', password='ExOhExOhEx', is_admin=False)
    add_user(username='HJDewit', password='simplify0923', is_admin=False)

    commands = {
        'ping': (0, False),
        'get_hk': (0, False),
        'turn_on': (1, True),
        'turn_off': (1, True),
        'set_fs': (1, True),
        'upload_fs': (0, False)
    }

    for name, (num_args, is_danger) in commands.items():
        c = add_telecommand(command_name=name,
                            num_arguments=num_args, is_dangerous=is_danger)

    command = Telecommands.query.filter_by(command_name='ping').first()
    flightschedule = add_flight_schedule(
        creation_date=timestamp, upload_date=timestamp, status=2, execution_time=timestamp)
    flightschedule_commands = add_command_to_flightschedule(
        timestamp=timestamp,
        flightschedule_id=flightschedule.id,
        command_id=command.id
    )

    command = Telecommands.query.filter_by(command_name='turn_on').first()
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
        receiver='comm',
        is_queued=False
    )

    command = Telecommands.query.filter_by(command_name='ping').first()
    flightschedule = add_flight_schedule(
        creation_date=time2, upload_date=time2, status=2, execution_time=time2)
    flightschedule_commands = add_command_to_flightschedule(
        timestamp=time2,
        flightschedule_id=flightschedule.id,
        command_id=command.id
    )

    flightschedulecommand_arg = add_arg_to_flightschedulecommand(
        index=1,
        argument='5',
        flightschedule_command_id=flightschedule_commands.id
    )

    message = add_message_to_communications(
        timestamp=time2,
        message='ping',
        sender='user',
        receiver='comm',
        is_queued=False
    )

    now = datetime.utcnow()
    add_passover(aos_timestamp=now - timedelta(seconds=20), los_timestamp=now)
    for i in range(5):
        p = add_passover(aos_timestamp=now + timedelta(minutes=i*5), los_timestamp=now + timedelta(minutes=i*5 + 1))

    print("Database has been seeded with demo data.")


@cli.command('import_commands')
def import_commands():
    """Imports commands from the CommandDocs.txt file in ex2_ground_station_software,
    and adds them to the database.
    """

    filepath = 'ex2_ground_station_software/CommandDocs.txt'

    if not os.path.exists(filepath):
        print(f'Couldn\'t find list of commands at {filepath}. Seeding database with no commands.')
        return False

    # first regenerate CommandDocs.txt
    print('Regenerating commands.')
    subprocess.run(['./regenerate_commands.sh'])

    with open('./ex2_ground_station_software/CommandDocs.txt', 'r') as f:
        text = f.read()

    # regex command based on current formatting of CommandDocs.txt; might need to be changed later
    blocks = re.findall('[\.\n]([A-Z0-9_.]*):[^\[]*\[([^\]]*)\]', text)

    for (command_name, arguments) in blocks:
        # currently false; need to figure out which commands should be considered dangerous
        is_dangerous = False

        if arguments == 'None':
            num_arguments = 0
        else:
            num_arguments = len(re.findall(',', arguments)) + 1

        # make a copy of each command for each server
        for prefix in server_prefixes:
            c = add_telecommand(command_name=(prefix + '.' + command_name).lower(), num_arguments=num_arguments,
                                is_dangerous=is_dangerous)

    print("Added new telecommands.")

    return True


if __name__ == '__main__':
    cli()
