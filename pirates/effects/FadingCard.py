from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from EffectController import EffectController

class FadingCard(EffectController, NodePath):

    def __init__(self, card=None, color=Vec4(1, 1, 1, 1), fadeTime=0.25, waitTime=1.25, startScale=0.25, endScale=3.0):
        NodePath.__init__(self, 'FadingCard')
        EffectController.__init__(self)
        self.fadeTime = fadeTime
        self.waitTime = waitTime
        self.startScale = startScale
        self.endScale = endScale
        self.fadeColor = color
        self.card = card
        if self.card:
            self.flashDummy = self.attachNewNode('FlashDummy')
            self.flashDummy.setBillboardPointEye(1.0)
            self.flashDummy.setDepthWrite(0)
            self.flashDummy.setLightOff()
            self.flashDummy.setFogOff()
            self.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
            self.flashDummy.hide()
            self.card.reparentTo(self.flashDummy)

    def createTrack(self):
        if not self.card:
            self.track = Sequence()
            return
        fadeIn = self.card.colorScaleInterval(self.fadeTime, self.fadeColor, startColorScale=Vec4(0, 0, 0, 0))
        fadeOut = self.card.colorScaleInterval(self.waitTime, Vec4(0, 0, 0, 0), startColorScale=self.fadeColor)
        scaleBlast = self.card.scaleInterval(self.fadeTime / 3.0 + self.waitTime, self.endScale, startScale=self.startScale, blendType='easeOut')
        self.track = Sequence(Wait(2 * self.fadeTime), Func(self.flashDummy.show), Parallel(Sequence(fadeIn, Wait(self.fadeTime), fadeOut), scaleBlast), Func(self.flashDummy.hide), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)

    def destroy(self):
        EffectController.destroy(self)