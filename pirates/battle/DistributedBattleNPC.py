from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.task import Task
from otp.otpbase import OTPGlobals
from pirates.uberdog.UberDogGlobals import *
from pirates.reputation.DistributedReputationAvatar import DistributedReputationAvatar
from pirates.battle.DistributedBattleAvatar import DistributedBattleAvatar
from pirates.battle import EnemyGlobals
from pirates.battle import WeaponGlobals
from pirates.pirate import BattleNPCGameFSM
from pirates.piratesbase import PiratesGlobals
from pirates.inventory import ItemGlobals
from pirates.piratesbase import PLocalizer
from pirates.pirate import AvatarTypes
from pirates.pirate import Biped
from pirates.leveleditor import CustomAnims
from pirates.battle import EnemySkills
from direct.showbase.PythonUtil import printStack
import random
import copy
import types
from direct.showbase import PythonUtil
from pirates.quest import QuestBase
from pirates.creature.Rooster import Rooster
from pirates.creature.Dog import Dog
from pirates.piratesbase import EmoteGlobals
propCache = {}

class DistributedBattleNPC(DistributedBattleAvatar):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedBattleNPC')
    deferrable = True

    def __init__(self, cr):
        NodePath.__init__(self, 'BattleNPC')
        DistributedBattleAvatar.__init__(self, cr)
        self.headTrack = None
        self.setNpc(1)
        self.lowEnd = base.options.getCharacterDetailSetting() == 0
        self.level = None
        self.cRay = None
        self.cRayNode = None
        self.cRayNodePath = None
        self.cRayBitMask = None
        self.lifter = None
        self.cTrav = None
        self.pusher = None
        self.floorChecksEnabled = False
        self.canCheckFloors = True
        self.cAggro = None
        self.cAggroNode = None
        self.cAggroNodePath = None
        self.cNotice = None
        self.cNoticeNode = None
        self.cNoticeNodePath = None
        self.noticeDistance = 35.0
        self.aggroSphereSize = None
        self.noticeSphereSize = None
        self.closeNoticeDistance = self.noticeDistance
        self.noticeIval = None
        self.noticeFlag = 0
        self.noticeSpeed = 0.5
        self.doneThreat = 0
        self.moveNoticeFlag = 0
        self.isMovingDontNotice = 0
        self.lastMovedTimeStamp = None
        self.shouldTurnToNotice = 1
        self.hasTurnedToNotice = 0
        self.localAvatarHasBeenNoticed = 0
        self.needNoticeGroundTracking = 0
        self.preselectedReaction = None
        self.usingPropNoNotice = 0
        self.noticeIdle = None
        self.respondedToLocalAttack = 0
        self.handler = None
        self.pendingBoardVehicle = None
        self.spawnIvals = []
        self.headingNode = self.attachNewNode('headingNode')
        self.enableZPrint = False
        self.animProp = None
        self.freezeTask = None
        self.animSet = 'default'
        self.animSetSetup = False
        self.loaded = 0
        self.lastSmoothPosUpdateTime = 0
        self.wantsActive = 0
        self.inInvasion = False
        self.isAlarmed = False
        self.alarmedAggroRadius = 0
        self.questMod = None
        self.altVisNode = None
        self.altVisType = None
        self.oldVisNode = None
        self.nearCallbacks = []
        self.skipLocalSmooth = False
        self.isPet = False
        return

    def __repr__(self):
        return '%s (Lvl %s)' % (self.getName(), self.level)

    def setAssociatedQuests(self, quests):
        self._associatedQuests = quests

    def getAnimStyleExtras(self):
        return []

    def setupCustomAnims(self, extraAnims=[]):
        if self.animSet != 'default':
            allAnims = copy.copy(CustomAnims.INTERACT_ANIMS.get(self.animSet))
            noticeAnims = []
            self.noticeAnim1 = allAnims.get('notice1', [self.noticeAnim1])[0]
            self.noticeAnim2 = allAnims.get('notice2', [self.noticeAnim2])[0]
            self.greetingAnim = allAnims.get('greeting', [self.greetingAnim])[0]
            if self.noticeAnim1:
                noticeAnims.append(self.noticeAnim1)
            if self.noticeAnim2:
                noticeAnims.append(self.noticeAnim2)
            if self.greetingAnim:
                noticeAnims.append(self.greetingAnim)
            if allAnims:
                if allAnims.has_key('walk'):
                    allAnims['walk'] = allAnims['walk'][:1]
                if allAnims.has_key('run'):
                    allAnims['run'] = allAnims['run'][:1]
                if allAnims.has_key('props'):
                    del allAnims['props']
                if allAnims.has_key('idles'):
                    for currIdle in allAnims['idles']:
                        allAnims[currIdle] = [
                         currIdle]

                    del allAnims['idles']
                if allAnims.has_key('extraAnims'):
                    for currAnim in allAnims['extraAnims']:
                        allAnims[currAnim] = [currAnim]

                    del allAnims['extraAnims']
                if self.startState != 'Idle':
                    allAnims.setdefault('walk', ['walk'])
                    allAnims.setdefault('walk_back_diagonal_left', ['walk_back_diagonal_left'])
                    allAnims.setdefault('walk_back_diagonal_right', ['walk_back_diagonal_right'])
                    allAnims.setdefault('run', ['run'])
                    allAnims.setdefault('run_diagonal_left', ['run_diagonal_left'])
                    allAnims.setdefault('run_diagonal_right', ['run_diagonal_right'])
            for anim in noticeAnims:
                allAnims[anim] = [
                 anim]

            for anim in self.getAnimStyleExtras():
                allAnims[anim] = [
                 anim]

            if extraAnims:
                for anim in extraAnims:
                    allAnims[anim] = [
                     anim]

            if allAnims:
                self.makeMyAnimDict(self.style.gender, allAnims)
            yieldThread('make Anims')

    def setupStyle(self):
        if self.style:
            self.setupCustomAnims()
            self.generateMyself()
            yieldThread('finished Gen')

    def addCustomAnimations(self, animList=[]):
        if self.style:
            self.setupCustomAnims(extraAnims=animList)
            self.generateMyself()
            yieldThread('finished Gen')

    def makeMyAnimDict(self, gender, animNames):
        pass

    def generateMyself(self):
        pass

    def setupActorAnims(self):
        if self.animSet != 'default' and self.animSetSetup == False:
            self.animSetSetup = True
            allAnims = CustomAnims.INTERACT_ANIMS.get(self.animSet)
            if allAnims == None:
                return
            allIdles = allAnims.get('idles')
            if type(allIdles) is dict:
                allAnims = allIdles.get(ItemGlobals.getSkillCategory(self.currentWeaponId))
                allIdles = allAnims.get('idles')
            allProps = allAnims.get('props')
            currChoice = random.choice(allIdles)
            animInfoCopy = copy.copy(Biped.Biped.animInfo)
            self.animInfo = animInfoCopy
            animStateNames = ['LandRoam', 'BayonetLandRoam']
            for currAnimState in animStateNames:
                oldAnimInfo = animInfoCopy.get(currAnimState)
                if oldAnimInfo == None:
                    continue
                newWalk, newWalkScale = allAnims.get('walk', [oldAnimInfo[1][0], oldAnimInfo[1][1]])
                newRun, newRunScale = allAnims.get('run', [oldAnimInfo[2][0], oldAnimInfo[2][1]])
                newAnimInfo = ((currChoice, oldAnimInfo[0][1]),) + ((newWalk, newWalkScale),) + ((newRun, newRunScale),) + oldAnimInfo[3:]
                if self.motionFSM.motionAnimFSM.state == currAnimState:
                    self.motionFSM.setAnimInfo(newAnimInfo)
                self.animInfo[currAnimState] = newAnimInfo
                yieldThread('custom anim info')

            self.holdAnimProp(allProps)
            self.noticeIdle = allAnims.get('noticeIdle', [None])[0]
            if self.canMove == False:
                self.canCheckFloors = False
            yieldThread('hold anim prop')
        return

    def announceGenerate(self):
        self.checkQuestObjMod()
        DistributedBattleAvatar.announceGenerate(self)
        if self.isPet:
            if self.battleTube:
                self.battleTube.setTangible(0)
            self.name = 'Pet ' + self.name
        if not self.loaded:
            self.setupStyle()
        self.setupActorAnims()
        self.setName(self.name)
        self.setPickable(0)
        self.accept('noticeStateChanged', self.handleNoticeChanged)
        self.accept('Local_Efficiency_Set', self.setEfficiency)
        if __dev__ and base.config.GetBool('show-aggro-radius', 0):
            if self.isBattleable():
                size = self.getAggroSphereSize()
                sphere = loader.loadModel('models/effects/explosion_sphere')
                sphere.reparentTo(self)
                sphere.setTransparency(1)
                sphere.setAlphaScale(0.3)
                sphere.setScale(render, size)
        if self.shadowPlacer:
            self.shadowPlacer.resetToOrigin()
            self.shadowPlacer.off()
        self.accept('questInterestChange-%s' % self.getUniqueId(), self.checkQuestObjMod, extraArgs=[True, True])
        self.accept('SwitchAgrroModel', self.handleAggroModelSwitch)
        self.setEfficiency(localAvatar.getEfficiency())

    def handleAggroModelSwitch(self):
        print 'handleAggroModelSwitch'
        self.updateCollisions()

    def checkQuestObjMod(self, doMod=True, interestChange=False):
        if self._associatedQuests and doMod:
            self.questMod = QuestBase.questObjMod(self._associatedQuests, self, localAvatar, self.cr)
            if self.questMod == 'hide':
                self.hide(invisibleBits=PiratesGlobals.INVIS_QUEST)
                self.disableBodyCollisions()
                self.disableBattleCollisions()
                self.setIgnoreProximity(True)
            elif self.questMod == 'show':
                self.show(invisibleBits=PiratesGlobals.INVIS_QUEST)
                self.enableBattleCollisions()
                self.updateCollisions()
            elif self.questMod and not interestChange:
                try:
                    eval('self.' + self.questMod[0] + '(' + self.questMod[1] + ')')
                except:
                    self.notify.warning('error executing npc mod funcion %s for quest %s' % (self.questMod, self._associatedQuests))

        return self.questMod

    def switchVisualMode(self, mode, skipHide=False):
        if self.altVisType == mode:
            return
        if mode == 'chickenFantifico':
            if not skipHide:
                self.getGeomNode().hide()
            self.isGhost = 0
            self.altVisType = mode
            self.altVisNode = Rooster()
            self.altVisNode.setAvatarType(AvatarTypes.Rooster)
            self.altVisNode.setScale(1.5)
            self.oldVisNode = self.getGeomNode()
            self.setGeomNode(self.attachNewNode(ModelNode('actorGeom')))
            self.altVisNode.reparentTo(self.getGeomNode())
            self.motionFSM.setAnimInfo(self.getAnimInfo('LandRoam'))
            self.style = None
            self.noticeAnim1 = 'crow'
            self.noticeAnim2 = ''
            self.greetingAnim = ''
        elif mode == 'notChickenFantifico':
            self.clearVisualMode(mode)
            self.isGhost = 1
            self.altVisType = mode
        return

    def clearVisualMode(self, visType=None):
        if self.oldVisNode:
            self.setGeomNode(self.oldVisNode)
            self.oldVisNode = None
        self.getGeomNode().show()
        self.altVisType = visType
        if self.altVisNode:
            self.altVisNode.removeNode()
            self.altVisNode = None
        self.motionFSM.setAnimInfo(self.getAnimInfo('LandRoam'))
        return

    def turnAggro(self):
        self.show(invisibleBits=PiratesGlobals.INVIS_QUEST)
        self.enableBattleCollisions()
        self.updateCollisions()
        self.setIgnoreProximity(False)
        self.nearCallbacks.append([self.sendUpdate, ['requestHostilize']])

    def turnFriendlyAndHide(self):
        self.hide(invisibleBits=PiratesGlobals.INVIS_QUEST)
        self.disableBodyCollisions()
        self.disableBattleCollisions()
        self.setIgnoreProximity(True)
        self.nearCallbacks = []

    def freezeShadow(self):
        self.shadowPlacer.off()
        self.freezeTask = None
        return

    def generate(self):
        DistributedBattleAvatar.generate(self)
        self.lastFloorCheckedXYZ = [0, 0, 0]

    def reparentTo(self, parent):
        DistributedBattleAvatar.reparentTo(self, parent)

    def wrtReparentTo(self, parent):
        DistributedBattleAvatar.wrtReparentTo(self, parent)

    def createGameFSM(self):
        self.gameFSM = BattleNPCGameFSM.BattleNPCGameFSM(self)

    def disable(self):
        if self.freezeTask:
            self.freezeTask.remove()
            self.freezeTask = None
        if self.pendingBoardVehicle:
            base.cr.relatedObjectMgr.abortRequest(self.pendingBoardVehicle)
            self.pendingBoardVehicle = None
        taskMgr.remove(self.uniqueName('removeCollisions'))
        taskMgr.remove(self.uniqueName('delayHelpCall'))
        self.ignore('Local_Efficiency_Set')
        self.ignoreAll()
        self.stopLookAt()
        self.disableBodyCollisions()
        if self.noticeIval:
            self.noticeIval.pause()
        self.noticeIval = None
        for currSpawnIval in self.spawnIvals:
            currSpawnIval.finish()

        self.spawnIvals = []
        self.nearCallbacks = []
        self.clearVisualMode()
        DistributedBattleAvatar.disable(self)
        return

    def delete(self):
        DistributedBattleAvatar.delete(self)

    def isDistributed(self):
        return 1

    def requestGameState(self, *args):
        self.gameFSM.request(*args)

    def setSpawnPos(self, x, y, z):
        pass

    def lookAtTarget(self, task=None):
        if self.currentTarget:
            self.headsUp(self.currentTarget)
            return Task.cont
        else:
            return Task.done

    def getUpdateLookAtTaskName(self):
        return self.taskName('lookAtTarget')

    def startLookAt(self):
        taskMgr.add(self.lookAtTarget, self.getUpdateLookAtTaskName())

    def stopLookAt(self):
        taskMgr.remove(self.getUpdateLookAtTaskName())

    def setLevel(self, level):
        if self.level is not None:
            return
        self.level = level
        enemyScale = self.getEnemyScale()
        self.height *= enemyScale
        self.setAvatarScale(self.scale * enemyScale)
        return

    def setMonsterNameTag(self):
        if self.isInInvasion():
            name = self.name
            if self.getNameText():
                self.getNameText()['text'] = name
        else:
            DistributedBattleAvatar.setMonsterNameTag(self)

    def setState(self, stateName, timeStamp):
        self.request(stateName)

    def boardVehicle(self, vehicleDoId):
        if self.pendingBoardVehicle:
            base.cr.relatedObjectMgr.abortRequest(self.pendingBoardVehicle)
            self.pendingBoardVehicle = None
        self.pendingBoardVehicle = base.cr.relatedObjectMgr.requestObjects([vehicleDoId], eachCallback=self.boardExistingVehicle)
        return

    def boardExistingVehicle(self, vehicle):
        self.reparentTo(vehicle.getModel())
        self.pendingBoardVehicle = None
        return

    def initializeBodyCollisions(self, collIdStr):
        pass

    def updateCollisions(self):
        self.cTrav = base.localAvatar.cTrav
        if self.collisionMode & PiratesGlobals.COLL_MODE_FLOORS_CL:
            if self.cRay == None:
                self.cRay = CollisionRay(0.0, 0.0, 4000.0, 0.0, 0.0, -1.0)
                self.cRayNode = CollisionNode(self.taskName('cRay'))
                self.cRayNode.addSolid(self.cRay)
                self.cRayNode.setFromCollideMask(PiratesGlobals.FloorBitmask | PiratesGlobals.ShipFloorBitmask)
                self.cRayNode.setIntoCollideMask(BitMask32.allOff())
                self.cRayNode.setBounds(BoundingSphere())
                self.cRayNode.setFinal(1)
                self.cRayNodePath = self.attachNewNode(self.cRayNode)
                self.lifter = CollisionHandlerGravity()
                self.lifter.setGravity(32.174 * 4.0)
                self.lifter.setReach(self.getFloorRayReach())
                self.lifter.setMaxVelocity(64.0)
                self.lifter.setInPattern('enterFloor%fn')
                self.lifter.setAgainPattern('againFloor%fn')
                hitFloorEvent = self.taskName('enterFloorcRay')
                againFloorEvent = self.taskName('againFloorcRay')
                self.accept(hitFloorEvent, self._hitFloorCallback)
                self.accept(againFloorEvent, self._hitFloorCallback)
        aggroSphereSize = self.getInstantAggroSphereSize()
        if aggroSphereSize != self.aggroSphereSize:
            if self.cAggro:
                self.cAggroNodePath.remove()
                self.cAggroNodePath = None
                self.cAggroNode = None
                self.cAggro = None
            self.aggroSphereSize = aggroSphereSize
        if self.cAggro == None and self.isBattleable() and aggroSphereSize > 0:
            self.cAggro = CollisionSphere(0, 0, 0, aggroSphereSize)
            self.cAggro.setTangible(0)
            self.cAggroNode = CollisionNode(self.uniqueName('AggroSphere'))
            self.cAggroNode.setFromCollideMask(BitMask32.allOff())
            self.cAggroNode.setIntoCollideMask(PiratesGlobals.WallBitmask)
            self.cAggroNode.addSolid(self.cAggro)
            self.cAggroNodePath = self.attachNewNode(self.cAggroNode)
            if base.config.GetBool('show-aggro-radius', 0):
                self.cAggroNodePath.show()
            if base.config.GetBool('npcs-auto-target', 1):
                enterCollEvent = self.uniqueName('enter' + 'AggroSphere')
                self.accept(enterCollEvent, self._handleEnterAggroSphere)
                if base.cr.gameStatManager.aggroModelIndex == 1:
                    self.accept('helpMeAggroThisPunk', self._handleAggroHelpRequested)
        noticeSphereSize = self.getEffectiveNoticeDistance()
        if noticeSphereSize != self.noticeSphereSize:
            if self.cNotice:
                self.cNoticeNodePath.remove()
                self.cAggroNodePath = None
                self.cNoticeNode = None
                self.cNotice = None
            self.noticeSphereSize = noticeSphereSize
        if self.cNotice == None and noticeSphereSize > 0:
            self.cNotice = CollisionSphere(0, 0, 0, noticeSphereSize)
            self.cNotice.setTangible(0)
            self.cNoticeNode = CollisionNode(self.uniqueName('NoticeSphere'))
            self.cNoticeNode.setFromCollideMask(BitMask32.allOff())
            if base.noticeSystemOn:
                self.cNoticeNode.setIntoCollideMask(PiratesGlobals.WallBitmask)
            else:
                self.cNoticeNode.setIntoCollideMask(BitMask32.allOff())
            self.cNoticeNode.addSolid(self.cNotice)
            self.cNoticeNodePath = self.attachNewNode(self.cNoticeNode)
            if base.config.GetBool('show-aggro-radius', 0):
                self.cNoticeNodePath.show()
            if base.config.GetBool('npcs-auto-target', 1):
                enterCollEvent = self.uniqueName('enter' + 'NoticeSphere')
                self.accept(enterCollEvent, self._handleEnterNoticeSphere)
        return

    def getEffectiveNoticeDistance(self):
        if base.cr.gameStatManager.aggroModelIndex == 1 and self.getTeam() not in [0, 4]:
            return self.getInstantAggroSphereSize() + self.noticeDistance
        else:
            return self.noticeDistance

    def handleNoticeChanged(self):
        if base.noticeSystemOn:
            self.cNoticeNode.setIntoCollideMask(PiratesGlobals.WallBitmask)
        else:
            self.cNoticeNode.setIntoCollideMask(BitMask32.allOff())
            self.abortNotice()

    def disableFloorChecks(self):
        if self.floorChecksEnabled and self.lifter:
            self.floorChecksEnabled = False
            self.cTrav.removeCollider(self.cRayNodePath)
            self.lifter.removeCollider(self.cRayNodePath)

    def enableFloorChecks(self):
        if self.canCheckFloors and self.floorChecksEnabled == False and self.lifter and (not self.ship or self.ship is localAvatar.ship):
            self.floorChecksEnabled = True
            self.lifter.addCollider(self.cRayNodePath, self)
            self.cTrav.addCollider(self.cRayNodePath, self.lifter)

    def performQuickFloorCheck(self, customReach=None):
        if self.cRayNodePath == None:
            self.notify.debug('aborting quick floor check for %s' % self.name)
            return
        self.notify.debug('performing quick floor check %s' % self.cRayNodePath)
        self.notify.debug('  myPos is %s' % self.getPos())
        if localAvatar.ship and self.ship is not localAvatar.ship:
            localAvatar.ship.stashPlaneCollisions()
        cTrav = CollisionTraverser('quickFloorCheck')
        floorRay = CollisionHandlerFloor()
        floorRay.setOffset(OTPGlobals.FloorOffset)
        if customReach != None:
            rayReach = customReach
        else:
            rayReach = self.getFloorRayReach()
        floorRay.setReach(rayReach)
        floorRay.addCollider(self.cRayNodePath, self)
        cTrav.addCollider(self.cRayNodePath, floorRay)
        cTrav.traverse(render)
        cTrav.removeCollider(self.cRayNodePath)
        floorRay.removeCollider(self.cRayNodePath)
        self.notify.debug('  quick floor check hasContact: %s' % floorRay.hasContact())
        self.notify.debug('  myPos NEW is %s' % self.getPos())
        self.lastFloorCheckedXYZ = [self.getX(), self.getY(), self.getZ()]
        if localAvatar.ship and self.ship is not localAvatar.ship:
            localAvatar.ship.unstashPlaneCollisions()
        return

    def disableBodyCollisions(self):
        if self.cRayNodePath:
            self.cTrav.removeCollider(self.cRayNodePath)
            self.floorChecksEnabled = False
            self.cRayNodePath.removeNode()
            self.cRayNodePath = None
        if self.cRayNode:
            self.cRayNode = None
        if self.cRay:
            self.cRay = None
        if self.lifter:
            self.lifter = None
        if self.cAggroNodePath:
            self.cTrav.removeCollider(self.cAggroNodePath)
            self.cAggroNodePath.removeNode()
            self.cAggroNodePath = None
        if self.cAggroNode:
            self.cAggroNode = None
        if self.cAggro:
            self.cAggro = None
        if self.handler:
            self.handler = None
        if self.cNoticeNodePath:
            self.cTrav.removeCollider(self.cNoticeNodePath)
            self.cNoticeNodePath.removeNode()
            self.cNoticeNodePath = None
        if self.cNoticeNode:
            self.cNoticeNode = None
        if self.cNotice:
            self.cNotice = None
        return

    def setIsAlarmed(self, isAlarmed, aggroRadius=0.0):
        self.isAlarmed = isAlarmed
        self.alarmedAggroRadious = aggroRadius
        if self.cAggro:
            if self.isAlarmed:
                self.cAggro.setRadius(aggroRadius)
            else:
                self.cAggro.setRadius(self.getInstantAggroSphereSize())

    def getIsAlarmed(self):
        return self.isAlarmed

    def sendRequestClientAggro(self):
        self.sendUpdate('requestClientAggro', [])

    def handleEnterProximity(self, collEntry):
        if self.nearCallbacks:
            for currCallback in self.nearCallbacks:
                currCallback[0](*currCallback[1])

            return
        DistributedBattleAvatar.handleEnterProximity(self, collEntry)

    def _handleEnterAggroSphere(self, collEntry):
        if localAvatar.getSiegeTeam():
            return
        if localAvatar.getGameState() in ('BenchRepair', 'PotionCrafting', 'Fishing'):
            return
        if not self.isBattleable():
            return
        skillEffects = self.getSkillEffects()
        if WeaponGlobals.C_SPAWN in skillEffects:
            return
        playerLevel = localAvatar.getLevel()
        if playerLevel <= EnemyGlobals.NEWBIE_AGGRO_LEVEL and not self.isAlarmed:
            return
        if base.cr.gameStatManager.aggroModelIndex == 1:
            self.delayedCallForHelp()
        self.sendRequestClientAggro()

    def delayedCallForHelp(self):
        taskMgr.doMethodLater(3.0, self.callForHelp, self.uniqueName('delayHelpCall'))

    def localAttackedMe(self):
        if self.respondedToLocalAttack:
            return
        else:
            self.respondedToLocalAttack = 1
            self.delayedCallForHelp()

    def callForHelp(self, task=None):
        messenger.send('helpMeAggroThisPunk', [self.doId])
        if task:
            return task.done

    def _handleAggroHelpRequested(self, allyDoId):
        if self.doId == allyDoId or self.respondedToLocalAttack:
            return
        ally = base.cr.doId2do.get(allyDoId)
        if ally:
            allyDistance = self.getDistance(ally)
            if allyDistance < EnemyGlobals.CALL_FOR_HELP_DISTANCE and self.getTeam() == ally.getTeam():
                self.sendRequestClientAggro()

    def _handleEnterNoticeSphere(self, collEntry):
        otherCollNode = collEntry.getFromNodePath()
        myCollNode = collEntry.getIntoNodePath()
        if not base.config.GetBool('want-npc-notice', 1):
            return
        if localAvatar.isInvisible():
            return
        if localAvatar.creatureTransformation and self.avatarType.isA(AvatarTypes.LandCreature):
            return
        skillEffects = self.getSkillEffects()
        if WeaponGlobals.C_SPAWN in skillEffects:
            return
        if self.isInInvasion():
            return
        self.firstNoticeLocalAvatar()
        self.noticeLocalAvatar()

    def shouldNotice(self):
        return localAvatar.getGameState() not in ['NPCInteract', 'Emote']

    def firstNoticeLocalAvatar(self):
        if not self.playNoticeAnims():
            return
        self.hasTurnedToNotice = 0
        self.localAvatarHasBeenNoticed = 1

    def abortNotice(self):
        if self.noticeIval:
            self.noticeFlag = 1
            self.noticeIval.pause()
            self.noticeFlag = 0
            self.doneThreat = 0
        self.noticeIval = None
        self.localAvatarHasBeenNoticed = 0
        return

    def endNotice(self):
        self.doneThreat = 0
        self.localAvatarHasBeenNoticed = 0

    def stateOkayForNotice(self):
        if self.getGameState() in ['LandRoam']:
            return 1
        return 0

    def noticeLocalAvatar(self):
        if self.isInInvasion() or self.getGameState() in ['Emote']:
            return
        if not self.shouldNotice() or self.isMovingDontNotice or self.noticeFlag:
            return
        if self.getDistance(localAvatar) > self.getEffectiveNoticeDistance() + 2.0 or not self.stateOkayForNotice():
            if self.gameFSM:
                pass
            self.endNotice()
            return
        heading = self.getHpr()
        if base.localAvatar.getGameState() == 'NPCInteract' and not (hasattr(self, 'dialogProcessMaster') and self.dialogProcessMaster):
            self.headsUp(base.camera)
        else:
            self.headsUp(localAvatar)
        if self.needNoticeGroundTracking:
            self.trackTerrain()
        noticeHeading = self.getHpr()
        self.setHpr(heading)
        angle = PythonUtil.fitDestAngle2Src(heading[0], noticeHeading[0])
        if self.needNoticeGroundTracking:
            newHpr = Vec3(angle, noticeHeading[1], noticeHeading[2])
        else:
            newHpr = Vec3(angle, heading[1], heading[2])
        noticeDif = abs(angle - heading[0])
        turnAnim = self.getTurnAnim(noticeDif)
        if self.noticeIval:
            self.noticeFlag = 1
            self.noticeIval.finish()
            self.noticeFlag = 0
            self.noticeIval = None
        if self.getDistance(localAvatar) > self.getEffectiveNoticeDistance() + 2.0:
            if self.hasTurnedToNotice:
                self.endNotice()
            else:
                self.noticeIval = Sequence(Wait(self.noticeSpeed), Func(self.noticeLocalAvatar))
                self.noticeIval.start()
        elif abs(noticeDif) > 15.0 and self.shouldTurnToNotice:
            if turnAnim:
                self.noticeIval = Sequence(Func(self.startShuffle, turnAnim), LerpHprInterval(self, duration=self.noticeSpeed, hpr=newHpr), Func(self.midShuffle), Wait(self.noticeSpeed), Func(self.endShuffle), Func(self.noticeLocalAvatar))
                self.noticeIval.start()
            else:
                self.noticeIval = Sequence(LerpHprInterval(self, duration=self.noticeSpeed, hpr=newHpr), Wait(self.noticeSpeed), Func(self.noticeLocalAvatar))
                self.noticeIval.start()
            self.doNoticeFX()
            self.hasTurnedToNotice = 1
        elif abs(noticeDif) < 45.0:
            duration = self.presetNoticeAnimation()
            if duration == None or self.doneThreat == 1:
                duration = self.noticeSpeed
            self.noticeIval = Sequence(Func(self.startNoticeLoop), Func(self.playNoticeAnim), Wait(duration), Func(self.endNoticeLoop), Func(self.noticeLocalAvatar))
            self.noticeIval.start()
            self.doNoticeFX()
        return

    def doNoticeFX(self):
        pass

    def presetNoticeAnimation(self):
        return 1.0

    def usableAnimInfo(self):
        if not hasattr(self, 'animInfo'):
            return None
        if self.altVisNode:
            return None
        return self.animInfo

    def getTurnAnim(self, noticeDif):
        turnAnim = 'walk'
        if self.usableAnimInfo():
            if noticeDif < 0:
                if len(self.animInfo['LandRoam']) + 1 >= PiratesGlobals.SPIN_LEFT_INDEX:
                    turnAnim = self.animInfo['LandRoam'][PiratesGlobals.SPIN_LEFT_INDEX][0]
            elif len(self.animInfo['LandRoam']) + 1 >= PiratesGlobals.SPIN_RIGHT_INDEX:
                turnAnim = self.animInfo['LandRoam'][PiratesGlobals.SPIN_RIGHT_INDEX][0]
        if turnAnim == 'idle':
            turnAnim = 'walk'
        return turnAnim

    def startShuffle(self, turnAnim):
        if self.playNoticeAnims():
            self.loop(turnAnim, blendDelay=0.3)
            self.motionFSM.motionAnimFSM.interruptSplash()

    def playNoticeAnims(self):
        if base.noticeSystemOn == 0:
            return 0
        return not self.isMovingDontNotice and self.motionFSM.motionAnimFSM.state == 'Idle'

    def midShuffle(self):
        if self.playNoticeAnims():
            if self.noticeIdle:
                self.loop(self.noticeIdle, blendDelay=0.3)
            else:
                self.loop('idle', blendDelay=0.3)

    def endShuffle(self):
        idleAnimInfo = self.animInfo['LandRoam'][PiratesGlobals.STAND_INDEX]
        if self.getCurrentAnim() == idleAnimInfo[0]:
            return
        try:
            self.loop(idleAnimInfo[0], blendDelay=0.3, rate=idleAnimInfo[1])
        except TypeError, e:
            self.notify.error('Invalid animation %s for %s|isInInvasion = %s|isGenerated = %s|mixer = %s' % (idleAnimInfo, `self`, self.isInInvasion(), self.isGenerated(), self._UsesAnimationMixer__mixer.__class__.__name__))

    def startNoticeLoop(self):
        pass

    def endNoticeLoop(self):
        pass

    def playNoticeAnim(self):
        if not self.doneThreat:
            self.doneThreat = 1

    def _hitFloorCallback(self, collEntry):
        self.floorNorm = collEntry.getInto().getNormal()
        self.disableFloorChecks()

    def canAggro(self):
        if self.aggroMode == EnemyGlobals.AGGRO_MODE_NEVER:
            return False
        return True

    def setupDebugCollisions(self):
        self.debugCSphere = CollisionSphere(0.0, 0.0, 0.0, 5)
        self.debugCSphere.setTangible(0)
        cSphereNode.addSolid(self.debugCSphere)
        self.debugCSphereNodePath = self.attachNewNode(cSphereNode)

    def cleanupDebugcollisions(self):
        if self.debugCSphereNodePath:
            self.debugCSphereNodePath.removeNode()
            del self.debugCSphereNodePath
            self.debugCSphereNodePath = None
        if self.debugCSphere:
            del self.debugCSphere
            self.debugCSphere = None
        return

    def _handleEnterSphereTest(self, collEntry):
        otherCollNode = collEntry.getFromNodePath()
        myCollNode = collEntry.getIntoNodePath()
        print 'NPC colliding me %s other %s' % (str(myCollNode), str(otherCollNode))

    def _handleAgainSphereTest(self, collEntry):
        print 'NPC colliding'

    def _handleExitSphereTest(self, collEntry):
        print 'NPC colliding'

    def updateMyAnimState(self, forwardVel, rotationVel, lateralVel):
        self.motionFSM.motionAnimFSM.updateNPCAnimState(forwardVel, rotationVel, lateralVel)

    def setSkipLocalSmooth(self, skip):
        self.skipLocalSmooth = skip

    def getSkipLocalSmooth(self):
        return self.skipLocalSmooth

    def smoothPosition(self):
        if self.skipLocalSmooth:
            if self.getGameState() not in ('Injured', 'Dying', 'Healing'):
                self.updateMyAnimState(0, 0, 0)
            return
        if not (self.invisibleMask & PiratesGlobals.INVIS_QUEST).isZero():
            return
        if self.lowEnd:
            DistributedBattleAvatar.smoothPosition(self)
            return
        cantMove = False
        if not self.canMove:
            cantMove = True
        parentObj = self.getParent()
        if cantMove == False:
            oldZ = self.getZ(parentObj)
            oldH = self.getH(parentObj)
            oldPos = self.getPos(parentObj)
        DistributedBattleAvatar.smoothPosition(self)
        if cantMove == False:
            if (self.getPos(parentObj) - oldPos).length() < 0.1:
                self.motionFSM.motionAnimFSM.updateNPCAnimState(0, 0, 0)
                if base.config.GetBool('want-npc-notice', 1) and abs(self.getH() - oldH) < 0.1:
                    if self.moveNoticeFlag and self.lastMovedTimeStamp and globalClock.getFrameTime() - self.lastMovedTimeStamp > 0.5 and not self.localAvatarHasBeenNoticed:
                        self.isMovingDontNotice = 0
                        self.firstNoticeLocalAvatar()
                        self.noticeLocalAvatar()
                        self.moveNoticeFlag = 0
                else:
                    self.lastMovedTimeStamp = globalClock.getFrameTime()
                return
            else:
                self.lastMovedTimeStamp = globalClock.getFrameTime()
                self.isMovingDontNotice = 1
                self.moveNoticeFlag = 1
                self.abortNotice()
            self.headingNode.reparentTo(parentObj)
            self.headingNode.setPos(oldPos)
            self.headingNode.setH(oldH)
            newPos = self.getPos(parentObj)
            if self.collisionMode & PiratesGlobals.COLL_MODE_FLOORS_CL:
                currZ = self.getZ()
                if abs(oldZ - currZ) <= 8:
                    self.setZ(parentObj, oldZ)
                else:
                    customReach = None
                    if currZ > oldZ:
                        customReach = self.getFloorRayReach() + (currZ - oldZ)
                        self.performQuickFloorCheck(customReach)
                self.headingNode.setZ(oldZ)
            inAttack = self.curAttackAnim and self.curAttackAnim.isPlaying()
            if inAttack:
                self.setH(parentObj, oldH)
            if self.enableZPrint:
                print '%s:  new z is %s, old z is %s' % (self.doId, newPos[2], oldZ)
            headingNodePos = self.headingNode.getPos()
            xDiff = abs(newPos[0] - headingNodePos[0])
            yDiff = abs(newPos[1] - headingNodePos[1])
            diffChangeLimitF = 0.01
            diffChangeLimitH = 0.075
            if self.getGameState() == 'Battle':
                diffChangeLimitH = 2.0
            if xDiff > diffChangeLimitF or yDiff > diffChangeLimitF:
                self.enableFloorChecks()
                if xDiff > diffChangeLimitH or yDiff > diffChangeLimitH and not inAttack:
                    self.headsUp(self.headingNode)
                    self.setH(self.getH() + 180)
            animTime = globalClock.getFrameTime()
            deltaTime = animTime - self.lastSmoothPosUpdateTime
            distMoved = self.headingNode.getDistance(self)
            if deltaTime <= 0:
                speed = 0
            else:
                speed = distMoved / deltaTime
            self.lastSmoothPosUpdateTime = animTime
            slideScale = 0.0
            if base.config.GetBool('npc-sidestep', 0) and distMoved > 0.005:
                moveVec = self.headingNode.getPos() - self.getPos(parentObj)
                self.headingNode.reparentTo(self)
                self.headingNode.setPos(0, 1, 0)
                self.headingNode.wrtReparentTo(parentObj)
                headVec = self.headingNode.getPos() - self.getPos(parentObj)
                moveAngle = headVec.relativeAngleRad(moveVec)
                cosVal = math.sin(moveAngle)
                slideScale = cosVal
            self.headingNode.reparentTo(hidden)
            if inAttack:
                hChange = 0.0
            else:
                hChange = self.getH(parentObj) - oldH
                if hChange and hChange < 0.1 and hChange > -0.1:
                    hChange = 0.0
            self.motionFSM.motionAnimFSM.updateNPCAnimState(speed, hChange, slideScale)
        if self.canCheckFloors == True and self.floorChecksEnabled == False and (self.getX() != self.lastFloorCheckedXYZ[0] or self.getY() != self.lastFloorCheckedXYZ[1] or self.getZ() != self.lastFloorCheckedXYZ[2]):
            self.performQuickFloorCheck()
        self.trackTerrain()
        return

    def getSpawnTrack(self):
        if self.checkQuestObjMod(doMod=False) == 'hide':
            return
        return DistributedBattleAvatar.getSpawnTrack(self)

    def setSpawnIn(self, timestamp):
        t = globalClockDelta.localElapsedTime(timestamp, bits=32)
        if t < 10:
            ival = self.getSpawnTrack()
            if ival:
                ival.start()
                self.spawnIvals.append(ival)
            else:
                ival = self.getFadeInTrack()
                if ival:
                    ival.start()
                    self.spawnIvals.append(ival)
        else:
            ival = self.getFadeInTrack()
            if ival:
                ival.start()
                self.spawnIvals.append(ival)

    def startLookAroundTask(self):
        pass

    def stopLookAroundTask(self):
        pass

    def b_setChat(self, chatString, chatFlags):
        messenger.send('wakeup')
        self.setChatAbsolute(chatString, chatFlags)
        self.d_setChat(chatString, chatFlags)

    def d_setChat(self, chatString, chatFlags):
        self.sendUpdate('setChat', [chatString, chatFlags])

    def setChat(self, chatString, chatFlags):
        chatFlags &= ~(CFQuicktalker | CFPageButton | CFQuitButton)
        if chatFlags & CFThought:
            chatFlags &= ~(CFSpeech | CFTimeout)
        else:
            chatFlags |= CFSpeech | CFTimeout
        self.setChatAbsolute(chatString, chatFlags)

    def getAggroRadius(self):
        if base.cr.activeWorld:
            return base.cr.activeWorld.getAggroRadius()
        return 0

    def getAggroSphereSize(self):
        if not self.canAggro():
            return 0
        playerLevel = base.localAvatar.getLevel()
        enemyLevel = self.getLevel()
        levelDiff = max(1, abs(playerLevel - enemyLevel) - EnemyGlobals.AGGRO_RADIUS_LEVEL_BUFFER)
        searchDist = self.getAggroRadius() / max(1.0, levelDiff / EnemyGlobals.AGGRO_RADIUS_FALLOFF_RATE)
        return max(searchDist, EnemyGlobals.MIN_SEARCH_RADIUS)

    def getInstantAggroSphereSize(self):
        if self.aggroRadius == EnemyGlobals.USE_DEFAULT_AGGRO:
            return self.getEffectiveAggroRadius()
        return self.aggroRadius

    def handleArrivedOnShip(self, ship):
        DistributedBattleAvatar.handleArrivedOnShip(self, ship)
        ship.battleNpcArrived(self)

    def handleLeftShip(self, ship):
        DistributedBattleAvatar.handleLeftShip(self, ship)
        ship.battleNpcLeft(self)

    def swapFloorCollideMask(self, oldMask, newMask):
        if self.cRayNode:
            collideMask = self.cRayNode.getFromCollideMask()
            collideMask = collideMask & ~oldMask
            collideMask |= newMask
            self.cRayNode.setFromCollideMask(collideMask)

    def onShipWithLocalAv(self, sameShip):
        if sameShip:
            self.enableFloorChecks()
        else:
            self.disableFloorChecks()

    def holdAnimProp(self, availProps):
        if self.isWeaponDrawn:
            return
        if availProps == None or len(availProps) == 0:
            return
        self.clearAnimProp()
        propPath = random.choice(availProps)
        propType = CustomAnims.PROP_TYPE_DYNAMIC
        if type(propPath) is types.ListType:
            propType = propPath[1]
            propPath = propPath[0]
        if propType == CustomAnims.PROP_TYPE_PERSIST:
            return
        if 'gator_high' in propPath:
            prop = None
        else:
            prop = self.getProp(propPath)
        if prop and not prop.isEmpty():
            if self.getName() == 'Captain Barbossa':
                handNode = self.leftHandNode
            else:
                handNode = self.rightHandNode
            if handNode == None:
                self.notify.warning('could not find hand to place prop %s in' % propPath)
                return
            prop.reparentTo(handNode)
            self.animProp = prop
            self.animPropType = propType
        else:
            self.notify.warning('could not load prop %s to be used with DistInteractiveProp' % propPath)
        return

    def getProp(self, propPath):
        model = propCache.get(propPath)
        if model:
            return model.copyTo(NodePath())
        else:
            prop = loader.loadModel(propPath)
            motion_blur = prop.find('**/motion_blur')
            if not motion_blur.isEmpty():
                motion_blur.stash()
            prop.flattenStrong()
            propCache[propPath] = prop
            return prop.copyTo(NodePath())

    def clearAnimProp(self):
        if self.animProp:
            animPropName = self.animProp.getName()
            allPropNodes = self.findAllMatches('**/' + animPropName)
            for node in allPropNodes:
                node.removeNode()

            self.animProp = None
        return

    def battleFX(self, effect):
        pass

    def setAggroMode(self, val):
        DistributedBattleAvatar.setAggroMode(self, val)
        if self.aggroMode == EnemyGlobals.AGGRO_MODE_DEFAULT or self.aggroMode == EnemyGlobals.AGGRO_MODE_CUSTOM:
            if self.cAggroNodePath:
                if self.cAggroNodePath.isStashed():
                    self.cAggroNodePath.unstash()
        elif self.cAggroNodePath:
            self.cAggroNodePath.stash()

    def resetAnimProp(self):
        allAnims = CustomAnims.INTERACT_ANIMS.get(self.animSet)
        if allAnims:
            allProps = allAnims.get('props')
            self.holdAnimProp(allProps)

    def motionFSMEnterState(self, state):
        if state == 'Idle':
            if self.animSet != 'default':
                allAnims = CustomAnims.INTERACT_ANIMS.get(self.animSet)
                if allAnims:
                    allProps = allAnims.get('props')
                    self.holdAnimProp(allProps)

    def motionFSMExitState(self, state):
        if state == 'Idle':
            self.clearAnimProp()

    def setAnimSet(self, animSet):
        self.animSet = animSet

    def setActorAnims(self, animSet, notice1, notice2, greet):
        self.animSet = animSet
        self.noticeAnim1 = notice1
        self.noticeAnim2 = notice2
        self.greetingAnim = greet
        if self.isGenerated():
            self.setupActorAnims()

    def requestAnimSet(self, animSet):
        if CustomAnims.INTERACT_ANIMS.has_key(animSet):
            idleAnim = CustomAnims.INTERACT_ANIMS.get(animSet).get('idles')[0]
            self.clearAnimProp()
            self.animSetSetup = False
            self.setupStyle()
            self.setupActorAnims()
            self.loop(idleAnim)

    def setCollisionMode(self, collisionMode):
        self.collisionMode = collisionMode
        self.updateCollisions()

    def setInitZ(self, z):
        self.initZ = z

    def playSkillMovie(self, skillId, ammoSkillId, skillResult, charge, targetId=0, areaIdList=[]):
        if self.currentTarget:
            self.headsUp(self.currentTarget)
        if targetId == 0 and self.currentTarget:
            targetId = self.currentTarget.doId
        DistributedBattleAvatar.playSkillMovie(self, skillId, ammoSkillId, skillResult, charge, targetId, areaIdList)

    def preprocessAttackAnim(self):
        if self.currentAttack[0] >= InventoryType.begin_WeaponSkillGrenade and self.currentAttack[0] < InventoryType.end_WeaponSkillGrenade:
            skillInfo = WeaponGlobals.getSkillAnimInfo(EnemySkills.EnemySkills.GRENADE_RELOAD)
            if not skillInfo:
                return
            anim = skillInfo[WeaponGlobals.PLAYABLE_INDEX]
            reloadAnim = getattr(self.cr.combatAnims, anim)(self, EnemySkills.EnemySkills.GRENADE_RELOAD, 0, 0, None, 1)
            if reloadAnim:
                self.curAttackAnim = Sequence(self.curAttackAnim, reloadAnim)
        return

    def checkWeaponSwitch(self, currentWeaponId, isWeaponDrawn):
        if isWeaponDrawn == self.isWeaponDrawn and currentWeaponId == self.currentWeaponId:
            self.setWalkForWeapon()
        DistributedBattleAvatar.checkWeaponSwitch(self, currentWeaponId, isWeaponDrawn)

    def getFloorRayReach(self):
        if self.ship:
            return 1000.0
        else:
            return 8.0

    def setShipId(self, shipId):
        DistributedBattleAvatar.setShipId(self, shipId)
        if self.lifter:
            self.lifter.setReach(self.getFloorRayReach())

    def setChatAbsolute(self, chatString, chatFlags, dialogue=None, interrupt=1):
        if not hasattr(self, 'nametag'):
            self.notify.warning('setChatAbsolute: no nametag, been deleted, but still trying to say something')
            printStack()
            return
        DistributedBattleAvatar.setChatAbsolute(self, chatString, chatFlags, dialogue, interrupt)

    def setGameState(self, gameState, timestamp=None, localArgs=[], localChange=0):
        DistributedBattleAvatar.setGameState(self, gameState, timestamp, localArgs)
        if self.dropShadow:
            self.dropShadow.setPos(self, (0, 0, 0))

    def setInInvasion(self, value):
        DistributedBattleAvatar.setInInvasion(self, value)
        if value:
            taskMgr.doMethodLater(5, self.removeCollisions, self.uniqueName('removeCollisions'))
            self.enableReducedMixing()
            self.setClipPlane(base.farCull)
            self.setMonsterNameTag()
            if base.config.GetBool('want-invasion-npc-minimap', 1):
                self.destroyMinimapObject()

    def removeCollisions(self, task=None):
        if self.battleTubeNodePaths:
            for np in self.battleTubeNodePaths:
                np.node().setIntoCollideMask(np.node().getIntoCollideMask() & ~PiratesGlobals.WallBitmask)

    def d_suggestResync(self, avId, timestampA, timestampB, serverTime, uncertainty):
        self.cr.timeManager.synchronize('suggested by %d' % avId)

    def setEfficiency(self, efficiency):
        if self.efficiency != efficiency:
            self.efficiency = efficiency
            if efficiency:
                self.enableReducedMixing()
            else:
                self.enableMixing()

    def setIsPet(self, isPet):
        self.isPet = isPet
        if isPet and self.creature:
            if not self.creature.nameText:
                self.scale = 2.0
                self.height = 4
                self.creature.initializeNametag3dPet()
            if self.avatarType.isA(AvatarTypes.Wasp):
                self.setAvatarScale(0.15)
                self.creature.nametag3d.setY(-3)
            if self.avatarType.isA(AvatarTypes.Dog):
                Dog.animDict['idle'] = 'models/char/dog_wag_standing_keys'
                self.creature.loadAnims(Dog.animDict, 'modelRoot', 'all')

    def playEmote(self, emoteId):
        from pirates.piratesbase import EmoteGlobals
        if self.isPet and emoteId == EmoteGlobals.EMOTE_DANCE_JIG:
            if self.avatarType == AvatarTypes.Chicken:
                self.loop('fly')
            elif self.avatarType == AvatarTypes.Dog:
                self.loop('wag_sitting')
            elif self.avatarType == AvatarTypes.Wasp:
                self.loop('idle')