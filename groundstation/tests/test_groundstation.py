import unittest

from groundstation.tests.base import BaseTestCase
import ex2_ground_station_software.src.groundStation as gs_software

# List of commands to test ground_station_software's DUMMY responses
# FORMAT:
# (command, expected server, expected port, expected buffer as bytestring)
commands = [
	("obc.time_management.get_time()", 1, 8, b'\n'),
	("obc.time_management.set_time(1234567890)", 1, 8, b'\x0bI\x96\x02\xd2'),
	("eps.time_management.get_eps_time()", 4, 8, b'\x00'),
	("eps.control.single_output_control(10 0 0)", 4, 14, b'\x00\n\x00\x00\x00'),
	("eps.configuration.get_active_config(136 2)", 4, 9, b'\x00\x88\x00\x02'),
	("obc.updater.get_app_info()", 1, 12, b'\x02'),
	("obc.updater.set_app_address(2097152)", 1, 12, b'\x03\x00 \x00\x00')
]

class Options():
	pass

class TestGroundstation(BaseTestCase):
	@classmethod
	def setUpClass(cls):
		opts = Options()
		opts.interface = 'dummy'
		opts.timeout = 10000
		cls.gs = gs_software.groundStation.groundStation(opts)

	def test_gs_commands(self):
		for c in commands:
			with self.subTest(c=c):
				server, port, toSend = self.gs.getInput(inVal=c[0])
				resp = self.gs.transaction(server, port, toSend)
				with self.subTest():
					self.assertEqual(resp[0]["Server"], c[1])
				with self.subTest():
					self.assertEqual(resp[0]["Port"], c[2])
				with self.subTest():
					self.assertEqual(resp[0]["Buffer"], c[3])

if __name__ == '__main__':
    unittest.main()
