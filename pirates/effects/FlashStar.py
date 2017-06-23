from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from pirates.piratesbase import PiratesGlobals
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class FlashStar(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.setColorScaleOff()
        self.startCol = Vec4(1.0, 1.0, 1.0, 1)
        self.fadeTime = 1.0
        self.rayScale = Vec3(9.0, 1.0, 1.0)
        self.startScale = 5.0
        self.splatScale = 10.0
        self.flashDummy = self.attachNewNode('FlashDummy')
        self.flashDummy.setBillboardPointEye(1.0)
        self.flashDummy.reparentTo(self)
        self.flashDummy.setDepthWrite(0)
        self.flashDummy.setLightOff()
        self.flashDummy.hide()
        self.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingColor, ColorBlendAttrib.OOneMinusIncomingAlpha))
        self.flash = loader.loadModel('models/effects/combat_hit_spark')
        self.flash.setDepthWrite(0)
        self.flash.setFogOff()
        self.flash.setLightOff()
        self.flash.setScale(self.splatScale)
        self.flash.reparentTo(self.flashDummy)
        self.spark = loader.loadModel('models/effects/hitSplats')
        self.spark.reparentTo(self.flash)
        flash2 = loader.loadModel('models/effects/hitSplats')
        flash2.reparentTo(self.spark)
        self.slashRay1 = loader.loadModel('models/effects/hitSplats')
        self.slashRay1.setScale(self.splatScale)
        self.slashRay1.reparentTo(self.flashDummy)
        self.slashRay2 = loader.loadModel('models/effects/hitSplats')
        self.slashRay2.setScale(self.splatScale)
        self.slashRay2.reparentTo(self.flashDummy)
        self.slashRay2.setR(45)
        self.slashRay3 = loader.loadModel('models/effects/hitSplats')
        self.slashRay3.setScale(self.splatScale)
        self.slashRay3.reparentTo(self.flashDummy)
        self.slashRay3.setR(90)
        self.slashRay4 = loader.loadModel('models/effects/hitSplats')
        self.slashRay4.setScale(self.splatScale)
        self.slashRay4.reparentTo(self.flashDummy)
        self.slashRay4.setR(135)

    def createTrack(self):
        self.flash.setScale(self.splatScale)
        self.flash.setColorScale(1, 1, 1, 1)
        fadeBlast = self.flash.colorScaleInterval(self.fadeTime, Vec4(0, 0, 0, 0), startColorScale=self.startCol, blendType='easeOut')
        scaleBlast = self.flash.scaleInterval(self.fadeTime, self.splatScale, startScale=self.startScale, blendType='easeOut')
        rand = random.uniform(0.0, 3.0)
        rScale = Vec3(self.rayScale[0] + rand, self.rayScale[1], self.rayScale[2])
        ray1Fadein = self.slashRay1.scaleInterval(self.fadeTime / 4, self.rayScale, startScale=Vec3(0, 0, 0), blendType='easeOut')
        ray1Fadeout = self.slashRay1.scaleInterval(self.fadeTime / 4, Vec3(0, 0, 0), startScale=rScale, blendType='easeIn')
        rand = random.uniform(0.0, 3.0)
        rScale = Vec3(self.rayScale[0] + rand, self.rayScale[1], self.rayScale[2])
        ray2Fadein = self.slashRay2.scaleInterval(self.fadeTime / 4, self.rayScale, startScale=Vec3(0, 0, 0), blendType='easeOut')
        ray2Fadeout = self.slashRay2.scaleInterval(self.fadeTime / 4, Vec3(0, 0, 0), startScale=rScale, blendType='easeIn')
        rand = random.uniform(0.0, 3.0)
        rScale = Vec3(self.rayScale[0] + rand, self.rayScale[1], self.rayScale[2])
        ray3Fadein = self.slashRay3.scaleInterval(self.fadeTime / 4, self.rayScale, startScale=Vec3(0, 0, 0), blendType='easeOut')
        ray3Fadeout = self.slashRay3.scaleInterval(self.fadeTime / 4, Vec3(0, 0, 0), startScale=rScale, blendType='easeIn')
        rand = random.uniform(0.0, 3.0)
        rScale = Vec3(self.rayScale[0] + rand, self.rayScale[1], self.rayScale[2])
        ray4Fadein = self.slashRay4.scaleInterval(self.fadeTime / 4, self.rayScale, startScale=Vec3(0, 0, 0), blendType='easeOut')
        ray4Fadeout = self.slashRay4.scaleInterval(self.fadeTime / 4, Vec3(0, 0, 0), startScale=rScale, blendType='easeIn')
        anim1 = Sequence(Wait(0.05), Parallel(ray1Fadein, ray1Fadeout))
        anim2 = Sequence(Wait(0.1), Parallel(ray2Fadein, ray2Fadeout))
        anim3 = Sequence(Wait(0.15), Parallel(ray3Fadein, ray3Fadeout))
        anim4 = Sequence(Wait(0.2), Parallel(ray4Fadein, ray4Fadeout))
        anim5 = Sequence(Wait(0.35), Parallel(ray1Fadein, ray1Fadeout))
        anim6 = Sequence(Wait(0.4), Parallel(ray2Fadein, ray2Fadeout))
        anim7 = Sequence(Wait(0.45), Parallel(ray3Fadein, ray3Fadeout))
        anim8 = Sequence(Wait(0.5), Parallel(ray4Fadein, ray4Fadeout))
        anim = Parallel(fadeBlast, scaleBlast, anim1, anim2, anim3, anim4, anim5, anim6, anim7, anim8)
        self.track = Sequence(Func(self.flashDummy.show), anim, Func(self.flashDummy.hide), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)