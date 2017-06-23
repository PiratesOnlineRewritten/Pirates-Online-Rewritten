from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.GameOptions import Options
from PooledEffect import PooledEffect
from EffectController import EffectController

class GypsyBallGlow(PooledEffect, EffectController):

    def __init__(self, effectParent=None, billboardOffset=1.0):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if effectParent:
            self.reparentTo(effectParent)
        self.glow = loader.loadModel('models/effects/gypsyBallGlow')
        self.glow.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingColor, ColorBlendAttrib.OOneMinusIncomingAlpha))
        self.glow.setBillboardPointEye(billboardOffset)
        self.glow.setColorScaleOff()
        self.glow.setDepthWrite(0)
        self.glow.setLightOff()
        self.glow.setFogOff()
        self.glow.setBin('fixed', 50)
        self.glow.reparentTo(self)
        self.glow.setScale(2.5)
        self.glowHalo = self.glow.find('**/glow_aura')
        self.glowHalo.setColorScale(0.25, 0.2, 0.3, 0.75)
        self.fadeIval = None
        self.scaleIval = None
        return

    def createTrack(self, lod=Options.SpecialEffectsHigh):
        self.glow.setColor(0.9, 0.85, 0.95, 0.95)
        if lod >= Options.SpecialEffectsHigh:
            fadeIn = self.glow.colorInterval(1.0, Vec4(0.85, 0.8, 0.9, 0.9), startColor=Vec4(0.95, 0.9, 1, 1), blendType='easeInOut')
            fadeOut = self.glow.colorInterval(1.0, Vec4(0.95, 0.9, 1, 1), startColor=Vec4(0.85, 0.8, 0.9, 0.9), blendType='easeInOut')
            self.fadeIval = Sequence(fadeIn, fadeOut)
        scaleUpHalo = self.glowHalo.scaleInterval(1.0, 1.0, startScale=0.8, blendType='easeInOut')
        scaleDownHalo = self.glowHalo.scaleInterval(1.0, 0.8, startScale=1.0, blendType='easeInOut')
        self.scaleIval = Sequence(scaleDownHalo, scaleUpHalo)
        self.startEffect = Sequence(Func(self.scaleIval.loop))
        self.endEffect = Sequence(Func(self.scaleIval.finish))
        if self.fadeIval:
            self.startEffect.append(Func(self.fadeIval.loop))
            self.endEffect.append(Func(self.fadeIval.finish))
        self.track = Sequence(self.startEffect, Wait(2.0), self.endEffect)

    def enableEffect(self):
        if self.scaleIval:
            self.scaleIval.loop()
        if self.fadeIval:
            self.fadeIval.loop()

    def disableEffect(self):
        if self.scaleIval:
            self.scaleIval.pause()
        if self.fadeIval:
            self.fadeIval.pause()

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        self.glow.removeNode()
        EffectController.destroy(self)
        PooledEffect.destroy(self)