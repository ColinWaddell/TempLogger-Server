from .choices import modes
from django.utils import timezone

SWITCH_OFF = 0
SWITCH_TEST = 1
SWITCH_IGNORE = 2
SWITCH_BOOST = 3
SWITCH_PAUSED = 3


def _always_thermo(thermostat):
    return SWITCH_TEST


def _always_off(thermostat):
    return SWITCH_OFF


def _timer(thermostat):
    ts_programs = thermostat.thermostatprograms_set.all()
    active_action = thermostat.get_active_action()

    for ts_program in ts_programs:
        program = ts_program.program
        if thermostat.program_active() and program.active and program.paused:
            return SWITCH_PAUSED

        for action in program.programaction_set.all():
            if action == active_action:
                if not program.active:
                    # Should only set the thermostat once
                    # so if someone fiddles with the target
                    # whilst the program's active their
                    # chosen temp remains the same
                    program.activate()
                    program.unpause()
                    thermostat.set_target(action.target)
                    thermostat.set_boost(0.0)
                return SWITCH_TEST
            else:
                program.deactivate()

    return SWITCH_OFF


Programs = {
    modes.ALWAYS_THERMO: _always_thermo,
    modes.ALWAYS_OFF: _always_off,
    modes.TIMER: _timer,
}