import unittest
import json

from datetime import datetime
from groundstation.tests.base import BaseTestCase
from groundstation import db
from groundstation.backend_api.models import Housekeeping
from groundstation.tests.utils import fakeHousekeepingAsDict
from groundstation.backend_api.housekeeping import HousekeepingLogList

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
            response = self.client.get(f'/api/housekeepinglog/{housekeeping.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Passive', data['data']['satelliteMode'])
            self.assertEqual(1.7, data['data']['batteryVoltage'])
            self.assertEqual(14, data['data']['noMCUResets'])
            self.assertIn(str(timestamp), data['data']['lastBeaconTime'])
            self.assertIn('success', data['status'])


    def test_get_housekeeping_incorrect_id(self):
        with self.client:
            response = self.client.get('/api/housekeepinglog/123')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Housekeeping Log does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_post_housekeeping(self):
        timestamp = str(datetime.fromtimestamp(1570749472))
        housekeepingData = fakeHousekeepingAsDict(timestamp)
        with self.client:
            response = self.client.post(
                '/api/housekeepinglog',
                data=json.dumps(housekeepingData),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertEqual(
                f'Housekeeping Log with timestamp {timestamp} was added!', 
                data['message']
            )
            self.assertIn('success', data['status'])

    def test_post_housekeeping_locally(self):
        """Since local data is wrapped differently than data over http, 
        we must send and receive it differently (locally it is a tuple of dicts)"""
        timestamp = str(datetime.fromtimestamp(1570749472))
        housekeepingData = fakeHousekeepingAsDict(timestamp)
        housekeepingLogList = HousekeepingLogList()
        response = housekeepingLogList.post(local_data=json.dumps(housekeepingData))
        self.assertEqual(response[1], 201)
        self.assertEqual(
            f'Housekeeping Log with timestamp {timestamp} was added!', 
            response[0]['message']
        )
        self.assertIn('success', response[0]['status'])


