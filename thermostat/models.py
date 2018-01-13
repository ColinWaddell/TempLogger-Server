from datetime import time
from django.utils import timezone
from django.db import models
from multiselectfield import MultiSelectField
from .choices import modes
from .choices import devices
from .choices import weekdays
from .choices import sensor_selection
from .programs import Programs
from log.models import TemperatureSensor


class Program(models.Model):
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    day = MultiSelectField(
        choices=weekdays.CHOICES,
        default=weekdays.DEFAULT,
        max_choices=7
    )

    def __str__(self):
        return self.name

    def active_day(self):
        today = timezone.now().isoweekday() - 1
        try:
            _ = self.day.index(str(pow(2, today)))
        except ValueError:
            return False
        finally:
            return True

    def activate(self):
        self.active = True
        self.save()

    def deactivate(self):
        self.activate = False
        self.save()
            

class ProgramAction(models.Model):
    on = models.TimeField()
    off = models.TimeField()
    target = models.FloatField(default=21.0)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def active_time(self, days=None):
        # Test time
        midnight = time(0, 0)
        on = self.on if not self.on == midnight else time (0, 0, 1)
        off = self.off  if not self.off == midnight else time (23, 59, 59)
        roll_over = False
        if on > off:
            _ = off
            off = on
            on = _
            roll_over  = True
        tz_now = timezone.now()
        now = time(tz_now.hour, tz_now.minute, tz_now.second)

        return (on <= now <= off) ^ roll_over


class Thermostat(models.Model):
    name = models.CharField(max_length=200)
    enabled = models.BooleanField(default=True)
    on = models.BooleanField(default=False)
    mode = models.CharField(max_length=50, choices=modes.CHOICES, default=modes.PROGRAM)
    sensor_selection = models.CharField(max_length=50, choices=sensor_selection.CHOICES, default=sensor_selection.LOWEST)
    device = models.CharField(max_length=50, choices=devices.CHOICES, default=devices.DUMMY)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True)
    target = models.FloatField(default=21.0)
    boost = models.IntegerField(default=0)

    def set_target(self, temp_c):
        self.target = temp_c
        self.save()

    def get_temperature(self):
        sensors = ThermostatSensors.objects.filter(thermostat=self)
        temps = list((ts.sensor.get_temperature() for ts in sensors))
        temp = sensor_selection.ROUTINES[self.sensor_selection](temps)
        return temp

    def get_actions(self):
        return ProgramAction.objects.filter(program=self.program)

    def update(self):
        Programs[self.mode](self)
        self.save()

    def too_warm(self):
        return self.get_temperature() > self.target

    def switch_on(self):
        device = devices.HANDLERS[self.device]()
        device.switch_on()
        self.on = True
        self.save()

    def switch_off(self):
        dev = devices.HANDLERS[self.device]()
        dev.switch_off()
        self.on = False
        self.save()

    def test(self):
        self.switch_off() if self.too_warm() else self.switch_on()

    def __str__(self):
        return self.name


class ThermostatSensors(models.Model):
    thermostat = models.ForeignKey(Thermostat, on_delete=models.CASCADE)
    sensor = models.ForeignKey(TemperatureSensor, on_delete=models.CASCADE)
