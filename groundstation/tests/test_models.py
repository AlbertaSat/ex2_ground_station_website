import unittest
from datetime import datetime
from sqlalchemy import exc

from groundstation.tests.base import BaseTestCase
from groundstation.backend_api.models import AdcsHK, AthenaHK, CharonHK, \
    DfgmHK, EpsHK, EpsStartupHK, Housekeeping, HyperionHK, IrisHK, \
    NorthernSpiritHK, SbandHK, UhfHK, User
from groundstation import db
from groundstation.backend_api.utils import add_telecommand, \
    add_flight_schedule, add_command_to_flightschedule, \
    add_arg_to_flightschedulecommand, add_user
from groundstation.tests.utils import fake_adcs_hk_as_dict, \
    fake_athena_hk_as_dict, fake_charon_hk_as_dict, fake_dfgm_hk_as_dict, \
    fake_eps_hk_as_dict, fake_eps_startup_hk_as_dict, fake_housekeeping_as_dict, \
    fake_hyperion_hk_as_dict, fake_iris_hk_as_dict, \
    fake_northern_spirit_hk_as_dict, fake_sband_hk_as_dict, fake_uhf_hk_as_dict

class TestUserModel(BaseTestCase):

    def test_unique_username_constraint(self):
        user1 = add_user('Alice', 'null')
        self.assertRaises(exc.IntegrityError, add_user, 'Alice', 'null')

    def test_password_hashes_are_random(self):
        user1 = add_user('Alice', 'password1')
        user2 = add_user('Bob', 'password2')
        self.assertNotEqual(user1.password_hash, user2.password_hash)

    def test_encode_auth_token(self):
        user = add_user('Alice', 'secret-password')
        auth_token = user.encode_auth_token_by_id()
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = add_user('Alice', 'secret-password')
        auth_token = user.encode_auth_token_by_id()
        user_id = User.decode_auth_token(auth_token)
        token_user = User.query.filter_by(id=user_id).first()
        self.assertEqual(user.id, token_user.id)
        self.assertEqual(user.username, token_user.username)


class TestHousekeepingModel(BaseTestCase):

    """Test adding a housekeeping entry"""
    def testAddHousekeepingEntry(self):
        timestamp = datetime.fromtimestamp(1659816386)
        housekeepingData = fake_housekeeping_as_dict(timestamp, 1)

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
        self.assertTrue(housekeeping.id)
        self.assertEqual(housekeeping.data_position, 1)

        # Test if subsystem data exists
        self.assertIsNotNone('adcs')
        self.assertIsNotNone('athena')
        self.assertIsNotNone('eps')
        self.assertIsNotNone('eps_startup')
        self.assertIsNotNone('uhf')
        self.assertIsNotNone('sband')
        self.assertIsNotNone('hyperion')
        self.assertIsNotNone('charon')
        self.assertIsNotNone('dfgm')
        self.assertIsNotNone('northern_spirit')
        self.assertIsNotNone('iris')

        # Test values
        self.assertEqual(housekeeping.adcs.Att_Estimate_Mode, 42)
        self.assertEqual(housekeeping.adcs.Longitude, 13.37)
        self.assertEqual(housekeeping.athena.MCU_core_temp, 42)
        self.assertEqual(housekeeping.eps.eps_cmd_hk, 42)
        self.assertEqual(housekeeping.eps.eps_timestamp_hk, 13.37)
        self.assertEqual(housekeeping.eps_startup.eps_cmd_startup, 42)
        self.assertEqual(housekeeping.eps_startup.eps_timestamp_startup, 13.37)
        self.assertEqual(housekeeping.uhf.scw1, 42)
        self.assertEqual(housekeeping.uhf.temperature, 13.37)
        self.assertEqual(housekeeping.sband.Output_Power, 42)
        self.assertEqual(housekeeping.hyperion.Port_Pd1, 42)
        self.assertEqual(housekeeping.charon.charon_temp7, 42)
        self.assertEqual(housekeeping.dfgm.Input_Current, 42)
        self.assertEqual(housekeeping.northern_spirit.ns_temp3, 42)
        self.assertEqual(housekeeping.iris.Error_number, 42)
        self.assertEqual(housekeeping.iris.NIR_Temperature, 13.37)

    """Test converting a housekeeping entry into json"""
    def testHousekeepingToJson(self):
        timestamp = datetime.fromtimestamp(1659816386)
        housekeepingData = fake_housekeeping_as_dict(timestamp, 1)

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
        self.assertTrue(isinstance(housekeeping.to_json(), dict))

class TestCommandModel(BaseTestCase):

    """Test adding a command"""
    def test_add_command(self):
        command = add_telecommand(command_name='ping', num_arguments=0, is_dangerous=False)
        self.assertTrue(command.id)
        self.assertEqual(command.command_name, 'ping')
        self.assertEqual(command.num_arguments, 0)
        self.assertEqual(command.is_dangerous, False)

class TestFlightScheduleModel(BaseTestCase):

    """"Test adding a flight schedule"""
    def test_add_flight_schedule(self):
        timestamp = datetime.fromtimestamp(1570749472)
        flightschedule = add_flight_schedule(
            creation_date=timestamp,
            upload_date=timestamp,
            status=2,
            execution_time=timestamp
        )
        self.assertTrue(flightschedule.id)
        self.assertEqual(timestamp, flightschedule.creation_date)
        self.assertEqual(timestamp, flightschedule.upload_date)

class TestFlightScheduleCommandsModel(BaseTestCase):

    """Test adding a command to the flight schedule"""
    def test_add_command_to_flight_schedule(self):
        timestamp = datetime.fromtimestamp(1570749472)
        command = add_telecommand(command_name='ping', num_arguments=0, is_dangerous=False)
        flightschedule = add_flight_schedule(
            creation_date=timestamp,
            upload_date=timestamp,
            status=2,
            execution_time=timestamp
        )
        flightschedule_commands = add_command_to_flightschedule(
                                    timestamp=timestamp,
                                    flightschedule_id=flightschedule.id,
                                    command_id=command.id
                                )
        self.assertTrue(flightschedule_commands.id)
        self.assertEqual(flightschedule_commands.timestamp, timestamp)
        self.assertEqual(flightschedule_commands.command_id, command.id)
        self.assertEqual(flightschedule_commands.flightschedule_id, flightschedule.id)

class TestFlightScheduleCommandsArgsModel(BaseTestCase):

    """Test adding an argument to a command"""
    def test_add_arg_to_flightschedule_command(self):
        timestamp = datetime.fromtimestamp(1570749472)
        command = add_telecommand(command_name='turn-on', num_arguments=1, is_dangerous=False)
        flightschedule = add_flight_schedule(
            creation_date=timestamp,
            upload_date=timestamp,
            status=2,
            execution_time=timestamp
        )
        flightschedule_commands = add_command_to_flightschedule(
                                    timestamp=timestamp,
                                    flightschedule_id=flightschedule.id,
                                    command_id=command.id
                                )
        command_arg = add_arg_to_flightschedulecommand(
                        index=0,
                        argument='5',
                        flightschedule_command_id=flightschedule_commands.id
                    )
        self.assertTrue(command_arg.id)
        self.assertEqual(command_arg.index, 0)
        self.assertEqual(command_arg.argument, '5')
        self.assertEqual(command_arg.flightschedulecommand_id, flightschedule_commands.id)


if __name__ == '__main__':
    unittest.main()
