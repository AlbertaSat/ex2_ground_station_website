import unittest
from datetime import datetime

from groundstation.tests.base import BaseTestCase
from groundstation.backend_api.models import Housekeeping
from groundstation import db
from groundstation.tests.utils import fakeHousekeepingAsDict

class TestHousekeepingModel(BaseTestCase):

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

	def testToJson(self):
		timestamp = datetime.fromtimestamp(1570749472)
		housekeepingData = fakeHousekeepingAsDict(timestamp)

		housekeeping = Housekeeping(**housekeepingData)
		db.session.add(housekeeping)
		db.session.commit()
		self.assertTrue(isinstance(housekeeping.toJson(), dict))


if __name__ == '__main__':
    unittest.main()
