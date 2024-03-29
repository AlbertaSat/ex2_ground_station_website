from flask_testing import TestCase, LiveServerTestCase
from groundstation import create_app, db
from selenium import webdriver
import urllib.request
from datetime import datetime, timedelta

from groundstation.backend_api.models import AdcsHK, AthenaHK, CharonHK, \
    DfgmHK, EpsHK, Housekeeping, HyperionHK, IrisHK, NorthernSpiritHK, \
    SbandHK, Telecommands, UhfHK
from groundstation.backend_api.utils import add_telecommand, \
    add_flight_schedule, add_command_to_flightschedule, add_user, \
    add_arg_to_flightschedulecommand, add_message_to_communications, \
    add_passover
from groundstation.tests.utils import fake_adcs_hk_as_dict, \
    fake_athena_hk_as_dict, fake_charon_hk_as_dict, fake_dfgm_hk_as_dict, \
    fake_eps_hk_as_dict, fake_housekeeping_as_dict, fake_hyperion_hk_as_dict, \
    fake_iris_hk_as_dict, fake_northern_spirit_hk_as_dict, \
    fake_sband_hk_as_dict, fake_uhf_hk_as_dict


app = create_app()

class BaseTestCase(TestCase):

    def create_app(self):
        app.config.from_object('groundstation.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class BaseTestCaseFrontEnd(LiveServerTestCase):

    def create_app(self):
        app.config.from_object('groundstation.config.TestingConfig')
        return app

    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.get(self.get_server_url())

        db.drop_all()
        db.create_all()
        db.session.commit()

        # seed the database for testing
        timestamp = datetime.fromtimestamp(1659816386)
        for i in range(20):
            housekeepingData = fake_housekeeping_as_dict(timestamp + timedelta(minutes=i*15), i)

            housekeeping = Housekeeping(
                **housekeepingData,
                adcs=AdcsHK(**fake_adcs_hk_as_dict()),
                athena=AthenaHK(**fake_athena_hk_as_dict()),
                eps=EpsHK(**fake_eps_hk_as_dict()),
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
                        receiver='comm',
                        is_queued=False
                    )

        now = datetime.utcnow()
        add_passover(timestamp=now - timedelta(seconds=10))
        for i in range(1, 20):
            p = add_passover(timestamp=now + timedelta(minutes=i*5))

        db.session.commit()

    def tearDown(self):
        self.driver.quit()
        db.session.remove()
        db.drop_all()
