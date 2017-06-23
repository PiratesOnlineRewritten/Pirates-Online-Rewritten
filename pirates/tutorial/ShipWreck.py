from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.actor import Actor
from pandac.PandaModules import *
from pirates.piratesbase.PiratesGlobals import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.SmokeCloud import SmokeCloud
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.Fire import Fire
from pirates.effects.BlackSmoke import BlackSmoke
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle import CannonGlobals
from pirates.battle import WeaponGlobals
from pirates.shipparts import ShipPart

class ShipWreck(NodePath):
    notify = directNotify.newCategory('ShipWreck')

    def __init__(self, npShipWreck, uid):
        NodePath.__init__(self, npShipWreck)
        self.tutorial = None
        self.hitCount = 0
        self.uid = uid
        self.coll = self.findAllMatches('**/+CollisionNode')
        self.__targetableCollisions = []
        return

    def delete(self):
        self.hitCount = 0
        self.clearTargetableCollisions()

    def makeTargetableCollision(self, doId):
        for i in range(0, self.coll.getNumPaths()):
            c = self.coll[i]
            c.setTag('objType', str(PiratesGlobals.COLL_SHIP_WRECK))
            c.setTag('propId', str(doId))
            self.addTargetableCollision(c)

        self.setTargetBitmask(True)

    def addTargetableCollision(self, coll):
        self.__targetableCollisions.append(coll)

    def getTargetableCollisions(self):
        return self.__targetableCollisions

    def clearTargetableCollisions(self):
        self.__targetableCollisions = []

    def setTargetBitmask(self, on):
        if on:
            for coll in self.__targetableCollisions:
                curMask = coll.node().getIntoCollideMask()
                newMask = curMask | PiratesGlobals.TargetBitmask
                coll.setCollideMask(newMask)

        else:
            for coll in self.__targetableCollisions:
                curMask = coll.node().getIntoCollideMask()
                newMask = curMask ^ PiratesGlobals.TargetBitmask
                coll.setCollideMask(newMask)

    def projectileWeaponHit(self, pos):
        if self.tutorial:
            self.tutorial.cannonHitWreck(self)
        if base.cr.wantSpecialEffects:
            explosionEffect = ExplosionFlip.getEffect()
            if explosionEffect:
                explosionEffect.reparentTo(render)
                explosionEffect.setPos(self, pos)
                explosionEffect.setScale(0.8)
                explosionEffect.play()
            smokeCloudEffect = SmokeCloud.getEffect()
            if smokeCloudEffect:
                smokeCloudEffect.reparentTo(render)
                smokeCloudEffect.setPos(self, pos)
                smokeCloudEffect.setScale(1.0)
                smokeCloudEffect.spriteScale = 1.0
                smokeCloudEffect.radius = 7.0
                smokeCloudEffect.play()
            shipSplintersAEffect = ShipSplintersA.getEffect()
            if shipSplintersAEffect:
                shipSplintersAEffect.reparentTo(render)
                shipSplintersAEffect.setPos(self, pos)
                shipSplintersAEffect.play()