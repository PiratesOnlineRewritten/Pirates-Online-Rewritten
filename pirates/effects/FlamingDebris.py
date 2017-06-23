from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from direct.distributed import DistributedObject
from pirates.effects.SmallSplash import SmallSplash
from pirates.effects.SmokeTrail import SmokeTrail
from pirates.effects.FlameTrail import FlameTrail
from pirates.effects.DustCloud import DustCloud
import random
from PooledEffect import PooledEffect
DebrisDict = {'0': 'models/props/rock_1_floor','1': 'models/props/rock_2_floor','2': 'models/props/rock_3_floor','3': 'models/props/rock_4_floor'}

class FlamingDebris(PooledEffect):

    def __init__(self):
        PooledEffect.__init__(self)
        self.collSphereRadius = 2.0
        self.startPos = Vec3(0, 0, 0)
        self.transNode = self.attachNewNode('trans')
        self.track = None
        self.playRotate = None
        filePrefix = DebrisDict.get(str(random.randint(0, 3)))
        self.debris = loader.loadModel(filePrefix)
        self.debris.reparentTo(self.transNode)
        self.debris.setScale(0.5)
        self.debris.setColorScale(0.8, 0.8, 0.8, 1.0)
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
        self.radiusDist = 50
        self.minHeight = 100
        self.maxHeight = 140
        self.velocityX = 0
        self.velocityY = 0
        return

    def createTrack(self, rate=1):
        if self.velocityX or self.velocityY:
            self.startVel = Vec3(self.velocityX + random.uniform(-10.0, 10.0), self.velocityY + random.uniform(-10.0, 10.0), random.uniform(self.minHeight, self.maxHeight))
        else:
            self.startVel = Vec3(random.uniform(-self.radiusDist, self.radiusDist), random.uniform(-self.radiusDist, self.radiusDist), random.uniform(self.minHeight, self.maxHeight))
        self.velocityX = 0
        self.velocityY = 0
        playProjectile = ProjectileInterval(self.transNode, startPos=self.startPos, startVel=self.startVel, duration=4, gravityMult=4.0)
        randomNumX = random.uniform(360, 2880)
        randomNumY = random.uniform(360, 2880)
        randomNumZ = random.uniform(360, 2880)
        self.playRotate = self.debris.hprInterval(6, Point3(randomNumX, randomNumY, randomNumZ))
        enableColl = Sequence(Wait(0.2), Func(self.cnode.setFromCollideMask, PiratesGlobals.TargetBitmask))
        playDebris = Parallel(playProjectile, enableColl)

        def startTrail():
            self.trailEffect = FlameTrail.getEffect()
            if self.trailEffect:
                self.trailEffect.reparentTo(self.transNode)
                self.trailEffect.play()

        self.track = Sequence(Func(startTrail), Func(self.transNode.reparentTo, self), playDebris, Func(self.cleanUpEffect))

    def play(self, rate=1):
        self.createTrack()
        base.cTrav.addCollider(self.collision, self.collHandler)
        self.track.start()
        self.playRotate.loop()

    def stop(self):
        if self.track:
            self.track.pause()
            self.track = None
        if self.playRotate:
            self.playRotate.pause()
            self.playRotate = None
        return

    def finish(self):
        self.stop()
        self.cleanUpEffect()

    def cleanUpEffect(self):
        self.detachNode()
        self.checkInEffect(self)

    def destroy(self):
        self.stop()
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
            if base.cr.activeWorld.getWater():
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
            dustCloudEffect = DustCloud.getEffect()
            if dustCloudEffect:
                dustCloudEffect.wrtReparentTo(render)
                dustCloudEffect.setPos(pos)
                dustCloudEffect.play()
            self.cnode.setFromCollideMask(PiratesGlobals.TargetBitmask.allOff())