from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from pirates.piratesbase import PiratesGlobals
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class FadingSigil(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.fadeTime = 1.0
        self.waitTime = 1.0
        self.startScale = 6.0
        self.endScale = 7.0
        self.fadeColor = Vec4(1.0, 1.0, 1.0, 1.0)
        self.flashDummy = self.attachNewNode('FlashDummy')
        self.flashDummy.setBillboardPointEye(1.0)
        self.flashDummy.reparentTo(self)
        self.flashDummy.hide()
        self.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.flash = loader.loadModel('models/effects/sigils')
        self.flash.setDepthWrite(0)
        self.flash.setColorScaleOff()
        self.flash.setFogOff()
        self.flash.setLightOff()
        self.flash.setScale(self.startScale)
        self.flash.reparentTo(self.flashDummy)

    def createTrack(self):
        self.flash.setScale(1)
        self.flash.setColorScale(1, 1, 1, 1)
        fadeIn = self.flash.colorScaleInterval(self.fadeTime, self.fadeColor, startColorScale=Vec4(0, 0, 0, 0))
        fadeOut = self.flash.colorScaleInterval(self.fadeTime, Vec4(0, 0, 0, 0), startColorScale=self.fadeColor)
        mover = self.flash.posInterval(self.fadeTime * 2 + self.waitTime, Vec3(0, 0, 1.0))
        scaleBlast = self.flash.scaleInterval(self.fadeTime * 2 + self.waitTime, self.endScale, startScale=self.startScale, blendType='easeOut')
        self.track = Sequence(Func(self.flashDummy.show), Parallel(Sequence(fadeIn, Wait(self.waitTime), fadeOut), scaleBlast, mover), Func(self.flashDummy.hide), Func(self.flash.setScale, 1.0), Func(self.flash.setColorScale, Vec4(1, 1, 1, 1)), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)