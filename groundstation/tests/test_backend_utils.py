from groundstation.tests.base import BaseTestCase
from groundstation.backend_api.models import Telecommands
from groundstation.backend_api.utils import add_telecommand
from unittest import mock


class TestUtils(BaseTestCase):

    def test_add_telecommand(self):

        commands = Telecommands.query.all()
        self.assertEqual(len(commands), 0)
        add_telecommand('TEST_COMMAND', 2, False)
        commands = Telecommands.query.all()
        self.assertTrue(len(commands) > 0)
