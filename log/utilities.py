from math import floor
from django.utils import timezone
from .models import Reading


def _log_range_days():
    oldest = Reading.objects.all().order_by("-datetime")[0]
    delta = timezone.now() - oldest.datetime
    return delta.days


def max_weeks():
    weeks = _log_range_days() / 7
    return floor(weeks)


def max_days():
    return _log_range_days()
