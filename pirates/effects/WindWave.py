from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class WindWave(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/windWaves')
        self.effectModel.setTwoSided(1)
        self.effectModel.setColorScale(1, 1, 1, 0.75)
        self.effectModel.reparentTo(self)
        self.inner = self.effectModel.find('**/inner')
        self.outer = self.effectModel.find('**/outer')
        self.setDepthWrite(0)
        self.setLightOff()

    def createTrack(self):
        textureStage = self.effectModel.findAllTextureStages()[0]
        self.effectModel.setTexOffset(textureStage, 0.0, 1.0)
        self.duration = 2.0
        self.setColorScale(1.0, 1.0, 1.0, 0.0)
        fadeIn = LerpColorScaleInterval(self, 1.5, Vec4(1.0, 1.0, 1.0, 1.0), startColorScale=Vec4(0.0, 0.0, 0.0, 0.0))
        fadeOut = LerpColorScaleInterval(self, 1.5, Vec4(0.0, 0.0, 0.0, 0.0), startColorScale=Vec4(1.0, 1.0, 1.0, 1.0))
        scaleIval = LerpScaleInterval(self.effectModel, self.duration / 1.5, Vec3(1.0, 1.0, 4.0), startScale=Vec3(1.0, 1.0, 4.0))
        uvScroll = LerpFunctionInterval(self.setNewUVs, self.duration / 1.5, toData=-1.0, fromData=1.0, extraArgs=[textureStage])
        rotate = LerpHprInterval(self.effectModel, self.duration, Vec3(360.0, 0.0, 0.0), startHpr=Vec3(0.0, 0.0, 0.0))
        self.startEffect = Sequence(Func(uvScroll.loop), Func(rotate.loop), fadeIn)
        self.endEffect = Sequence(fadeOut, Func(uvScroll.finish), Func(rotate.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration), self.endEffect)

    def setEffectColor(self, color):
        self.effectModel.setColorScale(color)

    def setNewUVs(self, offset, ts):
        self.inner.setTexOffset(ts, 0.0, -offset)
        self.outer.setTexOffset(ts, offset / 1.1, 0.0)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)