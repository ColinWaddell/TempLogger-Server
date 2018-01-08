from django.contrib import admin
from .models import TemperatureSensor, Reading

class ReadingAdmin(admin.ModelAdmin):
    model = Reading
    list_display = (
        'sensor',
        'datetime',
        'temperature_c',
    )

admin.site.register(TemperatureSensor)
admin.site.register(Reading, ReadingAdmin)