from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class JRSpawn(PooledEffect, EffectController):

    def __init__(self, parent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/pir_m_efx_chr_spawnRays')
        self.effectModel.reparentTo(self)
        self.rays = self.effectModel.find('**/rays')
        self.jolly = self.effectModel.find('**/jolly')
        self.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.setBillboardPointWorld()
        self.setTransparency(1)
        self.setDepthWrite(0)
        self.setLightOff()
        self.setFogOff()
        self.animNode = None
        self.anim = None
        return

    def createTrack(self):
        self.rays.setColorScale(VBase4(1, 1, 1, 0))
        self.jolly.setColorScale(VBase4(1, 1, 1, 0))
        self.animNode = NodePath('bottomAnimNode')
        self.anim = LerpPosInterval(self.animNode, startPos=VBase3(0, 0, 0), pos=VBase3(0.0, -1.0, 0.0), duration=1.75)
        self.rays.setTexProjector(TextureStage.getDefault(), self.animNode, NodePath())
        fadeInRays = LerpColorScaleInterval(self.rays, 1.0, VBase4(0.8, 1, 0.1, 1), startColorScale=VBase4(0.8, 1, 0.1, 0))
        fadeOutRays = LerpColorScaleInterval(self.rays, 2.0, VBase4(0.8, 1, 0.1, 0), startColorScale=VBase4(0.8, 1, 0.1, 1))
        scaleUpRays = LerpScaleInterval(self.rays, 2.0, VBase3(1, 1, 1.5), startScale=VBase3(0.5, 0.5, 0.2), blendType='easeInOut')
        scaleDownRays = LerpScaleInterval(self.rays, 2.0, VBase3(0.5, 0.5, 0.2), startScale=VBase3(1, 1, 1.5), blendType='easeInOut')
        fadeInJolly = LerpColorScaleInterval(self.jolly, 0.5, VBase4(1, 1, 1, 1), startColorScale=VBase4(1, 1, 1, 0))
        fadeOutJolly = LerpColorScaleInterval(self.jolly, 1.5, VBase4(1, 1, 1, 0), startColorScale=VBase4(1, 1, 1, 1))
        scaleUpJolly = LerpScaleInterval(self.jolly, 4.0, VBase3(1, 1, 1), startScale=VBase3(0.75, 0.75, 0.75))
        moveUpJolly = LerpPosInterval(self.jolly, 4.0, VBase3(0, -1, 1), startPos=VBase3(0, 0, 0))
        self.track = Sequence(Func(self.anim.loop), Parallel(fadeInRays, Sequence(scaleUpRays, Wait(1.0), Parallel(scaleDownRays, fadeOutRays)), Sequence(Wait(2.0), fadeInJolly, fadeOutJolly), scaleUpJolly, moveUpJolly), Func(self.anim.finish), Func(self.cleanUpEffect))

    def setupStencil(self, target):
        mask = 255
        stencil_A = StencilAttrib.make(1, StencilAttrib.SCFAlways, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOReplace, 6, mask, mask)
        stencil_B = StencilAttrib.make(1, StencilAttrib.SCFEqual, StencilAttrib.SOKeep, StencilAttrib.SOKeep, StencilAttrib.SOKeep, 6, mask, mask)
        target.setAttrib(stencil_A)
        self.setAttrib(stencil_B)

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)