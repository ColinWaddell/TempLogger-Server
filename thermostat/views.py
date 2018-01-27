from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from json import dumps
from django.http import HttpResponse
from .models import Thermostat, ThermostatEvent
from .events import SET, OFF
from django.core.exceptions import ObjectDoesNotExist

def events(request, units="weeks", ago=0):
    # calculate the dates
    if units == "weeks":
        offset = 7
    elif units == "days":
        offset = 1
    days_ago = offset*int(ago)
    now = timezone.now()
    dt = now - timedelta(days=days_ago)
    dt_next = dt - timedelta(days=days_ago+offset)
    logs = []

    for thermostat in Thermostat.objects.all():
        # pull the recordings
        events = ThermostatEvent.objects.filter(
            thermostat=thermostat,
            datetime__gte=dt_next,
            datetime__lte=dt,
        )
        values = [
            {
                "x": event.datetime.strftime("%Y/%m/%d %H:%M:%S"),
                "y": event.target if event.event == SET else 0.0,
            }
            for event in events
        ]
        # Run the last path to the current
        try:
            next_event = events.last().next()
            values.append(
                {
                    "x": next_event.datetime.strftime("%Y/%m/%d %H:%M:%S"),
                    "y": next_event.target if next_event.event == SET else 0.0,
                }
            )
        except ObjectDoesNotExist:
            values.append(
                {
                    "x": now.strftime("%Y/%m/%d %H:%M:%S"),
                    "y": values[-1]["y"]
                }
            )

        logs.append({
            "key": thermostat.name,
            "values": list(values),
            "classed": "thermostat",
            "area": True,
        })
    return HttpResponse(dumps(logs))
