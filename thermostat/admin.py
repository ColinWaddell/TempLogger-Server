from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from .models import Thermostat, Program, ProgramAction
from .models import ThermostatSensors, ThermostatPrograms, ThermostatEvent


class ProgramActionInline(admin.TabularInline):
    model = ProgramAction
    extra = 0


class ProgramAdmin(admin.ModelAdmin):
    inlines = [ProgramActionInline]
    formfield_overrides = {
        ProgramAction: {'day': CheckboxSelectMultiple},
    }


class ThermostatSensorsInline(admin.TabularInline):
    model = ThermostatSensors
    extra = 0


class ThermostatProgramsInline(admin.TabularInline):
    model = ThermostatPrograms
    extra = 0


class ThermostatAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'enabled',
        'mode',
        'device',
        'boost'
    )
    inlines = [ThermostatProgramsInline, ThermostatSensorsInline]
    readonly_fields = ('on', )

class ThermostatEventAdmin(admin.ModelAdmin):
    list_display = (
        'datetime',
        'event',
        'target',
        'thermostat'
    )

admin.site.register(Thermostat, ThermostatAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(ProgramAction)
admin.site.register(ThermostatEvent, ThermostatEventAdmin)
