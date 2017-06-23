from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from PooledEffect import PooledEffect
from otp.otpbase import OTPRender

class WaterWakes(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/waterwakes')
        self.effectModel.reparentTo(self)
        self.effectModel.setH(180)
        self.duration = 10.0
        self.inner = self.effectModel.find('**/inner')
        self.outer = self.effectModel.find('**/outer')
        self.hide(OTPRender.MainCameraBitmask)
        self.showThrough(OTPRender.EnviroCameraBitmask)
        self.setDepthWrite(0)
        self.setDepthTest(0)
        self.setBin('water', 10)
        self.setAttrib(ColorWriteAttrib.make(ColorWriteAttrib.CRed | ColorWriteAttrib.CGreen | ColorWriteAttrib.CBlue))
        mask = 268435455
        stencil = StencilAttrib.make(1, StencilAttrib.SCFEqual, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, 1, mask, mask)
        self.setAttrib(stencil)
        if not base.useStencils:
            self.hide()

    def createTrack(self):
        textureStage = self.effectModel.findAllTextureStages()[0]
        self.effectModel.setTexOffset(textureStage, 0.0, 1.0)
        self.setColorScale(1, 1, 1, 0)
        fadeIn = LerpColorScaleInterval(self, 1.5, Vec4(1, 1, 1, 0.8), startColorScale=Vec4(0, 0, 0, 0))
        fadeOut = LerpColorScaleInterval(self, 2.0, Vec4(0, 0, 0, 0), startColorScale=Vec4(1, 1, 1, 0.8))
        uvScroll = LerpFunctionInterval(self.setNewUVs, 5.0, toData=-1.0, fromData=1.0, extraArgs=[textureStage])
        self.startEffect = Sequence(Func(uvScroll.loop), fadeIn)
        self.endEffect = Sequence(fadeOut, Func(uvScroll.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration), self.endEffect)

    def setNewUVs(self, offset, ts):
        self.inner.setTexOffset(ts, 0.0, offset)
        self.outer.setTexOffset(ts, 0.0, offset)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)