from otp.otpbase import OTPGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.effects.Bonfire import Bonfire
import DistributedPCCannon

class DistributedIslandCannon(DistributedPCCannon.DistributedPCCannon):
    notify = directNotify.newCategory('DistributedIslandCannon')

    def __init__(self, cr):
        DistributedPCCannon.DistributedPCCannon.__init__(self, cr)
        self.pendingPlacement = None
        self.bf = None
        self.destructState = None
        self.island = None
        return

    def announceGenerate(self):
        DistributedPCCannon.DistributedPCCannon.announceGenerate(self)
        self.addDestructableCollision()

    def cleanupProp(self):
        if self.prop:
            self.prop.delete()
            self.prop = None
        return

    def disable(self):
        DistributedPCCannon.DistributedPCCannon.disable(self)
        if self.pendingPlacement:
            base.cr.relatedObjectMgr.abortRequest(self.pendingPlacement)
            self.pendingPlacement = None
        self.island = None
        return

    def setIslandId(self, islandId):
        self.islandId = islandId

        def putCannonOnIsland(island, self=self):
            self.notify.debug('putCannon %s on island %s' % (self.doId, islandId))
            self.island = island
            self.island.builder.attachCannon(self)
            self.accept(island.uniqueName('disable'), self.islandDisable)
            self.cannonExitEvent = island.uniqueName('stopCannon')
            self.pendingPlacement = None
            return

        if islandId > 0:
            self.pendingPlacement = base.cr.relatedObjectMgr.requestObjects([self.islandId], eachCallback=putCannonOnIsland)

    def setCannonIndex(self, cannonIndex):
        self.cannonIndex = cannonIndex

    def setIsDestructable(self, isDestructable):
        self.__isDestructable = isDestructable

    def setDestructState(self, state):
        if state != self.destructState:
            self.destructState = state
            if self.destructState == PiratesGlobals.CANNON_STATE_DESTRUCT:
                self.request('Off')
                bf = Bonfire(self)
                bf.reparentTo(self)
                bf.startLoop()
                self.bf = bf
            else:
                self.request('Idle')
                if self.bf:
                    self.bf.removeNode()
                    self.bf = None
        return

    def addDestructableCollision(self):
        if self.__isDestructable:
            self.prop.propCollisions.node().setIntoCollideMask(OTPGlobals.WallBitmask | PiratesGlobals.TargetBitmask)
            self.prop.propCollisions.setTag('objType', str(PiratesGlobals.COLL_CANNON))
            self.prop.propCollisions.setTag('cannonId', str(self.doId))
        self.prop.propCollisions.reparentTo(self)

    def islandDisable(self):
        if self.localAvatarUsingWeapon:
            self.stopWeapon(base.localAvatar)

    def sendHitByProjectile(self):
        if self.__isDestructable:
            self.sendUpdate('hitByProjectile')