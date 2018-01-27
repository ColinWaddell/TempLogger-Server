from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from json import dumps
from django.http import HttpResponse
from .models import Thermostat, ThermostatEvent
from .events import SET, OFF
from django.core.exceptions import ObjectDoesNotExist

def events(request, thermostat_id, units="weeks", ago=0):
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

    thermostat = get_object_or_404(Thermostat, pk=thermostat_id)
    # pull the recordings
    th_events = ThermostatEvent.objects.filter(
        thermostat=thermostat,
        datetime__gte=dt_next,
        datetime__lte=dt,
    )
    values = [
        {
            "x": event.datetime.strftime("%Y/%m/%d %H:%M:%S"),
            "y": event.target if event.event == SET else 0.0,
        }
        for event in th_events
    ]
    # Run up to first event
    try:
        prev_event = th_events[0].previous()
        values = [
            {
                "x": dt_next.strftime("%Y/%m/%d %H:%M:%S"),
                "y": prev_event.target if prev_event.event == SET else 0.0,
            }
        ] + values
    except ObjectDoesNotExist:
        pass

    # Run the last path to the current
    try:
        next_event = th_events.last().next()
        values.append(
            {
                "x": dt.strftime("%Y/%m/%d %H:%M:%S"),
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
