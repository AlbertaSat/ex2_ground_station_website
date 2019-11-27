import unittest
from datetime import datetime
from sqlalchemy import exc

from groundstation.tests.base import BaseTestCase
from groundstation.backend_api.models import Housekeeping, User, PowerChannels
from groundstation import db
from groundstation.tests.utils import fakeHousekeepingAsDict, fake_power_channel_as_dict
from groundstation.backend_api.utils import add_telecommand, \
    add_flight_schedule, add_command_to_flightschedule, \
    add_arg_to_flightschedulecommand, add_user

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
        timestamp = datetime.fromtimestamp(1570749472)
        housekeepingData = fakeHousekeepingAsDict(timestamp)

        housekeeping = Housekeeping(**housekeepingData)

        for i in range(1, 25):
            channel = fake_power_channel_as_dict(i)
            p = PowerChannels(**channel)
            housekeeping.channels.append(p)


        db.session.add(housekeeping)
        db.session.commit()
        self.assertTrue(housekeeping.id)
        self.assertEqual(housekeeping.satellite_mode, 'Passive')
        self.assertEqual(housekeeping.battery_voltage, 1.7)
        self.assertEqual(housekeeping.current_in, 1.2)
        self.assertEqual(housekeeping.no_MCU_resets, 14)
        self.assertEqual(housekeeping.last_beacon_time, timestamp)
        self.assertEqual(housekeeping.watchdog_1, 6000)
        self.assertEqual(housekeeping.watchdog_2, 11)
        self.assertEqual(housekeeping.watchdog_3, 0)
        self.assertEqual(housekeeping.panel_1_current, 1.1)
        self.assertEqual(housekeeping.panel_2_current, 1.0)
        self.assertEqual(housekeeping.panel_3_current, 1.2)
        self.assertEqual(housekeeping.panel_4_current, 1.0)
        self.assertEqual(housekeeping.panel_5_current, 1.0)
        self.assertEqual(housekeeping.panel_6_current, 1.0)
        self.assertEqual(housekeeping.temp_1, 11.0)
        self.assertEqual(housekeeping.temp_2, 11.0)
        self.assertEqual(housekeeping.temp_3, 14.0)
        self.assertEqual(housekeeping.temp_4, 12.0)
        self.assertEqual(housekeeping.temp_5, 11.0)
        self.assertEqual(housekeeping.temp_6, 10.0)
        for i in range(1, 25):
            self.assertEqual(housekeeping.channels[i-1].id, i)
            self.assertEqual(housekeeping.channels[i-1].hk_id, 1)
            self.assertEqual(housekeeping.channels[i-1].channel_no, i)
            self.assertEqual(housekeeping.channels[i-1].enabled, True)
            self.assertEqual(housekeeping.channels[i-1].current, 0.0)

    """Test converting a housekeeping entry into json"""
    def testHousekeepingToJson(self):
        timestamp = datetime.fromtimestamp(1570749472)
        housekeepingData = fakeHousekeepingAsDict(timestamp)

        housekeeping = Housekeeping(**housekeepingData)
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
