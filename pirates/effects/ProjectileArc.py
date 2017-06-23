from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from pirates.piratesbase import PiratesGlobals
from pirates.effects.DustRing import DustRing
from pirates.effects.SmallSplash import SmallSplash
from pirates.effects.CannonSplash import CannonSplash
import random

class ProjectileArc(DirectObject, NodePath):

    def __init__(self, wantRotate=1, wantColl=0):
        NodePath.__init__(self, 'projectileArcRenderParent')
        self.wantRotate = wantRotate
        self.wantColl = wantColl
        self.collSphereRadius = 3.0
        self.startPos = Vec3(0, 0, 0)
        self.startVel = Vec3(random.uniform(-20, 20), random.uniform(20, 60), random.uniform(10, 110))
        self.endPlaneZ = -100
        self.gravityMult = 2.0
        self.rotateMin = 360
        self.rotateMax = 2880
        self.track = None
        self.bigSplash = 0
        self.transNode = self.attachNewNode('trans')
        self.rotateNode = self.transNode.attachNewNode('rotate')
        self.arcHitEvent = 'projectileArcHit' + str(id(self))
        if self.wantColl:
            self.accept(self.arcHitEvent, self.weaponHitObject)
            self.collSphere = CollisionSphere(0, 0, 0, self.collSphereRadius)
            self.cnode = CollisionNode('collSphere')
            self.cnode.addSolid(self.collSphere)
            self.collision = self.transNode.attachNewNode(self.cnode)
            self.cnode.setFromCollideMask(PiratesGlobals.TargetBitmask)
            self.cnode.setIntoCollideMask(BitMask32.allOff())
            self.collHandler = CollisionHandlerEvent()
            self.collHandler.addInPattern(self.arcHitEvent)
        if self.wantRotate:
            randomNumX = random.uniform(self.rotateMin, self.rotateMax)
            randomNumY = random.uniform(self.rotateMin, self.rotateMax)
            randomNumZ = 0
            self.playRotate = self.rotateNode.hprInterval(6, Point3(randomNumX, randomNumY, randomNumZ))
        return

    def createTrack(self, rate=1):
        if self.wantColl:
            enableColl = Sequence(Wait(0.2), Func(self.cnode.setFromCollideMask, PiratesGlobals.TargetBitmask))
        self.playProjectile = ProjectileInterval(self.transNode, startPos=self.startPos, startVel=self.startVel, endZ=self.endPlaneZ, gravityMult=self.gravityMult)
        if self.wantColl:
            playDebris = Parallel(self.playProjectile, enableColl)
        else:
            playDebris = self.playProjectile
        self.track = Sequence(playDebris, Func(self.destroy))

    def play(self, rate=1):
        if self.startPos[2] > self.endPlaneZ:
            self.startCollisions()
            self.createTrack()
            self.track.start()
            if self.wantRotate:
                self.playRotate.loop()
        else:
            self.destroy()

    def startCollisions(self):
        if self.wantColl and base.cTrav != 0:
            base.cTrav.addCollider(self.collision, self.collHandler)
            self.cnode.setFromCollideMask(PiratesGlobals.TargetBitmask)

    def stop(self):
        if self.track != None:
            self.track.finish()
        if self.wantRotate:
            self.playRotate.finish()
        self.ignore(self.arcHitEvent)
        if self.wantColl and base.cTrav != 0:
            base.cTrav.removeCollider(self.collision)
        return

    def finish(self):
        self.stop()
        self.cleanUpEffect()

    def cleanUpEffect(self):
        self.detachNode()

    def destroy(self):
        self.ignore(self.arcHitEvent)
        self.stop()
        del self.track
        if self.wantColl and base.cTrav != 0:
            base.cTrav.removeCollider(self.collision)
        if self.wantRotate:
            del self.playRotate
        self.transNode.removeNode()
        del self.transNode
        self.removeNode()
        del self

    def weaponHitObject(self, entry):
        if not entry.hasSurfacePoint() or not entry.hasInto():
            return
        if not entry.getInto().isTangible():
            return
        hitObject = entry.getIntoNodePath()
        objType = hitObject.getNetTag('objType')
        if not objType:
            return
        objType = int(objType)
        if objType == PiratesGlobals.COLL_SEA and base.cr.wantSpecialEffects:
            pos = entry.getSurfacePoint(render)
            if base.cr.activeWorld and base.cr.activeWorld.getWater():
                entryWaterHeight = base.cr.activeWorld.getWater().calcHeight(pos[0], pos[1]) + 7.0
            else:
                entryWaterHeight = pos[2]
            if self.bigSplash:
                splashEffect = CannonSplash.getEffect()
                if splashEffect:
                    splashEffect.reparentTo(render)
                    splashEffect.setPos(pos[0], pos[1], entryWaterHeight)
                    splashEffect.play()
            else:
                splashEffect = SmallSplash.getEffect()
                if splashEffect:
                    splashEffect.reparentTo(render)
                    splashEffect.setPos(pos[0], pos[1], entryWaterHeight)
                    splashEffect.play()
            self.cnode.setFromCollideMask(PiratesGlobals.TargetBitmask.allOff())
        elif objType == PiratesGlobals.COLL_LAND and base.cr.wantSpecialEffects:
            pos = entry.getSurfacePoint(render)
            dustRingEffect = DustRing.getEffect()
            if dustRingEffect:
                dustRingEffect.reparentTo(render)
                dustRingEffect.setPos(pos)
                dustRingEffect.play()
            self.cnode.setFromCollideMask(PiratesGlobals.TargetBitmask.allOff())