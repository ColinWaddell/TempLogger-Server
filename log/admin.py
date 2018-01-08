from django.contrib import admin
from .models import TemperatureSensor, Reading

admin.site.register(TemperatureSensor)
admin.site.register(Reading)
