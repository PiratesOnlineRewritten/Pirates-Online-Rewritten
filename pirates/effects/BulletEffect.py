from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from direct.distributed import DistributedObject
from EffectController import EffectController
from PooledEffect import PooledEffect
import random
ObjectDict = {'0': 'models/props/testBoard','1': 'models/props/testBoard'}

class BulletEffect(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.objects = []
        self.objIvals = Parallel()
        self.effectScale = 1.0
        self.effectDummy = self.attachNewNode('effectDummy')

    def loadObjects(self, num):
        self.objects = []
        for i in range(num):
            filePrefix = ObjectDict.get(str(random.randint(0, 1)))
            obj = loader.loadModel(filePrefix)
            obj.reparentTo(self.effectDummy)
            self.objects.append(obj)

    def createTrack(self):
        self.objIvals = Parallel()
        for obj in self.objects:
            obj.setScale(self.effectScale * random.uniform(6, 10) / 10.0)
            startPosition = Vec3(self.effectScale * random.uniform(0, 25), self.effectScale * random.uniform(-5, 5), self.effectScale * random.uniform(-5, 5))
            startVelocity = Vec3(self.effectScale * random.uniform(-20, 20), self.effectScale * random.uniform(-20, 20), self.effectScale * random.uniform(20, 80))
            projectileIval = ProjectileInterval(obj, startPos=startPosition, startVel=startVelocity, endZ=-1000, gravityMult=4.0)
            rotationIval = obj.hprInterval(6, Point3(random.uniform(360, 2880), random.uniform(360, 2880), random.uniform(360, 2880)))
            objIval = Parallel(projectileIval, rotationIval)
            self.objIvals.append(objIval)

        self.track = Sequence(self.objIvals, Func(self.cleanUpEffect))

    def setEffectScale(self, scale):
        self.effectScale = scale

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)