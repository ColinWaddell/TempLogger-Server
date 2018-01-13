from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from .models import Thermostat, Program, ProgramAction, ThermostatSensors

class ProgramActionInline(admin.TabularInline):
    model = ProgramAction
    extra = 0


class ProgramAdmin(admin.ModelAdmin):
    inlines = [ProgramActionInline]
    formfield_overrides = {
        ProgramAction: {'day': CheckboxSelectMultiple},
    }
    readonly_fields = ('active', )


class ThermostatSensorsinline(admin.TabularInline):
    model = ThermostatSensors
    extra = 0


class ThermostatAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'enabled',
        'mode',
        'device',
        'program',
        'boost'
    )
    inlines = [ThermostatSensorsinline]
    readonly_fields = ('on', )

admin.site.register(Thermostat, ThermostatAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(ProgramAction)
