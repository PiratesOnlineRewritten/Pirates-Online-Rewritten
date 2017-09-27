from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI

class DistributedDinghyAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedDinghyAI')
    MULTIUSE = True

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)

        self.interactRadius = 0
        self.locationId = 0
        self.siegeTeam = 0

    def handleRequestInteraction(self, avatar, interactType, instant):
        return self.ACCEPT

    def handleRequestExit(self, avatar):
        return self.ACCEPT

    def setInteractRadius(self, interactRadius):
        self.interactRadius = interactRadius

    def d_setInteractRadius(self, interactRadius):
        self.sendUpdate('setInteractRadius', [interactRadius])

    def b_setInteractRadius(self, interactRadius):
        self.setInteractRadius(interactRadius)
        self.d_setInteractRadius(interactRadius)

    def getInteractRadius(self):
        return self.interactRadius

    def setLocationId(self, locationId):
        self.locationId = locationId

    def d_setLocationId(self, locationId):
        self.sendUpdate('setLocationId', [locationId])

    def b_setLocationId(self, locationId):
        self.setLocationId(locationId)
        self.d_setLocationId(locationId)

    def getLocationId(self):
        return self.locationId

    def setSiegeTeam(self, siegeTeam):
        self.siegeTeam = siegeTeam

    def d_setSiegeTeam(self, siegeTeam):
        self.sendUpdate('setSiegeTeam', [siegeTeam])

    def b_setSiegeTeam(self, siegeTeam):
        self.setSiegeTeam(siegeTeam)
        self.d_setSiegeTeam(siegeTeam)

    def getSiegeTeam(self):
        return self.siegeTeam
