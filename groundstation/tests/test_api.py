import json

import datetime
from flask import current_app
from groundstation.tests.base import BaseTestCase
from groundstation import db

from groundstation.backend_api.models import AdcsHK, AthenaHK, CharonHK, \
    DfgmHK, EpsHK, Housekeeping, FlightSchedules, HyperionHK, IrisHK, \
    NorthernSpiritHK, Passover, SbandHK, Telecommands, FlightScheduleCommands, \
    Communications, UhfHK, AutomatedCommands
from groundstation.tests.utils import fake_adcs_hk_as_dict, \
    fake_athena_hk_as_dict, fake_charon_hk_as_dict, fake_dfgm_hk_as_dict, \
    fake_eps_hk_as_dict, fake_housekeeping_as_dict, \
    fake_flight_schedule_as_dict, fake_hyperion_hk_as_dict, \
    fake_iris_hk_as_dict, fake_northern_spirit_hk_as_dict, fake_passover_as_dict, \
    fake_patch_update_as_dict, fake_sband_hk_as_dict, fake_telecommand_as_dict, \
    fake_message_as_dict, fake_uhf_hk_as_dict, fake_user_as_dict, \
    fake_automatedcommand_as_dict
from groundstation.backend_api.housekeeping import HousekeepingLogList
from groundstation.backend_api.flightschedule import FlightScheduleList
from groundstation.backend_api.automatedcommand import AutomatedCommandList
from groundstation.backend_api.passover import PassoverList
from groundstation.backend_api.telecommand import Telecommand, TelecommandList
from groundstation.backend_api.utils import add_telecommand, \
    add_flight_schedule, add_command_to_flightschedule, add_user
from groundstation.backend_api.communications import Communication, CommunicationList
from werkzeug.datastructures import MultiDict


class TestHousekeepingService(BaseTestCase):
    """Test the housekeeping/satellite model service"""

    def test_get_housekeeping(self):
        """Test getting a housekeeping log"""
        timestamp = datetime.datetime.fromtimestamp(1659816386)
        housekeepingData = fake_housekeeping_as_dict(timestamp, 1)

        housekeeping = Housekeeping(
            **housekeepingData,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        db.session.add(housekeeping)
        db.session.commit()

        with self.client:
            response = self.client.get(f'/api/housekeepinglog/{housekeeping.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn(data['status'], 'success')
            self.assertIn(data['data']['timestamp'], str(timestamp))
            self.assertEqual(data['data']['data_position'], 1)
            self.assertEqual(data['data']['adcs']['Att_Estimate_Mode'], 42)
            self.assertEqual(data['data']['adcs']['Longitude'], 13.37)
            self.assertEqual(data['data']['athena']['temparray1'], 42)
            self.assertEqual(data['data']['eps']['cmd'], 42)
            self.assertEqual(data['data']['eps']['timestamp'], 13.37)
            self.assertEqual(data['data']['uhf']['scw1'], 42)
            self.assertEqual(data['data']['uhf']['temperature'], 13.37)
            self.assertEqual(data['data']['sband']['Output_Power'], 13.37)
            self.assertEqual(data['data']['hyperion']['Port_Pd1'], 42)
            self.assertEqual(data['data']['charon']['charon_temp7'], 42)
            self.assertEqual(data['data']['dfgm']['Input_Current'], 42)
            self.assertEqual(data['data']['northern_spirit']['ns_temp3'], 42)
            self.assertEqual(data['data']['iris']['Error_number'], 42)
            self.assertEqual(data['data']['iris']['NIR_Temperature'], 13.37)

    def test_get_housekeeping_with_dynamic_filters_1(self):
        timestamp = datetime.datetime.fromtimestamp(1659816386)
        housekeepingData = fake_housekeeping_as_dict(timestamp, 11)
        housekeeping = Housekeeping(
            **housekeepingData,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        db.session.add(housekeeping)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/housekeepinglog?data_position=gt-12')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 0)
            response = self.client.get('/api/housekeepinglog?data_position=gt-10')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 1)

    def test_get_housekeeping_with_dynamic_filters_2(self):
        timestamp = datetime.datetime.fromtimestamp(1659816386)
        housekeepingDataOne = fake_housekeeping_as_dict(timestamp, 10)
        housekeepingDataTwo = fake_housekeeping_as_dict(timestamp, 20)
        housekeepingDataThree = fake_housekeeping_as_dict(timestamp, 30)

        housekeepingOne = Housekeeping(
            **housekeepingDataOne,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        housekeepingTwo = Housekeeping(
            **housekeepingDataTwo,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        housekeepingThree = Housekeeping(
            **housekeepingDataThree,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        db.session.add(housekeepingOne)
        db.session.add(housekeepingTwo)
        db.session.add(housekeepingThree)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/housekeepinglog?data_position=gt-9')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 3)
            response = self.client.get('/api/housekeepinglog?data_position=gt-15')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 2)
            response = self.client.get('/api/housekeepinglog?data_position=gt-25')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 1)
            response = self.client.get('/api/housekeepinglog?data_position=gt-30')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 0)

    def test_get_housekeeping_with_dynamic_filters_3_invalid_attribute(self):
        timestamp = datetime.datetime.fromtimestamp(1659816386)
        housekeepingData = fake_housekeeping_as_dict(timestamp, 1)
        housekeeping = Housekeeping(
            **housekeepingData,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        db.session.add(housekeeping)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/housekeepinglog?hello=gt-12')
            self.assertEqual(response.status_code, 400)

    def test_get_housekeeping_with_valid_start_date(self):
        for i in range(10):
            timestamp = datetime.datetime.fromtimestamp(1659816386 + i * 100)
            db.session.add(Housekeeping(
                **fake_housekeeping_as_dict(timestamp, i),
                adcs=AdcsHK(**fake_adcs_hk_as_dict()),
                athena=AthenaHK(**fake_athena_hk_as_dict()),
                eps=EpsHK(**fake_eps_hk_as_dict()),
                uhf=UhfHK(**fake_uhf_hk_as_dict()),
                sband=SbandHK(**fake_sband_hk_as_dict()),
                hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
                charon=CharonHK(**fake_charon_hk_as_dict()),
                dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
                northern_spirit=NorthernSpiritHK(
                    **fake_northern_spirit_hk_as_dict()),
                iris=IrisHK(**fake_iris_hk_as_dict())
            ))

        db.session.commit()

        with self.client:
            start_ts = datetime.datetime.fromtimestamp(1659816386 + 5 + 700).isoformat()
            url = '/api/housekeepinglog'
            query_string = MultiDict([
                ('timestamp', f'ge-{start_ts}')
            ])
            response = self.client.get(url, query_string=query_string)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 2)

    def test_get_housekeeping_with_valid_end_date(self):
        for i in range(10):
            timestamp = datetime.datetime.fromtimestamp(1659816386 + i * 100)
            db.session.add(Housekeeping(
                **fake_housekeeping_as_dict(timestamp, i),
                adcs=AdcsHK(**fake_adcs_hk_as_dict()),
                athena=AthenaHK(**fake_athena_hk_as_dict()),
                eps=EpsHK(**fake_eps_hk_as_dict()),
                uhf=UhfHK(**fake_uhf_hk_as_dict()),
                sband=SbandHK(**fake_sband_hk_as_dict()),
                hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
                charon=CharonHK(**fake_charon_hk_as_dict()),
                dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
                northern_spirit=NorthernSpiritHK(
                    **fake_northern_spirit_hk_as_dict()),
                iris=IrisHK(**fake_iris_hk_as_dict())
            ))

        db.session.commit()

        with self.client:
            end_ts = datetime.datetime.fromtimestamp(1659816386 + 5 + 700).isoformat()
            url = '/api/housekeepinglog'
            query_string = MultiDict([
                ('timestamp', f'le-{end_ts}')
            ])
            response = self.client.get(url, query_string=query_string)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 8)

    def test_get_housekeeping_with_valid_start_and_end_date(self):
        for i in range(10):
            timestamp = datetime.datetime.fromtimestamp(1659816386 + i * 100)
            db.session.add(Housekeeping(
                **fake_housekeeping_as_dict(timestamp, i),
                adcs=AdcsHK(**fake_adcs_hk_as_dict()),
                athena=AthenaHK(**fake_athena_hk_as_dict()),
                eps=EpsHK(**fake_eps_hk_as_dict()),
                uhf=UhfHK(**fake_uhf_hk_as_dict()),
                sband=SbandHK(**fake_sband_hk_as_dict()),
                hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
                charon=CharonHK(**fake_charon_hk_as_dict()),
                dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
                northern_spirit=NorthernSpiritHK(
                    **fake_northern_spirit_hk_as_dict()),
                iris=IrisHK(**fake_iris_hk_as_dict())
            ))

        db.session.commit()

        with self.client:
            start_ts = datetime.datetime.fromtimestamp(1659816386 + 5 + 200).isoformat()
            end_ts = datetime.datetime.fromtimestamp(1659816386 + 5 + 600).isoformat()
            url = '/api/housekeepinglog'
            query_string = MultiDict([
                ('timestamp', f'ge-{start_ts}'),
                ('timestamp', f'le-{end_ts}')
            ])
            response = self.client.get(url, query_string=query_string)
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 4)

    def test_get_housekeeping_with_valid_start_and_end_date_locally(self):
        for i in range(10):
            timestamp = datetime.datetime.fromtimestamp(1659816386 + i * 100)
            db.session.add(Housekeeping(
                **fake_housekeeping_as_dict(timestamp, i),
                adcs=AdcsHK(**fake_adcs_hk_as_dict()),
                athena=AthenaHK(**fake_athena_hk_as_dict()),
                eps=EpsHK(**fake_eps_hk_as_dict()),
                uhf=UhfHK(**fake_uhf_hk_as_dict()),
                sband=SbandHK(**fake_sband_hk_as_dict()),
                hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
                charon=CharonHK(**fake_charon_hk_as_dict()),
                dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
                northern_spirit=NorthernSpiritHK(
                    **fake_northern_spirit_hk_as_dict()),
                iris=IrisHK(**fake_iris_hk_as_dict())
            ))

        db.session.commit()

        start_ts = datetime.datetime.fromtimestamp(1659816386 + 5 + 200).isoformat()
        end_ts = datetime.datetime.fromtimestamp(1659816386 + 5 + 600).isoformat()
        local_args = MultiDict([
            ('timestamp', f'ge-{start_ts}'),
            ('timestamp', f'le-{end_ts}')
        ])
        endpoint = HousekeepingLogList()
        data, status_code = endpoint.get(local_args=local_args)
        self.assertEqual(status_code, 200)
        self.assertEqual(len(data['data']['logs']), 4)

    def test_get_housekeeping_with_invalid_start_and_valid_end_date(self):
        for i in range(10):
            timestamp = datetime.datetime.fromtimestamp(1659816386 + i * 100)
            db.session.add(Housekeeping(
                **fake_housekeeping_as_dict(timestamp, i),
                adcs=AdcsHK(**fake_adcs_hk_as_dict()),
                athena=AthenaHK(**fake_athena_hk_as_dict()),
                eps=EpsHK(**fake_eps_hk_as_dict()),
                uhf=UhfHK(**fake_uhf_hk_as_dict()),
                sband=SbandHK(**fake_sband_hk_as_dict()),
                hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
                charon=CharonHK(**fake_charon_hk_as_dict()),
                dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
                northern_spirit=NorthernSpiritHK(
                    **fake_northern_spirit_hk_as_dict()),
                iris=IrisHK(**fake_iris_hk_as_dict())
            ))

        db.session.commit()

        with self.client:
            start_ts = "invalid_date!"
            end_ts = datetime.datetime.fromtimestamp(1659816386 + 5 + 600).isoformat()
            url = '/api/housekeepinglog'
            query_string = MultiDict([
                ('timestamp', f'ge-{start_ts}'),
                ('timestamp', f'le-{end_ts}')
            ])
            response = self.client.get(url, query_string=query_string)
            self.assertEqual(response.status_code, 400)

    def test_get_housekeeping_incorrect_id(self):
        with self.client:
            response = self.client.get('/api/housekeepinglog/123')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Housekeeping Log does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_post_housekeeping(self):
        timestamp = str(datetime.datetime.fromtimestamp(1659816386))
        housekeepingData = fake_housekeeping_as_dict(timestamp, 1)
        housekeepingData['adcs'] = fake_adcs_hk_as_dict()
        housekeepingData['athena'] = fake_athena_hk_as_dict()
        housekeepingData['eps'] = fake_eps_hk_as_dict()
        housekeepingData['uhf'] = fake_uhf_hk_as_dict()
        housekeepingData['sband'] = fake_sband_hk_as_dict()
        housekeepingData['hyperion'] = fake_hyperion_hk_as_dict()
        housekeepingData['charon'] = fake_charon_hk_as_dict()
        housekeepingData['dfgm'] = fake_dfgm_hk_as_dict()
        housekeepingData['northern_spirit'] = fake_northern_spirit_hk_as_dict()
        housekeepingData['iris'] = fake_iris_hk_as_dict()

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
        """
        Since local data is wrapped differently than data over http,
        we must send and receive it differently (locally it is a tuple of dicts)
        """
        timestamp = str(datetime.datetime.fromtimestamp(1659816386))
        housekeepingData = fake_housekeeping_as_dict(timestamp, 1)
        housekeepingData['adcs'] = fake_adcs_hk_as_dict()
        housekeepingData['athena'] = fake_athena_hk_as_dict()
        housekeepingData['eps'] = fake_eps_hk_as_dict()
        housekeepingData['uhf'] = fake_uhf_hk_as_dict()
        housekeepingData['sband'] = fake_sband_hk_as_dict()
        housekeepingData['hyperion'] = fake_hyperion_hk_as_dict()
        housekeepingData['charon'] = fake_charon_hk_as_dict()
        housekeepingData['dfgm'] = fake_dfgm_hk_as_dict()
        housekeepingData['northern_spirit'] = fake_northern_spirit_hk_as_dict()
        housekeepingData['iris'] = fake_iris_hk_as_dict()

        housekeepingLogList = HousekeepingLogList()
        response = housekeepingLogList.post(local_data=json.dumps(housekeepingData))
        self.assertEqual(response[1], 201)
        self.assertEqual(
            f'Housekeeping Log with timestamp {timestamp} was added!',
            response[0]['message']
        )
        self.assertIn('success', response[0]['status'])

    def test_post_housekeeping_with_no_timestamp(self):
        """
        All housekeeping logs should have a timestamp with them
        ensure that this timestamp exists
        """
        housekeepingData = fake_housekeeping_as_dict(None, 1)
        housekeepingData['adcs'] = fake_adcs_hk_as_dict()
        housekeepingData['athena'] = fake_athena_hk_as_dict()
        housekeepingData['eps'] = fake_eps_hk_as_dict()
        housekeepingData['uhf'] = fake_uhf_hk_as_dict()
        housekeepingData['sband'] = fake_sband_hk_as_dict()
        housekeepingData['hyperion'] = fake_hyperion_hk_as_dict()
        housekeepingData['charon'] = fake_charon_hk_as_dict()
        housekeepingData['dfgm'] = fake_dfgm_hk_as_dict()
        housekeepingData['northern_spirit'] = fake_northern_spirit_hk_as_dict()
        housekeepingData['iris'] = fake_iris_hk_as_dict()

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
        housekeepingData = fake_housekeeping_as_dict('notadatetimeobject', 1)
        housekeepingData['adcs'] = fake_adcs_hk_as_dict()
        housekeepingData['athena'] = fake_athena_hk_as_dict()
        housekeepingData['eps'] = fake_eps_hk_as_dict()
        housekeepingData['uhf'] = fake_uhf_hk_as_dict()
        housekeepingData['sband'] = fake_sband_hk_as_dict()
        housekeepingData['hyperion'] = fake_hyperion_hk_as_dict()
        housekeepingData['charon'] = fake_charon_hk_as_dict()
        housekeepingData['dfgm'] = fake_dfgm_hk_as_dict()
        housekeepingData['northern_spirit'] = fake_northern_spirit_hk_as_dict()
        housekeepingData['iris'] = fake_iris_hk_as_dict()

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

    def test_post_housekeeping_with_no_data_position(self):
        """
        All housekeeping logs should have a data position with them which
        corresponds to the log's file number on the OBC. Ensure that
        data_position exists
        """
        housekeepingData = fake_housekeeping_as_dict(None, None)
        housekeepingData['adcs'] = fake_adcs_hk_as_dict()
        housekeepingData['athena'] = fake_athena_hk_as_dict()
        housekeepingData['eps'] = fake_eps_hk_as_dict()
        housekeepingData['uhf'] = fake_uhf_hk_as_dict()
        housekeepingData['sband'] = fake_sband_hk_as_dict()
        housekeepingData['hyperion'] = fake_hyperion_hk_as_dict()
        housekeepingData['charon'] = fake_charon_hk_as_dict()
        housekeepingData['dfgm'] = fake_dfgm_hk_as_dict()
        housekeepingData['northern_spirit'] = fake_northern_spirit_hk_as_dict()
        housekeepingData['iris'] = fake_iris_hk_as_dict()

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

    def test_post_housekeeping_with_no_subsystems(self):
        """
        All housekeeping logs should have each subsystem as a nested dict.
        Ensure that all subsystems are present in each log.
        """
        housekeepingData = fake_housekeeping_as_dict(1659816386, 1)
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

    def test_post_housekeeping_with_missing_one_subsystem(self):
        """
        All housekeeping logs should have each subsystem as a nested dict.
        Ensure that not a single subsystem is missing.
        """
        housekeepingData = fake_housekeeping_as_dict(None, None)
        housekeepingData['adcs'] = {}
        housekeepingData['athena'] = fake_athena_hk_as_dict()
        housekeepingData['eps'] = fake_eps_hk_as_dict()
        housekeepingData['uhf'] = fake_uhf_hk_as_dict()
        housekeepingData['sband'] = fake_sband_hk_as_dict()
        housekeepingData['hyperion'] = fake_hyperion_hk_as_dict()
        housekeepingData['charon'] = fake_charon_hk_as_dict()
        housekeepingData['dfgm'] = fake_dfgm_hk_as_dict()
        housekeepingData['northern_spirit'] = fake_northern_spirit_hk_as_dict()
        housekeepingData['iris'] = fake_iris_hk_as_dict()

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
        timestamp = datetime.datetime.fromtimestamp(1659816386)
        housekeepingDataOne = fake_housekeeping_as_dict(timestamp, 10)
        housekeepingDataTwo = fake_housekeeping_as_dict(timestamp, 20)
        housekeepingDataThree = fake_housekeeping_as_dict(timestamp, 30)

        housekeepingOne = Housekeeping(
            **housekeepingDataOne,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        housekeepingTwo = Housekeeping(
            **housekeepingDataTwo,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        housekeepingThree = Housekeeping(
            **housekeepingDataThree,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        db.session.add(housekeepingOne)
        db.session.add(housekeepingTwo)
        db.session.add(housekeepingThree)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/housekeepinglog')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 3)
            self.assertIn(str(timestamp), data['data']['logs'][0]['timestamp'])
            self.assertIn(str(timestamp), data['data']['logs'][1]['timestamp'])
            self.assertIn(str(timestamp), data['data']['logs'][2]['timestamp'])
            self.assertIn('success', data['status'])

    def test_get_all_housekeeping_order_by_date(self):
        """Ensure that housekeeping is returned by date"""
        timestamp1 = datetime.datetime.fromtimestamp(1659816386)
        timestamp2 = datetime.datetime.fromtimestamp(1659839583)
        housekeepingDataOne = fake_housekeeping_as_dict(timestamp1, 1)
        housekeepingDataTwo = fake_housekeeping_as_dict(timestamp2, 2)

        housekeepingOne = Housekeeping(
            **housekeepingDataOne,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        housekeepingTwo = Housekeeping(
            **housekeepingDataTwo,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        db.session.add(housekeepingOne)
        db.session.add(housekeepingTwo)
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
        timestamp = datetime.datetime.fromtimestamp(1659816386)
        housekeepingDataOne = fake_housekeeping_as_dict(timestamp, 1)
        housekeepingDataTwo = fake_housekeeping_as_dict(timestamp, 2)

        housekeepingOne = Housekeeping(
            **housekeepingDataOne,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        housekeepingTwo = Housekeeping(
            **housekeepingDataTwo,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        db.session.add(housekeepingOne)
        db.session.add(housekeepingTwo)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/housekeepinglog?limit=1')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 1)
            self.assertIn(str(timestamp), data['data']['logs'][0]['timestamp'])
            self.assertIn('success', data['status'])

    def test_get_housekeeping_by_data_position(self):
        timestamp = datetime.datetime.fromtimestamp(1659816386)
        housekeepingDataOne = fake_housekeeping_as_dict(timestamp, 10)
        housekeepingDataTwo = fake_housekeeping_as_dict(timestamp, 20)
        housekeepingDataThree = fake_housekeeping_as_dict(timestamp, 30)

        housekeepingOne = Housekeeping(
            **housekeepingDataOne,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        housekeepingTwo = Housekeeping(
            **housekeepingDataTwo,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        housekeepingThree = Housekeeping(
            **housekeepingDataThree,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        db.session.add(housekeepingOne)
        db.session.add(housekeepingTwo)
        db.session.add(housekeepingThree)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/housekeepinglog?data_position=eq-10')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 1)
            self.assertIn(str(timestamp), data['data']['logs'][0]['timestamp'])
            self.assertIn('success', data['status'])

    def test_get_housekeeping_by_invalid_data_position(self):
        timestamp = datetime.datetime.fromtimestamp(1659816386)
        housekeepingData = fake_housekeeping_as_dict(timestamp, 1)
        housekeeping = Housekeeping(
            **housekeepingData,
            adcs=AdcsHK(**fake_adcs_hk_as_dict()),
            athena=AthenaHK(**fake_athena_hk_as_dict()),
            eps=EpsHK(**fake_eps_hk_as_dict()),
            uhf=UhfHK(**fake_uhf_hk_as_dict()),
            sband=SbandHK(**fake_sband_hk_as_dict()),
            hyperion=HyperionHK(**fake_hyperion_hk_as_dict()),
            charon=CharonHK(**fake_charon_hk_as_dict()),
            dfgm=DfgmHK(**fake_dfgm_hk_as_dict()),
            northern_spirit=NorthernSpiritHK(
                **fake_northern_spirit_hk_as_dict()),
            iris=IrisHK(**fake_iris_hk_as_dict())
        )

        db.session.add(housekeeping)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/housekeepinglog?data_position=eq-2')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['logs']), 0)

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
        timestamp = datetime.datetime.fromtimestamp(1659816386)
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
        timestamp = datetime.datetime.fromtimestamp(1659816386)
        flightschedule = fake_flight_schedule_as_dict(execution_time=str(timestamp))
        self.assertEqual(len(FlightSchedules.query.all()), 0)

        post_data = json.dumps(flightschedule)
        response = FlightScheduleList().post(local_data=post_data)

        self.assertEqual(response[1], 201)
        num_flightschedules = len(FlightSchedules.query.all())
        self.assertTrue(num_flightschedules > 0)

    def test_with_missing_commands(self):
        timestamp = datetime.datetime.fromtimestamp(1659816386)
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
        timestamp = datetime.datetime.fromtimestamp(1659816386)
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
        timestamp = datetime.datetime.fromtimestamp(1659816386)
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
        timestamp = datetime.datetime.fromtimestamp(1659816386)
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
        timestamp = datetime.datetime.fromtimestamp(1659816386)
        for i in range(10):
            flightschedule = FlightSchedules(**fake_flight_schedule_as_dict(execution_time=timestamp))
            db.session.add(flightschedule)
        db.session.commit()

        response = FlightScheduleList().get(local_args={'limit':3})
        self.assertEqual(response[1], 200)
        self.assertEqual(len(response[0]['data']['flightschedules']), 3)

    def test_get_flight_schedule_by_id(self):
        timestamp = datetime.datetime.fromtimestamp(1659816386)
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
        timestamp = datetime.datetime.fromtimestamp(1659816386)
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
        timestamp = datetime.datetime.fromtimestamp(1659816386)
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

#########################################################################
#Test automated command sequence model
class TestAutomatedCommandService(BaseTestCase):

    def test_post_without_admin_priviliges(self):
        current_app.config.update(BYPASS_AUTH=False)

        commands = {
            'ping': (0,False),
            'get-hk':(0,False),
        }
        for name, (num_args, is_danger) in commands.items():
            c = add_telecommand(command_name=name, num_arguments=num_args, is_dangerous=is_danger)
        command1 = Telecommands.query.filter_by(command_name='ping').first()

        user = add_user('user', 'user', is_admin=False)
        auth_token = user.encode_auth_token_by_id().decode()

        automatedcommand = fake_automatedcommand_as_dict(command_id=command1.id)
        self.assertEqual(len(AutomatedCommands.query.all()), 0)

        with self.client:
            post_data = json.dumps(automatedcommand)
            kw_args = {'data': post_data, 'content_type': 'application/json'}
            response = self.client.post(
                '/api/automatedcommands',
                headers={'Authorization': f'Bearer {auth_token}'},
                **kw_args
            )
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertIn('fail', response_data['status'])
            self.assertIn('You do not have permission to create automated commands.', response_data['message'])

    def test_post_with_admin_priviliges(self):
        current_app.config.update(BYPASS_AUTH=False)

        commands = {
            'ping': (0,False),
            'get-hk':(0,False),
        }
        for name, (num_args, is_danger) in commands.items():
            c = add_telecommand(command_name=name, num_arguments=num_args, is_dangerous=is_danger)
        command1 = Telecommands.query.filter_by(command_name='ping').first()

        admin = add_user('admin', 'admin', is_admin=True)
        auth_token = admin.encode_auth_token_by_id().decode()

        automatedcommand = fake_automatedcommand_as_dict(command_id=command1.id)
        self.assertEqual(len(AutomatedCommands.query.all()), 0)

        with self.client:
            post_data = json.dumps(automatedcommand)
            kw_args = {'data': post_data, 'content_type': 'application/json'}
            response = self.client.post(
                '/api/automatedcommands',
                headers={'Authorization': f'Bearer {auth_token}'},
                **kw_args
            )
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('success', response_data['status'])

        num_automatedcommands = len(AutomatedCommands.query.all())
        self.assertTrue(num_automatedcommands > 0)

    def test_patch_without_admin_priviliges(self):
        current_app.config.update(BYPASS_AUTH=False)

        commands = {
            'ping': (0,False),
            'get-hk':(0,False),
        }
        for name, (num_args, is_danger) in commands.items():
            c = add_telecommand(command_name=name, num_arguments=num_args, is_dangerous=is_danger)
        command1 = Telecommands.query.filter_by(command_name='ping').first()
        command2 = Telecommands.query.filter_by(command_name='get-hk').first()

        user = add_user('user', 'user', is_admin=False)
        auth_token = user.encode_auth_token_by_id().decode()

        automatedcommand = AutomatedCommands(command_id=command1.id, priority=1)
        db.session.add(automatedcommand)
        db.session.commit()

        patch_update = {'command': {'command_id': command2.id}, 'priority': 2, 'args': []}
        post_data = json.dumps(patch_update)

        with self.client:
            response = self.client.patch(
                f'api/automatedcommands/{automatedcommand.id}',
                headers={'Authorization': f'Bearer {auth_token}'},
                data=post_data,
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertIn('fail', response_data['status'])
            self.assertIn('You do not have permission to patch automated commands.', response_data['message'])

    def test_patch_with_admin_priviliges(self):
        current_app.config.update(BYPASS_AUTH=False)

        commands = {
            'ping': (0,False),
            'get-hk':(0,False),
        }
        for name, (num_args, is_danger) in commands.items():
            c = add_telecommand(command_name=name, num_arguments=num_args, is_dangerous=is_danger)
        command1 = Telecommands.query.filter_by(command_name='ping').first()
        command2 = Telecommands.query.filter_by(command_name='get-hk').first()

        admin = add_user('admin', 'admin', is_admin=True)
        auth_token = admin.encode_auth_token_by_id().decode()

        automatedcommand = AutomatedCommands(command_id=command1.id, priority=1)
        db.session.add(automatedcommand)
        db.session.commit()

        patch_update = {'command': {'command_id': command2.id}, 'priority': 2, 'args': []}
        post_data = json.dumps(patch_update)

        with self.client:
            response = self.client.patch(
                f'api/automatedcommands/{automatedcommand.id}',
                headers={'Authorization': f'Bearer {auth_token}'},
                data=post_data,
                content_type='application/json'
            )
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_data['data']['command']['command_id'], command2.id)
            self.assertEqual(response_data['data']['priority'], 2)
            self.assertIn('success', response_data['status'])

    def test_delete_without_admin_priviliges(self):
        current_app.config.update(BYPASS_AUTH=False)

        commands = {
            'ping': (0,False),
            'get-hk':(0,False),
        }
        for name, (num_args, is_danger) in commands.items():
            c = add_telecommand(command_name=name, num_arguments=num_args, is_dangerous=is_danger)
        command1 = Telecommands.query.filter_by(command_name='ping').first()

        user = add_user('user', 'user', is_admin=False)
        auth_token = user.encode_auth_token_by_id().decode()

        automatedcommand = AutomatedCommands(command_id=command1.id, priority=1)
        db.session.add(automatedcommand)
        db.session.commit()

        with self.client:
            response = self.client.delete(
                f'api/automatedcommands/{automatedcommand.id}',
                headers={'Authorization': f'Bearer {auth_token}'}
            )
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 403)
            self.assertIn('fail', response_data['status'])
            self.assertIn('You do not have permission to delete automated commands.', response_data['message'])

    def test_delete_with_admin_priviliges(self):
        current_app.config.update(BYPASS_AUTH=False)

        commands = {
            'ping': (0,False),
            'get-hk':(0,False),
        }
        for name, (num_args, is_danger) in commands.items():
            c = add_telecommand(command_name=name, num_arguments=num_args, is_dangerous=is_danger)
        command1 = Telecommands.query.filter_by(command_name='ping').first()

        admin = add_user('admin', 'admin', is_admin=True)
        auth_token = admin.encode_auth_token_by_id().decode()

        automatedcommand = AutomatedCommands(command_id=command1.id, priority=1)
        db.session.add(automatedcommand)
        db.session.commit()

        with self.client:
            response = self.client.delete(
                f'api/automatedcommands/{automatedcommand.id}',
                headers={'Authorization': f'Bearer {auth_token}'}
            )
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(AutomatedCommands.query.filter_by(id=automatedcommand.id).first(), None)
            self.assertIn('success', response_data['status'])

    def test_get_all_automatedcommands(self):
        commands = {
            'ping': (0,False),
            'get-hk':(0,False),
        }
        for name, (num_args, is_danger) in commands.items():
            c = add_telecommand(command_name=name, num_arguments=num_args, is_dangerous=is_danger)
        command1 = Telecommands.query.filter_by(command_name='ping').first()

        for i in range(10):
            automatedcommand = AutomatedCommands(command_id=command1.id, priority=i)
            db.session.add(automatedcommand)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/automatedcommands')
            response_data = json.loads(response.data.decode())
            automatedcommands = response_data['data']['automatedcommands']
            self.assertEqual(len(automatedcommands), 10)

    def test_get_all_automatedcommands_limit_by(self):
        commands = {
            'ping': (0,False),
            'get-hk':(0,False),
        }
        for name, (num_args, is_danger) in commands.items():
            c = add_telecommand(command_name=name, num_arguments=num_args, is_dangerous=is_danger)
        command1 = Telecommands.query.filter_by(command_name='ping').first()

        for i in range(10):
            automatedcommand = AutomatedCommands(command_id=command1.id, priority=i)
            db.session.add(automatedcommand)
        db.session.commit()

        with self.client:
            response = self.client.get('/api/automatedcommands?limit=3')
            response_data = json.loads(response.data.decode())
            automatedcommands = response_data['data']['automatedcommands']
            self.assertEqual(len(automatedcommands), 3)

    def test_get_all_automatedcommands_locally_limit_by(self):
        commands = {
            'ping': (0,False),
            'get-hk':(0,False),
        }
        for name, (num_args, is_danger) in commands.items():
            c = add_telecommand(command_name=name, num_arguments=num_args, is_dangerous=is_danger)
        command1 = Telecommands.query.filter_by(command_name='ping').first()

        for i in range(10):
            automatedcommand = AutomatedCommands(command_id=command1.id, priority=i)
            db.session.add(automatedcommand)
        db.session.commit()

        response = AutomatedCommandList().get(local_args={'limit':3})
        self.assertEqual(response[1], 200)
        self.assertEqual(len(response[0]['data']['automatedcommands']), 3)



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

            p = Passover(aos_timestamp=d, los_timestamp=d)
            db.session.add(p)

        db.session.commit()

        with self.client:
            response = self.client.get('/api/passovers?next=true&limit=1')
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('next_passovers' in response_data['data'].keys())
            self.assertEqual(len(response_data['data']['next_passovers']), 1)
            self.assertEqual(str(correct_next_passover).split('+')[0], response_data['data']['next_passovers'][0]['aos_timestamp'])

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

            p = Passover(aos_timestamp=d, los_timestamp=d)
            db.session.add(p)

        db.session.commit()

        with self.client:
            response = self.client.get('/api/passovers?next=true&limit=5')
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('next_passovers' in response_data['data'].keys())
            self.assertEqual(len(response_data['data']['next_passovers']), 5)
            self.assertEqual(str(correct_next_passover).split('+')[0], response_data['data']['next_passovers'][0]['aos_timestamp'])

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

            p = Passover(aos_timestamp=d, los_timestamp=d)
            db.session.add(p)

        db.session.commit()

        with self.client:
            response = self.client.get('/api/passovers?most-recent=true')
            response_data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('most_recent_passover' in response_data['data'].keys())
            self.assertEqual(str(correct_most_recent_passover).split('+')[0], response_data['data']['most_recent_passover']['aos_timestamp'])

    def test_get_next_passover_when_none_exist(self):

        current_time = datetime.datetime.now(datetime.timezone.utc)
        offset = datetime.timedelta(minutes=90)
        for i in range(-10, -5, 1):
            d = current_time + i * offset
            p = Passover(aos_timestamp=d, los_timestamp=d)
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
