from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from pirates.piratesbase import PiratesGlobals
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class ThunderBallGlow(PooledEffect, EffectController):

    def __init__(self, effectParent=None, billboardOffset=1.0):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.setColorScaleOff()
        self.setBillboardPointEye(billboardOffset)
        self.fadePulse = None
        self.track1 = None
        if effectParent:
            self.reparentTo(effectParent)
        self.glow = loader.loadModel('models/effects/gypsyBallGlow')
        self.glow.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
        self.glow.setDepthWrite(0)
        self.glow.setFogOff()
        self.glow.setLightOff()
        self.glow.setBin('fixed', 50)
        self.glow.reparentTo(self)
        self.glow.setScale(2.5)
        return

    def createTrack(self):
        randomness = random.random() / 4.0
        fadeIn = self.glow.colorInterval(0.25 + randomness, Vec4(0.5, 0.8, 0.9, 0.75), startColor=Vec4(0.5, 0.9, 1, 1), blendType='easeInOut')
        fadeOut = self.glow.colorInterval(0.25 + randomness, Vec4(0.5, 0.9, 1, 1), startColor=Vec4(0.5, 0.8, 0.9, 0.75), blendType='easeInOut')
        self.fadePulse = Sequence(fadeIn, fadeOut)
        glowPart = self.glow.find('**/glow_aura')
        glowPart.setColorScale(0.25, 0.2, 0.3, 0.75)
        scaleUp = glowPart.scaleInterval(0.25 + randomness, 1.0, startScale=0.8, blendType='easeInOut')
        scaleDown = glowPart.scaleInterval(0.25 + randomness, 0.75, startScale=1.0, blendType='easeInOut')
        self.track1 = Sequence(scaleDown, scaleUp)

    def play(self, rate=1):
        self.createTrack()
        self.fadePulse.start()
        self.track1.start()

    def stop(self):
        if self.fadePulse:
            self.fadePulse.finish()
        if self.track1:
            self.track1.finish()

    def startLoop(self, rate=1):
        self.createTrack()
        self.fadePulse.loop()
        self.track1.loop()

    def stopLoop(self):
        if self.fadePulse:
            self.fadePulse.finish()
        if self.track1:
            self.track1.finish()
        self.cleanUpEffect()

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        if self.pool:
            self.checkInEffect(self)

    def destroy(self):
        self.fadePulse = None
        self.track1 = None
        if hasattr(self, 'glow'):
            self.glow.removeNode()
            self.glow = None
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        return