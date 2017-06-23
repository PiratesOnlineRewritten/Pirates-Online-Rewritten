from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class SoulSpiral(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/soulspiral')
        self.effectModel2 = loader.loadModel('models/effects/soulspiral')
        self.effectModel3 = loader.loadModel('models/effects/soulspiral')
        self.effectModel4 = loader.loadModel('models/effects/soulspiral')
        self.effectModel.setColorScaleOff()
        self.effectModel2.setColorScaleOff()
        self.effectModel.reparentTo(self)
        self.effectModel2.reparentTo(self)
        self.effectModel3.reparentTo(self.effectModel)
        self.effectModel4.reparentTo(self.effectModel2)
        self.effectModel.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.effectModel2.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.effectModel.setScale(0.2, 0.2, 0.2)
        self.effectModel2.setTwoSided(1)
        self.effectModel2.setScale(0.16, 0.16, 0.18)
        self.effectModel2.setH(25)
        self.setDepthWrite(0)
        self.setLightOff()
        self.setColorScaleOff()
        self.effectColor = Vec4(1, 1, 1, 1)
        texture = self.effectModel.findAllTextures()[0]
        texture.setBorderColor(VBase4(0.0, 0.0, 0.0, 0.0))
        texture.setWrapU(Texture.WMBorderColor)
        texture.setWrapV(Texture.WMBorderColor)

    def createTrack(self):
        textureStage = self.effectModel.findAllTextureStages()[0]
        self.effectModel.setTexOffset(textureStage, 0.0, 1.0)
        self.effectModel2.setTexOffset(textureStage, 0.0, 1.0)
        duration = 1.5
        self.setColorScale(1.0, 1.0, 1.0, 0.75)
        fadeOut = LerpColorScaleInterval(self, 0.5, Vec4(0.0, 0.0, 0.0, 0.0), startColorScale=Vec4(1.0, 1.0, 1.0, 0.75))
        uvScrollA = LerpFunctionInterval(self.setNewUVs, duration, toData=-2.5, fromData=1.0, extraArgs=[self.effectModel2, textureStage])
        uvScrollB = LerpFunctionInterval(self.setNewUVs, duration, toData=-2.5, fromData=1.0, extraArgs=[self.effectModel, textureStage])
        rotate = LerpHprInterval(self.effectModel, 1.5 * duration, Vec3(360, 0, 0), startHpr=Vec3(0, 0, 0))
        self.startEffect = Sequence(Func(rotate.loop), Func(uvScrollA.loop), Wait(duration / 2.0), Func(uvScrollB.loop))
        self.endEffect = Sequence(fadeOut, Func(uvScrollA.finish), Func(uvScrollB.finish), Func(rotate.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(duration), self.endEffect)

    def setNewUVs(self, offset, part, ts):
        part.setTexOffset(ts, 0.0, offset)

    def setEffectColor(self, color):
        self.effectColor = color + Vec4(0.7, 0.7, 0.7, 1.0)
        self.effectModel.setColorScale(self.effectColor)
        self.effectModel2.setColorScale(self.effectColor)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        self.stop()
        if self.track:
            self.track = None
        self.removeNode()
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        return