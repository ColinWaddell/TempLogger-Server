from django.core.management.base import BaseCommand
from thermostat.models import Thermostat

class Command(BaseCommand):
    help = 'Test all the thermostats status'

    def handle(self, *args, **options):
        thermostats = Thermostat.objects.all()
        for thermostat in thermostats:
            thermostat.update()
