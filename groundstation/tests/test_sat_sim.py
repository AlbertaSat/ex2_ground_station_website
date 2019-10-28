import unittest
from unittest import mock
import json

from groundstation.tests.base import BaseTestCase
from groundstation.satellite_simulator.sat_sim import Environment, Satellite, Simulator, SatelliteComponent

class TestSatelliteSimulator(BaseTestCase):

    @mock.patch('groundstation.satellite_simulator.sat_sim.Satellite._broadcast_beacon')
    @mock.patch('groundstation.satellite_simulator.sat_sim.open')
    @mock.patch('groundstation.satellite_simulator.sat_sim.time.sleep')
    def test_ping(self, mocked_time_sleep, _, mocked_broadcast):
        environment = Environment(connection_strength=10, connection_stability=10,
            packet_drop_probability=0)

        satellite = Satellite([], beacon_Interval=20)
        simulator = Simulator(environment, satellite)
        del environment, satellite

        data = ('PING', [])
        for i in range(25):
            resp = simulator.send_to_sat(data)
            self.assertEqual(resp, 'PING-RESPONSE')
            simulator.step()

        mocked_time_sleep.assert_called()
        mocked_broadcast.assert_called_once()

    @mock.patch('groundstation.satellite_simulator.sat_sim.Satellite._broadcast_beacon')
    @mock.patch('groundstation.satellite_simulator.sat_sim.open')
    @mock.patch('groundstation.satellite_simulator.sat_sim.time.sleep')
    def turn_on_gps(self, mocked_time_sleep, mocked_open, _):
        environment = Environment(connection_strength=10, connection_stability=10,
            packet_drop_probability=0)

        def effect_of_gps_on(old_value):
            new_value = old_value - 0.01
            return new_value

        satellite_components = [
            SatelliteComponent('GPS', [('battery_Voltage', effect_of_gps_on)], []),
            ]
        satellite = Satellite(satellite_components)
        simulator = Simulator(environment, satellite)
        del environment, satellite

        data = ('TURN-ON', ['GPS'])
        resp = simulator.send_to_sat(data)
        self.assertEqual(resp, '200 OK')
        self.assertTrue(simulator.satellite.components['GPS'].is_on)

    @mock.patch('groundstation.satellite_simulator.sat_sim.Satellite._broadcast_beacon')
    @mock.patch('groundstation.satellite_simulator.sat_sim.open')
    @mock.patch('groundstation.satellite_simulator.sat_sim.time.sleep')
    def test_get_hk(self, mocked_time_sleep, mocked_open, _):

        environment = Environment(connection_strength=10, connection_stability=10,
            packet_drop_probability=0)

        satellite = Satellite([])
        simulator = Simulator(environment, satellite)
        del environment, satellite

        data = ('GET-HK', [])
        resp = simulator.send_to_sat(data)
        hk_dict = json.loads(resp)
        self.assertTrue(len(hk_dict) > 0)

    @mock.patch('groundstation.satellite_simulator.sat_sim.Satellite._broadcast_beacon')
    @mock.patch('groundstation.satellite_simulator.sat_sim.open')
    @mock.patch('groundstation.satellite_simulator.sat_sim.time.sleep')
    def test_component_effects_battery(self, mocked_time_sleep, mocked_open, _):
        environment = Environment(connection_strength=10, connection_stability=10,
            packet_drop_probability=0)

        def effect_of_gps_on(old_value):
            new_value = old_value - 0.01
            return new_value

        satellite_components = [
            SatelliteComponent('GPS', [('battery_Voltage', effect_of_gps_on)], []),
            ]
        satellite = Satellite(satellite_components)
        simulator = Simulator(environment, satellite)
        del environment, satellite

        starting_voltage = simulator.satellite.battery_Voltage

        data = ('TURN-ON', ['GPS'])
        simulator.send_to_sat(data)
        for i in range(10):
            simulator.step()

        data = ('GET-HK', [])
        resp = simulator.send_to_sat(data)
        hk_dict = json.loads(resp)
        self.assertTrue(hk_dict['battery_Voltage'] < starting_voltage)

    @mock.patch('groundstation.satellite_simulator.sat_sim.Satellite._broadcast_beacon')
    @mock.patch('groundstation.satellite_simulator.sat_sim.open')
    @mock.patch('groundstation.satellite_simulator.sat_sim.time.sleep')
    def test_full_packet_loss(self, mocked_time_sleep, mocked_open, _):
        environment = Environment(connection_strength=10, connection_stability=10,
            packet_drop_probability=1)

        satellite = Satellite([])
        simulator = Simulator(environment, satellite)
        del environment, satellite

        data = ('PING', [])
        for i in range(100):
            resp = simulator.send_to_sat(data)
            self.assertEqual(resp, 'NO-RESPONSE')
            simulator.step()

    @mock.patch('groundstation.satellite_simulator.sat_sim.Satellite._broadcast_beacon')
    @mock.patch('groundstation.satellite_simulator.sat_sim.open')
    @mock.patch('groundstation.satellite_simulator.sat_sim.time.sleep')
    def test_some_packet_loss(self, mocked_time_sleep, mocked_open, _):
        environment = Environment(connection_strength=10, connection_stability=10,
            packet_drop_probability=0.5)

        satellite = Satellite([])
        simulator = Simulator(environment, satellite)
        del environment, satellite

        responses = 0
        data = ('PING', [])
        for i in range(100):
            resp = simulator.send_to_sat(data)
            if resp == 'PING-RESPONSE':
                responses += 1
        self.assertTrue(responses < 100)





if __name__ == '__main__':
    unittest.main()
