from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class InjuredEffect(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.dummy = self.attachNewNode(ModelNode('dummyNode'))
        self.effectModel = loader.loadModel('models/effects/stunRing')
        self.effectModel.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.effectModel.setTwoSided(1)
        self.effectModel.setScale(1)
        self.effectModel.reparentTo(self.dummy)
        self.setDepthWrite(0)
        self.setLightOff()
        self.duration = 1.5
        self.effectScale = 1.0

    def createTrack(self):
        self.effectModel.setScale(Vec3(1 * self.effectScale, 1 * self.effectScale, 1.3 * self.effectScale))
        textureStage = self.effectModel.findTextureStage('*')
        if textureStage:
            self.effectModel.setTexOffset(textureStage, 0.0, 1.0)
        self.setColorScale(1.0, 1.0, 1.0, 0.0)
        fadeIn = LerpColorScaleInterval(self, 0.5, Vec4(1, 1, 1, 0.4), startColorScale=Vec4(0, 0, 0, 0))
        fadeOut = LerpColorScaleInterval(self, 0.5, Vec4(0, 0, 0, 0), startColorScale=Vec4(1, 1, 1, 0.4))
        pulseFadeOut = LerpColorScaleInterval(self.effectModel, self.duration / 2.25, Vec4(1, 1, 1, 0.18), startColorScale=Vec4(1, 1, 1, 0.6))
        pulseFadeIn = LerpColorScaleInterval(self.effectModel, self.duration / 1.75, Vec4(1, 1, 1, 0.6), startColorScale=Vec4(1, 1, 1, 0.15))
        fade = Sequence(pulseFadeIn, pulseFadeOut)
        rotateOne = LerpHprInterval(self.effectModel, self.duration / 3.0, Vec3(0, -25, 25), startHpr=Vec3(0, 25, -25), blendType='easeOut')
        rotateTwo = LerpHprInterval(self.effectModel, self.duration / 3.0, Vec3(0, 25, -25), startHpr=Vec3(0, -25, 25), blendType='easeOut')
        rotate = Sequence(rotateOne, rotateTwo)
        rotateH = LerpHprInterval(self.dummy, self.duration / 3.0, Vec3(0, 0, 0), startHpr=Vec3(360, 0, 0))
        self.startEffect = Sequence(Func(rotate.loop), Func(rotateH.loop), Func(fade.loop), fadeIn)
        self.endEffect = Sequence(fadeOut, Func(rotate.finish), Func(rotateH.finish), Func(fade.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(3.0 * self.duration), self.endEffect)

    def setNewUVs(self, offset, ts):
        self.effectModel.setTexOffset(ts, 0.0, -offset)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)