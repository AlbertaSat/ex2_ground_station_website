import unittest
import json

import datetime
from groundstation.tests.base import BaseTestCase
from groundstation import db

from groundstation.backend_api.models import Housekeeping, FlightSchedules, Passover, Telecommands, FlightScheduleCommands
from groundstation.tests.utils import fakeHousekeepingAsDict, fake_flight_schedule_as_dict, fake_passover_as_dict, fake_patch_update_as_dict
from groundstation.backend_api.housekeeping import HousekeepingLogList
from groundstation.backend_api.flightschedule import FlightScheduleList
from groundstation.backend_api.passover import PassoverList
from groundstation.backend_api.telecommand import TelecommandService
from groundstation.backend_api.utils import add_telecommand, add_flight_schedule, add_command_to_flightschedule

from unittest import mock

class TestHousekeepingService(BaseTestCase):
    """Test the housekeeping/satellite model service"""

    def test_get_housekeeping(self):
        """Test getting a housekeeping log"""
        timestamp = datetime.datetime.fromtimestamp(1570749472)
        housekeepingData = fakeHousekeepingAsDict(timestamp)

        housekeeping = Housekeeping(**housekeepingData)
        db.session.add(housekeeping)
        db.session.commit()

        with self.client:
            response = self.client.get(f'/api/housekeepinglog/{housekeeping.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Passive', data['data']['satellite_mode'])
            self.assertEqual(1.7, data['data']['battery_voltage'])
            self.assertEqual(14, data['data']['no_MCU_resets'])
            self.assertIn(str(timestamp), data['data']['last_beacon_time'])
            self.assertIn('success', data['status'])


    def test_get_housekeeping_incorrect_id(self):
        with self.client:
            response = self.client.get('/api/housekeepinglog/123')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Housekeeping Log does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_post_housekeeping(self):
        timestamp = str(datetime.datetime.fromtimestamp(1570749472))
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
        timestamp = str(datetime.datetime.fromtimestamp(1570749472))
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
        del housekeepingData['last_beacon_time']
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
        timestamp = datetime.datetime.fromtimestamp(1570749472)
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
            self.assertIn('Passive', data['data']['logs'][0]['satellite_mode'])
            self.assertIn('Passive', data['data']['logs'][1]['satellite_mode'])
            self.assertIn('success', data['status'])

    def test_get_all_housekeeping_order_by_date(self):
        """Ensure that housekeeping is returned by date"""
        timestamp1 = datetime.datetime.fromtimestamp(1570749472)
        timestamp2 = datetime.datetime.fromtimestamp(1570749502)
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
        timestamp = datetime.datetime.fromtimestamp(1570749472)
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
            self.assertIn('Passive', data['data']['logs'][0]['satellite_mode'])
            self.assertIn('success', data['status'])


#########################################################################
#Test telecommand model/get and post

class TestTelecommandService(BaseTestCase):

    def test_post_telecommand(self):

        command = {
        'command_name' : "TEST_COMMAND",
        'num_args' : 0,
        'is_dangerous' : False
        }

        service = TelecommandService()

        response = service.post(local_data=json.dumps(command))
        print(response)
        # data = json.loads(response.data.decode())
        self.assertEqual(response[1], 201)
        self.assertIn('success', response[0]['status'])
        self.assertIn(f'Command {command["command_name"]} was added!', response[0]['message'])

#########################################################################
#Test flight schedule functions
class TestFlightScheduleService(BaseTestCase):

    def test_post_with_no_commands(self):
        flightschedule = fake_flight_schedule_as_dict()
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
        flightschedule = fake_flight_schedule_as_dict()
        self.assertEqual(len(FlightSchedules.query.all()), 0)

        post_data = json.dumps(flightschedule)
        response = FlightScheduleList().post(local_data=post_data)

        self.assertEqual(response[1], 201)
        num_flightschedules = len(FlightSchedules.query.all())
        self.assertTrue(num_flightschedules > 0)

    def test_with_missing_commands(self):
        flightschedule = fake_flight_schedule_as_dict()
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
        flightschedule = fake_flight_schedule_as_dict(is_queued=True, commands=[])

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



    def test_get_all_flightschedules(self):
        for i in range(10):
            flightschedule = FlightSchedules(**fake_flight_schedule_as_dict())
            db.session.add(flightschedule)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/flightschedules')
            response_data = json.loads(response.data.decode())
            flightschedules = response_data['data']['flightschedules']
            self.assertEqual(len(flightschedules), 10)

    def test_get_all_flightschedules_limit_by(self):
        for i in range(10):
            flightschedule = FlightSchedules(**fake_flight_schedule_as_dict())
            db.session.add(flightschedule)
        db.session.commit()
        with self.client:
            response = self.client.get('/api/flightschedules?limit=3')
            response_data = json.loads(response.data.decode())
            flightschedules = response_data['data']['flightschedules']
            self.assertEqual(len(flightschedules), 3)

    def test_get_all_flightschedules_locally_limit_by(self):
        for i in range(10):
            flightschedule = FlightSchedules(**fake_flight_schedule_as_dict())
            db.session.add(flightschedule)
        db.session.commit()

        response = FlightScheduleList().get(local_args={'limit':3})
        self.assertEqual(response[1], 200)
        self.assertEqual(len(response[0]['data']['flightschedules']), 3)

    def test_get_flight_schedule_by_id(self):
        flightschedule = FlightSchedules(**fake_flight_schedule_as_dict())
        db.session.add(flightschedule)
        db.session.commit()
        id = flightschedule.id
        with self.client:
            response = self.client.get(f'/api/flightschedules/{id}')
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_data['data']['flightschedule_id'], id)

    def test_patch_flight_schedule(self):
        timestamp = datetime.datetime.fromtimestamp(1570749472)
        commands = {
            'ping': (0,False),
            'get-hk':(0,False),
        }

        for name, (num_args, is_danger) in commands.items():
            c = add_telecommand(command_name=name, num_arguments=num_args, is_dangerous=is_danger)

        command1 = Telecommands.query.filter_by(command_name='ping').first()
        command2 = Telecommands.query.filter_by(command_name='get-hk').first()
        flightschedule = add_flight_schedule(creation_date=timestamp, upload_date=timestamp)
        flightschedule_commands1 = add_command_to_flightschedule(
                                timestamp=timestamp,
                                flightschedule_id=flightschedule.id,
                                command_id=command1.id
                            )
        flightschedule_commands2 = add_command_to_flightschedule(
                                timestamp=timestamp,
                                flightschedule_id=flightschedule.id,
                                command_id=command2.id
                            )
        post_data = json.dumps(fake_patch_update_as_dict(timestamp))
        with self.client:
            response = self.client.patch(
                f'api/flightschedules/{flightschedule.id}',
                data=post_data,
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response_data['data']['commands']), 3)
            self.assertEqual(response_data['data']['commands'][0]['command']['command_id'], 2)
            self.assertEqual(response_data['data']['commands'][2]['command']['command_id'], 1)

    def test_delete_flightschedule(self):
        timestamp = datetime.datetime.fromtimestamp(1570749472)
        commands = {
            'ping': (0,False),
            'get-hk':(0,False),
        }
        for name, (num_args, is_danger) in commands.items():
            c = add_telecommand(command_name=name, num_arguments=num_args, is_dangerous=is_danger)

        command1 = Telecommands.query.filter_by(command_name='ping').first()
        flightschedule = add_flight_schedule(creation_date=timestamp, upload_date=timestamp)
        flightschedule_commands = add_command_to_flightschedule(
                                timestamp=timestamp,
                                flightschedule_id=flightschedule.id,
                                command_id=command1.id
                            )
        with self.client:
            response = self.client.delete(f'api/flightschedules/{flightschedule.id}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(FlightSchedules.query.filter_by(id=flightschedule.id).first(), None)
            self.assertEqual(
                FlightScheduleCommands.query.filter_by(id=flightschedule_commands.id).first(), 
                None
            )






class TestPassoverService(BaseTestCase):

    def test_get_all_passovers_with_empty_db(self):
        datetimes = [datetime.datetime.utcnow() for i in range(5)]

        with self.client:
            post_data = json.dumps(fake_passover_as_dict(datetimes))
            kw_args = {'data':post_data, 'content_type':'application/json'}

            response = self.client.post('/api/passovers', **kw_args)
            response_data = json.loads(response.data.decode())
            self.assertEqual(len(response_data['data']['passovers'], 5))
            self.assertEqual(response.status_code, 201)

    def test_get_all_passovers_with_empty_db(self):
        with self.client:
            response = self.client.get('/api/passovers')
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response_data['data']['passovers']), 0)

    def test_invalid_post_with_no_passover_objects(self):
        with self.client:
            post_data = json.dumps(fake_passover_as_dict([]))
            kw_args = {'data':post_data, 'content_type':'application/json'}

            response = self.client.post('/api/passovers', **kw_args)
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)

    # this test has some solid jank but testing date time is super annoying so its fine for now
    def test_get_next_passover(self):

        current_time = datetime.datetime.now(datetime.timezone.utc)
        print('current_time', str(current_time))
        offset = datetime.timedelta(minutes=90)
        correct_next_passover = None
        for i in range(-10, 10, 1):
            d = current_time + i * offset
            if i == 0:
                continue
            if i == 1:
                correct_next_passover = d
                print('correct_next_passover', correct_next_passover)

            p = Passover(timestamp=d)
            db.session.add(p)

        db.session.commit()

        with self.client:
            response = self.client.get('/api/passovers?next-only=true')
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response_data['data']['passovers']), 1)
            self.assertEqual(str(correct_next_passover).split('+')[0], response_data['data']['passovers'][0]['timestamp'])
