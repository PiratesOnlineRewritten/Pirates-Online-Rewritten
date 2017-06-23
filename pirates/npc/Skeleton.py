from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.showbase import ShadowPlacer
from direct.actor import Actor
from direct.fsm import ClassicFSM
from direct.fsm import State
from direct.distributed.ClockDelta import *
from otp.otpbase import OTPGlobals
from pirates.effects.DarkAura import DarkAura
from pirates.effects.SkeletonGlow import SkeletonGlow
from pirates.piratesbase import PiratesGlobals
from pirates.pirate import Biped, AvatarTypes
from pirates.pirate.BipedAnimationMixer import BipedAnimationMixer
from pirates.battle import EnemyGlobals
from direct.interval.IntervalGlobal import *
from pirates.effects.JRDeathEffect import JRDeathEffect
from pirates.effects.ShockwaveRing import ShockwaveRing
from pirates.effects.JRSpiritEffect import JRSpiritEffect
from pirates.makeapirate import NPCPirate
import random
AvType2style = {AvatarTypes.EarthUndead[0]: '1',AvatarTypes.EarthUndead[1]: '8',AvatarTypes.EarthUndead[2]: '4',AvatarTypes.EarthUndead[3]: '4',AvatarTypes.EarthUndead[4]: '1',AvatarTypes.EarthUndead[5]: '1',AvatarTypes.EarthUndead[6]: '2',AvatarTypes.EarthUndead[7]: '2',AvatarTypes.EarthUndead[8]: '8',AvatarTypes.EarthUndead[9]: '8',AvatarTypes.EarthUndead[10]: '1',AvatarTypes.EarthUndead[11]: '1',AvatarTypes.EarthUndead[12]: '2',AvatarTypes.EarthUndead[13]: '8',AvatarTypes.EarthUndead[14]: '4',AvatarTypes.AirUndead[0]: '1',AvatarTypes.AirUndead[1]: '2',AvatarTypes.AirUndead[2]: '8',AvatarTypes.AirUndead[3]: '1',AvatarTypes.AirUndead[4]: '2',AvatarTypes.AirUndead[5]: '8',AvatarTypes.AirUndead[6]: '1',AvatarTypes.AirUndead[7]: '2',AvatarTypes.AirUndead[8]: '8',AvatarTypes.AirUndead[9]: '4',AvatarTypes.FireUndead[0]: '1',AvatarTypes.FireUndead[1]: '2',AvatarTypes.FireUndead[2]: '8',AvatarTypes.FireUndead[3]: '1',AvatarTypes.FireUndead[4]: '2',AvatarTypes.FireUndead[5]: '8',AvatarTypes.FireUndead[6]: '1',AvatarTypes.FireUndead[7]: '2',AvatarTypes.FireUndead[8]: '8',AvatarTypes.FireUndead[9]: '4',AvatarTypes.WaterUndead[0]: 'djcr',AvatarTypes.WaterUndead[1]: 'djjm',AvatarTypes.WaterUndead[2]: 'djko',AvatarTypes.WaterUndead[3]: 'djpa',AvatarTypes.WaterUndead[4]: 'djtw',AvatarTypes.WaterUndead[5]: 'djcr',AvatarTypes.WaterUndead[6]: 'djjm',AvatarTypes.WaterUndead[7]: 'djko',AvatarTypes.WaterUndead[8]: 'djpa',AvatarTypes.WaterUndead[9]: 'djtw',AvatarTypes.FrenchUndead[0]: 'fr1',AvatarTypes.FrenchUndead[1]: 'fr2',AvatarTypes.FrenchUndead[2]: 'fr3',AvatarTypes.FrenchUndead[3]: 'fr4',AvatarTypes.FrenchUndead[4]: 'frb1',AvatarTypes.SpanishUndead[0]: 'sp1',AvatarTypes.SpanishUndead[1]: 'sp2',AvatarTypes.SpanishUndead[2]: 'sp3',AvatarTypes.SpanishUndead[3]: 'sp4',AvatarTypes.SpanishUndead[4]: 'spb1'}
AnimDict = {}
AnimListDict = {'djcr': Biped.DefaultAnimList,'djjm': Biped.DefaultAnimList,'djko': Biped.DefaultAnimList,'djpa': Biped.DefaultAnimList,'djtw': Biped.DefaultAnimList,'1': Biped.DefaultAnimList,'2': Biped.DefaultAnimList,'4': Biped.DefaultAnimList,'8': Biped.DefaultAnimList,'fr1': Biped.DefaultAnimList,'fr2': Biped.DefaultAnimList,'fr3': Biped.DefaultAnimList,'fr4': Biped.DefaultAnimList,'frb1': Biped.DefaultAnimList,'sp1': Biped.DefaultAnimList,'sp2': Biped.DefaultAnimList,'sp3': Biped.DefaultAnimList,'sp4': Biped.DefaultAnimList,'spb1': Biped.DefaultAnimList}
djcrCustomAnimList = [
 [
  'intro', '2']]
djjmCustomAnimList = [
 [
  'intro', '2']]
djkoCustomAnimList = [
 [
  'intro', '2']]
djpaCustomAnimList = [
 [
  'intro', '2']]
djtwCustomAnimList = [
 [
  'intro', '2']]
gp1CustomAnimList = [
 [
  'idle', '1'], ['intro', '2'], ['run', '1'], ['walk', '1']]
gp2CustomAnimList = [
 [
  'idle', '2'], ['intro', '2'], ['run', '2'], ['walk', '2']]
gp4CustomAnimList = [
 [
  'idle', '4'], ['intro', '2'], ['run', '4'], ['walk', '4']]
gp8CustomAnimList = [
 [
  'idle', '8'], ['intro', '2'], ['into_idle', '8'], ['run', '8'], ['walk', '8']]
frgp1CustomAnimList = [
 [
  'foil_coup', '1'], ['foil_hack', '1'], ['foil_idle', '1'], ['foil_slash', '1'], ['foil_thrust', '1'], ['foil_kick', '1'], ['sword_advance', '1'], ['walk', '1']]
frgp2CustomAnimList = [
 [
  'foil_coup', '1'], ['foil_hack', '1'], ['foil_idle', '1'], ['foil_slash', '1'], ['foil_thrust', '1'], ['foil_kick', '1'], ['sword_advance', '1'], ['walk', '1']]
frgp3CustomAnimList = [
 [
  'foil_coup', '1'], ['foil_hack', '1'], ['foil_idle', '1'], ['foil_slash', '1'], ['foil_thrust', '1'], ['foil_kick', '1'], ['sword_advance', '1'], ['walk', '1']]
frgp4CustomAnimList = [
 [
  'foil_coup', '1'], ['foil_hack', '1'], ['foil_idle', '1'], ['foil_slash', '1'], ['foil_thrust', '1'], ['foil_kick', '1'], ['sword_advance', '1'], ['walk', '1']]
spgp1CustomAnimList = [
 [
  'dualcutlass_comboA', '4'], ['dualcutlass_comboB', '4'], ['dualcutlass_draw', '4'], ['dualcutlass_idle', '4'], ['dualcutlass_hurt', '4'], ['dualcutlass_walk', '4']]
spgp2CustomAnimList = [
 [
  'dualcutlass_comboA', '4'], ['dualcutlass_comboB', '4'], ['dualcutlass_draw', '4'], ['dualcutlass_idle', '4'], ['dualcutlass_hurt', '4'], ['dualcutlass_walk', '4']]
spgp3CustomAnimList = [
 [
  'dualcutlass_comboA', '4'], ['dualcutlass_comboB', '4'], ['dualcutlass_draw', '4'], ['dualcutlass_idle', '4'], ['dualcutlass_hurt', '4'], ['dualcutlass_walk', '4']]
spgp4CustomAnimList = [
 [
  'dualcutlass_comboA', '4'], ['dualcutlass_comboB', '4'], ['dualcutlass_draw', '4'], ['dualcutlass_idle', '4'], ['dualcutlass_hurt', '4'], ['dualcutlass_walk', '4']]
CustomAnimDict = {'djcr': djcrCustomAnimList,'djjm': djjmCustomAnimList,'djko': djkoCustomAnimList,'djpa': djpaCustomAnimList,'djtw': djtwCustomAnimList,'1': gp1CustomAnimList,'2': gp2CustomAnimList,'4': gp4CustomAnimList,'8': gp8CustomAnimList,'fr1': frgp1CustomAnimList,'fr2': frgp2CustomAnimList,'fr3': frgp3CustomAnimList,'fr4': frgp4CustomAnimList,'frb1': frgp4CustomAnimList,'sp1': spgp1CustomAnimList,'sp2': spgp2CustomAnimList,'sp3': spgp3CustomAnimList,'sp4': spgp4CustomAnimList,'spb1': spgp4CustomAnimList}
SecondaryCustomAnimDict = {'djcr': [],'djjm': [],'djko': [],'djpa': [],'djtw': [],'1': [],'2': [],'4': [],'8': [],'fr1': gp1CustomAnimList,'fr2': gp2CustomAnimList,'fr3': gp8CustomAnimList,'fr4': gp4CustomAnimList,'frb1': gp4CustomAnimList,'sp1': gp1CustomAnimList,'sp2': gp2CustomAnimList,'sp3': gp8CustomAnimList,'sp4': gp4CustomAnimList,'spb1': gp4CustomAnimList}
ModelDict = {'djcr': 'models/char/dj_crash','djjm': 'models/char/dj_jimmylegs','djko': 'models/char/dj_koleniko','djpa': 'models/char/dj_palifico','djtw': 'models/char/dj_twins','1': 'models/char/jr_gp1','2': 'models/char/jr_gp2','4': 'models/char/jr_gp4','8': 'models/char/jr_gp3','fr1': 'models/char/fr_gp1','fr2': 'models/char/fr_gp2','fr3': 'models/char/fr_gp3','fr4': 'models/char/fr_gp4','frb1': 'models/char/fr_gp4','sp1': 'models/char/sp_gp1','sp2': 'models/char/sp_gp2','sp3': 'models/char/sp_gp3','sp4': 'models/char/sp_gp4','spb1': 'models/char/sp_gp4'}
SuffixDict = {'djcr': '_dj_cr','djjm': '_dj_jm','djko': '_dj_ko','djpa': '_dj_pa','djtw': '_dj_tw','1': '_gp','2': '_gp','4': '_gp','8': '_gp','fr1': '_fr_gp','fr2': '_fr_gp','fr3': '_fr_gp','fr4': '_fr_gp','frb1': '_fr_gp','sp1': '_sp_gp','sp2': '_sp_gp','sp3': '_sp_gp','sp4': '_sp_gp','spb1': '_sp_gp'}
SecondarySuffixDict = {'fr1': '_gp','fr2': '_gp','fr3': '_gp','fr4': '_gp','frb1': '_gp','sp1': '_gp','sp2': '_gp','sp3': '_gp','sp4': '_gp','spb1': '_gp'}

class Skeleton(Biped.Biped):
    animInfo = {}

    def __init__(self, animationMixerClass=BipedAnimationMixer):
        try:
            self.Skeleton_initialized
        except:
            self.Skeleton_initialized = 1
            Biped.Biped.__init__(self, animationMixerClass=animationMixerClass)
            self.loaded = 0
            self.dna = None
            self.shadowFileName = 'models/misc/drop_shadow'
            self.prevSpeedClock = 0
            self.overridingAnim = None
            self.overridingAnimMult = 1.0
            self.headFudgeHpr = Vec3(0, 0, 0)
            self.glow = None
            self.darkAura = None
            self.loadAnimatedHead = False
            self.deathEffect = None
            self.shockwaveRingIval = None
            self.shockwaveRingEffect = None
            self.spiritIval = None
            self.spiritEffect = None

        return

    def disable(self):
        self.cleanupEffects()

    def delete(self):
        try:
            self.Skeleton_deleted
        except:
            self.loaded = 0
            self.Skeleton_deleted = 1
            self.deleteDropShadow()
            self.model.delete()
            del self.model
            Biped.Biped.delete(self)
            self.undoExtraNodes()

    def cleanupEffects(self):
        if self.deathEffect:
            self.deathEffect.stop()
            self.deathEffect = None
        if self.shockwaveRingIval:
            self.shockwaveRingIval.pause()
            self.shockwaveRingIval = None
        if self.shockwaveRingEffect:
            self.shockwaveRingEffect.stop()
            self.shockwaveRingEffect = None
        if self.spiritIval:
            self.spiritIval.pause()
            self.spiritIval = None
        if self.spiritEffect:
            self.spiritEffect.stop()
            self.spiritEffect = None
        if self.darkAura:
            self.darkAura.finish()
            self.darkAura = None
        if self.glow:
            self.glow.destroy()
            self.glow = None
        return

    def setupNodes(self):
        self.headNode = self.controlJoint(None, 'modelRoot', 'def_head01', '1000')
        self.scaleNode = self.controlJoint(None, 'modelRoot', 'def_scale_jt', '1000')
        exposedHeadJoint = self.getLOD('1000').find('**/def_head01')
        if not exposedHeadJoint.isEmpty():
            self.headNode.reparentTo(exposedHeadJoint)
        return

    def undoExtraNodes(self):
        jointNameScale = 'def_scale_jt'
        if self.headNode:
            self.headNode.removeNode()
            self.headNode = None
        if not self.isEmpty():
            joints = self.findAllMatches('**/*' + jointNameScale)
            if not joints.isEmpty():
                joints.detach()
                joints.clear()
        if self.scaleNode:
            self.scaleNode.removeNode()
            self.scaleNode = None
        return

    def setLODs(self):
        self.setLODNode()
        avatarDetail = base.config.GetString('avatar-detail', 'high')
        if avatarDetail == 'high':
            dist = [
             0, 20, 80, 280]
        elif avatarDetail == 'med':
            dist = [
             0, 10, 40, 280]
        elif avatarDetail == 'low':
            dist = [
             0, 5, 20, 280]
        self.addLOD(1000, dist[1], dist[0])
        self.addLOD(500, dist[2], dist[1])
        self.addLOD(250, dist[3], dist[2])

    def generateSkeleton(self, type='g'):
        parent = self.getParent()
        self.detachNode()
        self.setLODs()
        self.model = NPCPirate.NPCPirate(self)
        self.generateSkeletonBody()
        self.setRenderReflection()
        self.loaded = 1
        self.setupNodes()
        self.getWeaponJoints()
        self.enableMixing()
        self.reparentTo(parent)

    def generateSkeletonBody(self, copy=1):
        filePrefix = ModelDict.get(self.style)
        animPrefix = 'models/char/mp'
        if filePrefix is None:
            self.notify.error('unknown body style: %s' % self.style)
        animList = AnimListDict[self.style]
        for anim in animList:
            animSuffix = ''
            for i in range(0, len(CustomAnimDict[self.style])):
                if anim[0] == CustomAnimDict[self.style][i][0]:
                    animSuffix = SuffixDict[self.style] + CustomAnimDict[self.style][i][1]
                    break
                else:
                    for j in range(0, len(SecondaryCustomAnimDict[self.style])):
                        if anim[0] == SecondaryCustomAnimDict[self.style][j][0]:
                            animSuffix = SecondarySuffixDict[self.style] + SecondaryCustomAnimDict[self.style][j][1]
                            break

            AnimDict[anim[0]] = animPrefix + '_' + anim[1] + animSuffix

        lodString = '1000'
        if loader.loadModel(filePrefix + '_' + '1000', okMissing=True) != None:
            lodString = '1000'
        self.loadModel(filePrefix + '_' + lodString, 'modelRoot', '1000', copy)
        if loader.loadModel(filePrefix + '_' + '500', okMissing=True) != None:
            lodString = '500'
        self.loadModel(filePrefix + '_' + lodString, 'modelRoot', '500', copy)
        if loader.loadModel(filePrefix + '_' + '250', okMissing=True) != None:
            lodString = '250'
        self.loadModel(filePrefix + '_' + lodString, 'modelRoot', '250', copy)
        self.loadAnims(AnimDict, 'modelRoot', 'all')
        self.makeSubpart('head', ['def_head_base', 'zz_head01'], [])
        self.makeSubpart('torso', ['zz_spine01'], ['zz_head01'])
        self.makeSubpart('legs', ['dx_root'], ['zz_spine01'])
        self.setSubpartsComplete(True)
        self.find('**/actorGeom').setH(180)
        self.flattenSkeleton()
        return

    def flattenSkeleton(self):
        for lodName in self.getLODNames():
            self.getPart('legs', lodName).flattenStrong()
            if lodName != '1000':
                exposedHeadJoint = self.getLOD(lodName).find('**/def_head01')
                if not exposedHeadJoint.isEmpty():
                    exposedHeadJoint.removeNode()

    def updateSkeletonDNA(self, newDNA, fForce=0):
        pass

    def setAvatarType(self, avatarType=AvatarTypes.EarthUndead[0]):
        if self.loaded:
            return
        self.avatarType = avatarType
        self.style = AvType2style[self.avatarType.getNonBossType()]
        self.generateSkeleton()
        self.initializeDropShadow()
        self.initializeNametag3d()
        self.setHeight(8.0)

    def scaleAnimRate(self, forwardSpeed):
        rate = 1.0
        myMaxSpeed = self.getMaxSpeed()
        if myMaxSpeed > 0 and forwardSpeed > 0:
            currTime = globalClockDelta.globalClock.getFrameTime()
            maxSpeed = myMaxSpeed * (currTime - self.prevSpeedClock)
            prevTime = self.prevSpeedClock
            self.prevSpeedClock = currTime
            rate = min(1.25, forwardSpeed / maxSpeed)
        return rate

    def getNametagJoints(self):
        joints = []
        for lodName in self.getLODNames():
            bundle = self.getPartBundle('legs', lodName)
            joint = bundle.findChild('name_tag')
            if joint:
                joints.append(joint)

        return joints

    def getMaxSpeed(self):
        return 0

    def getDeathAnimName(self, animNum=None):
        animStrings = [
         'death', 'death4']
        if animNum not in range(len(animStrings)):
            animNum = random.choice(range(0, len(animStrings)))
        return animStrings[animNum]

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.5), ('walk', 1.0), ('run', 1.0), ('walk', -1.0), ('strafe_left', 1), ('strafe_right', 1), ('run_diagonal_left', 1), ('run_diagonal_right', 1), ('walk_back_diagonal_left', 1), ('walk_back_diagonal_right', 1), ('fall_ground', 1), ('fall_ground', 1)))
        cls.setupAnimInfoState('WaterRoam', (('tread_water', 1.0), ('swim', 1.0), ('swim', 1.0), ('swim_back', 1.0), ('swim_left_diagonal', 1.0), ('swim_right_diagonal', 1.0), ('swim_left_diagonal', 1.0), ('swim_right_diagonal', 1.0), ('swim_back_diagonal_left', 1.0), ('swim_back_diagonal_right', 1.0), ('fall_ground', 1), ('fall_ground', 1)))
        cls.setupAnimInfoState('LandTreasureRoam', (('chest_idle', 1.0), ('chest_walk', 1.0), ('chest_walk', 1.0), ('chest_walk', -1.0), ('strafe_left', 1.0), ('strafe_right', 1.0), ('run_diagonal_left', 1), ('run_diagonal_right', 1), ('walk_back_diagonal_left', 1), ('walk_back_diagonal_right', 1), ('fall_ground', 1), ('fall_ground', 1)))
        cls.setupAnimInfoState('WaterRoam', (('tread_water', 1.0), ('swim', 1.0), ('swim', 1.0), ('swim_back', 1.0), ('swim_left_diagonal', 1.0), ('swim_right_diagonal', 1.0), ('swim_left_diagonal', 1.0), ('swim_right_diagonal', 1.0), ('swim_back_diagonal_left', 1.0), ('swim_back_diagonal_right', 1.0), ('fall_ground', 1), ('fall_ground', 1)))


Skeleton.setupAnimInfo()