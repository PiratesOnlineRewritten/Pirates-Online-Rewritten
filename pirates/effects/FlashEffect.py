from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController

class FlashEffect(NodePath, EffectController):

    def __init__(self):
        NodePath.__init__(self, 'FlashEffect')
        EffectController.__init__(self)
        self.fadeTime = 0.15
        self.effectColor = Vec4(1, 1, 1, 1)
        model = loader.loadModel('models/effects/particleCards')
        self.effectModel = model.find('**/particleWhiteGlow')
        self.effectModel.setBillboardAxis(0)
        self.effectModel.reparentTo(self)
        self.effectModel.setColorScale(0, 0, 0, 0)
        self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.setBillboardPointWorld()
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()

    def createTrack(self):
        fadeBlast = self.effectModel.colorScaleInterval(self.fadeTime, Vec4(0, 0, 0, 0), startColorScale=Vec4(self.effectColor), blendType='easeOut')
        scaleBlast = self.effectModel.scaleInterval(self.fadeTime, 5, startScale=1.0, blendType='easeIn')
        self.track = Sequence(Parallel(fadeBlast, scaleBlast), Func(self.cleanUpEffect))

    def setEffectColor(self, color, wantBlending=True):
        self.effectColor = color
        if wantBlending:
            self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        else:
            self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MNone))