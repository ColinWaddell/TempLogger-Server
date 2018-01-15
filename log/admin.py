from django.contrib import admin
from .models import Reading, TemperatureSensor

class ReadingAdmin(admin.ModelAdmin):
    model = Reading
    list_display = (
        'datetime',
        'temperature_c',
    )

admin.site.register(Reading, ReadingAdmin)
admin.site.register(TemperatureSensor)
