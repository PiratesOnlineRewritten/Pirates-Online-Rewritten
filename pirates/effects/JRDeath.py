from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.particles import ParticleEffect
from direct.particles import Particles
from direct.particles import ForceGroup
from EffectController import EffectController
from PooledEffect import PooledEffect
import random

class JRDeath(PooledEffect, EffectController):

    def __init__(self, parent=None):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.effectModel = loader.loadModel('models/effects/pir_m_efx_chr_deathRays')
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
        texture = self.jolly.findAllTextures()[0]
        texture.setBorderColor(VBase4(0.0, 0.0, 0.0, 0.0))
        texture.setWrapU(Texture.WMBorderColor)
        texture.setWrapV(Texture.WMBorderColor)
        self.animNode = NodePath('bottomAnimNode')
        self.anim = LerpPosInterval(self.animNode, startPos=VBase3(0, 0, 0), pos=VBase3(0.0, -1.0, 0.0), duration=1.75)
        self.rays.setTexProjector(TextureStage.getDefault(), self.animNode, NodePath())
        fadeInRays = LerpColorScaleInterval(self.rays, 0.2, VBase4(0.8, 1, 0.1, 1), startColorScale=VBase4(0.8, 1, 0.1, 0))
        fadeOutRays = LerpColorScaleInterval(self.rays, 0.75, VBase4(0.8, 1, 0.1, 0), startColorScale=VBase4(0.8, 1, 0.1, 1))
        scaleUpRays = LerpScaleInterval(self.rays, 0.2, VBase3(1, 1, 1), startScale=VBase3(1, 1, 0), blendType='easeOut')
        scaleDownRays = LerpScaleInterval(self.rays, 0.75, VBase3(1, 1, 0), startScale=VBase3(1, 1, 1), blendType='easeIn')
        scaleJollyIval = LerpScaleInterval(self.jolly, 3.5, Vec3(1.5, 1.0, 4.0), startScale=Vec3(0.4, 1.0, 0.75))
        textureStage = self.jolly.findAllTextureStages()[0]
        uvScrollA = LerpFunctionInterval(self.setNewUVs, 1.0, toData=-2.6, fromData=0.0, extraArgs=[self.jolly, textureStage])
        uvScrollB = LerpFunctionInterval(self.setNewUVs, 0.75, toData=-6.5, fromData=-2.6, extraArgs=[self.jolly, textureStage])
        self.track = Sequence(Func(self.anim.loop), Parallel(fadeInRays, scaleUpRays, scaleJollyIval, Sequence(uvScrollA, uvScrollB), Sequence(Wait(0.2), Parallel(fadeOutRays, scaleDownRays))), Func(self.anim.finish), Func(self.cleanUpEffect))

    def setNewUVs(self, offset, part, ts):
        part.setTexOffset(ts, 0.0, offset)

    def setupStencil(self, target):
        tex = self.rays.findAllTextures()[0]
        geom = target.find('**/*actorGeom')
        geom.setTransparency(1)
        geom.setTexture(tex, 100)
        geom.setTexProjector(geom.findAllTextureStages()[0], self.animNode, NodePath())
        geom.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        geom.setColorScale(VBase4(0.8, 1, 0.1, 1))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)