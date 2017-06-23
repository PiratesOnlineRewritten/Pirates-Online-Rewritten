from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.GameOptions import Options
from EffectController import EffectController
import random

class CandleFlame(EffectController, NodePath):

    def __init__(self, newParent=render, billboardOffset=1.0):
        NodePath.__init__(self, 'CandleFlame')
        EffectController.__init__(self)
        self.newParent = newParent
        self.setBillboardPointEye(billboardOffset)
        self.setColorScaleOff()
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()
        self.setBin('fixed', 120)
        self.glow = loader.loadModel('models/effects/candleFlame')
        self.glow.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.glow.reparentTo(self)
        self.glow.setPos(0, 0, 0.15)
        self.glowHalo = loader.loadModel('models/effects/candleHalo')
        self.glowHalo.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.glowHalo.reparentTo(self)
        self.glowHalo.setPos(0, 0, 0.15)
        self.scaleIval = None
        self.haloIval = None
        return

    def createTrack(self, lod=Options.SpecialEffectsHigh):
        baseScale = Vec3(1.1, 1.1, 1.1)
        endScale = Vec3(1.0, 1.0, 1.4)
        self.scaleIval = Sequence()
        numIvals = min(2, lod + 1)
        for i in range(numIvals):
            randomness = random.random() / 10
            self.scaleIval.append(self.glow.scaleInterval(0.1 + randomness, endScale, startScale=baseScale, blendType='easeInOut'))
            self.scaleIval.append(self.glow.scaleInterval(0.1 + randomness, baseScale, startScale=endScale, blendType='easeInOut'))

        randomness = random.random() / 20
        scaleUpHalo = self.glowHalo.scaleInterval(0.1 + randomness, 2.0, startScale=2.2, blendType='easeInOut')
        scaleDownHalo = self.glowHalo.scaleInterval(0.1 + randomness, 2.2, startScale=2.0, blendType='easeInOut')
        self.haloIval = Sequence(scaleUpHalo, scaleDownHalo)
        self.startEffect = Sequence(Func(self.scaleIval.loop), Func(self.haloIval.loop))
        self.endEffect = Sequence(Func(self.scaleIval.finish), Func(self.haloIval.finish))
        self.track = Sequence(self.startEffect, Wait(2.0), self.endEffect)
        self.reparentTo(self.newParent)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)

    def destroy(self):
        self.scaleIval.finish()
        self.haloIval.finish()
        self.glow.removeNode()
        self.glowHalo.removeNode()
        EffectController.destroy(self)