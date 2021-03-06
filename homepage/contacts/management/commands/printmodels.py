"""Print all models names and number of entiries of each model
"""
import sys

from django.core.management.base import BaseCommand
from django.core.management.base import NoArgsCommand
from django.db import models


class Command(NoArgsCommand):
    """Implement django-admin.py command
    """
    help = 'Print project models info'

    def __format_output(self, col1, col2):
        """All output formatting stuff must be placed here.
        """
        return '%-50s%-20s' % (col1, col2)

    def __print(self, model_name, entries_count):
        """Format and print data to screen
        """
        output = self.__format_output(model_name, entries_count)
        self.stdout.write(output + '\n')
        self.stderr.write('error: %s\n' % output)

    def handle(self, *args, **options):
        """Command handler
        """
        self.stdout.write(self.__format_output('Model name', 'Number of entiries') + '\n')
        for app in models.get_apps():
            for app_model in models.get_models(app, include_auto_created=True):
                self.__print('%s:%s' % (app.__name__, app_model.__name__),
                             app_model.objects.count())
