from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from PooledEffect import PooledEffect
from EffectController import EffectController
from otp.otpbase import OTPRender

class JRDeathBlast(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        model = loader.loadModel('models/effects/particleCards')
        self.ring = model.find('**/particleBlast')
        self.ring.reparentTo(self)
        model = loader.loadModel('models/effects/particleCards')
        self.flash = model.find('**/particleBlast')
        self.flash.reparentTo(self)
        self.setDepthTest(0)
        self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()
        self.hide()
        self.hide(OTPRender.MainCameraBitmask)
        self.showThrough(OTPRender.EnviroCameraBitmask)
        self.setBin('shadow', 0)
        self.setTransparency(TransparencyAttrib.MAlpha)
        self.ring.setHpr(0, -90, 0)
        self.flash.setBillboardAxis(0)

    def createTrack(self, rate=1):
        self.ring.setColorScale(0.8, 1, 0.1, 1)
        self.ring.setScale(5)
        self.flash.setColorScale(0.8, 1, 0.1, 1)
        self.flash.setScale(10)
        self.hide()
        ringFadeBlast = self.ring.colorScaleInterval(0.5, Vec4(0, 0, 0, 0))
        ringScaleBlast = self.ring.scaleInterval(0.5, 50, blendType='easeIn', other=render)
        flashFadeBlast = self.flash.colorScaleInterval(1.5, Vec4(0, 0, 0, 0), blendType='easeOut')
        flashScaleBlast = self.flash.scaleInterval(1.5, 30, blendType='easeIn')
        self.track = Sequence(Func(self.show), Parallel(ringScaleBlast, ringFadeBlast, flashScaleBlast, flashFadeBlast), Func(self.hide), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)