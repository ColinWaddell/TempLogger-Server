from django.utils import timezone
from datetime import time

ALWAYS_OFF = "Always off"
ALWAYS_THERMO = "Just the thermostat"
TIMER = "Timer Program"

CHOICES = [
    (ALWAYS_OFF, ALWAYS_OFF),
    (ALWAYS_THERMO, ALWAYS_THERMO),
    (TIMER, TIMER)
]
