from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class Wind(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.fadeTime = 0.7
        self.startScale = Vec3(0.5, 1.0, 0.5)
        self.endScale = Vec3(2.0, 1.0, 2.0)
        self.fadeColor = Vec4(0.8, 0.8, 0.8, 0.5)
        self.flashDummy = self.attachNewNode('FlashDummy')
        self.flashDummy.reparentTo(self)
        self.flashDummy.hide()
        self.flash = loader.loadModel('models/effects/wind_tunnel')
        self.flash.setDepthWrite(0)
        self.flash.setLightOff()
        self.flash.setTransparency(1)
        self.flash.setScale(self.startScale)
        self.flash.reparentTo(self.flashDummy)
        self.flash.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))

    def createTrack(self):
        self.flash.setScale(2.0)
        self.flash.setColorScale(self.fadeColor)
        fadeIn = self.flash.colorScaleInterval(self.fadeTime / 3, self.fadeColor, startColorScale=Vec4(0, 0, 0, 0))
        fadeOut = self.flash.colorScaleInterval(self.fadeTime / 3, Vec4(0, 0, 0, 0), startColorScale=self.fadeColor)
        texStage = self.flash.findAllTextureStages()[0]
        self.scroller = LerpFunctionInterval(self.setNewUVs, fromData=0.0, toData=3.0, duration=self.fadeTime, extraArgs=[texStage])
        self.startEffect = Parallel(fadeIn, Func(self.scroller.loop), Func(self.flashDummy.show))
        self.endEffect = Sequence(fadeOut, Func(self.flashDummy.hide), Func(self.scroller.pause), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.fadeTime), self.endEffect)

    def setNewUVs(self, time, texStage):
        self.flash.setTexOffset(texStage, time, 0)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)