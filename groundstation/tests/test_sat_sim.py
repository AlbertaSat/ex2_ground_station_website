import unittest
from unittest import mock
import json

from groundstation.tests.base import BaseTestCase
import sys
sys.path.append(".")
from satellite_simulator.sat_sim import Environment, Satellite, Simulator, SatelliteComponent

class TestSatelliteSimulator(BaseTestCase):
    """Tests the satellite simulator
    """

    @mock.patch('satellite_simulator.sat_sim.Satellite._broadcast_beacon')
    @mock.patch('satellite_simulator.sat_sim.open')
    @mock.patch('satellite_simulator.sat_sim.time.sleep')
    def test_ping(self, mocked_time_sleep, _, mocked_broadcast):
        environment = Environment(connection_strength=10, connection_stability=10,
            packet_drop_probability=0)

        satellite = Satellite([], beacon_interval=20)
        simulator = Simulator(environment, satellite)
        del environment, satellite

        data = ('PING', [])
        for i in range(25):
            resp = simulator.send_to_sat(data)
            self.assertEqual(resp, 'PING-RESPONSE')

        mocked_time_sleep.assert_called()

    @mock.patch('satellite_simulator.sat_sim.Satellite._broadcast_beacon')
    @mock.patch('satellite_simulator.sat_sim.open')
    @mock.patch('satellite_simulator.sat_sim.time.sleep')
    def turn_on_gps(self, mocked_time_sleep, mocked_open, _):
        environment = Environment(connection_strength=10, connection_stability=10,
            packet_drop_probability=0)

        volt_effect = lambda old_value, time_delta : old_value - (0.01 * time_delta)

        satellite_components = [
            SatelliteComponent('GPS', 0, [('battery_voltage', volt_effect)], []),
            ]
        satellite = Satellite(satellite_components)
        simulator = Simulator(environment, satellite)
        del environment, satellite

        data = ('TURN-ON', ['0'])
        resp = simulator.send_to_sat(data)
        self.assertEqual(resp, '200 OK')
        self.assertTrue(simulator.satellite.components[0][0].is_on)

    @mock.patch('satellite_simulator.sat_sim.Satellite._broadcast_beacon')
    @mock.patch('satellite_simulator.sat_sim.open')
    @mock.patch('satellite_simulator.sat_sim.time.sleep')
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

    # TODO: hard to test now so just ignore
    # @mock.patch('satellite_simulator.sat_sim.Satellite._broadcast_beacon')
    # @mock.patch('satellite_simulator.sat_sim.open')
    # @mock.patch('satellite_simulator.sat_sim.time.sleep')
    # def test_component_effects_battery(self, mocked_time_sleep, mocked_open, _):
    #     environment = Environment(connection_strength=10, connection_stability=10,
    #         packet_drop_probability=0)
    #
    #     volt_effect = lambda old_value, time_delta : old_value - (0.01 * time_delta)
    #
    #     satellite_components = [
    #         SatelliteComponent('GPS', 0, [('battery_voltage', volt_effect)], []),
    #         ]
    #     satellite = Satellite(satellite_components)
    #     simulator = Simulator(environment, satellite)
    #     del environment, satellite
    #
    #     starting_voltage = simulator.satellite.battery_voltage
    #
    #     data = ('TURN-ON', ['0'])
    #     simulator.send_to_sat(data)
    #
    #     data = ('GET-HK', [])
    #     resp = simulator.send_to_sat(data)
    #     hk_dict = json.loads(resp)
    #     self.assertTrue(hk_dict['battery_voltage'] < starting_voltage)

    @mock.patch('satellite_simulator.sat_sim.Satellite._broadcast_beacon')
    @mock.patch('satellite_simulator.sat_sim.open')
    @mock.patch('satellite_simulator.sat_sim.time.sleep')
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

    @mock.patch('satellite_simulator.sat_sim.Satellite._broadcast_beacon')
    @mock.patch('satellite_simulator.sat_sim.open')
    @mock.patch('satellite_simulator.sat_sim.time.sleep')
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
