from django.core.management.base import BaseCommand
from thermostat.models import Thermostat

class Command(BaseCommand):
    help = 'Test all the thermostats for status updates'

    def handle(self, *args, **options):
        _ = [thermostats.update() for thermostats in Thermostat.objects.all()]
