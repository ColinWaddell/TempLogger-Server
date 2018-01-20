from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from json import dumps
from django.http import HttpResponse
from .models import Thermostat, ThermostatEvent
from .events import SET, OFF
from django.core.exceptions import ObjectDoesNotExist

def events(request, weeks_ago=0):
    logs = []
    for thermostat in Thermostat.objects.all():
        # calculate the dates
        days_ago = 7*int(weeks_ago)
        dt = timezone.now()  - timedelta(days=days_ago)
        dt_week = dt - timedelta(days=days_ago+7)

        # pull the recordings
        events = ThermostatEvent.objects.filter(
            thermostat=thermostat,
            datetime__gte=dt_week,
            datetime__lte=dt,
        )
        values = [
            {
                "x": event.datetime.strftime("%Y/%m/%d %H:%M:%S"),
                "y": event.target if event.event==SET else 0.0,
            }
            for event in events
        ]
        logs.append({
            "key": thermostat.name,
            "values": list(values),
            "classed": "thermostat",
            "area": True,
        })
    return HttpResponse(dumps(logs))