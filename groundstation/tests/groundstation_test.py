import unittest

from comm import convert_command_syntax
from groundstation.tests.base import BaseTestCase
import ex2_ground_station_software.src.groundStation as gs_software

"""These tests must be run manually by
	`python3 manage.py test groundstation_test`
after running `source ./update.sh` and building libcsp in this repo.
"""

# List of commands to test ground_station_software's DUMMY responses
# FORMAT:
# (command (website format), expected server, expected port, expected buffer)
commands = [
	("obc.time_management.get_time", 1, 8, b'\n'),
	("obc.time_management.set_time 1234567890", 1, 8, b'\x0bI\x96\x02\xd2'),
	("eps.time_management.get_eps_time", 4, 8, b'\x00'),
	("eps.control.single_output_control 10 0 0", 4, 14, b'\x00\n\x00\x00\x00'),
	("eps.configuration.get_active_config 136 2", 4, 9, b'\x00\x88\x00\x02'),
	("obc.updater.get_app_info", 1, 12, b'\x02'),
	("obc.updater.set_app_address 2097152", 1, 12, b'\x03\x00 \x00\x00')
]

class Options():
	"""Dummy container to store ground station options.
	"""
	pass

class TestGroundstation(BaseTestCase):
	@classmethod
	def setUpClass(cls):
		opts = Options()
		opts.interface = 'dummy'
		opts.timeout = 10000
		cls.gs = gs_software.groundStation.groundStation(opts)

	def test_command_converter(self):
		with self.subTest(c="obc.time_management.get_time"):
			web_command = "obc.time_management.get_time"
			self.assertEqual("obc.time_management.get_time()", convert_command_syntax(web_command))
		with self.subTest(c="obc.time_management.set_time 123456789"):
			web_command = "obc.time_management.set_time 123456789"
			self.assertEqual("obc.time_management.set_time(123456789)", convert_command_syntax(web_command))
		with self.subTest(c="eps.configuration.get_active_config 136 2"):
			web_command = "eps.configuration.get_active_config 136 2"
			self.assertEqual("eps.configuration.get_active_config(136 2)", convert_command_syntax(web_command))
		with self.subTest(c="eps.control.single_output_control 10 0 0"):
			web_command = "eps.control.single_output_control 10 0 0"
			self.assertEqual("eps.control.single_output_control(10 0 0)", convert_command_syntax(web_command))

	def test_gs_commands(self):
		for c in commands:
			with self.subTest(c=c):
				gs_command = convert_command_syntax(c[0])
				server, port, toSend = self.gs.getInput(inVal=gs_command)
				resp = self.gs.transaction(server, port, toSend)
				with self.subTest():
					self.assertEqual(resp[0]["Server"], c[1])
				with self.subTest():
					self.assertEqual(resp[0]["Port"], c[2])
				with self.subTest():
					self.assertEqual(resp[0]["Buffer"], c[3])

if __name__ == '__main__':
    unittest.main()
