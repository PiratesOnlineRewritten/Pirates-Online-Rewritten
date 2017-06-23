from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from pirates.piratesbase import PiratesGlobals
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class ThunderBolt(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.fadeTime = 0.14
        self.waitTime = 0.2
        self.startScale = 1.0
        self.endScale = 1.01
        self.fadeColor = Vec4(1.0, 1.0, 1.0, 1.0)
        self.flashDummy = self.attachNewNode('FlashDummy')
        self.flashDummy.setBillboardPointEye()
        self.flashDummy.setDepthWrite(0)
        self.flashDummy.setColorScaleOff()
        self.flashDummy.setFogOff()
        self.flashDummy.setLightOff()
        self.flashDummy.reparentTo(self)
        self.flashDummy.setScale(self.startScale)
        self.flashDummy.hide()
        self.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.flasha = loader.loadModel('models/effects/lightning_strike')
        self.flasha.reparentTo(self.flashDummy)
        self.flashb = loader.loadModel('models/effects/lightning_strike')
        self.flashb.reparentTo(self.flasha)

    def createTrack(self):
        self.flashDummy.setScale(self.startScale)
        self.flashDummy.setColorScale(1, 1, 1, 1)
        if random.choice((1, 10)) > 5:
            self.flasha.setH(random.uniform(-60.0, 60.0))
        else:
            self.flasha.setH(random.uniform(120.0, 240.0))
        fadeOut = self.flashDummy.colorScaleInterval(self.fadeTime, Vec4(0, 0, 0, 0), startColorScale=self.fadeColor)
        scaleBlast = self.flashDummy.scaleInterval(self.fadeTime * 2 + self.waitTime, self.endScale, startScale=self.startScale, blendType='easeOut')
        self.track = Sequence(Func(self.flashDummy.show), Parallel(Sequence(Wait(self.waitTime), fadeOut), scaleBlast), Func(self.flashDummy.hide), Func(self.flashDummy.setScale, 1.0), Func(self.flashDummy.setColorScale, Vec4(1, 1, 1, 1)), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)