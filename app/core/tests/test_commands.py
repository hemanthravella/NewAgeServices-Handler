"""This will test commands created"""
import time
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.test import SimpleTestCase
from psycopg2 import OperationalError


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """This will hold the tests which test the commands created"""

    def test_wait_for_db(self,patched_check):
        """This will test if the db is ready"""
        patched_check.return_value = True
        call_command("wait_for_db")

        patched_check.assert_called_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_with_delay(self,patched_sleep,patched_check):
        """This will test for the errors and delay"""
        patched_check.side_effect = [OperationalError] * 2 + [ImproperlyConfigured] * 2 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 5)
        patched_check.assert_called_with(databases=['default'])
