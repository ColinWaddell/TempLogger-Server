from thermostat.devices.dummy import DummyDevice
from thermostat.devices.phat import PhatNO, PhatNC

DUMMY = "Dummy"
PHAT_NO = "Automation pHAT - NO Connection"
PHAT_NC = "Automation pHAT - NC Connection"

CHOICES = [
    (DUMMY, DUMMY),
    (PHAT_NO, PHAT_NO),
    (PHAT_NC, PHAT_NC),
]

HANDLERS = {
    DUMMY: DummyDevice,
    PHAT_NO: PhatNO,
    PHAT_NC: PhatNC
}
