from math import floor
from datetime import time
from django.utils import timezone
from django.db import models
from .choices.multiselect import MultiSelectCustomField
from .choices import modes
from .choices import devices
from .choices import weekdays
from .choices import sensor_selection
from .programs import Programs, SWITCH_OFF, SWITCH_TEST, SWITCH_IGNORE, SWITCH_BOOST
from log.models import TemperatureSensor


class Program(models.Model):
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    day = MultiSelectCustomField(
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
            return True
        except ValueError:
            return False

    def activate(self):
        self.active = True
        self.save()

    def deactivate(self):
        self.active = False
        self.save()
            

class ProgramAction(models.Model):
    on = models.TimeField()
    off = models.TimeField()
    target = models.FloatField(default=21.0)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    def active_time(self):
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
    boost_start = models.DateTimeField(blank=True, null=True)

    def set_target(self, temp_c):
        self.target = temp_c
        self.save()

    def jog_target(self, delta):
        self.target = self.target + delta
        self.save()

    def get_boost_remaining(self):
        now = timezone.now()
        then = self.boost_start + timezone.timedelta(hours=self.boost)
        diff = then - now
        seconds = diff.total_seconds()
        hours = floor(seconds / 60 / 60)
        minutes = (seconds / 60) % 60
        if hours:
            return "%d hour%s %d minutes" % (
                hours, 
                "s" if hours > 1 else "",
                minutes
            )
        else:
            return "%d minutes" % (minutes)

    def set_boost(self, hours):
        self.boost = hours
        self.boost_start = timezone.now()
        self.save()

    def set_mode(self, mode):
        self.mode = mode
        if not mode==modes.PROGRAM:
            self.program.deactivate()
        self.save()

    def programmed(self):
        return self.mode == modes.PROGRAM

    def always_off(self):
        return self.mode == modes.ALWAYS_OFF

    def get_temperature(self):
        sensors = ThermostatSensors.objects.filter(thermostat=self)
        temps = list((ts.sensor.get_temperature() for ts in sensors))
        temp = sensor_selection.ROUTINES[self.sensor_selection](temps)
        return temp

    def get_actions(self):
        return ProgramAction.objects.filter(program=self.program)

    def update(self):
        test = self._boost_test()
        if  test == SWITCH_IGNORE:
            test = Programs[self.mode](self)

        if test == SWITCH_OFF:
            self.switch_off()
        elif test == SWITCH_TEST:
            self.test()
        elif test == SWITCH_IGNORE:
            pass

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

    def _boost_test(self):
        if self.boost:
            now = timezone.now()
            then = self.boost_start + timezone.timedelta(hours=self.boost) 
            if now < then:
                return SWITCH_TEST
            else:
                # boost needs deactivated
                self.boost = 0.0
        return SWITCH_IGNORE


    def __str__(self):
        return self.name


class ThermostatSensors(models.Model):
    thermostat = models.ForeignKey(Thermostat, on_delete=models.CASCADE)
    sensor = models.ForeignKey(TemperatureSensor, on_delete=models.CASCADE)
