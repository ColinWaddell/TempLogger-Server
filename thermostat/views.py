from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Thermostat, ThermostatSensors, Program, ProgramAction
from .choices import modes
from .choices import sensor_selection


def index(request, noscript=False):
    thermostats = Thermostat.objects.all()
    _ = [thermostat.update() for thermostat in thermostats]
    mode_choices = (mode[0] for mode in modes.CHOICES)
    data = {
        "thermostats": thermostats,
        "choices": {
            "modes": mode_choices,
        },
        "noscript": noscript
    }

    return render(request, 'thermostats.html', data)


def mode(request, thermostat_id, mode):
    thermostat = get_object_or_404(Thermostat, pk=thermostat_id)
    thermostat.set_mode(mode)
    return index(request)


def unpause(request, thermostat_id):
    print("UNPAUSE")
    thermostat = get_object_or_404(Thermostat, pk=thermostat_id)
    thermostat.get_active_program().unpause()
    return index(request)


def pause(request, thermostat_id):
    print("PAUSE")
    thermostat = get_object_or_404(Thermostat, pk=thermostat_id)
    thermostat.get_active_program().pause()
    thermostat.switch_off()
    return index(request)


def jog_target(request, thermostat_id, delta):
    thermostat = get_object_or_404(Thermostat, pk=thermostat_id)
    thermostat.jog_target(int(delta))
    return index(request)


def boost(request, thermostat_id, hours):
    thermostat = get_object_or_404(Thermostat, pk=thermostat_id)
    thermostat.set_boost(int(hours))
    return index(request)


def status(request):
    sensors = ThermostatSensors.objects.all()
    actions = ProgramAction.objects.all()
    programs = Program.objects.all()

    everything = serializers.serialize("json",
                                       list(thermostats) +
                                       list(sensors) +
                                       list(actions) +
                                       list(programs))

    return HttpResponse(everything, content_type='application/json')
