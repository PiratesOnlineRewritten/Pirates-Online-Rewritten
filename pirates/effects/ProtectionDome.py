from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from PooledEffect import PooledEffect

class ProtectionDome(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/raydome')
        self.effectModel.reparentTo(self)
        self.effectModel.setTwoSided(1)
        self.setDepthWrite(0)
        self.setBin('fixed', 0)
        self.duration = 10.0
        self.inner = self.effectModel.find('**/inner')
        self.outer = self.effectModel.find('**/outer')
        self.inner.setColorScale(0.75, 1, 1, 0.3)
        self.outer.setColorScale(0.2, 0.5, 0.8, 0.2)
        self.effectModel.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))

    def createTrack(self):
        textureStage = self.effectModel.findAllTextureStages()[0]
        self.effectModel.setTexOffset(textureStage, 0.0, 1.0)
        self.setColorScale(1, 1, 1, 0)
        fadeIn = LerpColorScaleInterval(self, 2.0, Vec4(1, 1, 1, 1), startColorScale=Vec4(0, 0, 0, 0))
        fadeOut = LerpColorScaleInterval(self, 2.0, Vec4(0, 0, 0, 0), startColorScale=Vec4(1, 1, 1, 1))
        uvScroll = LerpFunctionInterval(self.setNewUVs, 5.0, toData=-1.0, fromData=1.0, extraArgs=[textureStage])
        self.startEffect = Sequence(Func(uvScroll.loop), fadeIn)
        self.endEffect = Sequence(fadeOut, Func(uvScroll.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration), self.endEffect)

    def setNewUVs(self, offset, ts):
        self.inner.setTexOffset(ts, offset, -1 * offset)
        self.outer.setTexOffset(ts, 3 * offset, -1 * offset)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)