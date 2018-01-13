from .choices import modes


def _always_active(thermostat):
    thermostat.test()


def _always_off(thermostat):
    thermostat.switch_off()


def _program(thermostat):
    program = thermostat.program

    for action in thermostat.get_actions():
        if program.active_day and action.active_time():
            thermostat.test()
            if not program.active:
                program.activate()
                thermostat.set_target(action.target)
                return
        else:
            if program.active:
                program.deactivate()
                thermostat.switch_off()
                return


Programs = {
    modes.ALWAYS_ACTIVE: _always_active,
    modes.ALWAYS_OFF: _always_off,
    modes.PROGRAM: _program
}