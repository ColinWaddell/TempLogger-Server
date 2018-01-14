from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core import serializers

from .models import Thermostat, ThermostatSensors, Program, ProgramAction
from .choices import modes
from .choices import sensor_selection

# Create your views here.
def index(request):
    thermostats = Thermostat.objects.all()
    mode_choices = (mode[0] for mode in modes.CHOICES)
    return render(
            request, 
            'thermostats.html',
            {
                "thermostats": thermostats,
                "choices": {
                    "modes": mode_choices,
                }
            }
        )


def mode(request, thermostat_id, mode):
    thermostat = get_object_or_404(Thermostat, pk=thermostat_id)
    thermostat.set_mode(mode)
    thermostat.update()
    return index(request)


def jog_target(request, thermostat_id, delta):
    thermostat = get_object_or_404(Thermostat, pk=thermostat_id)
    thermostat.jog_target(int(delta))
    thermostat.update()
    return index(request)


def boost(request, thermostat_id, hours):
    thermostat = get_object_or_404(Thermostat, pk=thermostat_id)
    thermostat.set_boost(int(hours))
    thermostat.update()
    return index(request)

def status(request):
    sensors = ThermostatSensors.objects.all()
    actions = ProgramAction.objects.all()
    programs = Program.objects.all()

    everything = serializers.serialize("json", 
        list(thermostats) + 
        list(sensors) + 
        list(actions) + 
        list(programs)
    )

    return HttpResponse(everything, content_type='application/json')
