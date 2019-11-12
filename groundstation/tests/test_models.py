import unittest
from datetime import datetime

from groundstation.tests.base import BaseTestCase
from groundstation.backend_api.models import Housekeeping
from groundstation import db
from groundstation.tests.utils import fakeHousekeepingAsDict
from groundstation.backend_api.utils import add_telecommand, add_flight_schedule, add_command_to_flightschedule, \
add_arg_to_flightschedulecommand

class TestHousekeepingModel(BaseTestCase):

    """Test adding a housekeeping entry"""
    def testAddHousekeepingEntry(self):
        timestamp = datetime.fromtimestamp(1570749472)
        housekeepingData = fakeHousekeepingAsDict(timestamp)

        housekeeping = Housekeeping(**housekeepingData)
        db.session.add(housekeeping)
        db.session.commit()
        self.assertTrue(housekeeping.id)
        self.assertEqual(housekeeping.satellite_mode, 'Passive')
        self.assertEqual(housekeeping.battery_voltage, 1.7)
        self.assertEqual(housekeeping.current_in, 1.2)
        self.assertEqual(housekeeping.no_MCU_resets, 14)
        self.assertEqual(housekeeping.last_beacon_time, timestamp)

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
        flightschedule = add_flight_schedule(creation_date=timestamp, upload_date=timestamp, status=2)
        self.assertTrue(flightschedule.id)
        self.assertEqual(timestamp, flightschedule.creation_date)
        self.assertEqual(timestamp, flightschedule.upload_date)

class TestFlightScheduleCommandsModel(BaseTestCase):

    """Test adding a command to the flight schedule"""
    def test_add_command_to_flight_schedule(self):
        timestamp = datetime.fromtimestamp(1570749472)
        command = add_telecommand(command_name='ping', num_arguments=0, is_dangerous=False)
        flightschedule = add_flight_schedule(creation_date=timestamp, upload_date=timestamp, status=2)
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
        flightschedule = add_flight_schedule(creation_date=timestamp, upload_date=timestamp, status=2)
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
