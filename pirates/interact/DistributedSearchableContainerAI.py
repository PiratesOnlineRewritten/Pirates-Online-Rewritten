from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from direct.directnotify import DirectNotifyGlobal

class DistributedSearchableContainerAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSearchableContainerAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.color = [1.0, 1.0, 1.0, 1.0]

    def handleRequestInteraction(self, avatar, interactType, instance):
        return self.DENY

    def setSearchTime(self, searchTime):
        self.searchTime = searchTime

    def d_setSearchTime(self, searchTime):
        self.sendUpdate('setSearchTime', [searchTime])

    def b_setSearchTime(self, searchTime):
        self.setSearchTime(searchTime)
        self.d_setSearchTime(searchTime)

    def getSearchTime(self):
        return self.searchTime

    def setType(self, searchType):
        self.type = searchType

    def d_setType(self, searchType):
        self.sendUpdate('setType', [searchType])

    def b_setType(self, searchType):
        self.setType(searchType)
        self.d_setType(searchType)

    def getType(self):
        return self.type

    def setContainerColor(self, color):
        self.color = color

    def d_setContainerColor(self, color):
        self.sendUpdate('setContainerColor', color)

    def b_setContainerColor(self, color):
        self.setContainerColor(color)
        self.d_setContainerColor(color)

    def getContainerColor(self):
        return self.color

    def setSphereScale(self, sphereScale):
        self.sphereScale = sphereScale

    def d_setSphereScale(self, sphereScale):
        self.sendUpdate('setSphereScale', [sphereScale])

    def b_setSphereScale(self, sphereScale):
        self.setSphereScale(sphereScale)
        self.d_setSphereScale(sphereScale)

    def getSphereScale(self):
        return self.sphereScale

    def setVisZone(self, visZone):
        self.visZone = visZone

    def d_setVisZone(self, visZone):
        self.sendUpdate('setVisZone', [visZone])

    def b_setVisZone(self, visZone):
        self.setVisZone(visZone)
        self.d_setVisZone(visZone)

    def getVisZone(self):
        return self.visZone

    def getVisZone(self):
        return self.visZone