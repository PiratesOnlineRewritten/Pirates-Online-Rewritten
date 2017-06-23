from pirates.interact.SimpleInteractive import SimpleInteractive
from pirates.piratesbase import PLocalizer

class WheelInteractive(SimpleInteractive):

    def __init__(self, ship):
        self.ship = ship
        wheel = ship.model.locators.find('**/location_wheel')
        if not wheel:
            wheel = ship.model.root.attachNewNode('dummyWheel')
        SimpleInteractive.__init__(self, wheel, 'wheel-%s' % ship.doId, PLocalizer.InteractWheel)

    def interactionAllowed(self, avId):
        return self.ship.canTakeWheel(avId)

    def requestInteraction(self, avId):
        self.ship.requestPilot(avId)