from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from json import dumps
from django.http import HttpResponse
from .models import Reading
from .models import TemperatureSensor
from thermostat.models import Thermostat
from django.core.exceptions import ObjectDoesNotExist
from .utilities import max_weeks, max_days

def index(request, ago=0, units="weeks"):
    log_range = {
        "ago": ago,
        "units": units,
    }
    if units == "weeks":
        log_range["max"] = range(1, max_weeks() + 1)
    elif units == "days":
        log_range["max"] = range(1, max_days() + 1)
    return render(request, 'log.html', {"range": log_range})


def get(request, thermostat_id, units='weeks', ago=0):
    # calculate the dates
    if units == "weeks":
        offset = 7
    elif units == "days":
        offset = 1
    days_ago = offset*int(ago)
    dt = timezone.now()  - timedelta(days=days_ago)
    dt_next = dt - timedelta(days=days_ago+offset)
    logs = []

    thermostat = get_object_or_404(Thermostat, pk=thermostat_id)
    th_sensors = thermostat.thermostatsensors_set.all()

    for th_sensor in th_sensors:
        sensor = th_sensor.sensor
        # pull the recordings
        readings = Reading.objects.filter(
            sensor=sensor,
            datetime__gte=dt_next,
            datetime__lte=dt,
        )
        values = [
            {
                "x": reading.datetime.strftime("%Y/%m/%d %H:%M:%S"),
                "y": reading.temperature_c,
            }
            for reading in readings
        ]
        # Save
        logs.append(
            {
                "key": sensor.name,
                "values": list(values),
                "classed": "reading"
            }
        )
    return HttpResponse(dumps(logs))

def update(request, sensor_id, temperature_c):
    feedback = {
        "error": ""
    }

    sensor_id = int(sensor_id)
    temperature_c = float(temperature_c)

    try:
        sensor = TemperatureSensor.objects.get(pk=sensor_id)

        logged_reading = {
            "sensor": sensor,
            "temperature_c": temperature_c,
            "datetime": timezone.now()
        }

        logged_reading = Reading(**logged_reading)
        logged_reading.save()

    except ObjectDoesNotExist:
        feedback = {
            "error": "Sensor %d does not exist" % sensor_id
        }

    return HttpResponse(dumps(feedback))
