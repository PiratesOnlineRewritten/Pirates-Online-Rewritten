from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from pirates.distributed import DistributedInteractive
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.interact import InteractiveBase

class DistributedSurfaceTreasure(DistributedInteractive.DistributedInteractive):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSurfaceTreasure')

    def __init__(self, cr):
        NodePath.__init__(self, 'DistributedSurfaceTreasure')
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        self.showLerp = None
        self.visZone = ''
        return

    def generate(self):
        DistributedInteractive.DistributedInteractive.generate(self)
        self.chest = loader.loadModel('models/props/treasureChest')
        self.chest.reparentTo(self)
        self.chest.setScale(0.6)
        self.chestLid = self.chest.find('**/top')
        self.initInteractOpts()
        self.belongsToTeam = PiratesGlobals.INVALID_TEAM
        self.value = 0

    def announceGenerate(self):
        DistributedInteractive.DistributedInteractive.generate(self)
        self.getParentObj().builder.addSectionObj(self, self.visZone)

    def initInteractOpts(self):
        self.setInteractOptions(sphereScale=10, diskRadius=10, proximityText=PLocalizer.PVPPickUpTreasure, exclusive=0)

    def disable(self):
        DistributedInteractive.DistributedInteractive.disable(self)
        self.getParentObj().builder.removeSectionObj(self, self.visZone)
        self.chest.removeNode()
        del self.chest
        del self.chestLid
        if self.showLerp:
            self.showLerp.pause()

    def setLocation(self, parentId, zoneId):
        DistributedInteractive.DistributedInteractive.setLocation(self, parentId, zoneId)
        if zoneId == PiratesGlobals.ShipZoneOnDeck:
            ship = base.cr.doId2do[parentId]
            self.reparentTo(ship.transNode)

    def handleEnterProximity(self, collEntry):
        DistributedInteractive.DistributedInteractive.handleEnterProximity(self, collEntry)
        print 'enterproximityoftreasure'

    def enterProximity(self):
        if (self.belongsToTeam == PiratesGlobals.INVALID_TEAM or self.belongsToTeam != localAvatar.getTeam()) and self.value > 0:
            base.cr.interactionMgr.addInteractive(self, InteractiveBase.PROXIMITY)
            messenger.send('enterProximityOfInteractive')
        else:
            base.cr.interactionMgr.removeInteractive(self, InteractiveBase.PROXIMITY)
        self.accept(self.proximityCollisionExitEvent, self.handleExitProximity)

    def setWithdrawType(self, withdrawType):
        self.withdrawType = withdrawType

    def setOpen(self, open):
        if open:
            self.chestLid.setHpr(0, -40, 0)
        else:
            self.chestLid.setHpr(0, 0, 0)

    def showProximityInfo(self):
        self.cr.activeWorld.updateTreasureProximityText(self)
        DistributedInteractive.DistributedInteractive.showProximityInfo(self)

    def startLooting(self, lootType):
        self.acceptInteraction()
        print 'st: start looting'
        if lootType == PiratesGlobals.WITHDRAW_INCREMENTAL:
            base.localAvatar.b_setGameState('Stealing')

    def stopLooting(self):
        print 'st: stop looting'
        self.rejectInteraction()
        if base.localAvatar.lootCarried > 0:
            base.localAvatar.b_setGameState('LandTreasureRoam')
        else:
            base.localAvatar.b_setGameState(base.localAvatar.gameFSM.defaultState)

    def setBelongsToTeam(self, team):
        self.belongsToTeam = team

    def setValue(self, value):
        self.value = value

    def requestInteraction(self, avId, interactType=0):
        base.localAvatar.motionFSM.off()
        DistributedInteractive.DistributedInteractive.requestInteraction(self, avId, interactType)

    def rejectInteraction(self):
        base.localAvatar.motionFSM.on()
        DistributedInteractive.DistributedInteractive.rejectInteraction(self)

    def setEmpty(self, empty):
        if self.showLerp:
            self.showLerp.finish()
        if empty:
            self.showLerp = Sequence(Func(self.setTransparency, 1), LerpColorScaleInterval(self, 0.5, Vec4(1, 1, 1, 0)))
            self.showLerp.start()
        else:
            self.showLerp = Sequence(LerpColorScaleInterval(self, 0.5, Vec4(1, 1, 1, 1)), Func(self.clearTransparency))
            self.showLerp.start()

    def setVisZone(self, zone):
        self.visZone = zone

    def getVisZone(self):
        return self.visZone