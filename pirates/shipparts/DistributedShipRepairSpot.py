from pandac.PandaModules import NodePath, ModelNode
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.fsm.StatePush import FunctionCall, StateVar
from pirates.distributed.DistributedInteractive import DistributedInteractive
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.pvp import PVPGlobals

class DistributedShipRepairSpot(DistributedInteractive):
    notify = directNotify.newCategory('DistributedShipRepairSpot')

    def __init__(self, cr):
        DistributedInteractive.__init__(self, cr)

    def setShipId(self, shipId):
        self._shipId = shipId

    def setIndex(self, index):
        self._index = index

    def announceGenerate(self):
        DistributedInteractive.announceGenerate(self)
        ship = self.cr.doId2do[self._shipId]
        NodePath.__init__(self, 'ship-%s-repairSpot-%s' % (ship.doId, self._index))
        ship.repairSpots[self.doId] = self
        root = ModelNode('ship-%s-repairSpot-%s' % (ship.doId, self._index))
        root.setPreserveTransform(1)
        self.assign(NodePath(root))
        locName = PVPGlobals.RepairSpotLocatorNames[self._index]
        locator = ship.findLocator('**/%s;+s' % locName)
        self.setPos(locator.getPos(ship.getModelRoot()))
        self.setHpr(locator.getHpr(ship.getModelRoot()))
        self.setScale(locator.getScale(ship.getModelRoot()))
        self.reparentTo(ship.getModelRoot())
        self.setInteractOptions(proximityText=PLocalizer.InteractRepairSpot, diskRadius=10.0, sphereScale=6.0)
        self.setAllowInteract(1)
        self.checkInUse()
        self._statePushes = DestructiveScratchPad(evalUsable=FunctionCall(self._evalUsableState, ship._repairSpotMgr._state.fullHealth, ship.getWheelInUseSV()).pushCurrentState())

    def disable(self):
        self._statePushes.destroy()
        self._statePushes = None
        if self.userId == localAvatar.doId:
            self.stopRepairing()
        DistributedInteractive.disable(self)
        self.detachNode()
        return

    def _evalUsableState(self, fullShipHealth, steeringWheelInUse):
        if not fullShipHealth:
            self.setInteractOptions(proximityText=PLocalizer.InteractRepairSpot, resetState=0)
            self.setAllowInteract(1)
        else:
            self.setInteractOptions(proximityText='', resetState=0)
            self.setAllowInteract(0)

    def requestInteraction(self, avId, interactType=0):
        DistributedInteractive.requestInteraction(self, avId, interactType)

    def rejectInteraction(self):
        if self.userId != localAvatar.doId:
            localAvatar.motionFSM.on()
        DistributedInteractive.rejectInteraction(self)

    def kickInteraction(self):
        if self.userId == localAvatar.doId:
            localAvatar.guiMgr.createWarning(PLocalizer.Minigame_Repair_KickedFromRepairSpotWarning)
            localAvatar.motionFSM.on()
        DistributedInteractive.rejectInteraction(self)

    def startRepairing(self):
        localAvatar.b_setGameState('ShipRepair')

    def stopRepairing(self):
        if self.userId == localAvatar.doId and localAvatar.getGameState() == 'ShipRepair':
            localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)
            base.localAvatar.motionFSM.on()

    def requestExit(self):
        DistributedInteractive.requestExit(self)
        self.stopRepairing()

    def enterWaiting(self):
        DistributedInteractive.enterWaiting(self)
        localAvatar.motionFSM.off()
        self.accept('shipSinking-' + str(self._shipId), self.shipSinking)

    def exitWaiting(self):
        DistributedInteractive.exitWaiting(self)
        self.ignore('shipSinking-' + str(self._shipId))

    def enterUse(self):
        DistributedInteractive.enterUse(self)
        self.accept('shipSinking-' + str(self._shipId), self.shipSinking)
        self.startRepairing()

    def exitUse(self):
        self.stopRepairing()
        DistributedInteractive.exitUse(self)
        self.ignore('shipSinking-' + str(self._shipId))

    def shipSinking(self):
        self.notify.debug('shipSinking %s' % self._shipId)
        self.requestExit()

    def setUserId(self, avId):
        oldId = self.userId
        DistributedInteractive.setUserId(self, avId)
        if oldId != avId:
            self.checkInUse()

    def checkInUse(self):
        if self.userId and localAvatar.getDoId() != self.userId:
            self.setAllowInteract(0)
        else:
            self.setAllowInteract(1)

    def handleArrivedOnShip(self, ship):
        pass

    def handleLeftShip(self, ship):
        pass

    def setAllowInteract(self, allow, forceOff=False):
        DistributedInteractive.setAllowInteract(self, allow)
        if not allow and forceOff and localAvatar.getDoId() == self.userId:
            self.requestExit()