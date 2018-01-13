from .choices import modes


def _always_active(thermostat):
    thermostat.test()


def _always_off(thermostat):
    thermostat.switch_off()


def _program(thermostat):
    program = thermostat.program

    if not program.active:
        program.activate()
        for program_action in thermostat.get_actions():
            action = program_action.action
            if program.active_day and action.active_time():
                thermostat.test()

    program.deactivate()
    thermostat.switch_off()


Programs = {
    modes.ALWAYS_ACTIVE: _always_active,
    modes.ALWAYS_OFF: _always_off,
    modes.PROGRAM: _program
}