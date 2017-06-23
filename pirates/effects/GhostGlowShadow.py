from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from otp.otpbase import OTPRender
from EffectController import EffectController
from PooledEffect import PooledEffect

class GhostGlowShadow(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleCards')
        self.glow = model.find('**/particleSparkle')
        self.glow.setHpr(0, -90, 0)
        self.glow.hide()
        self.effectColor = Vec4(1, 1, 1, 1)
        self.lodDistance = 50
        self.hide(OTPRender.MainCameraBitmask)
        self.showThrough(OTPRender.EnviroCameraBitmask)
        self.setTransparency(TransparencyAttrib.MAlpha)
        self.setBin('shadow', -10)
        self.setDepthTest(0)
        self.setLightOff()
        self.setScale(18)
        self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.glowRoot = self.attachNewNode('geomRoot')
        self.lod = LODNode('glowLOD')
        lodNP = self.glowRoot.attachNewNode(self.lod)
        self.glow.reparentTo(lodNP)

    def createTrack(self):
        self.glow.setColorScale(self.effectColor)
        self.lod.clearSwitches()
        self.lod.addSwitch(self.lodDistance, 0)
        pulseIval = Sequence(LerpScaleInterval(self.glow, 0.5, 1.2, blendType='easeInOut'), LerpScaleInterval(self.glow, 0.5, 1.0, blendType='easeInOut'))
        self.startEffect = Sequence(Func(self.glow.show), Func(pulseIval.loop))
        self.endEffect = Sequence(Func(pulseIval.finish), Func(self.glow.hide), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(1.0), self.endEffect)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)