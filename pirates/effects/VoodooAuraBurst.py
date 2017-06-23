from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class VoodooAuraBurst(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/pir_m_efx_chr_auraBurstA')
        self.effectModel.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOneMinusIncomingAlpha))
        self.effectColor = Vec4(1, 1, 1, 1)
        self.effectModel.setDepthWrite(0)
        self.effectModel.setColorScaleOff()
        self.effectModel.setTwoSided(1)
        self.effectModel.setLightOff()
        self.effectModel.setTransparency(1)
        self.effectModel.reparentTo(self)
        self.effectModel.setColorScale(0, 0, 0, 0)

    def createTrack(self):
        self.effectModel.setColorScale(0, 0, 0, 0)
        textureStage = self.effectModel.findAllTextureStages()[0]
        fadeOut = LerpColorScaleInterval(self.effectModel, 0.75, Vec4(0, 0, 0, 0), startColorScale=self.effectColor, blendType='easeIn')
        scaleIval = LerpScaleInterval(self.effectModel, 0.75, Vec3(2.0, 2.0, 0.25), startScale=Vec3(0.25, 0.25, 1.5))
        uvScroll = LerpFunctionInterval(self.setNewUVs, 0.75, toData=1.0, fromData=0.0, extraArgs=[self.effectModel, textureStage])
        self.startEffect = Parallel(fadeOut, scaleIval, uvScroll)
        self.endEffect = Sequence(Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(1.0), self.endEffect)

    def setEffectColor(self, color):
        self.effectColor = color

    def setNewUVs(self, offset, part, ts):
        part.setTexOffset(ts, 0.0, offset)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        self.stop()
        if self.track:
            self.track = None
        self.removeNode()
        EffectController.destroy(self)
        PooledEffect.destroy(self)
        return