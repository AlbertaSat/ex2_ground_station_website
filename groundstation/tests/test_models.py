import unittest
from datetime import datetime

from groundstation.tests.base import BaseTestCase
from groundstation.backend_api.models import Housekeeping
from groundstation import db
from groundstation.tests.utils import fakeHousekeepingAsDict, add_command, add_flight_schedule, add_command_to_flightschedule

class TestHousekeepingModel(BaseTestCase):

	"""Test adding a housekeeping entry"""
	def testAddHousekeepingEntry(self):
		timestamp = datetime.fromtimestamp(1570749472)
		housekeepingData = fakeHousekeepingAsDict(timestamp)

		housekeeping = Housekeeping(**housekeepingData)
		db.session.add(housekeeping)
		db.session.commit()
		self.assertTrue(housekeeping.id)
		self.assertEqual(housekeeping.satelliteMode, 'Passive')
		self.assertEqual(housekeeping.batteryVoltage, 1.7)
		self.assertEqual(housekeeping.currentIn, 1.2)
		self.assertEqual(housekeeping.noMCUResets, 14)
		self.assertEqual(housekeeping.lastBeaconTime, timestamp)

	"""Test converting a housekeeping entry into json"""
	def testHousekeepingToJson(self):
		timestamp = datetime.fromtimestamp(1570749472)
		housekeepingData = fakeHousekeepingAsDict(timestamp)

		housekeeping = Housekeeping(**housekeepingData)
		db.session.add(housekeeping)
		db.session.commit()
		self.assertTrue(isinstance(housekeeping.toJson(), dict))

class TestCommandModel(BaseTestCase):

	"""Test adding a command"""
	def test_add_command(self):
		command = add_command(command_name='ping', num_arguments=0)
		self.assertTrue(command.id)
		self.assertEqual(command.command_name, 'ping')
		self.assertEqual(command.num_arguments, 0)

class TestFlightScheduleModel(BaseTestCase):

	""""Test adding a flight schedule"""
	def test_add_flight_schedule(self):
		timestamp = datetime.fromtimestamp(1570749472)
		flightschedule = add_flight_schedule(creation_date=timestamp, upload_date=timestamp)
		self.assertTrue(flightschedule.id)
		self.assertEqual(timestamp, flightschedule.creation_date)
		self.assertEqual(timestamp, flightschedule.upload_date)

class TestFlightScheduleCommandsModel(BaseTestCase):

	"""Test adding a command to the flight schedule"""
	def test_add_command_to_flight_schedule(self):
		timestamp = datetime.fromtimestamp(1570749472)
		command = add_command(command_name='ping', num_arguments=0)
		flightschedule = add_flight_schedule(creation_date=timestamp, upload_date=timestamp)
		flightschedule_commands = add_command_to_flightschedule(
									timestamp=timestamp,
									flightschedule_id=flightschedule.id,
									command_id=command.id
								)
		self.assertTrue(flightschedule_commands.id)
		self.assertEqual(flightschedule_commands.timestamp, timestamp)
		self.assertEqual(flightschedule_commands.command_id, command.id)
		self.assertEqual(flightschedule_commands.flightschedule_id, flightschedule.id)



if __name__ == '__main__':
    unittest.main()
