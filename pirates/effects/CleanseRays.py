from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class CleanseRays(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/pir_m_efx_chr_tubeRays')
        self.effectModel.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.effectModel.setBillboardAxis(0)
        self.effectModel.setDepthWrite(0)
        self.effectModel.setColorScaleOff()
        self.effectModel.setLightOff()
        self.effectModel.reparentTo(self)
        texture = self.effectModel.findAllTextures()[0]
        texture.setBorderColor(VBase4(0.0, 0.0, 0.0, 0.0))
        texture.setWrapU(Texture.WMBorderColor)
        texture.setWrapV(Texture.WMBorderColor)

    def createTrack(self):
        textureStage = self.effectModel.findAllTextureStages()[0]
        duration = 5.5
        self.setNewUVs(1.0, self.effectModel, textureStage)
        scaleIval = LerpScaleInterval(self, duration, Vec3(1.2, 1.2, 1.6), startScale=Vec3(0.8, 0.8, 0.2))
        uvScroll = LerpFunctionInterval(self.setNewUVs, duration, toData=-2.0, fromData=1.0, extraArgs=[self.effectModel, textureStage])
        self.startEffect = Parallel(scaleIval, uvScroll)
        self.endEffect = Sequence(Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(duration), self.endEffect)

    def setNewUVs(self, offset, part, ts):
        part.setTexOffset(ts, 0.0, offset)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)