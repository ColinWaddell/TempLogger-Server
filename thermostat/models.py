from math import floor
from datetime import time
from django.utils import timezone
from django.db import models
from .choices.multiselect import MultiSelectCustomField
from .choices import modes
from .choices import devices
from .choices import weekdays
from .choices import sensor_selection
from . import events
from .programs import Programs, SWITCH_OFF, SWITCH_TEST, SWITCH_IGNORE, SWITCH_BOOST, SWITCH_PAUSED
from log.models import TemperatureSensor


class Program(models.Model):
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=False)
    paused = models.BooleanField(default=False)
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

    def pause(self):
        self.paused = True
        self.save()

    def unpause(self):
        self.paused = False
        self.save()


class ProgramAction(models.Model):
    on = models.TimeField()
    off = models.TimeField()
    target = models.FloatField(default=21.0)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    class Meta:
        ordering = ['on']

    def active_time(self):
        # Test time
        midnight = time(0, 0)
        on = self.on if not self.on == midnight else time(0, 0, 1)
        off = self.off if not self.off == midnight else time(23, 59, 59)
        roll_over = False
        if on > off:
            _ = off
            off = on
            on = _
            roll_over = True
        tz_now = timezone.now()
        now = time(tz_now.hour, tz_now.minute, tz_now.second)

        return (on <= now <= off) ^ roll_over


class Thermostat(models.Model):
    name = models.CharField(max_length=200)
    enabled = models.BooleanField(default=True)
    on = models.BooleanField(default=False)
    mode = models.CharField(max_length=50, choices=modes.CHOICES, default=modes.TIMER)
    sensor_selection = models.CharField(max_length=50, choices=sensor_selection.CHOICES, default=sensor_selection.LOWEST)
    device = models.CharField(max_length=50, choices=devices.CHOICES, default=devices.DUMMY)
    target = models.FloatField(default=21.0)
    boost = models.IntegerField(default=0)
    boost_start = models.DateTimeField(blank=True, null=True)

    def set_target(self, temp_c):
        self.target = temp_c
        self.log_event(events.SET)
        self.save()

    def jog_target(self, delta):
        self.set_target(self.target + delta)

    def get_boost_remaining(self):
        now = timezone.now()
        then = self.boost_start + timezone.timedelta(hours=self.boost)
        diff = then - now
        seconds = diff.total_seconds()
        hours = floor(seconds / 60 / 60)
        minutes = floor((seconds / 60) % 60)
        if hours:
            return "%d hour%s %d minutes" % (
                hours,
                "s" if hours > 1 else "",
                minutes
            )
        elif minutes:
            return "%d minute%s" % (
                minutes,
                "s" if minutes > 1 else ""
            )
        else:
            return "%d second%s" % (
                seconds,
                "s" if seconds > 1 else ""
            )

    def set_boost(self, hours):
        self.boost = hours
        self.boost_start = timezone.now()
        self.save()

    def set_mode(self, mode):
        self.mode = mode
        if not mode == modes.TIMER:
            if self.program_active():
                self.get_active_program().deactivate()
        self.save()

    def get_active_action(self):
        ts_programs = self.thermostatprograms_set.all()
        active_today = [ts_program.program for ts_program in ts_programs
                        if ts_program.program.active_day()]
        if not len(active_today):
            return None

        active_now = [action for program in active_today
                      for action in program.programaction_set.all()
                      if action.active_time()]
        try:
            return active_now[0]
        except IndexError:
            return None

    def get_active_program(self):
        active_action = self.get_active_action()
        return active_action.program

    def program_active(self):
        active_actions = self.get_active_action()
        return True if active_actions else False

    def programmed(self):
        return self.mode == modes.TIMER

    def always_off(self):
        return self.mode == modes.ALWAYS_OFF

    def get_temperature(self):
        sensors = ThermostatSensors.objects.filter(thermostat=self)
        temps = list((ts.sensor.get_temperature() for ts in sensors))
        temp = sensor_selection.ROUTINES[self.sensor_selection](temps)
        return temp

    def update(self):
        test = self._boost_test()
        if test == SWITCH_IGNORE:
            test = Programs[self.mode](self)

        if test == SWITCH_OFF:
            self.log_event(events.OFF)
            self.switch_off()
        elif test == SWITCH_TEST:
            self.log_event(events.SET)
            self.test()
        elif test == SWITCH_PAUSED:
            self.log_event(events.OFF)
            self.switch_off()
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

    def log_event(self, event):
        # Only log changes of thermostat control state
        try:
            last_te = ThermostatEvent.objects.filter(thermostat=self).order_by('-id')[0]
            new_event = not last_te.event == event or \
                        not last_te.target == self.target
        except IndexError:
            new_event = True

        if new_event:
            te = ThermostatEvent(
                datetime=timezone.now(),
                thermostat=self,
                event=event,
                target=self.target
            )
            te.save()

    def test(self):
        self.switch_off() if self.too_warm() else self.switch_on()

    def status_icon(self):
        on = 'glyphicon-flash'
        off = 'glyphicon-stop'
        paused = 'glyphicon-pause'
        program = 'glyphicon-play'
        thermo_watching = 'glyphicon-eye-open'

        if self.on:
            return on

        if self.mode == modes.ALWAYS_THERMO and self.too_warm():
            return thermo_watching

        print(self.program_active())
        if self.mode == modes.TIMER and self.program_active():
            if self.get_active_program().paused:
                return paused
            else:
                return program

        return off

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


class ThermostatPrograms(models.Model):
    thermostat = models.ForeignKey(Thermostat, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

class ThermostatEvent(models.Model):
    datetime = models.DateTimeField('date published')
    event = models.CharField(max_length=50, choices=events.CHOICES, default=events.OFF)
    thermostat = models.ForeignKey(Thermostat, on_delete=models.CASCADE)
    target = models.FloatField(blank=True, null=True, default=0.0)
