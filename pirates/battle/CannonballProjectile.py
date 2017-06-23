from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from pirates.battle import WeaponGlobals
from pirates.battle import WeaponConstants
from pirates.piratesbase import PiratesGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle.ProjectileAmmo import ProjectileAmmo
from pirates.effects.PolyTrail import PolyTrail
from pirates.effects.FireTrail import FireTrail
from pirates.effects.FuryTrail import FuryTrail
from pirates.effects.ThunderBallGlow import ThunderBallGlow
from pirates.effects.FlamingSkull import FlamingSkull
import random

class CannonballProjectile(ProjectileAmmo):
    default_motion_color = [
     Vec4(0.1, 0.2, 0.4, 1.0), Vec4(0.1, 0.2, 0.4, 1.0), Vec4(0.1, 0.2, 0.4, 1.0), Vec4(0.1, 0.2, 0.4, 1.0), Vec4(0.1, 0.2, 0.4, 1.0)]
    fire_motion_color = [
     Vec4(1.0, 0.0, 0.0, 1.0), Vec4(1.0, 0.5, 0.0, 1.0), Vec4(1.0, 0.5, 0.0, 1.0), Vec4(1.0, 0.5, 0.0, 1.0), Vec4(1.0, 0.5, 0.0, 1.0)]
    r = 0.8
    small_vertex_list = [Vec4(r, 0.0, r, 1.0), Vec4(r, 0.0, -r, 1.0), Vec4(-r, 0.0, -r, 1.0), Vec4(-r, 0.0, r, 1.0), Vec4(r, 0.0, r, 1.0)]
    r = 2.0
    large_vertex_list = [Vec4(r, 0.0, r, 1.0), Vec4(r, 0.0, -r, 1.0), Vec4(-r, 0.0, -r, 1.0), Vec4(-r, 0.0, r, 1.0), Vec4(r, 0.0, r, 1.0)]
    r = 1.0
    chainshot_vertex_list = [Vec4(-r, 0, 0, 1), Vec4(r, 0, 0, 1), Vec4(-r, 0, 0, 1)]

    def __init__(self, cr, ammoSkillId, event, buffs=[]):
        self.trailEffect = None
        self.buffs = buffs
        self.glowA = None
        self.glowB = None
        self.glowATrack = None
        self.glowBTrack = None
        self.rotateIval = None
        ProjectileAmmo.__init__(self, cr, ammoSkillId, event, True)
        self.effectFlag = WeaponGlobals.getSkillEffectFlag(ammoSkillId)
        self.effectIval = None
        return

    def removeNode(self):
        self.cleanupMotionTrails()
        ProjectileAmmo.removeNode(self)

    def loadModel(self):
        self.mtrail = None
        self.strail = None
        self.scaleIval = None
        maxGlowScale = 8
        minGlowScale = 7
        if not base.config.GetBool('want-special-effects', 1):
            cannonball = loader.loadModel('models/ammunition/cannonball')
        else:
            if self.ammoSkillId in (InventoryType.CannonRoundShot, InventoryType.CannonGrapeShot):
                cannonball = loader.loadModel('models/ammunition/cannonball')
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                    self.createMotionTrails(self)
                if base.options.getSpecialEffectsSetting() == base.options.SpecialEffectsLow:
                    self.createSimpleMotionTrail(self)
            else:
                if self.ammoSkillId == InventoryType.CannonChainShot:
                    cannonball = loader.loadModel('models/ammunition/chainShot')
                    ball1 = cannonball.find('**/ball_0')
                    ball1.setBillboardPointEye()
                    ball2 = cannonball.find('**/ball_1')
                    ball2.setBillboardPointEye()
                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                        randVal = random.uniform(-180.0, 180.0)
                        randSpeed = random.uniform(-0.1, 0.1)
                        randDirection = 1
                        self.effectIval = cannonball.hprInterval(0.4 + randSpeed, Point3(randVal, 360 * randDirection, 0), startHpr=Point3(randVal, 0, 0))
                        self.effectIval.loop()
                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                        self.createMotionTrails(self, self.chainshot_vertex_list)
                    if base.options.getSpecialEffectsSetting() == base.options.SpecialEffectsLow:
                        self.createSimpleMotionTrail(self)
                elif self.ammoSkillId == InventoryType.CannonFirebrand:
                    cannonball = loader.loadModel('models/ammunition/cannonball')
                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                        self.trailEffect = FireTrail.getEffect()
                        if self.trailEffect:
                            self.trailEffect.reparentTo(cannonball)
                            self.trailEffect.startLoop()
                elif self.ammoSkillId == InventoryType.CannonFlamingSkull or self.ammoSkillId == InventoryType.CannonFirebrand:
                    maxGlowScale = 28
                    minGlowScale = 24
                    cannonball = loader.loadModel('models/ammunition/cannonball')
                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                        self.trailEffect = FireTrail.getEffect()
                        if self.trailEffect:
                            self.trailEffect.wantGlow = base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium
                            self.trailEffect.reparentTo(cannonball)
                            self.trailEffect.startLoop()
                elif self.ammoSkillId == InventoryType.CannonFury:
                    maxGlowScale = 40
                    minGlowScale = 30
                    cannonball = self.attachNewNode('cannonball')
                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                        self.trailEffect = FuryTrail.getEffect()
                        if self.trailEffect:
                            self.trailEffect.wantGlow = base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium
                            self.trailEffect.wantBlur = base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh
                            self.trailEffect.reparentTo(cannonball)
                            self.trailEffect.startLoop()
                elif self.ammoSkillId == InventoryType.CannonComet:
                    cannonball = self.attachNewNode('cannonball')
                    cannonball1 = loader.loadModel('models/ammunition/cannonball')
                    self.trailEffect = FireTrail.getEffect()
                    if self.trailEffect:
                        self.trailEffect.wantGlow = base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium
                        self.trailEffect.reparentTo(cannonball1)
                        self.trailEffect.startLoop()
                    self.createMotionTrails(self, self.small_vertex_list, self.fire_motion_color)
                    cannonball2 = loader.loadModel('models/ammunition/cannonball')
                    self.trailEffect = FireTrail.getEffect()
                    if self.trailEffect:
                        self.trailEffect.wantGlow = base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium
                        self.trailEffect.reparentTo(cannonball2)
                        self.trailEffect.startLoop()
                    self.createMotionTrails(self, self.small_vertex_list, self.fire_motion_color)
                    cannonball3 = loader.loadModel('models/ammunition/cannonball')
                    self.trailEffect = FireTrail.getEffect()
                    if self.trailEffect:
                        self.trailEffect.wantGlow = base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium
                        self.trailEffect.reparentTo(cannonball3)
                        self.trailEffect.startLoop()
                    self.createMotionTrails(self, self.small_vertex_list, self.fire_motion_color)
                    cannonball1.reparentTo(cannonball)
                    cannonball1.setPos(0, 4, -4)
                    cannonball2.reparentTo(cannonball)
                    cannonball2.setPos(0, -4, -4)
                    cannonball3.reparentTo(cannonball)
                    cannonball3.setPos(0, 0, 4)
                    self.effectIval = cannonball.hprInterval(1.0, Point3(0, 0, 360), startHpr=Point3(0, 0, 0))
                    self.effectIval.loop()
                elif self.ammoSkillId == InventoryType.CannonGrappleHook:
                    cannonball = loader.loadModel('models/ammunition/GrapplingHook')
                    cannonball.flattenStrong()
                    prop = cannonball.getChild(0)
                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                        self.effectIval = Sequence(LerpHprInterval(prop, 2.0, Point3(0, 0, 360), startHpr=Point3(0, 0, 0)))
                        self.effectIval.loop()
                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                        self.createMotionTrails(self, self.small_vertex_list)
                    if base.options.getSpecialEffectsSetting() <= base.options.SpecialEffectsMedium:
                        self.createSimpleMotionTrail(self)
                elif self.ammoSkillId == InventoryType.CannonThunderbolt:
                    maxGlowScale = 19
                    minGlowScale = 15
                    cannonball = self.attachNewNode('cannonball')
                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                        self.trailEffect = ThunderBallGlow.getEffect()
                        if self.trailEffect:
                            self.trailEffect.reparentTo(cannonball)
                            self.trailEffect.setScale(0.5)
                            self.trailEffect.startLoop()
                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsHigh:
                        self.glowA = loader.loadModel('models/effects/flareRing')
                        self.glowA.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
                        self.glowA.setDepthWrite(0)
                        self.glowA.setFogOff()
                        self.glowA.setLightOff()
                        self.glowA.setBin('fixed', 120)
                        self.glowA.setColorScale(0.5, 0.8, 1, 0.5)
                        self.glowA.reparentTo(cannonball)
                        self.glowA.setBillboardPointEye()
                        scaleUp = self.glowA.scaleInterval(0.1, 4.5, startScale=3.5, blendType='easeInOut')
                        scaleDown = self.glowA.scaleInterval(0.1, 3.5, startScale=4.5, blendType='easeInOut')
                        self.glowATrack = Sequence(scaleUp, scaleDown)
                        self.glowATrack.loop()
                    if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsMedium:
                        self.createMotionTrails(self)
                    if base.options.getSpecialEffectsSetting() == base.options.SpecialEffectsLow:
                        self.createSimpleMotionTrail(self)
                elif self.ammoSkillId == InventoryType.CannonExplosive:
                    cannonball = loader.loadModel('models/ammunition/cannonball')
                else:
                    cannonball = loader.loadModel('models/ammunition/cannonball')
                    if self.ammoSkillId == InventoryType.CannonBullet:
                        cannonball.setColor(0.85, 0.85, 0.66, 1.0)
                    elif self.ammoSkillId == InventoryType.CannonGasCloud:
                        cannonball.setColor(0.55, 1.0, 0.58, 1.0)
                    elif self.ammoSkillId == InventoryType.CannonSkull:
                        cannonball.setColor(1.0, 0.55, 0.55, 1.0)
                    elif self.ammoSkillId == InventoryType.CannonFlameCloud:
                        cannonball.setColor(1.0, 0.1, 0.9, 1.0)
                    elif self.ammoSkillId == InventoryType.CannonBarShot:
                        cannonball.setColor(0.0, 0.1, 0.75, 1.0)
                    elif self.ammoSkillId == InventoryType.CannonKnives:
                        cannonball.setColor(0.98, 1.0, 0.35, 1.0)
                    elif self.ammoSkillId == InventoryType.CannonMine:
                        cannonball.setColor(0.69, 0.52, 0.19, 1.0)
                    elif self.ammoSkillId == InventoryType.CannonBarnacles:
                        cannonball.setColor(0.05, 0.65, 0.03, 1.0)
                if self.ammoSkillId == InventoryType.CannonGrapeShot:
                    cannonball.setScale(0.8)
                cannonball.setScale(2.0)
            if WeaponConstants.C_OPENFIRE in self.buffs:
                if base.options.getSpecialEffectsSetting() >= base.options.SpecialEffectsLow:
                    self.glowB = loader.loadModel('models/effects/lanternGlow')
                    self.glowB.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
                    self.glowB.setDepthWrite(0)
                    self.glowB.setFogOff()
                    self.glowB.setLightOff()
                    self.glowB.setBin('fixed', 120)
                    self.glowB.setColorScale(1, 0.8, 0.5, 0.9)
                    self.glowB.reparentTo(cannonball)
                    self.glowB.setBillboardPointEye()
                    scaleUp = self.glowB.scaleInterval(0.1, maxGlowScale, startScale=minGlowScale, blendType='easeInOut')
                    scaleDown = self.glowB.scaleInterval(0.1, minGlowScale, startScale=maxGlowScale, blendType='easeInOut')
                    self.glowBTrack = Sequence(scaleUp, scaleDown)
                    self.glowBTrack.loop()
        return cannonball

    def destroy(self):
        self.cleanupMotionTrails()
        if self.trailEffect:
            self.trailEffect.stopLoop()
            self.trailEffect = None
        if self.effectIval:
            self.effectIval.finish()
            self.effectIval = None
        if self.glowATrack:
            self.glowATrack.finish()
            self.glowATrack = None
        if self.glowBTrack:
            self.glowBTrack.finish()
            self.glowBTrack = None
        if self.rotateIval:
            self.rotateIval.finish()
            self.rotateIval = None
        ProjectileAmmo.destroy(self)
        return

    def createMotionTrails(self, parent, vertex_list=small_vertex_list, motion_color=default_motion_color):
        self.mtrail = PolyTrail(None, vertex_list, motion_color, 0.3)
        self.mtrail.setUnmodifiedVertexColors(motion_color)
        self.mtrail.reparentTo(parent)
        self.mtrail.motion_trail.geom_node_path.setTwoSided(False)
        self.mtrail.setBlendModeOn()
        self.mtrail.setTimeWindow(0.3)
        self.mtrail.beginTrail()
        return

    def createSimpleMotionTrail(self, parent):
        self.strail = loader.loadModel('models/effects/cannonTrail')
        self.strail.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.scaleIval = LerpScaleInterval(self.strail, 0.25, Vec3(3.3, 16, 3.3), startScale=Vec3(3.3, 3, 3.3))
        self.scaleIval.start()
        self.strail.setColorScale(0.2, 0.3, 0.5, 1.0)
        self.strail.reparentTo(parent)

    def cleanupMotionTrails(self):
        if self.mtrail:
            self.mtrail.destroy()
            self.mtrail = None
        if self.strail:
            self.strail.detachNode()
            self.strail = None
        if self.scaleIval:
            self.scaleIval.pause()
            self.scaleIval = None
        return