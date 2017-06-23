from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class HitPulse(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectColor = Vec4(1, 1, 1, 1)
        self.effectModel = loader.loadModel('models/effects/pir_m_efx_chr_hitRings')
        self.effectModel.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.effectModel.setDepthWrite(0)
        self.effectModel.setColorScaleOff()
        self.effectModel.setLightOff()
        self.effectModel.setTwoSided(1)
        self.effectModel.reparentTo(self)
        self.effectModel.setTransparency(1)
        texture = self.effectModel.findAllTextures()[0]
        texture.setBorderColor(VBase4(0.0, 0.0, 0.0, 0.0))
        texture.setWrapU(Texture.WMBorderColor)
        texture.setWrapV(Texture.WMBorderColor)

    def createTrack(self):
        textureStage = self.effectModel.findAllTextureStages()[0]
        duration = 1.25
        scaleIval = LerpScaleInterval(self.effectModel, duration, 6.0, startScale=3.0)
        fadeIn = LerpColorScaleInterval(self.effectModel, 0.3, self.effectColor, startColorScale=(0,
                                                                                                  0,
                                                                                                  0,
                                                                                                  0))
        uvScroll = LerpFunctionInterval(self.setNewUVs, duration, toData=0.75, fromData=0.3, extraArgs=[self.effectModel, textureStage])
        self.startEffect = Sequence(Parallel(fadeIn, uvScroll, scaleIval))
        self.endEffect = Sequence(Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, self.endEffect)

    def setEffectColor(self, color, wantBlending=True):
        self.effectColor = color
        self.effectModel.setColorScale(self.effectColor)
        if wantBlending:
            self.effectModel.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        else:
            self.effectModel.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MNone))

    def setNewUVs(self, offset, part, ts):
        part.setTexOffset(ts, offset, 0.0)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)