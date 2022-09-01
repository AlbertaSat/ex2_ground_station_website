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
import click

from flask.cli import FlaskGroup

from groundstation import create_app, db
from groundstation.backend_api.models import AdcsHK, AthenaHK, CharonHK, \
    DfgmHK, EpsHK, EpsStartupHK, HyperionHK, IrisHK, NorthernSpiritHK, SbandHK, \
    UhfHK, User, Housekeeping, Telecommands
from groundstation.tests.utils import fake_adcs_hk_as_dict, \
    fake_athena_hk_as_dict, fake_charon_hk_as_dict, fake_dfgm_hk_as_dict, \
    fake_eps_hk_as_dict, fake_eps_startup_hk_as_dict, fake_housekeeping_as_dict, \
    fake_hyperion_hk_as_dict, fake_iris_hk_as_dict, \
    fake_northern_spirit_hk_as_dict, fake_sband_hk_as_dict, fake_uhf_hk_as_dict
from groundstation.backend_api.housekeeping import HousekeepingLogList
from groundstation.backend_api.utils import add_telecommand, \
    add_flight_schedule, add_command_to_flightschedule, add_user, \
    add_arg_to_flightschedulecommand, add_message_to_communications, \
    add_passover

from ex2_ground_station_software.src.system import SatelliteNodes, services
AVAILABLE_OBCS = tuple(node[1] for node in SatelliteNodes if node[0] == 'OBC')
AVAILABLE_EPS = tuple(node[1] for node in SatelliteNodes if node[0] == 'EPS')


app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command('recreate_db')
def recreate_db():
    """Drops and recreates the database (with no initial data)
    """
    db.drop_all()
    db.create_all()
    db.session.commit()

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
    """Imports commands and adds admin and non-admin user as well as a base passover.
    """
    ctx.invoke(import_commands)  # no telecommands added if import fails

    add_user(username='Admin_user', password='Admin_user', is_admin=True)
    add_user(username='albert', password='albert', is_admin=False)

    now = datetime.utcnow()
    add_passover(aos_timestamp=now - timedelta(seconds=60), los_timestamp=now)


@cli.command('seed_db_example')
@click.pass_context
def seed_db_example(ctx):
    """Imports commands, adds users and example data.
    """
    # generate timestamps for flightschedule commands
    timestamp = datetime.utcnow()
    data_position = 1
    for x in range(20):
        # 20 days
        for y in range(3):
            # 3 entries per day
            housekeepingData = fake_housekeeping_as_dict(
                timestamp + timedelta(days=x, minutes=y*15), data_position)

            data_position += 1

            housekeeping = Housekeeping(
                **housekeepingData,
                adcs=AdcsHK(**fake_adcs_hk_as_dict()),
                athena=AthenaHK(**fake_athena_hk_as_dict()),
                eps=EpsHK(**fake_eps_hk_as_dict()),
                eps_startup=EpsStartupHK(**fake_eps_startup_hk_as_dict()),
                uhf=UhfHK(**fake_uhf_hk_as_dict()),
                sband=SbandHK(**fake_sband_hk_as_dict()),
                hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
                charon=CharonHK(**fake_charon_hk_as_dict()),
                dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
                northern_spirit=NorthernSpiritHK(
                    **fake_northern_spirit_hk_as_dict()),
                iris=IrisHK(**fake_iris_hk_as_dict())
            )

            db.session.add(housekeeping)
    db.session.commit()

    ctx.invoke(import_commands)  # no telecommands added if import fails

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
        p = add_passover(aos_timestamp=now + timedelta(minutes=i*5),
                         los_timestamp=now + timedelta(minutes=i*5 + 1))
    print("Database has been seeded.")


@cli.command('demo_db')
def demo_db():
    db.drop_all()
    db.create_all()

    timestamp = datetime.fromtimestamp(1570749472)
    time2 = datetime.fromisoformat('2019-11-04 00:05:23.283+00:00')
    #time3 = datetime.fromisoformat('2019-11-05 00:08:43.203+00:00')
    #time4 = datetime.fromisoformat('2019-11-05 00:15:20.118+00:00')

    housekeepingData = fake_housekeeping_as_dict(timestamp)
    hkd2 = fake_housekeeping_as_dict(time2)
    #hkd3 = fake_housekeeping_as_dict(time3)
    #hkd4 = fake_housekeeping_as_dict(time4)

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
        p = add_passover(aos_timestamp=now + timedelta(minutes=i*5),
                         los_timestamp=now + timedelta(minutes=i*5 + 1))

    print("Database has been seeded with demo data.")


@cli.command('import_commands')
def import_commands():
    """Imports commands from the system.py file in ex2_ground_station_software/src,
    and adds them to the database.
    """
    for serv in services:
        subservice = services[serv]['subservice']

        supported_prefixes = list(services[serv]['supports'])
        if 'OBC' in supported_prefixes:
            supported_prefixes.remove('OBC')
            supported_prefixes.extend(AVAILABLE_OBCS)
        if 'EPS' in supported_prefixes:
            supported_prefixes.remove('EPS')
            supported_prefixes.extend(AVAILABLE_EPS)

        for subName in subservice.keys():
            sub = subservice[subName]
            inoutInfo = sub['inoutInfo']
            info = 'Not yet available' if not 'what' in sub else sub['what']
            
            if inoutInfo['args'] is None:
                num_arguments = 0
                arg_list=None
            else:
                num_arguments = len(inoutInfo['args'])
                arg_list=''
                for arg in inoutInfo['args'].keys():
                    arg_list = arg_list + str(arg) + ', '
                arg_list = arg_list[:-2]
                
            is_dangerous = False
            for i, prefix in enumerate(supported_prefixes):
                if i == 0:
                    # Only one 'copy' of a command needs the about_info
                    add_telecommand(command_name=(prefix + '.' + serv + '.' + subName).lower(), num_arguments=num_arguments,
                                    is_dangerous=is_dangerous, about_info=info, arg_labels=arg_list)
                else:
                    add_telecommand(command_name=(prefix + '.' + serv + '.' + subName).lower(), num_arguments=num_arguments,
                                    is_dangerous=is_dangerous, about_info=None, arg_labels=None)

    print("Added new telecommands.")

    return True


if __name__ == '__main__':
    cli()
