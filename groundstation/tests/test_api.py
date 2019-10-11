import unittest
import json

from datetime import datetime
from groundstation.tests.base import BaseTestCase
from groundstation import db
from groundstation.api.models import Housekeeping
from groundstation.tests.utils import fakeHousekeepingAsDict

class TestHousekeepingService(BaseTestCase):
	"""Test the housekeeping/satellite model service"""

	def test_get_housekeeping(self):
		"""Test getting a housekeeping log"""
		timestamp = datetime.fromtimestamp(1570749472)
		housekeepingData = fakeHousekeepingAsDict(timestamp)

		housekeeping = Housekeeping(**housekeepingData)
		db.session.add(housekeeping)
		db.session.commit()

		with self.client:
			response = self.client.get(f'/housekeepinglog/{housekeeping.id}')
			data = json.loads(response.data.decode())
			self.assertEqual(response.status_code, 200)
			self.assertIn('Passive', data['data']['satelliteMode'])
			self.assertEqual(1.7, data['data']['batteryVoltage'])
			self.assertEqual(14, data['data']['noMCUResets'])
			self.assertIn(str(timestamp), data['data']['lastBeaconTime'])
			self.assertIn('success', data['status'])



