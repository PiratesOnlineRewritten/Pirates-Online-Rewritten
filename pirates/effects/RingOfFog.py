from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController

class RingOfFog(NodePath, EffectController):

    def __init__(self):
        NodePath.__init__(self, 'RingOfFog')
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/pir_m_efx_env_ringOfFog')
        self.effectModel.setColorScale(Vec4(0, 0, 0, 0))
        self.effectModel.setScale(3500)
        self.effectModel.reparentTo(self)
        self.setTransparency(1)
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()
        self.setBin('water', 100)
        self.effectColor = Vec4(1, 1, 1, 1)

    def setEffectColor(self, color):
        self.effectColor = color

    def createTrack(self):
        animNode = NodePath('animNode')
        anim = LerpPosInterval(animNode, startPos=VBase3(0, 0, 0), pos=VBase3(1.0, -3.0, 0.0), duration=100.0)
        self.effectModel.setTexProjector(TextureStage.getDefault(), animNode, NodePath())
        fadeInEffect = LerpColorScaleInterval(self.effectModel, 1.0, self.effectColor, startColorScale=Vec4(0, 0, 0, 0))
        fadeOutEffect = LerpColorScaleInterval(self.effectModel, 1.0, Vec4(0, 0, 0, 0), startColorScale=self.effectColor)
        self.startEffect = Sequence(Func(anim.loop), fadeInEffect)
        self.endEffect = Sequence(fadeOutEffect, Func(anim.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(10.0), self.endEffect)

    def startAdjustTask(self):
        pass

    def stopAdjustTask(self):
        pass

    def adjustTask(self, task):
        pass

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)