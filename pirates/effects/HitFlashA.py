from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from pirates.piratesbase import PiratesGlobals
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class HitFlashA(PooledEffect, EffectController):

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.useRay = 0
        self.useSpark = 1
        self.rayAngle = 0.0
        self.rayFlareValue = 0.35
        self.setColorScaleOff()
        self.startCol = Vec4(1.0, 1.0, 1.0, 1)
        self.fadeTime = 0.6
        self.startScale = 2.0
        self.splatScale = 10.0
        self.flashDummy = self.attachNewNode('FlashDummy')
        self.flashDummy.reparentTo(self)
        self.flashDummy.hide()
        self.flashDummy.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.flash = loader.loadModel('models/effects/combat_hit_spark')
        self.flash.setDepthWrite(0)
        self.flash.setFogOff()
        self.flash.setLightOff()
        self.flash.setScale(self.splatScale)
        self.flash.reparentTo(self.flashDummy)
        self.flash.setBillboardPointEye(1.0)
        self.spark = loader.loadModel('models/effects/hitSplats')
        self.spark.reparentTo(self.flash)
        flash2 = loader.loadModel('models/effects/hitSplats')
        flash2.reparentTo(self.spark)
        self.slashRay = loader.loadModel('models/effects/hitSplats')
        self.slashRay.setDepthWrite(0)
        self.slashRay.setFogOff()
        self.slashRay.setLightOff()
        self.slashRay.setScale(self.splatScale)
        self.slashRay.reparentTo(self.flashDummy)
        self.slashRay.setTwoSided(1)

    def createTrack(self):
        self.flash.setScale(self.splatScale)
        self.flash.setColorScale(1, 1, 1, 1)
        fadeBlast = self.flash.colorScaleInterval(self.fadeTime, Vec4(0, 0, 0, 0), startColorScale=self.startCol, blendType='easeOut')
        scaleBlast = self.flash.scaleInterval(self.fadeTime, self.splatScale, startScale=self.startScale, blendType='easeOut')
        scaleSlashRay = self.slashRay.scaleInterval(self.fadeTime / 4, Vec3(self.splatScale * 2.0, 0.2, 0.2), startScale=Vec3(self.startScale, 0.2, self.splatScale * self.rayFlareValue), blendType='easeOut')
        fadeSlashRay = self.slashRay.colorScaleInterval(self.fadeTime, Vec4(0, 0, 0, 0), startColorScale=self.startCol, blendType='easeIn')
        anim = Parallel(fadeBlast, scaleBlast)
        if self.useRay:
            anim.append(scaleSlashRay)
            anim.append(fadeSlashRay)
            self.slashRay.show()
            self.slashRay.setR(self.rayAngle)
        else:
            self.slashRay.hide()
        if self.useSpark:
            self.spark.show()
        else:
            self.spark.hide()
        self.track = Sequence(Func(self.flashDummy.show), anim, Func(self.flashDummy.hide), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)