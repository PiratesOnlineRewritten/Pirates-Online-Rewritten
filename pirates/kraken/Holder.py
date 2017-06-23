from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Creature import Creature
from pirates.kraken.TentacleUtils import TentacleUtils
from pirates.pirate import AvatarTypes
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.piratesbase import PiratesGlobals
from direct.actor import Actor
from direct.interval.IntervalGlobal import *

class Holder(Creature, TentacleUtils):
    ModelInfo = ('models/char/holderTentacle_high', 'models/char/holderTentacle_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({'pain': SoundGlobals.SFX_MONSTER_KRAKEN_PAIN,'death': SoundGlobals.SFX_MONSTER_KRAKEN_DEATH})
    sfx = {}
    AnimList = (
     ('idle', 'idle'), ('emerge', 'emerge'), ('release', 'release'), ('death', 'death'))

    class AnimationMixer(Creature.AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('CrabAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],),'emerge': (ACTION['ACTION'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', -1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', -1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0), ('idle', 1.0)))

    def __init__(self):
        Creature.__init__(self)
        TentacleUtils.__init__(self)
        self.collideBattleMask = PiratesGlobals.TargetBitmask | PiratesGlobals.WallBitmask | PiratesGlobals.BattleAimBitmask | PiratesGlobals.CameraBitmask
        if not Holder.sfx:
            for name in Holder.SfxNames:
                Holder.sfx[name] = loader.loadSfx('audio/' + Holder.SfxNames[name])

        self.hitIval = Sequence(self.colorScaleInterval(0.3, (1, 0, 0, 1), (1, 1, 1,
                                                                            1)), self.colorScaleInterval(0.3, (1,
                                                                                                               1,
                                                                                                               1,
                                                                                                               1), (1,
                                                                                                                    0,
                                                                                                                    0,
                                                                                                                    1)))

    def announceGenerate(self):
        self.initStatusTable()
        self.startUpdateTask()

    def uniqueName(self, name):
        return name + '-%s' % id(self)

    def disable(self):
        self.stopIdleTask()
        self.stopUpdateTask()
        self.removeEffects()

    @classmethod
    def setupAssets(cls):
        cls.animInfo = Creature.animInfo.copy()
        cls.setupAnimInfo()
        filePrefix = cls.ModelInfo[1]
        animList = cls.AnimList
        animDict = {}
        for anim in animList:
            animDict[anim[0]] = filePrefix + anim[1]

        cls.animDict = animDict
        filePrefix = cls.ModelInfo[1]
        for name in cls.SfxNames:
            cls.sfx[name] = loadSfx(cls.SfxNames[name])

        cls.actor = Actor.Actor()
        avatarDetail = base.config.GetString('avatar-detail', 'high')
        if avatarDetail == 'high':
            dist = [
             0, 1000, 4000, 24000]
        elif avatarDetail == 'med':
            dist = [
             0, 600, 3000, 24000]
        elif avatarDetail == 'low':
            dist = [
             0, 200, 2000, 24000]
        else:
            raise StandardError, 'Invalid avatar-detail: %s' % avatarDetail
        cls.actor.setLODNode()
        cls.actor.addLOD('hi', dist[1], dist[0])
        cls.actor.addLOD('med', dist[2], dist[1])
        cls.actor.addLOD('low', dist[3], dist[2])
        cls.actor.loadModel(filePrefix + 'high', 'modelRoot', 'hi')
        cls.actor.loadModel(filePrefix + 'medium', 'modelRoot', 'med')
        cls.actor.loadModel(filePrefix + 'low', 'modelRoot', 'low')
        cls.actor.loadAnims(cls.animDict, 'modelRoot', 'all')

    def setupCollisions(self):
        self.initStatusTable()
        self.findAllMatches('**/tube').detach()
        for i in range(len(self.statusTable)):
            self.setupCollisionNode(i)

    def setupCollisionNode(self, section):
        length = self.statusTable[section][0].getDistance(self.statusTable[section][1])
        cNode = CollisionNode('tube')
        cNode.addSolid(CollisionTube(Point3(0, 0, 0), Point3(length, 0, 0), len(self.statusTable) - section / 2.0 + 2.5))
        cNode.setFromCollideMask(BitMask32.allOff())
        cNode.setIntoCollideMask(self.collideBattleMask)
        self.statusTable[section][1].attachNewNode(cNode)

    def hit(self):
        self.hitIval.start()

    def initStatusTableBETA(self):
        self.statusTable = []
        if self.hasLOD():
            root = self.find('**/+LODNode').getChild(0)
        else:
            root = self
        jointList = [
         root.find('**/def_tent_03'), root.find('**/def_tent_05'), root.find('**/def_tent_06'), root.find('**/def_tent_08'), root.find('**/def_tent_10'), root.find('**/def_tent_12')]
        for i in range(len(jointList) - 1):
            self.statusTable.append([jointList[i], jointList[i + 1], 0, Vec3(0, 0, 0), [None, None, None, None]])

        return
