from .generic import GenericDevice

class DummyDevice(GenericDevice):

    def switch_on(self):
        print("Dummy: Enabled")

    def switch_off(self):
        print("Dummy: Disabled")