import unittest
import json

from datetime import datetime
from groundstation.tests.base import BaseTestCase
from groundstation import db
from groundstation.backend_api.models import Housekeeping, FlightSchedules
from groundstation.tests.utils import fakeHousekeepingAsDict, fake_flight_schedule_as_dict
from groundstation.backend_api.housekeeping import HousekeepingLogList
from groundstation.backend_api.flightschedule import FlightScheduleList

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

    def test_post_housekeeping_with_no_timestamp(self):
        """all housekeeping logs/beacons should have a timestamp with them
            ensure that this timestamp exists
        """
        housekeepingData = fakeHousekeepingAsDict(None)
        del housekeepingData['lastBeaconTime']
        with self.client:
            response = self.client.post(
                'api/housekeepinglog',
                data=json.dumps(housekeepingData),
                content_type='application/json'
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload', data['message'])
        self.assertIn('fail', data['status'])

    def test_post_housekeeping_with_invalid_timestamp(self):
        """Ensure that the timestamp is a valid datetime"""
        housekeepingData = fakeHousekeepingAsDict('notadatetimeobject')
        with self.client:
            response = self.client.post(
                'api/housekeepinglog',
                data=json.dumps(housekeepingData),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_all_housekeeping(self):
        """Get all housekeeping that is currently in the database"""
        timestamp = datetime.fromtimestamp(1570749472)
        housekeepingData1 = fakeHousekeepingAsDict(timestamp)
        housekeepingData2 = fakeHousekeepingAsDict(timestamp)

        housekeeping1 = Housekeeping(**housekeepingData1)
        db.session.add(housekeeping1)
        db.session.commit()

        housekeeping2 = Housekeeping(**housekeepingData2)
        db.session.add(housekeeping2)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/housekeepinglog')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 2)
            self.assertIn('Passive', data['data']['logs'][0]['satelliteMode'])
            self.assertIn('Passive', data['data']['logs'][1]['satelliteMode'])
            self.assertIn('success', data['status'])

    def test_get_all_housekeeping_order_by_date(self):
        """Ensure that housekeeping is returned by date"""
        timestamp1 = datetime.fromtimestamp(1570749472)
        timestamp2 = datetime.fromtimestamp(1570749502)
        housekeepingData1 = fakeHousekeepingAsDict(timestamp1)
        housekeepingData2 = fakeHousekeepingAsDict(timestamp2)

        housekeeping1 = Housekeeping(**housekeepingData1)
        db.session.add(housekeeping1)
        db.session.commit()

        housekeeping2 = Housekeeping(**housekeepingData2)
        db.session.add(housekeeping2)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/housekeepinglog')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 2)
            self.assertEqual(data['data']['logs'][0]['id'], 1)
            self.assertEqual(data['data']['logs'][1]['id'], 2)
            self.assertIn('success', data['status'])

    def test_get_all_housekeeping_limit_by(self):
        timestamp = datetime.fromtimestamp(1570749472)
        housekeepingData1 = fakeHousekeepingAsDict(timestamp)
        housekeepingData2 = fakeHousekeepingAsDict(timestamp)

        housekeeping1 = Housekeeping(**housekeepingData1)
        db.session.add(housekeeping1)
        db.session.commit()

        housekeeping2 = Housekeeping(**housekeepingData2)
        db.session.add(housekeeping2)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/housekeepinglog?limit=1')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 1)
            self.assertIn('Passive', data['data']['logs'][0]['satelliteMode'])
            self.assertIn('success', data['status'])

class TestFlightScheduleService(BaseTestCase):

    def test_post_with_no_commands(self):
        flightschedule = fake_flight_schedule_as_dict(False, [])
        self.assertEqual(len(FlightSchedules.query.all()), 0)

        with self.client:
            post_data = json.dumps(flightschedule)
            response = self.client.post(
                'api/flightschedules',
                data=post_data,
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)

        num_flightschedules = len(FlightSchedules.query.all())
        self.assertTrue(num_flightschedules > 0)

    def test_local_post_no_commands(self):
        flightschedule = fake_flight_schedule_as_dict(False, [])
        self.assertEqual(len(FlightSchedules.query.all()), 0)

        post_data = json.dumps(flightschedule)
        response = FlightScheduleList().post(local_data=post_data)

        self.assertEqual(response[1], 201)
        num_flightschedules = len(FlightSchedules.query.all())
        self.assertTrue(num_flightschedules > 0)

    def test_with_missing_commands(self):
        flightschedule = fake_flight_schedule_as_dict(False, [])
        flightschedule.pop('commands')

        with self.client:
            post_data = json.dumps(flightschedule)
            response = self.client.post(
                'api/flightschedules',
                data=post_data,
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('commands', response_data['errors'].keys())

    def test_multiple_queued_posts(self):
        flightschedule = fake_flight_schedule_as_dict(True, [])

        with self.client:
            post_data = json.dumps(flightschedule)
            kw_args = {'data':post_data, 'content_type':'application/json'}

            response_1 = self.client.post('api/flightschedules', **kw_args)
            response_data = json.loads(response_1.data.decode())
            self.assertEqual(response_1.status_code, 201)

            response_2 = self.client.post('api/flightschedules', **kw_args)
            response_data = json.loads(response_2.data.decode())
            self.assertEqual(response_2.status_code, 400)
            self.assertIn('A Queued flight schedule already exists!', response_data['message'])

    # TODO: Test with actuall command objects in the post data
