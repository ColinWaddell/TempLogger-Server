from django.utils import timezone
from datetime import time

ALWAYS_OFF = "Always off"
ALWAYS_ACTIVE = "Just the thermostat"
PROGRAM = "Run a program"

CHOICES = [
    (ALWAYS_OFF, ALWAYS_OFF),
    (ALWAYS_ACTIVE, ALWAYS_ACTIVE),
    (PROGRAM, PROGRAM)
]
