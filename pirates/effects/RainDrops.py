from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController
import random

class RainDrops(EffectController, NodePath):

    def __init__(self, reference=None):
        NodePath.__init__(self, 'RainDrops')
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/rainDrops')
        self.effectModel.reparentTo(self)
        self.effectModel.setScale(80)
        self.effectModel.setZ(-10)
        self.effectModel.setDepthWrite(0)
        self.effectModel.setDepthTest(0)
        self.effectModel.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.duration = 10.0
        self.angle = 0.0
        self.reference = reference
        self.layer1 = self.effectModel.find('**/cylinder01')
        self.layer2 = self.effectModel.find('**/cylinder02')
        self.layer3 = self.effectModel.find('**/cylinder03')

    def createTrack(self):
        self.angle = random.randint(-20, 20)
        self.layer1.setP(self.angle)
        self.layer2.setP(self.angle / 1.2)
        self.layer3.setP(self.angle / 2.0)
        textureStage = self.effectModel.findAllTextureStages()[0]
        self.effectModel.setTexOffset(textureStage, 0.0, 1.0)
        self.setColorScale(1, 1, 1, 0)
        fadeIn = LerpColorScaleInterval(self, 1.5, Vec4(1, 1, 1, 1), startColorScale=Vec4(0, 0, 0, 0))
        fadeOut = LerpColorScaleInterval(self, 1.5, Vec4(0, 0, 0, 0), startColorScale=Vec4(1, 1, 1, 1))
        uvScroll = LerpFunctionInterval(self.setNewUVs, 0.6, toData=1.0, fromData=-1.0, extraArgs=[textureStage])
        self.startEffect = Sequence(Func(uvScroll.loop), fadeIn)
        self.endEffect = Sequence(fadeOut, Func(uvScroll.finish), Func(self.cleanUpEffect))
        self.track = Sequence(self.startEffect, Wait(self.duration), self.endEffect)

    def setNewUVs(self, offset, ts):
        if self.reference:
            self.setPos(self.reference.getPos(self.getParent()))
        self.layer1.setTexOffset(ts, 0.0, offset)
        self.layer2.setTexOffset(ts, 0.0, offset)
        self.layer3.setTexOffset(ts, 0.0, offset)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)

    def destroy(self):
        EffectController.destroy(self)