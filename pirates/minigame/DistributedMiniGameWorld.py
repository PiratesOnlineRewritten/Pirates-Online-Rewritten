from pirates.instance import DistributedInstanceWorld

class DistributedMiniGameWorld(DistributedInstanceWorld.DistributedInstanceWorld):

    def __init__(self, cr):
        DistributedInstanceWorld.DistributedInstanceWorld.__init__(self, cr)
        self._turnOnWorldGrid = True

    def generate(self):
        DistributedInstanceWorld.DistributedInstanceWorld.generate(self)

    def announceGenerate(self):
        DistributedInstanceWorld.DistributedInstanceWorld.announceGenerate(self)

    def turnOn(self, av=None):
        DistributedInstanceWorld.DistributedInstanceWorld.turnOn(self, None)
        if self.worldGrid and av and self._turnOnWorldGrid:
            self.worldGrid.turnOn(av)
        self._turnOnIslands()
        return

    def turnOff(self, cacheIslands=[]):
        DistributedInstanceWorld.DistributedInstanceWorld.turnOff(self, cacheIslands)

    def addWorldInterest(self, area=None):
        DistributedInstanceWorld.DistributedInstanceWorld.addWorldInterest(self, area)
        if area:
            area.turnOn(localAvatar)

    def removeWorldInterest(self, area=None):
        if not (area and area.gridVisContext):
            area = None
        DistributedInstanceWorld.DistributedInstanceWorld.removeWorldInterest(self, area)
        return