from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class ConeRays(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectColor = Vec4(1, 1, 1, 1)
        self.effectModel = loader.loadModel('models/effects/pir_m_efx_chr_coneRays')
        self.effectModel.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.effectModel.setBillboardAxis(0)
        self.effectModel.setDepthWrite(0)
        self.effectModel.setColorScaleOff()
        self.effectModel.setLightOff()
        self.effectModel.reparentTo(self)
        self.effectModel.setTransparency(1)
        texture = self.effectModel.findAllTextures()[0]
        texture.setBorderColor(VBase4(0.0, 0.0, 0.0, 0.0))
        texture.setWrapU(Texture.WMBorderColor)
        texture.setWrapV(Texture.WMBorderColor)

    def createTrack(self):
        textureStage = self.effectModel.findAllTextureStages()[0]
        duration = 1.5
        self.effectModel.setColorScale(0, 0, 0, 0)
        self.setNewUVs(-0.6, self.effectModel, textureStage)
        scaleIval = LerpScaleInterval(self.effectModel, duration, Vec3(2.25, 2.25, 0.25), startScale=Vec3(1, 1, 2.25))
        uvScroll = LerpFunctionInterval(self.setNewUVs, duration, toData=1.0, fromData=-1.0, extraArgs=[self.effectModel, textureStage])
        self.startEffect = Sequence(Wait(0.2), Func(self.effectModel.setColorScale, Vec4(self.effectColor)), Parallel(uvScroll, scaleIval))
        self.endEffect = Sequence(Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, self.endEffect)

    def setEffectColor(self, color):
        self.effectColor = color
        self.effectModel.setColorScale(self.effectColor)

    def setNewUVs(self, offset, part, ts):
        part.setTexOffset(ts, 0.0, offset)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)