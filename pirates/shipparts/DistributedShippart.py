from direct.distributed.ClockDelta import *
from direct.distributed import DistributedNode
from direct.interval.IntervalGlobal import *
from pirates.piratesbase.PiratesGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer

class DistributedShippart(DistributedNode.DistributedNode):
    notify = directNotify.newCategory('DistributedShippart')

    def __init__(self, cr):
        DistributedNode.DistributedNode.__init__(self, cr)
        self.dna = None
        self.prop = None
        self.hasHpMeter = 0
        self.level = 0
        self.classType = 0
        self.lastZoneLevel = 0
        self.ship = None
        self.geomParent = None
        self.flash = None
        self.sentReadyMessage = 0
        self.pendingLinkToParent = None
        self.pendingLinkToShip = None
        self.instHigh = None
        self.instMed = None
        self.instLow = None
        self.instFlat = None
        self.instColl = None
        return

    def generate(self):
        DistributedNode.DistributedNode.generate(self)

    def announceGenerate(self):
        DistributedNode.DistributedNode.announceGenerate(self)
        self.ship = self.cr.doId2do[self.shipId]
        self.load()

    def disable(self):
        self.unload()
        DistributedNode.DistributedNode.disable(self)

    def delete(self):
        if self.prop:
            self.prop = None
        self.ship = None
        DistributedNode.DistributedNode.delete(self)
        return

    def load(self):
        self.createProp()
        if not self.prop.loaded:
            self.prop.ship = self.ship
            self.loadModel()
            self.addPropToShip()
            self.propLoaded()

    def propLoaded(self):
        pass

    def createProp(self):
        pass

    def unload(self):
        if self.prop:
            self.prop = None
        return

    def loadModel(self):
        self.prop.loadModel(self.dna)
        self.prop.loadHigh()
        self.prop.loadMedium()
        self.prop.loadLow()

    def unloadModel(self):
        self.prop.unloadModel()

    def getLevel(self):
        if self.ship:
            return self.ship.getLevel()
        else:
            return 1

    def addPropToShip(self):
        self.prop.addToShip()

    def isReady(self):
        return self.sentReadyMessage

    def sendReadyMessage(self):
        if not self.sentReadyMessage:
            self.sentReadyMessage = 1
            messenger.send('shippartReady-%s' % self.doId, [self])

    def setGeomParentId(self, geomParentId):
        self.geomParentId = geomParentId

    def getGeomParentId(self):
        return self.geomParentId

    def setShipId(self, shipId):
        self.shipId = shipId

    def getShipId(self):
        return self.shipId

    def setClassType(self, val):
        self.classType = val

    def setLevel(self, val):
        self.level = val

    def getTeam(self):
        return self.ship.getTeam()

    def getPVPTeam(self):
        return self.ship.getPVPTeam()

    def handleArrivedOnShip(self, ship):
        pass

    def handleLeftShip(self, ship):
        pass

    def getSkillRankBonus(self, skillId):
        return 0

    def getSkillRank(self, skillId):
        return 0