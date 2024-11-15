"""
This is to wait for the successful connection of the db
"""
import time

from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError


class Command(BaseCommand):
    """ Django command to wait for database"""

    def handle(self, *args, **options):
        """Entry point for command."""
        self.stdout.write("Waiting for db connection...", ending="")

        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except OperationalError:
                self.stdout.write(self.style.ERROR('database unavailable, waiting 1 second'))
                time.sleep(1)
            except ImproperlyConfigured:
                self.stdout.write(self.style.ERROR('Database configuration is not valid'))

            self.stdout.write(self.style.SUCCESS("DB connection is successful"))
