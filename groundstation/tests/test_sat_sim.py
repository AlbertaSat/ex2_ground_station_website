import unittest

from groundstation.tests.base import BaseTestCase
from groundstation.satelliteSimulator.satSim import Environment, Satellite, Simulator, SatelliteComponent

class TestSatelliteSimulator(BaseTestCase):

    def test_ping(self):
        environment = Environment(connection_strength=10, connection_stability=10,
            packet_drop_probability=0, no_delay=True)

        satellite = Satellite([])
        simulator = Simulator(environment, satellite)
        del environment, satellite

        data = ('PING', [])
        for i in range(100):
            resp = simulator.send_to_sat(data)
            self.assertEqual(resp, 'PING-RESPONSE')
            simulator.step()

    def turn_on_gps(self):
        environment = Environment(connection_strength=10, connection_stability=10,
            packet_drop_probability=0, no_delay=True)

        def effect_of_gps_on(old_value):
            new_value = old_value - 0.01
            return new_value

        satellite_components = [
            SatelliteComponent('GPS', [('batteryVoltage', effect_of_gps_on)], []),
            ]
        satellite = Satellite(satellite_components)
        simulator = Simulator(environment, satellite)
        del environment, satellite

        data = ('TURN-ON', ['GPS'])
        resp = simulator.send_to_sat(data)
        self.assertEqual(resp, '200 OK')
        self.assertTrue(simulator.satellite.components['GPS'].is_on)

    def test_get_hk(self):
        import json

        environment = Environment(connection_strength=10, connection_stability=10,
            packet_drop_probability=0, no_delay=True)

        satellite = Satellite([])
        simulator = Simulator(environment, satellite)
        del environment, satellite

        data = ('GET-HK', [])
        resp = simulator.send_to_sat(data)
        hk_dict = json.loads(resp)
        self.assertTrue(len(hk_dict) > 0)

    def test_component_effects_battery(self):
        import json
        environment = Environment(connection_strength=10, connection_stability=10,
            packet_drop_probability=0, no_delay=True)

        def effect_of_gps_on(old_value):
            new_value = old_value - 0.01
            return new_value

        satellite_components = [
            SatelliteComponent('GPS', [('batteryVoltage', effect_of_gps_on)], []),
            ]
        satellite = Satellite(satellite_components)
        simulator = Simulator(environment, satellite)
        del environment, satellite

        starting_voltage = simulator.satellite.batteryVoltage

        data = ('TURN-ON', ['GPS'])
        simulator.send_to_sat(data)
        for i in range(10):
            simulator.step()

        data = ('GET-HK', [])
        resp = simulator.send_to_sat(data)
        hk_dict = json.loads(resp)
        self.assertTrue(hk_dict['batteryVoltage'] < starting_voltage)

    def test_full_packet_loss(self):
        environment = Environment(connection_strength=10, connection_stability=10,
            packet_drop_probability=1, no_delay=True)

        satellite = Satellite([])
        simulator = Simulator(environment, satellite)
        del environment, satellite

        data = ('PING', [])
        for i in range(100):
            resp = simulator.send_to_sat(data)
            self.assertEqual(resp, 'NO-RESPONSE')
            simulator.step()

    def test_some_packet_loss(self):
        environment = Environment(connection_strength=10, connection_stability=10,
            packet_drop_probability=0.5, no_delay=True)

        satellite = Satellite([])
        simulator = Simulator(environment, satellite)
        del environment, satellite

        responses = 0
        data = ('PING', [])
        for i in range(100):
            resp = simulator.send_to_sat(data)
            if resp == 'PING-RESPONSE':
                responses += 1
        self.assertTrue(responses in range(20, 80))





if __name__ == '__main__':
    unittest.main()
