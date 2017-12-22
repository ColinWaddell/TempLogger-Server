from django.utils import timezone
from .models import Reading
from math import floor

def max_weeks():
    oldest = Reading.objects.all().order_by("-datetime")[0]
    delta = timezone.now() - oldest.datetime
    weeks = delta.days / 7
    return floor(weeks)
