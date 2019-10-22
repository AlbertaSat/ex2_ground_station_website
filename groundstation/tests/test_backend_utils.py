from populate_database import populate_commands_table
from groundstation.tests.base import BaseTestCase
from groundstation.backend_api.models import Commands
from unittest import mock


class TestUtils(BaseTestCase):

    @mock.patch('populate_database.print')
    def test_populate_commands(self, _):

        commands = Commands.query.all()
        self.assertEqual(len(commands), 0)
        populate_commands_table()
        commands = Commands.query.all()
        self.assertTrue(len(commands) > 0)
