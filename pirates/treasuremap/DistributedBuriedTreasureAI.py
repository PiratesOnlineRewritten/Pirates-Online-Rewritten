from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI

class DistributedBuriedTreasureAI(DistributedInteractiveAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBuriedTreasureAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        self.currentDepth = 0
        self.visZone = ''

    def setStartingDepth(self, depth):
        self.startingDepth = depth

    def d_setStartingDepth(self, depth):
        self.sendUpdate('setStartingDepth', [depth])

    def b_setStartingDepth(self, depth):
        self.setStartingDepth(depth)
        self.d_setStartingDepth(depth)

    def getStartingDepth(self):
        return self.startingDepth

    def setCurrentDepth(self, depth):
        self.currentDepth = depth

    def d_setCurrentDepth(self, depth):
        self.sendUpdate('setCurrentDepth', [depth])

    def b_setCurrentDepth(self, depth):
        self.setCurrentDepth(depth)
        self.d_setCurrentDepth(depth)

    def getCurrentDepth(self):
        return self.currentDepth

    def setVisZone(self, visZone):
        self.visZone = visZone

    def d_setVisZone(self, visZone):
        self.sendUpdate('setVisZone', [visZone])

    def b_setVisZone(self, visZone):
        self.setVisZone(visZone)
        self.d_setVisZone(visZone)

    def getVisZone(self):
        return self.visZone

    def d_startDigging(self):
        self.sendUpdate('startDigging', [])

    def d_stopDigging(self, questProgress):
        self.sendUpdate('stopDigging', [questProgress])