DUMMY = "Dummy"
PHAT = "Automation pHAT"

CHOICES = [
    (DUMMY, DUMMY),
    (PHAT, PHAT),
]

class DummyDevice():

    def switch_on(self):
        print("Dummy: Enabled")

    def switch_off(self):
        print("Dummy: Disabled")
        

HANDLERS = {
    DUMMY: DummyDevice,
    PHAT: DummyDevice
}