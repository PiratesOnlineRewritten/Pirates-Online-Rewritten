from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from direct.distributed import DistributedObject
from pirates.effects.DustRing import DustRing
from pirates.effects.SmallSplash import SmallSplash
import random
from PooledEffect import PooledEffect
DebrisDict = {'0': 'models/props/testBoard','1': 'models/props/testBoard'}

class ShipDebris(PooledEffect):

    def __init__(self):
        PooledEffect.__init__(self)
        self.collSphereRadius = 2.0
        self.startPos = Vec3(0, 0, 0)
        self.startVel = Vec3(random.uniform(-25, 25), random.uniform(20, 140), random.uniform(10, 120))
        self.endPlaneZ = -10
        self.transNode = self.attachNewNode('trans')
        filePrefix = DebrisDict.get(str(random.randint(0, 1)))
        self.debris = loader.loadModel(filePrefix)
        self.debris.reparentTo(self.transNode)
        self.weaponHitEvent = 'weaponHit' + str(id(self))
        self.accept(self.weaponHitEvent, self.weaponHitObject)
        self.collSphere = CollisionSphere(0, 0, 0, self.collSphereRadius)
        self.cnode = CollisionNode('collSphere')
        self.cnode.addSolid(self.collSphere)
        self.collision = self.transNode.attachNewNode(self.cnode)
        self.cnode.setFromCollideMask(PiratesGlobals.TargetBitmask)
        self.cnode.setIntoCollideMask(BitMask32.allOff())
        self.collHandler = CollisionHandlerEvent()
        self.collHandler.addInPattern(self.weaponHitEvent)
        self.createTrack()

    def createTrack(self, rate=1):
        playProjectile = ProjectileInterval(self.transNode, startPos=self.startPos, startVel=self.startVel, endZ=self.endPlaneZ, gravityMult=4.0)
        randomNumX = random.uniform(360, 2880)
        randomNumY = random.uniform(360, 2880)
        randomNumZ = random.uniform(360, 2880)
        self.playRotate = self.debris.hprInterval(6, Point3(randomNumX, randomNumY, randomNumZ))
        enableColl = Sequence(Wait(0.2), Func(self.cnode.setFromCollideMask, PiratesGlobals.TargetBitmask))
        playDebris = Parallel(playProjectile, enableColl)
        self.track = Sequence(Func(self.transNode.reparentTo, self), playDebris, Func(self.cleanUpEffect))

    def play(self, rate=1):
        if self.startPos[2] > self.endPlaneZ:
            base.cTrav.addCollider(self.collision, self.collHandler)
            self.track.start()
            self.playRotate.loop()
        else:
            self.finish()

    def stop(self):
        if self.track:
            self.track.finish()
        if self.playRotate:
            self.playRotate.finish()

    def finish(self):
        self.stop()
        self.cleanUpEffect()

    def cleanUpEffect(self):
        if base.cTrav:
            base.cTrav.removeCollider(self.collision)
        self.detachNode()
        self.checkInEffect(self)

    def destroy(self):
        self.stop()
        del self.track
        self.removeNode()
        self.ignore(self.weaponHitEvent)
        PooledEffect.destroy(self)

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