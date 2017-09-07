from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPRender
from pirates.creature.Creature import Creature
from pirates.kraken.TentacleUtils import TentacleUtils
from pirates.pirate import AvatarTypes
from pirates.audio import SoundGlobals
from pirates.piratesbase import PiratesGlobals
import math
import random

class Grabber(Creature, TentacleUtils):
    ModelInfo = ('models/char/grabberTentacle_high', 'models/char/grabberTentacle_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({'pain': SoundGlobals.SFX_MONSTER_KRAKEN_PAIN,'death': SoundGlobals.SFX_MONSTER_KRAKEN_DEATH})
    sfx = {}
    AnimList = (
     ('idle_d', 'idle'), ('idle_a', 'idleA'), ('idle_a_to_b', 'idle_alt_a_to_b'), ('idle_b', 'idleB'), ('idle_b_to_c', 'idle_alt_b_to_c'), ('idle_c', 'idleC'), ('idle_c_to_a', 'idle_alt_c_to_a'), ('grab_avatar', 'grab'), ('grab_avatar_idle', 'grab_idle'), ('lift_avatar', 'lift_player'), ('lift_avatar_idle', 'lift_player_idle'), ('lower_avatar', 'lower_player'), ('release_avatar', 'release_player'), ('emerge', 'emerge'), ('grab_mast', 'grab_mast'), ('grab_mast_idle', 'grab_mast_idle'), ('death', 'death'), ('hit_react', 'hit_reaction'), ('smackdown_avatar', 'smackdown_player'))

    class AnimationMixer(Creature.AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('CrabAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {'idle_d': (LOOP['LOOP'],),'idle_a_to_b': (ACTION['ACTION'],),'idle_b_to_c': (ACTION['ACTION'],),'idle_c_to_a': (ACTION['ACTION'],),'idle_a': (LOOP['LOOP'],),'idle_b': (LOOP['LOOP'],),'idle_c': (LOOP['LOOP'],),'grab_avatar': (ACTION['ACTION'],),'grab_avatar_idle': (LOOP['LOOP'],),'lift_avatar': (ACTION['ACTION'],),'lift_avatar_idle': (LOOP['LOOP'],),'lower_avatar': (ACTION['ACTION'],),'release_avatar': (ACTION['ACTION'],),'emerge': (ACTION['ACTION'],),'grab_mast': (ACTION['ACTION'],),'grab_mast_idle': (LOOP['LOOP'],),'death': (ACTION['ACTION'],),'hit_react': (ACTION['ACTION'],),'smackdown_avatar': (ACTION['ACTION'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', -1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', -1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))

    def __init__(self):
        Creature.__init__(self)
        TentacleUtils.__init__(self)
        self.collideBattleMask = PiratesGlobals.TargetBitmask | PiratesGlobals.BattleAimBitmask
        if not Grabber.sfx:
            for name in Grabber.SfxNames:
                Grabber.sfx[name] = loader.loadSfx('audio/' + Grabber.SfxNames[name])

        self.joints = None
        self.idle = None
        self.iTask = None
        self.hitIval = Sequence(
            self.colorScaleInterval(0.3, (1, 0, 0, 1), (1, 1, 1,1)), 
            self.colorScaleInterval(0.3, (1, 1, 1, 1), (1, 0, 0, 1)))
        self.generateCreature()
        self.target = loader.loadModel('models/misc/smiley')
        self.target.reparentTo(self.getGrabTargetNode())
        self.target.hide()
        self.enableMixing()
        return

    def generateCreature(self):
        filePrefix = self.ModelInfo[1]
        hasLOD = False
        if hasLOD:
            self.loadModel(filePrefix + 'hi', 'modelRoot', 'hi', copy=1)
            self.loadModel(filePrefix + 'med', 'modelRoot', 'med', copy=1)
            self.loadModel(filePrefix + 'low', 'modelRoot', 'low', copy=1)
            self.setLODs()
        else:
            self.loadModel(self.ModelInfo[0], copy=1)
        CreatureAnimDict = {}
        for anim in self.AnimList:
            CreatureAnimDict[anim[0]] = filePrefix + anim[1]

        if hasLOD:
            self.loadAnims(CreatureAnimDict, 'modelRoot', 'all')
        else:
            self.loadAnims(CreatureAnimDict)

    def announceGenerate(self):
        self.initStatusTable()
        self.startUpdateTask()

    def setupReflection(self):
        OTPRender.renderReflection(True, self, 'grabber', None)
        return

    def getJoints(self):
        if not self.joints:
            self.joints = self.findAllMatches('**/def_tent_*')
            self.joints.sort(key=NodePath.getName)
        return self.joints

    def showJoints(self):
        axis = loader.loadModel('models/misc/xyzAxis')
        axis.setBin('fixed', 100)
        axis.setDepthTest(0)
        joints = self.getJoints()
        for joint in joints:
            joint.get_children().detach()
            axis.instanceTo(joint.attachNewNode('buffer'))

    def uniqueName(self, name):
        return name + '-%s' % id(self)

    def disable(self):
        self.stopIdleTask()
        self.stopUpdateTask()
        self.removeEffects()

    def delete(self):
        pass

    def startIdleTask(self):
        self.stopIdleTask()
        if not self.idle:
            options = [
             'a', 'b', 'c', 'd']
            self.idle = random.choice(options)
            self.loop('idle_' + self.idle)
        self.iTask = self.doMethodLater(lerp(5, 20, random.random()), self.chooseIdle, `(random.random())` + '-idle')

    def chooseIdle(self, task):
        transInfo = {'a': {'b': ('idle_a_to_b', 1),'c': ('idle_c_to_a', -1)},'b': {'a': ('idle_a_to_b', -1),'c': ('idle_b_to_c', 1),'d': ('idle_a_to_b', -1)},'c': {'a': ('idle_c_to_a', 1),'b': ('idle_b_to_c', -1),'d': ('idle_a_to_b', -1)},'d': {'b': ('idle_a_to_b', 1),'c': ('idle_c_to_a', -1)}}
        options = ['a', 'b', 'c', 'd']
        options.remove(self.idle)
        next = random.choice(options)
        info = transInfo[self.idle].get(next)
        if info:
            transitionAnim, playRate = info
            self.setPlayRate(playRate, transitionAnim)
            self.play(transitionAnim, blendInT=0.5, blendOutT=0)
            self.loop('idle_' + next, rate=playRate, blendT=0, blendDelay=self.getDuration(transitionAnim))
        else:
            self.loop('idle_' + next)
        self.idle = next
        task.delayTime = lerp(5, 30, random.random())
        return task.again

    def stopIdleTask(self):
        if self.iTask:
            taskMgr.remove(self.iTask)
            self.iTask = None
        return

    def hit(self):
        self.hitIval.start()

    def setupCollisions(self):
        self.initStatusTable()
        self.findAllMatches('**/tube').detach()
        self.getGrabTipNode().findAllMatches('**/sphere').detach()
        for i in range(len(self.statusTable)):
            self.setupCollisionNode(i)

        cNode = CollisionNode('sphere')
        cNode.addSolid(CollisionSphere(Point3(0), 3))
        cNode.setFromCollideMask(BitMask32.allOff())
        cNode.setIntoCollideMask(BitMask32.allOff())
        sphere = self.getGrabTipNode().attachNewNode(cNode)
        sphere.setScale(1, 0.5, 1)
        sphere.show()

    def getGrabTargetNode(self):
        return self.find('**/grab_target')

    def getGrabTipNode(self):
        return self.find('**/tent_tip_pickup')

    def setupCollisionNode(self, section):
        length = self.statusTable[section][0].getDistance(self.statusTable[section][1])
        cNode = CollisionNode('tube')
        cNode.addSolid(CollisionTube(Point3(-5, 0, 0), Point3(length - 5, 0, 0), 3.5 + section / 2.0))
        cNode.setFromCollideMask(BitMask32.allOff())
        cNode.setIntoCollideMask(self.collideBattleMask)
        np = self.statusTable[section][1].attachNewNode(cNode)

    def initStatusTableBETA(self):
        self.statusTable = []
        if self.hasLOD():
            root = self.find('**/+LODNode').getChild(0)
        else:
            root = self
        jointList = [
         root.find('**/def_tent_01'), root.find('**/def_tent_04'), root.find('**/def_tent_07'), root.find('**/def_tent_10'), root.find('**/def_tent_14')]
        for i in range(len(jointList) - 1):
            self.statusTable.append([jointList[i], jointList[i + 1], 0, Vec3(0, 0, 0), [None, None, None, None]])

        return
