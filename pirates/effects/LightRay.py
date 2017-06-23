from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class LightRay(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/pir_m_efx_env_lightRay')
        self.effectModel.reparentTo(self)
        self.backRay = self.effectModel.find('**/back')
        self.backRay.setColorScale(1, 1, 1, 0.25)
        self.effectScale = 1.0
        self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.setBillboardPointEye()
        self.setTransparency(1)
        self.setDepthWrite(0)
        self.setFogOff()
        self.setColorScale(1, 1, 1, 0.25)
        self.animSequence = None
        return

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)

    def randomize(self):
        self.effectModel.setPos(random.randint(-2, 2), random.randint(-2, 2), 0)
        self.effectModel.setScale(random.randint(30, 60) / 10.0, 1, random.randint(10, 15) / 10.0)
        self.setColorScale(1, 1, 1, random.randint(1, 2) / 10.0)

    def createTrack(self):
        self.effectModel.setColorScale(0, 0, 0, 0)
        self.mainAnimNode = NodePath('mainAnimNode')
        randOffset = random.randint(10, 20) / 10.0
        self.mainAnim = LerpPosInterval(self.mainAnimNode, startPos=VBase3(0 + randOffset, 0 + randOffset, 0), pos=VBase3(2.0 + randOffset, 1.0 + randOffset, 0.0), duration=25.0)
        self.effectModel.setTexProjector(TextureStage.getDefault(), self.mainAnimNode, NodePath())
        fadeInEffect = LerpColorScaleInterval(self.effectModel, 1.5, Vec4(1, 1, 1, 1), startColorScale=Vec4(0, 0, 0, 0))
        fadeOutEffect = LerpColorScaleInterval(self.effectModel, 1.5, Vec4(0, 0, 0, 0), startColorScale=Vec4(1, 1, 1, 1))
        self.animSequence = Sequence(Func(self.randomize), fadeInEffect, Wait(random.randint(10, 30) / 10.0), fadeOutEffect)
        self.startEffect = Sequence(Wait(random.randint(0, 20) / 10.0), Func(self.mainAnim.loop), Func(self.animSequence.loop))
        self.endEffect = Sequence(Func(self.animSequence.finish), Func(self.mainAnim.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(3.0), self.endEffect)

    def stop(self):
        if self.animSequence:
            self.animSequence.pause()
            self.animSequence = None
        EffectController.stop(self)
        return

    def finish(self):
        if self.animSequence:
            self.animSequence.pause()
            self.animSequence = None
        EffectController.finish(self)
        return

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)