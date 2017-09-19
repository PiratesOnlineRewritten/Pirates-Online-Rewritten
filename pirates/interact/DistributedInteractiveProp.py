from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.interval.IntervalGlobal import ActorInterval
from direct.distributed.ClockDelta import globalClockDelta
import re
import random
import types
from pirates.distributed import DistributedInteractive
from pirates.distributed import DistributedTargetableObject
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.interact import InteractiveBase
from pirates.pirate import BattleNPCGameFSM
from pirates.pirate import AvatarType
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.battle import WeaponGlobals
from pirates.leveleditor import CustomAnims
from pirates.interact import InteractivePropBase

class DistributedInteractiveProp(DistributedInteractive.DistributedInteractive, DistributedTargetableObject.DistributedTargetableObject, Actor.Actor, InteractivePropBase.InteractivePropBase):
    DiskUseColor = (1, 0, 0, 1)
    DiskWaitingColor = (1, 0, 0, 1)
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteractiveProp')
    WantHpCheck = base.config.GetBool('want-hp-check', 1)

    def __init__(self, cr):
        NodePath.__init__(self, 'DistributedInteractiveProp')
        DistributedInteractive.DistributedInteractive.__init__(self, cr)
        DistributedTargetableObject.DistributedTargetableObject.__init__(self, cr)
        Actor.Actor.__init__(self)
        self.__geomLoaded = 0
        self.anims = None
        self.uniqueId = ''
        self.parentObjId = None
        self.pendingPlacement = None
        self.battleTube = None
        self.name = 'Prop'
        self.interactSeq = None
        self.isNpc = 1
        self.interactAble = None
        self.interactType = None
        self.avId = None
        self.pendingMovie = None
        self.currentTarget = None
        self.skillEffects = []
        self.myIvals = {}
        return

    def generate(self):
        DistributedInteractive.DistributedInteractive.generate(self)
        DistributedTargetableObject.DistributedTargetableObject.generate(self)
        self.battleCollisionBitmask = PiratesGlobals.WallBitmask | PiratesGlobals.TargetBitmask | PiratesGlobals.RadarAvatarBitmask
        self.aimTubeNodePaths = []
        self.battleTubeNodePaths = []
        self.battleTubeRadius = 2.0
        self.battleTubeHeight = 5.0
        self.belongsToTeam = PiratesGlobals.TUTORIAL_ENEMY_TEAM
        self.avatarType = AvatarType.AvatarType()
        self.level = 1
        if self.WantHpCheck:
            self.__hp = 1
            self.__maxHp = 1
        else:
            self.hp = 1
            self.maxHp = 1

    if WantHpCheck:

        def get_hp(self):
            return self.__hp

        def set_hp(self, hp):
            if type(hp) in [types.IntType, types.FloatType]:
                self.__hp = hp
            else:
                self.__hp = 1

        hp = property(get_hp, set_hp)

        def get_maxHp(self):
            return self.__maxHp

        def set_maxHp(self, maxHp):
            if type(maxHp) in [types.IntType, types.FloatType]:
                self.__maxHp = maxHp
            else:
                self.__maxHp = 1

        maxHp = property(get_maxHp, set_maxHp)

    def announceGenerate(self):
        DistributedInteractive.DistributedInteractive.announceGenerate(self)
        DistributedTargetableObject.DistributedTargetableObject.announceGenerate(self)
        myParentId = self.getLocation()[0]
        myParent = self.cr.doId2do[myParentId]
        self.reparentTo(myParent)
        self.gameFSM = BattleNPCGameFSM.BattleNPCGameFSM(self)
        self.motionFSM = None
        self.loadGeom()
        self.setName(PLocalizer.PracticeDummy)
        self.cr.uidMgr.addUid(self.uniqueId, self.getDoId())
        self.initInteractOpts()
        self.initializeBattleCollisions()
        return

    def setModelPath(self, modelPath):
        self.notify.debug('setModelPath %s' % modelPath)
        self.modelPath = modelPath

    def loadGeom(self):
        if self.__geomLoaded:
            return
        if re.search('_zero', self.modelPath):
            self.geom = self.loadModel(self.modelPath)
            modelPrefix = re.sub('_zero', '', self.modelPath)
            self.anims = self.loadAnims({'idle': modelPrefix + '_idle','boxing_hit_head_right': modelPrefix + '_hit_medium','deathIdle': modelPrefix + '_death_idle',self.getDeathAnimName(): modelPrefix + '_death'})
            self.loop('idle')
        else:
            self.geom = loader.loadModel(self.modelPath)
            lod = self.geom.find('**/+LODNode')
            if lod:
                lodNode = lod.node()
                switch = lodNode.getNumSwitches() - 1
                if switch >= 0:
                    outVal = lodNode.getOut(switch)
                    inVal = max(lodNode.getIn(switch), 100000)
                    lodNode.setSwitch(switch, inVal, outVal)
            self.geom.reparentTo(self)
        self.__geomLoaded = 1

    def unloadGeom(self):
        if not self.isEmpty() and self.anims:
            self.unloadAnims(self.anims)
        self.__geomLoaded = 0

    def setParentObjId(self, parentObjId):
        self.parentObjId = parentObjId

        def putObjOnParent(parentObj, self=self):
            self.notify.debug('putObj %s on parent %s' % (self.doId, parentObj))
            self.parentObj = parentObj
            self.reparentTo(parentObj)
            self.pendingPlacement = None
            return

        if parentObjId > 0:
            self.pendingPlacement = base.cr.relatedObjectMgr.requestObjects([self.parentObjId], eachCallback=putObjOnParent)

    def initInteractOpts(self):
        if self.interactAble == 'player':
            self.setInteractOptions(sphereScale=6, diskRadius=8, allowInteract=False, isTarget=True)

    def disable(self):
        if self.pendingMovie:
            self.cr.relatedObjectMgr.abortRequest(self.pendingMovie)
        if self.interactSeq:
            self.interactSeq.pause()
            self.interactSeq = None
        self.unloadGeom()
        taskMgr.remove(self.uniqueName('playReact'))
        self.deleteBattleCollisions()
        self.cleanupMovies()
        self.avId = None
        DistributedInteractive.DistributedInteractive.disable(self)
        DistributedTargetableObject.DistributedTargetableObject.disable(self)
        self.gameFSM.cleanup()
        return

    def delete(self):
        DistributedInteractive.DistributedInteractive.delete(self)
        DistributedTargetableObject.DistributedTargetableObject.delete(self)
        Actor.Actor.delete(self)

    def requestInteraction(self, avId, interactType=0):
        DistributedInteractive.DistributedInteractive.requestInteraction(self, avId, interactType)
        base.localAvatar.setCurrentTarget(self.doId)

    def initializeBattleCollisions(self):
        if self.interactAble != 'player' or self.battleTubeNodePaths:
            return
        self.battleTubeEvent = self.uniqueName('battleAvatarTube')
        self.battleTube = CollisionTube(0, 0, 0, 0, 0, self.battleTubeHeight, self.battleTubeRadius)
        self.battleTube.setTangible(1)
        battleTubeNode = CollisionNode(self.battleTubeEvent)
        battleTubeNode.addSolid(self.battleTube)
        battleTubeNode.setIntoCollideMask(self.battleCollisionBitmask)
        battleTubeNodePath = self.attachNewNode(battleTubeNode)
        battleTubeNodePath.setTag('objType', str(PiratesGlobals.COLL_AV))
        battleTubeNodePath.setTag('avId', str(self.doId))
        self.aimTubeEvent = self.uniqueName('aimTube')
        aimTube = CollisionTube(0, 0, 0, 0, 0, self.battleTubeHeight, self.battleTubeRadius * 1.5)
        aimTube.setTangible(0)
        aimTubeNode = CollisionNode(self.aimTubeEvent)
        aimTubeNode.addSolid(aimTube)
        aimTubeNode.setIntoCollideMask(PiratesGlobals.BattleAimBitmask)
        aimTubeNodePath = self.attachNewNode(aimTubeNode)
        aimTubeNodePath.setTag('objType', str(PiratesGlobals.COLL_AV))
        aimTubeNodePath.setTag('avId', str(self.doId))
        self.cr.targetMgr.addTarget(aimTubeNodePath.get_key(), self)
        self.aimTubeNodePaths.append(aimTubeNodePath)
        self.battleTubeNodePaths.append(battleTubeNodePath)

    def deleteBattleCollisions(self):
        if self.battleTube:
            self.battleTube = None
        for np in self.battleTubeNodePaths:
            np.removeNode()

        self.battleTubeNodePaths = []
        for np in self.aimTubeNodePaths:
            if hasattr(self.cr, 'targetMgr'):
                self.cr.targetMgr.removeTarget(np.get_key())
            np.removeNode()

        self.aimTubeNodePaths = []
        return

    def getTeam(self):
        return self.belongsToTeam

    def getLevel(self):
        return self.level

    def targetedWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, attacker, pos, charge=0, delay=None, multihit=0, itemEffects=[]):
        if skillResult in [WeaponGlobals.RESULT_HIT, WeaponGlobals.RESULT_MISTIMED_HIT] and (skillId == InventoryType.CutlassSlash or skillId == InventoryType.CutlassSweep):
            if base.config.GetBool('want-easy-combos', 1):
                if skillResult == WeaponGlobals.RESULT_HIT:
                    self.gameFSM.request('Death')
            else:
                self.gameFSM.request('Death')
        DistributedTargetableObject.DistributedTargetableObject.targetedWeaponHit(self, skillId, ammoSkillId, skillResult, targetEffects, attacker, pos, charge, delay, multihit)

    def getDeathAnimName(self, animNum=None):
        return 'death'

    def getDeathTrack(self):
        animName = self.getDeathAnimName()
        duration = self.getDuration(animName)
        deathIval = Parallel(Func(self.setTransparency, 1), self.actorInterval(animName), Sequence(Wait(duration / 2.0), LerpColorScaleInterval(self, duration / 2.0, Vec4(1, 1, 1, 0), startColorScale=Vec4(1)), Func(self.hide), Func(self.clearColorScale), Func(self.clearTransparency)))
        return deathIval

    def getSkillEffects(self):
        return []

    def rebuild(self):
        if not self.isDisabled():
            self.loop('idle')
            if not self.gameFSM.isInTransition():
                self.gameFSM.request('Off')
            self.initializeBattleCollisions()
            self.show()

    def moveSelf(self, xyz):
        randX = random.random() * 0.3 - 0.15
        randY = random.random() * 0.3 - 0.15
        randZ = random.random() * 0.3 - 0.15
        self.setPos(xyz[0] + randX, xyz[1] + randY, xyz[2] + randZ)
        self.setH(self.getH() - random.random() * 6)
        self.setP(random.random() * 7)
        self.setR(random.random() * 7)

    def finishInteraction(self, xyzhpr):
        self.setPos(xyzhpr[0])
        self.setP(xyzhpr[1][1])
        self.setR(xyzhpr[1][2])

    def playInteraction(self, task=None):
        currPos = self.getPos()
        currHpr = self.getHpr()
        currPosX = currPos[0]
        currPosY = currPos[1]
        currPosZ = currPos[2]
        currH = currHpr[0]
        currP = currHpr[1]
        currR = currHpr[2]
        self.interactSeq = Sequence(Func(self.moveSelf, (currPosX, currPosY, currPosZ)), Wait(0.05), Func(self.moveSelf, (currPosX, currPosY, currPosZ)), Wait(0.05), Func(self.moveSelf, (currPosX, currPosY, currPosZ)), Wait(0.05), Func(self.moveSelf, (currPosX, currPosY, currPosZ)), Wait(0.05), Func(self.moveSelf, (currPosX, currPosY, currPosZ)), Wait(0.05), Func(self.moveSelf, (currPosX, currPosY, currPosZ)), Wait(0.05), Func(self.finishInteraction, (VBase3(currPosX, currPosY, currPosZ), (currH, currP, currR))))
        self.interactSeq.start()

    def setMovie(self, avId, timestamp):
        if avId == 0:
            self.stopMovie(timestamp)
            return
        av = self.cr.doId2do.get(avId)
        self.avId = avId
        if av:
            self.playMovie(av, timestamp)
        else:
            self.pendingMovie = base.cr.relatedObjectMgr.requestObjects([avId], eachCallback=Functor(self.playPendingMovie, timestamp))

    def playPendingMovie(self, timestamp, av):
        self.playMovie(av, timestamp)

    def createTransitionIval(self, av, animType, transitionBeginCallback=None, transitionEndCallback=None):
        availAnims = CustomAnims.INTERACT_ANIMS.get(self.interactType)
        if availAnims == None:
            self.notify.warning('undefined interaction type %s, not found in CustomAnims.INTERACT_ANIMS' % self.interactType)
        else:
            transAnims = availAnims.get(animType, [''])
            transAnim = random.choice(transAnims)
        transitionIval = Sequence()
        if transitionBeginCallback:
            transitionIval.append(Func(transitionBeginCallback))
        transitionIval.append(av.actorInterval(transAnim, blendInT=0, blendOutT=0))
        if transitionEndCallback:
            transitionIval.append(Func(transitionEndCallback))
        return transitionIval

    def cleanupMovies(self):
        for currIval in self.myIvals.values():
            currIval.pause()

        self.myIvals = {}

    def stopMovie(self, timestamp):
        av = self.cr.doId2do.get(self.avId)
        if av:

            def endInteractSetup():

                def blah(task=None):
                    av.loop(av.getAnimInfo('LandRoam')[PiratesGlobals.STAND_INDEX][0])
                    self.adjustPos(av)
                    return task.done

                taskMgr.doMethodLater(0, blah, self.uniqueName('blahadjustpos'))
                return

            def endInteractCleanup():
                av.canMove = True
                av.startSmooth()
                av.motionFSM.request('On')
                av.clearAnimProp()
                av.usingPropNoNotice = 0
                del self.myIvals[self.avId]
                self.avId = None
                return

            self.cleanupMovies()
            ival = self.createTransitionIval(av, 'idleOutof', transitionBeginCallback=endInteractSetup, transitionEndCallback=endInteractCleanup)
            ival.start(startT=globalClockDelta.localElapsedTime(timestamp, bits=32))
            self.myIvals[self.avId] = ival

    def playMovie(self, av, timestamp):
        self.pendingMovie = None
        av.stopSmooth()
        av.motionFSM.request('Off')
        availAnims = CustomAnims.INTERACT_ANIMS.get(self.interactType)
        availProps = None
        if availAnims == None:
            self.notify.warning('undefined interaction type %s, not found in CustomAnims.INTERACT_ANIMS' % self.interactType)
        else:
            availProps = availAnims.get('props')
            availIdles = availAnims.get('idles')
            intoAnims = availAnims.get('idleInto', [''])
        self.interactAnim = random.choice(availIdles)

        def interactSetup():
            av.usingPropNoNotice = 1
            av.abortNotice()
            self.adjustPos(av)
            av.loop(self.interactAnim)

        def playInteract():
            if self.interactType == 'hit':
                av.play(self.interactAnim)
                if self.interactAnim == 'boxing_kick':
                    reactDelay = 0.43
                else:
                    reactDelay = 0.4
                taskMgr.doMethodLater(reactDelay, self.playInteraction, self.uniqueName('playReact'))
            else:
                if self.interactType == 'sit':
                    av.loop(self.interactAnim, blendT=av.motionFSM.BLENDAMT)
                    posOffset, hprOffset = self.getLocatorOffset(av.getParent())
                    av.setPos(posOffset[0], posOffset[1], posOffset[2])
                    av.setHpr(hprOffset[0], hprOffset[1], hprOffset[2])
                elif self.interactType == 'stockade':
                    av.loop(self.interactAnim, blendT=av.motionFSM.BLENDAMT)
                    myPos = self.getPos(av.getParent())
                    myHpr = self.getHpr(av.getParent())
                    av.setPos(myPos[0], myPos[1], myPos[2])
                    av.setHpr(myHpr[0], myHpr[1], myHpr[2])
                else:
                    av.loop(self.interactAnim, blendT=0)
                    posOffset, hprOffset = self.getLocatorOffset(av.getParent())
                    if self.interactType not in PiratesGlobals.INTERACT_TYPES_WITHOUT_FORCE_POS:
                        av.setPos(posOffset[0], posOffset[1], posOffset[2])
                        av.setHpr(hprOffset[0], hprOffset[1], hprOffset[2])
                if availProps:
                    av.holdAnimProp(availProps)
            av.interactAnim = self.interactAnim
            del self.myIvals[self.avId]
            av.canMove = False
            self.sendUpdate('inPosition')

        self.cleanupMovies()
        ival = self.createTransitionIval(av, 'idleInto', interactSetup, playInteract)
        startTime = globalClockDelta.localElapsedTime(timestamp, bits=32)
        ival.start(startT=startTime)
        self.myIvals[self.avId] = ival
        return

    def getLocatorOffset(self, avParent):
        dummyNode = self.attachNewNode('dummyNode')
        if self.modelPath == 'models/props/chair_fancy':
            dummyNode.setX(1.75)
            dummyNode.setY(-1.0)
            dummyNode.setH(180)
        elif self.modelPath == 'models/props/chair_bank':
            dummyNode.setX(1.75)
            dummyNode.setY(-1.25)
            dummyNode.setH(180)
        elif self.modelPath == 'models/props/chair_shanty':
            dummyNode.setX(2.0)
            dummyNode.setY(-0.5)
            dummyNode.setH(180)
        elif self.modelPath == 'models/props/chair_bar':
            dummyNode.setX(1.75)
            dummyNode.setY(-0.5)
            dummyNode.setH(180)
        elif self.modelPath == 'models/props/pir_m_prp_cnt_crate_ravensCove':
            dummyNode.setH(180)
        else:
            locatorNode = self.find('**/avatar_position')
            if locatorNode and not locatorNode.isEmpty():
                dummyNode.reparentTo(locatorNode)
                dummyNode.setH(180)
        posOffset = dummyNode.getPos(avParent)
        hprOffset = dummyNode.getHpr(avParent)
        dummyNode.removeNode()
        return [
         posOffset, hprOffset]

    def setInteractAble(self, interactAble):
        self.interactAble = interactAble

    def setInteractType(self, interactType):
        self.interactType = interactType

    def propSlashed(self):
        if not base.config.GetBool('want-easy-combos', 1):
            messenger.send('didSlash')

    def propSlashedBonus(self):
        if base.config.GetBool('want-easy-combos', 1):
            messenger.send('didSlash')

    def getShortName(self):
        return self.getName()

    def isBoss(self):
        return False

    def isInInvasion(self):
        return False

    def getArmorScale(self):
        return 1.0

    def getMinimapObject(self):
        return None

    def destroyMinimapObject(self):
        pass

    def getAvatarType(self):
        return self.avatarType