from importlib.util import find_spec
from .generic import GenericDevice
from .dummy import DummyDevice

if find_spec("automationhat") is None:
    print("AutomationPHAT not available.")
    print("Using Dummy device instead.")
    PhatNC = DummyDevice
    PhatNO = DummyDevice

else:
    
    import automationhat

    class PhatConnections():
        NO = 0
        NC = 1

    class PhatDevice(GenericDevice):
        
        def __init__(self, connection=PhatConnections.NO):
            self._connection = connection

        def switch_on(self):
            if self._connection == PhatConnections.NO:
                automationhat.relay.one.on()
                print("Switch On - NC => on")
            else:
                # NC Connection = Invert
                print("Switch On - NC => off")
                automationhat.relay.one.off()

        def switch_off(self):
            if self._connection == PhatConnections.NO:
                print("Switch Off - NO => off")
                automationhat.relay.one.off()
            else:
                # NC Connection = Invert
                print("Switch Off - NC => on")
                automationhat.relay.one.on()


    class PhatNO(PhatDevice):

        def __init__(self):
            super().__init__(PhatConnections.NO)

    class PhatNC(PhatDevice):

        def __init__(self):
            super().__init__(PhatConnections.NC)
