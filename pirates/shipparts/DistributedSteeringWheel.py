from pandac.PandaModules import *
from pirates.distributed import DistributedInteractive
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.shipparts import DistributedShippart
from pirates.shipparts import Wheel
from pirates.ship import ShipGlobals
from pirates.piratesgui import PiratesGuiGlobals
from direct.showbase.PythonUtil import report, quickProfile

class DistributedSteeringWheel(DistributedInteractive.DistributedInteractive, DistributedShippart.DistributedShippart):
    notify = directNotify.newCategory('DistributedSteeringWheel')

    def __init__(self, cr):
        NodePath.__init__(self, 'steeringWheel')
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        DistributedShippart.DistributedShippart.__init__(self, cr)
        self.ship = None
        return

    def generate(self):
        DistributedInteractive.DistributedInteractive.generate(self)
        DistributedShippart.DistributedShippart.generate(self)

    def announceGenerate(self):
        DistributedInteractive.DistributedInteractive.announceGenerate(self)
        DistributedShippart.DistributedShippart.announceGenerate(self)
        if not self.cr.tutorial:
            self.setInteractOptions(proximityText=PLocalizer.InteractWheel, sphereScale=6)
        if self.proximityCollisionNodePath:
            self.proximityCollisionNodePath.reparentTo(self.ship.getModelCollisionRoot())
            trans = self.ship.getLocatorTransform('location_wheel')
            if trans:
                trans = trans.setScale(6)
                self.proximityCollisionNodePath.setTransform(trans)
        self.ship.wheel = [None, self]
        self.setAllowInteract(1)
        self.checkInUse()
        return

    def load(self):
        pass

    def disable(self):
        self.notify.debug('Disable ' + str(self.doId))
        DistributedInteractive.DistributedInteractive.disable(self)
        DistributedShippart.DistributedShippart.disable(self)

    def delete(self):
        self.notify.debug('Delete ' + str(self.doId))
        if self.ship:
            if self.ship.steeringAvId == base.localAvatar.doId:
                self.ship.clientSteeringEnd()
            self.ship.wheel = [
             None, None]
        self.ship = None
        DistributedInteractive.DistributedInteractive.delete(self)
        DistributedShippart.DistributedShippart.delete(self)
        return

    def requestInteraction(self, avId, interactType=0):
        av = base.cr.doId2do.get(avId)
        if self.isInteractionAllowed(av):
            base.localAvatar.motionFSM.off()
            DistributedInteractive.DistributedInteractive.requestInteraction(self, avId, interactType)

    def isInteractionAllowed(self, av):
        return self.ship.canTakeWheel(self, av)

    def rejectInteraction(self):
        base.localAvatar.motionFSM.on()
        DistributedInteractive.DistributedInteractive.rejectInteraction(self)

    def requestExit(self):
        DistributedInteractive.DistributedInteractive.requestExit(self)
        if base.localAvatar:
            if base.localAvatar.ship:
                base.localAvatar.ship.clientSteeringEnd()

    def enterWaiting(self):
        DistributedInteractive.DistributedInteractive.enterWaiting(self)
        self.accept('shipSinking-' + str(self.shipId), self.shipSinking)

    def exitWaiting(self):
        DistributedInteractive.DistributedInteractive.exitWaiting(self)
        self.ignore('shipSinking-' + str(self.shipId))

    def enterUse(self):
        DistributedInteractive.DistributedInteractive.enterUse(self)
        av = base.cr.doId2do.get(self.ship.steeringAvId)
        av.stopCompassEffect()
        self.accept('shipSinking-' + str(self.shipId), self.shipSinking)

    def exitUse(self):
        DistributedInteractive.DistributedInteractive.exitUse(self)
        av = base.cr.doId2do.get(self.ship.steeringAvId)
        av.startCompassEffect()
        self.ignore('shipSinking-' + str(self.shipId))

    def shipSinking(self):
        self.notify.debug('[DistributedSteeringWheel] shipSinking %s' % self.ship.doId)
        self.requestExit()

    def loadTargetIndicator(self):
        if self.isGenerated():
            self.disk = loader.loadModel('models/effects/selectionCursor')
            trans = self.ship.getLocatorTransform('location_wheel')
            if trans:
                self.disk.setTransform(trans)
            self.disk.setScale(self.diskRadius)
            self.disk.setColorScale(0, 1, 0, 1)
            self.disk.setP(self.disk, -90)
            self.disk.setZ(self.disk, 0.025)
            self.disk.setBillboardAxis(6)
            self.disk.reparentTo(self.ship.getModelRoot())
            self.disk.setBin('shadow', 0)
            self.disk.setTransparency(TransparencyAttrib.MAlpha)
            self.disk.setDepthWrite(0)

    def setUserId(self, avId):
        DistributedInteractive.DistributedInteractive.setUserId(self, avId)
        self.ship.setWheelInUse(self.userId != 0)
        self.checkInUse()

    def checkInUse(self):
        if self.userId and base.localAvatar.getDoId() != self.ship.ownerId and localAvatar.getDoId() != self.userId:
            self.setAllowInteract(0)
        elif self.userId and base.localAvatar.getDoId() == self.ship.ownerId:
            self.proximityText = PLocalizer.InteractWheelCaptain
            self.setAllowInteract(1)
        else:
            self.proximityText = PLocalizer.InteractWheel
            self.setAllowInteract(1)

    def setAllowInteract(self, allow, forceOff=False):
        DistributedInteractive.DistributedInteractive.setAllowInteract(self, allow)
        if not allow and forceOff:
            if self.ship.steeringAvId == base.localAvatar.doId:
                self.requestExit()