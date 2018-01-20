from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from json import dumps
from django.http import HttpResponse
from .models import Reading
from .models import TemperatureSensor
from django.core.exceptions import ObjectDoesNotExist
from .utilities import max_weeks

def index(request, weeks_ago=0):
    weeks = {
        "ago": weeks_ago,
        "max": range(1, max_weeks() + 1)
    }
    return render(request, 'log.html', {"weeks": weeks})


def get(request, weeks_ago=0):
    logs = []
    sensors = TemperatureSensor.objects.all()
    for sensor in sensors:
        # calculate the dates
        days_ago = 7*int(weeks_ago)
        dt = timezone.now()  - timedelta(days=days_ago)
        dt_week = dt - timedelta(days=days_ago+7)

        # pull the recordings
        readings = Reading.objects.filter(
            sensor=sensor,
            datetime__gte=dt_week,
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
