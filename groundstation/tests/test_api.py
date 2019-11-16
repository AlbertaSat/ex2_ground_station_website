import unittest
import json

import datetime
from flask import current_app
from groundstation.tests.base import BaseTestCase
from groundstation import db

from groundstation.backend_api.models import Housekeeping, FlightSchedules, \
    Passover, Telecommands, FlightScheduleCommands, Communications, PowerChannels
from groundstation.tests.utils import fakeHousekeepingAsDict, \
    fake_flight_schedule_as_dict, fake_passover_as_dict, \
    fake_patch_update_as_dict, fake_telecommand_as_dict, \
    fake_message_as_dict, fake_user_as_dict, fake_power_channel_as_dict
from groundstation.backend_api.housekeeping import HousekeepingLogList
from groundstation.backend_api.flightschedule import FlightScheduleList
from groundstation.backend_api.passover import PassoverList
from groundstation.backend_api.telecommand import Telecommand, TelecommandList
from groundstation.backend_api.utils import add_telecommand, \
    add_flight_schedule, add_command_to_flightschedule, add_user
from groundstation.backend_api.communications import Communication, CommunicationList
from unittest import mock

class TestHousekeepingService(BaseTestCase):
    """Test the housekeeping/satellite model service"""

    def test_get_housekeeping(self):
        """Test getting a housekeeping log"""
        timestamp = datetime.datetime.fromtimestamp(1570749472)
        housekeepingData = fakeHousekeepingAsDict(timestamp)

        housekeeping = Housekeeping(**housekeepingData)

        for i in range(1, 25):
            channel = fake_power_channel_as_dict(i)
            p = PowerChannels(**channel)
            housekeeping.channels.append(p)

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
            self.assertEqual(6000, data['data']['watchdog_1'])
            self.assertEqual(11, data['data']['watchdog_2'])
            self.assertEqual(0, data['data']['watchdog_3'])
            self.assertEqual(1.1, data['data']['panel_1_current'])
            self.assertEqual(1.0, data['data']['panel_2_current'])
            self.assertEqual(1.2, data['data']['panel_3_current'])
            self.assertEqual(1.0, data['data']['panel_4_current'])
            self.assertEqual(1.0, data['data']['panel_5_current'])
            self.assertEqual(1.0, data['data']['panel_6_current'])
            self.assertEqual(11.0, data['data']['temp_1'])
            self.assertEqual(11.0, data['data']['temp_2'])
            self.assertEqual(14.0, data['data']['temp_3'])
            self.assertEqual(12.0, data['data']['temp_4'])
            self.assertEqual(11.0, data['data']['temp_5'])
            self.assertEqual(10.0, data['data']['temp_6'])
            for i in range(1, 25):
                self.assertEqual(data['data']['channels'][i-1]['id'], i)
                # \/ Should probably be housekeeping.id or smth instead of just 1
                self.assertEqual(data['data']['channels'][i-1]['hk_id'], 1)
                self.assertEqual(data['data']['channels'][i-1]['channel_no'], i)
                self.assertEqual(data['data']['channels'][i-1]['enabled'], True)
                self.assertEqual(data['data']['channels'][i-1]['current'], 0.0)
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

    def test_post_housekeeping_with_channels(self):
        timestamp = str(datetime.datetime.fromtimestamp(1570749472))
        housekeepingData = fakeHousekeepingAsDict(timestamp)
        for i in range(1, 25):
            channel = fake_power_channel_as_dict(i)
            housekeepingData['channels'].append(channel)

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


#########################################################################
#Test telecommand model/get and post
class TestTelecommandService(BaseTestCase):

    def test_get_telecommand_by_name(self):
        telecommand = add_telecommand('ping', 0, False)
        with self.client:
            response = self.client.get(f'/api/telecommands/{telecommand.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(0, data['data']['num_arguments'])
            self.assertEqual(False, data['data']['is_dangerous'])

    def test_get_telecommand_with_invalid_command_name(self):
        with self.client:
            response = self.client.get('/api/telecommands/30')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data['message'], 'telecommand does not exist')

class TestTelecommandList(BaseTestCase):

    def test_get_all_telecommands(self):
        t1 = add_telecommand('ping', 0, False)
        t2 = add_telecommand('self-destruct', 10, is_dangerous=True)
        with self.client:
            response = self.client.get('/api/telecommands')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['telecommands']), 2)

    def test_local_post_telecommand(self):
        command = fake_telecommand_as_dict('ping', 0)
        service = TelecommandList()
        response = service.post(local_data=json.dumps(command))
        self.assertEqual(response[1], 201)
        self.assertEqual('success', response[0]['status'])

    def test_post_telecommand_happy_path(self):
        command = fake_telecommand_as_dict('ping', 0)
        with self.client:
            post_data = json.dumps(command)
            kw_args = {'data':post_data, 'content_type':'application/json'}

            response = self.client.post('/api/telecommands', **kw_args)
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)

    def test_post_telecommand_invalid_json(self):
        command = fake_telecommand_as_dict('ping', 0)
        command.pop('command_name')
        with self.client:
            post_data = json.dumps(command)
            kw_args = {'data':post_data, 'content_type':'application/json'}

            response = self.client.post('/api/telecommands', **kw_args)
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)

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
        flightschedule = fake_flight_schedule_as_dict(status=1, commands=[])

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
        flightschedule = add_flight_schedule(creation_date=timestamp, upload_date=timestamp, status=2)
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
        flightschedule = add_flight_schedule(creation_date=timestamp, upload_date=timestamp, status=2)
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

    def test_get_without_auth_token(self):
        current_app.config.update(BYPASS_AUTH=False)
        admin = add_user('Alice', 'password', is_admin=True)
        with self.client:
            response = self.client.get('/api/flightschedules', headers={})
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)

    def test_get_with_auth_token(self):
        current_app.config.update(BYPASS_AUTH=False)

        user = add_user('Alice', 'password', is_admin=False)
        auth_token = user.encode_auth_token_by_id().decode()
        with self.client:
            response = self.client.get('/api/flightschedules', headers={'Authorization': f'Bearer {auth_token}'})
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)



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
        # print('current_time', str(current_time))
        offset = datetime.timedelta(minutes=90)
        correct_next_passover = None
        for i in range(-10, 10, 1):
            d = current_time + i * offset
            if i == 0:
                continue
            if i == 1:
                correct_next_passover = d
                # print('correct_next_passover', correct_next_passover)

            p = Passover(timestamp=d)
            db.session.add(p)

        db.session.commit()

        with self.client:
            response = self.client.get('/api/passovers?next-only=true')
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response_data['data']['passovers']), 1)
            self.assertEqual(str(correct_next_passover).split('+')[0], response_data['data']['passovers'][0]['timestamp'])

class TestUserService(BaseTestCase):

    def test_post_new_user_without_admin_priviliges(self):
        current_app.config.update(BYPASS_AUTH=False)

        admin = add_user('admin', 'admin', is_admin=True)
        user = add_user('user', 'user', is_admin=False)
        auth_token = user.encode_auth_token_by_id().decode()
        with self.client:
            user_dict = fake_user_as_dict('new_user', 'new_user')
            post_data = json.dumps(user_dict)
            kw_args = {'data':post_data, 'content_type':'application/json'}
            response = self.client.post('/api/users', headers={'Authorization': f'Bearer {auth_token}'}, **kw_args)
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertIn('fail', response_data['status'])
            self.assertIn('You do not have permission to create users.', response_data['message'])

    def test_post_new_user_with_admin_priviliges(self):
        current_app.config.update(BYPASS_AUTH=False)

        admin = add_user('admin', 'admin', is_admin=True)
        user = add_user('user', 'user', is_admin=False)
        auth_token = admin.encode_auth_token_by_id().decode()
        with self.client:
            user_dict = fake_user_as_dict('new_user', 'new_user')
            post_data = json.dumps(user_dict)
            kw_args = {'data':post_data, 'content_type':'application/json'}
            response = self.client.post('/api/users', headers={'Authorization': f'Bearer {auth_token}'}, **kw_args)
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', response_data['status'])

    def test_post_duplicate_username(self):
        current_app.config.update(BYPASS_AUTH=False)

        admin = add_user('Alice', 'password', is_admin=True)
        user1 = add_user('Bob', 'password', is_admin=False)
        auth_token = admin.encode_auth_token_by_id().decode()
        with self.client:
            user_dict = fake_user_as_dict('Bob', 'secret-password')
            post_data = json.dumps(user_dict)
            kw_args = {'data':post_data, 'content_type':'application/json'}
            response = self.client.post('/api/users', headers={'Authorization': f'Bearer {auth_token}'}, **kw_args)
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('dev_message', response_data.keys())

    def test_missing_password_data(self):
        current_app.config.update(BYPASS_AUTH=False)

        admin = add_user('Alice', 'password', is_admin=True)
        auth_token = admin.encode_auth_token_by_id().decode()
        with self.client:
            user_dict = fake_user_as_dict('Bob', 'secret-password')
            user_dict.pop('password')
            post_data = json.dumps(user_dict)
            kw_args = {'data':post_data, 'content_type':'application/json'}
            response = self.client.post('/api/users', headers={'Authorization': f'Bearer {auth_token}'}, **kw_args)
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('The posted data is not valid!', response_data['message'])
####################################################################
#Test Communications functions
class TestCommunicationsService(BaseTestCase):

    def test_post_valid_communication(self):
        # service = CommunicationsList()
        test_message = fake_message_as_dict()
        # response = service.post()

        with self.client:
            response = self.client.post(
                '/api/communications',
                data=json.dumps(test_message),
                content_type='application/json'
            )
            data=json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            # print(test_message)
            msg = test_message['message']
            self.assertEqual(
                f'message {msg} was sent!',
                data['message']
            )
            self.assertEqual('success', data['status'])

    def test_get_all_communications(self):
        test_message_1 = fake_message_as_dict()
        test_message_2 = fake_message_as_dict(message='test 2')

        test_message_1 = Communications(**test_message_1)
        test_message_2 = Communications(**test_message_2)

        db.session.add(test_message_1)
        db.session.add(test_message_2)
        db.session.commit()

        with self.client:
            response=self.client.get('/api/communications')
            data=json.loads(response.data.decode())
            # print(data)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(len(data['data']['messages']), 2)
            self.assertIn('test', data['data']['messages'][0]['message'])
            self.assertIn('test 2', data['data']['messages'][1]['message'])

    def test_get_communications_with_query_params(self):
        test_message_1 = fake_message_as_dict()
        test_message_2 = fake_message_as_dict(message='test 2')

        test_message_1 = Communications(**test_message_1)
        test_message_2 = Communications(**test_message_2)

        db.session.add(test_message_1)
        db.session.add(test_message_2)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/communications?last_id=1&receiver=tester2')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(len(data['data']['messages']), 1)
            self.assertIn('test 2', data['data']['messages'][0]['message'])



#         with self.client:
#             response = self.client.post(
#                 '/api/housekeepinglog',
#                 data=json.dumps(housekeepingData),
#                 content_type='application/json'
#             )
#             data = json.loads(response.data.decode())
#             self.assertEqual(response.status_code, 201)
#             self.assertEqual(
#                 f'Housekeeping Log with timestamp {timestamp} was added!',
#                 data['message']
#             )
#             self.assertIn('success', data['status'])
