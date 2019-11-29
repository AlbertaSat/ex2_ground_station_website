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
from werkzeug.datastructures import MultiDict


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

    def test_get_housekeeping_with_dynamic_filters_1(self):
        timestamp = datetime.datetime.fromtimestamp(1570749472)
        housekeepingData = fakeHousekeepingAsDict(timestamp)
        housekeepingData['temp_1'] = 11
        housekeeping = Housekeeping(**housekeepingData)

        for i in range(1, 25):
            channel = fake_power_channel_as_dict(i)
            p = PowerChannels(**channel)
            housekeeping.channels.append(p)

        db.session.add(housekeeping)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/housekeepinglog?temp_1=gt-12')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 0)
            response = self.client.get('/api/housekeepinglog?temp_1=gt-10')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 1)

    def test_get_housekeeping_with_dynamic_filters_2(self):
        timestamp = datetime.datetime.fromtimestamp(1570749472)
        housekeepingData = fakeHousekeepingAsDict(timestamp)
        housekeepingData['temp_1'] = 11
        housekeepingData['temp_2'] = 12
        housekeepingData['temp_3'] = 13
        housekeeping = Housekeeping(**housekeepingData)

        for i in range(1, 25):
            channel = fake_power_channel_as_dict(i)
            p = PowerChannels(**channel)
            housekeeping.channels.append(p)

        db.session.add(housekeeping)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/housekeepinglog?temp_1=gt-10&temp_2=gt-11&temp_3=gt-12')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 1)
            response = self.client.get('/api/housekeepinglog?temp_1=gt-10&temp_2=gt-11&temp_3=gt-14')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 0)

    def test_get_housekeeping_with_dynamic_filters_3(self):
        timestamp = datetime.datetime.fromtimestamp(1570749472)
        housekeepingData = fakeHousekeepingAsDict(timestamp)
        housekeepingData['battery_voltage'] = 16
        housekeepingData['watchdog_1'] = 140
        housekeepingData['panel_5_current'] = 0.5
        housekeeping = Housekeeping(**housekeepingData)

        for i in range(1, 25):
            channel = fake_power_channel_as_dict(i)
            p = PowerChannels(**channel)
            housekeeping.channels.append(p)

        db.session.add(housekeeping)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/housekeepinglog?battery_voltage=eq-16&watchdog_1=lt-150&panel_5_current=gt-0.2')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 1)
            response = self.client.get('/api/housekeepinglog?battery_voltage=eq-15&watchdog_1=lt-150&panel_5_current=gt-0.2')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 0)

    def test_get_housekeeping_with_dynamic_filters_4(self):

        for i in range(15):
            timestamp = datetime.datetime.fromtimestamp(1570749472 + i)
            housekeepingData = fakeHousekeepingAsDict(timestamp)
            housekeepingData['battery_voltage'] = 16 + i
            housekeeping = Housekeeping(**housekeepingData)

            for i in range(1, 25):
                channel = fake_power_channel_as_dict(i)
                p = PowerChannels(**channel)
                housekeeping.channels.append(p)

            db.session.add(housekeeping)

        db.session.commit()

        with self.client:
            response = self.client.get('/api/housekeepinglog?battery_voltage=gt-20&battery_voltage=lt-24')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 3)

            response = self.client.get('/api/housekeepinglog?battery_voltage=gt-20&battery_voltage=lt-24&battery_voltage=eq-17')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 0)

            response = self.client.get('/api/housekeepinglog?battery_voltage=gt-20&limit=1&battery_voltage=lt-24')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 1)

    def test_get_housekeeping_with_dynamic_filters_5_invalid_attribute(self):
        timestamp = datetime.datetime.fromtimestamp(1570749472)
        housekeepingData = fakeHousekeepingAsDict(timestamp)
        housekeepingData['temp_1'] = 11
        housekeeping = Housekeeping(**housekeepingData)

        for i in range(1, 25):
            channel = fake_power_channel_as_dict(i)
            p = PowerChannels(**channel)
            housekeeping.channels.append(p)
        db.session.add(housekeeping)
        db.session.commit()
        with self.client:
            response = self.client.get('/api/housekeepinglog?tempp_1=gt-12')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)

    def test_get_housekeeping_with_valid_start_date(self):

        for i in range(10):
            timestamp = datetime.datetime.fromtimestamp(1570749472 + i * 100)
            db.session.add(Housekeeping(**fakeHousekeepingAsDict(timestamp)))
        db.session.commit()
        with self.client:
            start_ts = datetime.datetime.fromtimestamp(1570749472 + 5 + 700).isoformat()
            url = '/api/housekeepinglog'
            query_string = MultiDict([
                ('last_beacon_time', f'ge-{start_ts}')
            ])
            response = self.client.get(url, query_string=query_string)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 2)

    def test_get_housekeeping_with_valid_end_date(self):
        for i in range(10):
            timestamp = datetime.datetime.fromtimestamp(1570749472 + i * 100)
            db.session.add(Housekeeping(**fakeHousekeepingAsDict(timestamp)))
        db.session.commit()
        with self.client:
            end_ts = datetime.datetime.fromtimestamp(1570749472 + 5 + 700).isoformat()
            url = '/api/housekeepinglog'
            query_string = MultiDict([
                ('last_beacon_time', f'le-{end_ts}')
            ])
            response = self.client.get(url, query_string=query_string)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 8)

    def test_get_housekeeping_with_valid_start_and_end_date(self):
        for i in range(10):
            timestamp = datetime.datetime.fromtimestamp(1570749472 + i * 100)
            db.session.add(Housekeeping(**fakeHousekeepingAsDict(timestamp)))
        db.session.commit()
        with self.client:
            start_ts = datetime.datetime.fromtimestamp(1570749472 + 5 + 200).isoformat()
            end_ts = datetime.datetime.fromtimestamp(1570749472 + 5 + 600).isoformat()
            url = '/api/housekeepinglog'
            query_string = MultiDict([
                ('last_beacon_time', f'ge-{start_ts}'),
                ('last_beacon_time', f'le-{end_ts}')
            ])
            response = self.client.get(url, query_string=query_string)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 4)

    def test_get_housekeeping_with_valid_start_and_end_date_locally(self):
        for i in range(10):
            timestamp = datetime.datetime.fromtimestamp(1570749472 + i * 100)
            db.session.add(Housekeeping(**fakeHousekeepingAsDict(timestamp)))
        db.session.commit()
        start_ts = datetime.datetime.fromtimestamp(1570749472 + 5 + 200).isoformat()
        end_ts = datetime.datetime.fromtimestamp(1570749472 + 5 + 600).isoformat()
        local_args = MultiDict([
            ('last_beacon_time', f'ge-{start_ts}'),
            ('last_beacon_time', f'le-{end_ts}')
        ])
        endpoint = HousekeepingLogList()
        data, status_code = endpoint.get(local_args=local_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(len(data['data']['logs']), 4)

    def test_get_housekeeping_with_invalid_start_and_valid_end_date(self):
        for i in range(10):
            timestamp = datetime.datetime.fromtimestamp(1570749472 + i * 100)
            db.session.add(Housekeeping(**fakeHousekeepingAsDict(timestamp)))
        db.session.commit()
        with self.client:
            start_ts = "ubinoanciwnaw"
            end_ts = datetime.datetime.fromtimestamp(1570749472 + 5 + 600).isoformat()
            url = '/api/housekeepinglog'
            filter_string = f'last_beacon_time=ge-{start_ts}&last_beacon_time=le-{end_ts}'
            query_string = MultiDict([
                ('last_beacon_time', f'ge-{start_ts}'),
                ('last_beacon_time', f'le-{end_ts}')
            ])
            response = self.client.get(url, query_string=query_string)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)

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
        timestamp = datetime.datetime.fromtimestamp(1570749472)
        flightschedule = fake_flight_schedule_as_dict(execution_time=str(timestamp))
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
        timestamp = datetime.datetime.fromtimestamp(1570749472)
        flightschedule = fake_flight_schedule_as_dict(execution_time=str(timestamp))
        self.assertEqual(len(FlightSchedules.query.all()), 0)

        post_data = json.dumps(flightschedule)
        response = FlightScheduleList().post(local_data=post_data)

        self.assertEqual(response[1], 201)
        num_flightschedules = len(FlightSchedules.query.all())
        self.assertTrue(num_flightschedules > 0)

    def test_with_missing_commands(self):
        timestamp = datetime.datetime.fromtimestamp(1570749472)
        flightschedule = fake_flight_schedule_as_dict(execution_time=str(timestamp))
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
        timestamp = datetime.datetime.fromtimestamp(1570749472)
        flightschedule = fake_flight_schedule_as_dict(status=1, commands=[], execution_time=str(timestamp))

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
        timestamp = datetime.datetime.fromtimestamp(1570749472)
        for i in range(10):
            flightschedule = FlightSchedules(**fake_flight_schedule_as_dict(execution_time=timestamp))
            db.session.add(flightschedule)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/flightschedules')
            response_data = json.loads(response.data.decode())
            flightschedules = response_data['data']['flightschedules']
            self.assertEqual(len(flightschedules), 10)

    def test_get_all_flightschedules_limit_by(self):
        timestamp = datetime.datetime.fromtimestamp(1570749472)
        for i in range(10):
            flightschedule = FlightSchedules(**fake_flight_schedule_as_dict(execution_time=timestamp))
            db.session.add(flightschedule)
        db.session.commit()
        with self.client:
            response = self.client.get('/api/flightschedules?limit=3')
            response_data = json.loads(response.data.decode())
            flightschedules = response_data['data']['flightschedules']
            self.assertEqual(len(flightschedules), 3)

    def test_get_all_flightschedules_locally_limit_by(self):
        timestamp = datetime.datetime.fromtimestamp(1570749472)
        for i in range(10):
            flightschedule = FlightSchedules(**fake_flight_schedule_as_dict(execution_time=timestamp))
            db.session.add(flightschedule)
        db.session.commit()

        response = FlightScheduleList().get(local_args={'limit':3})
        self.assertEqual(response[1], 200)
        self.assertEqual(len(response[0]['data']['flightschedules']), 3)

    def test_get_flight_schedule_by_id(self):
        timestamp = datetime.datetime.fromtimestamp(1570749472)
        flightschedule = FlightSchedules(**fake_flight_schedule_as_dict(execution_time=timestamp))
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
        flightschedule = add_flight_schedule(
            creation_date=timestamp,
            upload_date=timestamp,
            status=2,
            execution_time=timestamp)
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
        flightschedule = add_flight_schedule(
            creation_date=timestamp,
            upload_date=timestamp,
            status=2,
            execution_time=timestamp)

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

            p = Passover(timestamp=d)
            db.session.add(p)

        db.session.commit()

        with self.client:
            response = self.client.get('/api/passovers?next=true&limit=1')
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('next_passovers' in response_data['data'].keys())
            self.assertEqual(len(response_data['data']['next_passovers']), 1)
            self.assertEqual(str(correct_next_passover).split('+')[0], response_data['data']['next_passovers'][0]['timestamp'])

    def test_get_next_5_passovers(self):

        current_time = datetime.datetime.now(datetime.timezone.utc)
        offset = datetime.timedelta(minutes=90)
        correct_next_passover = None
        for i in range(-10, 20, 1):
            d = current_time + i * offset
            if i == 0:
                continue
            if i == 1:
                correct_next_passover = d

            p = Passover(timestamp=d)
            db.session.add(p)

        db.session.commit()

        with self.client:
            response = self.client.get('/api/passovers?next=true&limit=5')
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('next_passovers' in response_data['data'].keys())
            self.assertEqual(len(response_data['data']['next_passovers']), 5)
            self.assertEqual(str(correct_next_passover).split('+')[0], response_data['data']['next_passovers'][0]['timestamp'])

    def test_get_most_recent_passover(self):

        current_time = datetime.datetime.now(datetime.timezone.utc)
        # print('current_time', str(current_time))
        offset = datetime.timedelta(minutes=90)
        correct_most_recent_passover = None
        for i in range(-10, 10, 1):
            d = current_time + i * offset
            if i == 0:
                continue
            if i == -1:
                correct_most_recent_passover = d

            p = Passover(timestamp=d)
            db.session.add(p)

        db.session.commit()

        with self.client:
            response = self.client.get('/api/passovers?most-recent=true')
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('most_recent_passover' in response_data['data'].keys())
            self.assertEqual(str(correct_most_recent_passover).split('+')[0], response_data['data']['most_recent_passover']['timestamp'])

    def test_get_next_passover_when_none_exist(self):

        current_time = datetime.datetime.now(datetime.timezone.utc)
        offset = datetime.timedelta(minutes=90)
        for i in range(-10, -5, 1):
            d = current_time + i * offset
            p = Passover(timestamp=d)
            db.session.add(p)

        db.session.commit()

        with self.client:
            response = self.client.get('/api/passovers?next=true')
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('next_passovers' in response_data['data'].keys())
            self.assertEqual(len(response_data['data']['next_passovers']), 0)

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

    def test_post_as_authenticated_user(self):
        current_app.config.update(BYPASS_AUTH=False)
        user = add_user('Bob', 'password', is_admin=False)
        auth_token = user.encode_auth_token_by_id().decode()
        test_message = fake_message_as_dict(sender='Bob')
        test_message['timestamp'] = str(test_message['timestamp'])
        with self.client:
            response = self.client.post(
                '/api/communications',
                headers={'Authorization': f'Bearer {auth_token}'},
                data=json.dumps(test_message),
                content_type='application/json'
            )
            data=json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)

    def test_post_as_unauthenticated_user(self):
        current_app.config.update(BYPASS_AUTH=False)
        user = add_user('Bob', 'password', is_admin=False)
        auth_token = user.encode_auth_token_by_id().decode()
        test_message = fake_message_as_dict(sender='Bob')
        test_message['timestamp'] = str(test_message['timestamp'])
        with self.client:
            response = self.client.post(
                '/api/communications',
                data=json.dumps(test_message),
                content_type='application/json'
            )
            data=json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)

    def test_post_with_invalid_token(self):
        current_app.config.update(BYPASS_AUTH=False)
        user = add_user('Bob', 'password', is_admin=False)
        auth_token = "uydbisjanxsifbinewkrnieuwd"
        test_message = fake_message_as_dict(sender='Bob')
        test_message['timestamp'] = str(test_message['timestamp'])
        with self.client:
            response = self.client.post(
                '/api/communications',
                headers={'Authorization': f'Bearer {auth_token}'},
                data=json.dumps(test_message),
                content_type='application/json'
            )
            data=json.loads(response.data.decode())
            self.assertEqual(response.status_code, 401)

    def test_local_post_with_auth(self):
        current_app.config.update(BYPASS_AUTH=False)
        test_message = fake_message_as_dict(sender='Bob')
        test_message['timestamp'] = str(test_message['timestamp'])
        endpoint = CommunicationList()
        response = endpoint.post(local_data=json.dumps(test_message))
        self.assertEqual(response[1], 201)
        self.assertIn('success', response[0]['status'])

    def test_post_valid_communication(self):
        # service = CommunicationsList()
        test_message = fake_message_as_dict()
        test_message['timestamp'] = str(test_message['timestamp'])
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

    def test_get_all_communications_newest_first(self):
        messages = []
        for i in range(10):
            test_message = Communications(**fake_message_as_dict(message=f'test message {i}'))
            messages.append(test_message)
            db.session.add(test_message)

        db.session.commit()

        messages.sort(key=lambda obj : -1 * obj.id)

        with self.client:
            response=self.client.get('/api/communications?newest-first=true')
            data=json.loads(response.data.decode())
            # print(data)
            for resp_message_idx in range(len(data['data']['messages'])):
                self.assertEqual(messages[resp_message_idx].id, data['data']['messages'][resp_message_idx]['message_id'])



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

    def test_get_communication_with_max_id_empty_db(self):
        """This test exposes a bug which was fixed on branch 'hotfix/communications-dynamic-filter'
        """
        with self.client:
            response = self.client.get('/api/communications?max=true')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(len(data['data']['messages']), 0)

    def test_get_communication_with_max_id_non_empty_db(self):
        test_message_1 = fake_message_as_dict()
        test_message_2 = fake_message_as_dict(message='test 2')

        test_message_1 = Communications(**test_message_1)
        test_message_2 = Communications(**test_message_2)

        db.session.add(test_message_1)
        db.session.add(test_message_2)
        db.session.commit()

        correct_max_id = test_message_2.id

        with self.client:
            response = self.client.get('/api/communications?max=true')
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['status'], 'success')
            self.assertEqual(len(data['data']['messages']), 1)
            self.assertEqual(correct_max_id, data['data']['messages'][0]['message_id'])





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
