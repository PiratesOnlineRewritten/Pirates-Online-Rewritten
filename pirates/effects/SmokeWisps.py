from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class SmokeWisps(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.modelScale = 0.35
        self.effectModel = loader.loadModel('models/effects/smokeWisp')
        self.effectModel.setScale(self.modelScale)
        self.effectModel.setDepthWrite(0)
        self.effectModel.setColorScaleOff()
        self.effectModel.setLightOff()
        self.effectModel.setBillboardPointEye(1.0)
        self.effectModel.reparentTo(self)

    def createTrack(self):
        textureStage = self.effectModel.findAllTextureStages()[0]
        duration = 2.0 + random.uniform(0.0, 1.0)
        fadeIn = self.effectModel.colorScaleInterval(1.0, Vec4(0.9, 0.9, 0.9, 1.0), startColorScale=Vec4(0, 0, 0, 0), blendType='easeOut')
        fadeOut = self.effectModel.colorScaleInterval(1.0, Vec4(0, 0, 0, 0), startColorScale=Vec4(0.9, 0.9, 0.9, 1.0), blendType='easeOut')
        scaleUp = self.effectModel.scaleInterval(3.0, Vec3(1, 1, self.modelScale), startScale=Vec3(1, 1, 0), blendType='easeOut')
        uvScroll = LerpFunctionInterval(self.setNewUVs, duration, toData=0, fromData=1, extraArgs=[self.effectModel, textureStage])
        self.startEffect = Sequence(Func(uvScroll.loop), Parallel(fadeIn, scaleUp))
        self.endEffect = Sequence(fadeOut, Func(uvScroll.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(10.0), self.endEffect)

    def destroy(self):
        self.stop()
        if self.track:
            self.track = None
        self.removeNode()
        return

    def setNewUVs(self, offset, part, ts):
        part.setTexOffset(ts, 1, offset)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)