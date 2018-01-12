from django.db import models
from multiselectfield import MultiSelectField
from .choices import modes
from .choices import devices
from .choices import weekdays
from .choices import sensor_selection
from log.models import TemperatureSensor


class Program(models.Model):
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    active.boolean = True
    override = models.BooleanField(default=False)
    day = MultiSelectField(
        choices=weekdays.CHOICES,
        default=weekdays.DEFAULT,
        max_choices=7
    )

    def __str__(self):
        return self.name


class ProgramAction(models.Model):
    on = models.TimeField()
    off = models.TimeField()
    target = models.FloatField(default=21.0)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)


class Thermostat(models.Model):
    name = models.CharField(max_length=200)
    enabled = models.BooleanField(default=True)
    mode = models.CharField(max_length=50, choices=modes.CHOICES, default=modes.PROGRAM)
    sensor_selection = models.CharField(max_length=50, choices=sensor_selection.CHOICES, default=sensor_selection.LOWEST)
    device = models.CharField(max_length=50, choices=devices.CHOICES, default=devices.DUMMY)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True)
    boost = models.IntegerField(default=0)

    def get_temperature(self):
        sensors = ThermostatSensors.objects.filter(thermostat=self)
        temps = list((ts.sensor.get_temperature() for ts in sensors))
        temp = sensor_selection.ROUTINES[self.sensor_selection](temps)
        return temp


    def update(self):
        pass


    def __str__(self):
        return self.name


class ThermostatSensors(models.Model):
    thermostat = models.ForeignKey(Thermostat, on_delete=models.CASCADE)
    sensor = models.ForeignKey(TemperatureSensor, on_delete=models.CASCADE)
