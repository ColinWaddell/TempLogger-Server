from .choices import modes
from django.utils import timezone

SWITCH_OFF = 0
SWITCH_TEST = 1
SWITCH_IGNORE = 2
SWITCH_BOOST = 3

def _ALWAYS_THERMO(thermostat):
    return SWITCH_TEST


def _always_off(thermostat):
    return SWITCH_OFF


def _program(thermostat):
    program = thermostat.program

    for action in thermostat.get_actions():
        if program.active_day() and action.active_time():
            if not program.active:
                # Should only set the thermostat once
                # so if someone fiddles with the target
                # whilst the program's active their
                # chosen temp remains the same
                program.activate()
                thermostat.set_target(action.target)
                thermostat.set_boost(0.0)
            return SWITCH_TEST
        else:
            program.deactivate()

    return SWITCH_OFF


Programs = {
    modes.ALWAYS_THERMO: _ALWAYS_THERMO,
    modes.ALWAYS_OFF: _always_off,
    modes.PROGRAM: _program,
}