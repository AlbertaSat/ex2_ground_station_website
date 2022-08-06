import unittest
import sys
import os

from groundstation.tests.base import BaseTestCase

sys.path.append(os.path.join(sys.path[0], 'ex2_ground_station_software', 'src'))
from groundStation import GroundStation

"""These tests must be run manually by
    `python3 manage.py test groundstation_test`
after running `source ./update.sh` and building libcsp in this repo.
"""

# List of commands to test ground_station_software's DUMMY responses
# FORMAT:
# (command, expected server, expected port, expected buffer)
commands = [
    ("ex2.time_management.get_time()", 1, 8, 10, b'\n'),
    ("ari.time_management.set_time(1234567890)", 3, 8, 11, b'\x0bI\x96\x02\xd2'),
    ("yuk.logger.get_file()", 2, 13, 0, b'\x00'),
    ("eps.time_management.get_eps_time()", 4, 8, 0, b'\x00'),
    ("eps.control.single_output_control(10,0,0)", 4, 14, 0, b'\x00\n\x00\x00\x00'),
    ("eps.configuration.get_active_config(136,2)", 4, 9, 0, b'\x00\x88\x00\x02'),
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
        opts.hkeyfile = 'test_key.dat'
        opts.u = False
        opts.device = ''
        opts.satellite = 'EX2'
        cls.gs = GroundStation(opts)

    def test_gs_commands(self):
        for c in commands:
            with self.subTest(c=c):
                transactObj = self.gs.interactive.getTransactionObject(c[0], self.gs.networkManager)
                resp = transactObj.execute()
                with self.subTest():
                    self.assertEqual(resp['dst'], c[1])
                with self.subTest():
                    self.assertEqual(resp['dport'], c[2])
                with self.subTest():
                    self.assertEqual(resp['subservice'], c[3])
                with self.subTest():
                    self.assertEqual(resp['args'], c[4])

if __name__ == '__main__':
    unittest.main()
