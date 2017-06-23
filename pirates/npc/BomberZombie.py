from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.npc.Skeleton import Skeleton
from pirates.movement.AnimationMixer import AnimationMixer
from pirates.pirate.BipedAnimationMixer import BipedAnimationMixer
from pirates.pirate import AvatarTypes
AnimDict = {}

class BomberZombie(Skeleton):
    AnimList = (
     ('idle', 'idle'), ('idle_hit', 'idle_hit'), ('walk', 'walk'), ('walk_hit', 'walk_hit'), ('run', 'run'), ('run_hit', 'run_hit'), ('death', 'death'))

    class AnimationMixer(AnimationMixer):
        notify = DirectNotifyGlobal.directNotify.newCategory('BomberZombieAnimationMixer')
        LOOP = BipedAnimationMixer.LOOP
        ACTION = BipedAnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['IDLE'], LOOP['IDLE'], LOOP['IDLE']),'idle_hit': (ACTION['INPLACE_1'], ACTION['INPLACE_1'], ACTION['INPLACE_1']),'walk': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),'walk_hit': (ACTION['INMOTION_1'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),'run': (LOOP['MOTION'], LOOP['MOTION'], LOOP['MOTION']),'run_hit': (ACTION['INMOTION_1'], ACTION['INMOTION_1'], ACTION['INMOTION_1']),'death': (ACTION['MOVIE'], ACTION['MOVIE'], ACTION['MOVIE'])}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('walk', 1.0), ('run', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('walk', 1.0), ('run', 1.0)))

    def __init__(self):
        Skeleton.__init__(self, animationMixerClass=self.AnimationMixer)

    def setAvatarType(self, avatarType=AvatarTypes.BomberZombie):
        if self.loaded:
            return
        self.avatarType = avatarType
        self.style = 'bz'
        self.generateSkeleton()
        self.initializeDropShadow()
        self.initializeNametag3d()
        self.setHeight(8.0)

    def generateSkeletonBody(self, copy=1):
        filePrefix = 'models/char/jr_gp1'
        animPrefix = 'models/char/mp_zombie'
        animSuffix = '_gp2'
        if filePrefix is None:
            self.notify.error('unknown body style: %s' % self.style)
        animList = BomberZombie.AnimList
        for anim in animList:
            AnimDict[anim[0]] = animPrefix + '_' + anim[1] + animSuffix

        lodString = '1000'
        self.loadModel(filePrefix + '_' + lodString, 'modelRoot', '1000', copy)
        self.loadAnims(AnimDict, 'modelRoot', 'all')
        if loader.loadModel(filePrefix + '_' + '1000', okMissing=True) != None:
            lodString = '1000'
        self.loadModel(filePrefix + '_' + lodString, 'modelRoot', '1000', copy)
        if loader.loadModel(filePrefix + '_' + '500', okMissing=True) != None:
            lodString = '500'
        self.loadModel(filePrefix + '_' + lodString, 'modelRoot', '500', copy)
        if loader.loadModel(filePrefix + '_' + '250', okMissing=True) != None:
            lodString = '250'
        self.loadModel(filePrefix + '_' + lodString, 'modelRoot', '250', copy)
        self.makeSubpart('head', ['def_head_base'], [])
        self.makeSubpart('torso', ['zz_spine01'], ['def_head_base'])
        self.makeSubpart('legs', ['dx_root'], ['zz_spine01'])
        self.setSubpartsComplete(True)
        self.find('**/actorGeom').setH(180)
        self.flattenSkeleton()
        self.setLightOff(1)
        return

    def getDeathAnimName(self):
        return 'death'