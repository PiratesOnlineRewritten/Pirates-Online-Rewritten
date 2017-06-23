import time
import random
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.fsm import FSM
from direct.actor import Actor
from direct.task import Task
from direct.distributed import DistributedObject
from direct.showbase.PythonUtil import DelayedCall
import ShipWreck
from pirates.audio import SoundGlobals
from pirates.npc import Skeleton
from pirates.pirate import Pirate
from pirates.pirate import HumanDNA
from pirates.quest import QuestParser
from pirates.battle.Cannon import Cannon, distFireSfxNames
from pirates.makeapirate import MakeAPirate
from pirates.piratesbase import PiratesGlobals, PLocalizer, TimeOfDayManager, TODGlobals
from pirates.cutscene import CutsceneData
from pirates.tutorial import TutorialGlobals
from pirates.leveleditor import NPCList
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.effects.ProjectileEffect import ProjectileEffect
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.CeilingDebris import CeilingDebris
from pirates.effects.CeilingDust import CeilingDust
from pirates.effects.RingOfFog import RingOfFog
from pirates.piratesbase import UserFunnel
from pirates.world.LocationConstants import LocationIds
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.inventory import ItemGlobals
CannonDistance = 200
CannonballHitEvent = 'tutorialCannonballHit'

def _playHitEffect(pos, hitObject, skillId, task=None):
    attackerId = 0
    objType = None
    ProjectileEffect(base.cr, attackerId, hitObject, objType, pos, skillId, InventoryType.GrenadeExplosion)
    shakeCamera = False
    if localAvatar.ship:
        shakeCamera = False
    if localAvatar.style.tutorial >= PiratesGlobals.TUT_GOT_SEACHEST:
        if localAvatar.gameFSM.lockFSM:
            shakeCamera = False
    if shakeCamera:
        cameraShaker = CameraShaker()
        cameraShaker.reparentTo(render)
        cameraShaker.shakeSpeed = 0.04
        cameraShaker.shakePower = 1.0
        cameraShaker.numShakes = 3
        cameraShaker.scalePower = 1
        cameraShaker.play(400.0)
    messenger.send(CannonballHitEvent)
    return


class TutorialInteriorEffects():

    def __init__(self, startFire=False, cannonDelay=None):
        self._target = render.attachNewNode('target')
        self._target.setPos(0, CannonDistance, 0)
        self._skillId = 12906
        self._ammoSkillId = self._skillId
        self._startFire = startFire
        self._cannonDelay = cannonDelay
        self._seachest = None
        return

    def destroy(self):
        self.ignore('enableBoatBoarding')
        self.stop()
        self._target.removeNode()
        del self._target

    def start(self):
        self._shootTaskString = 'TutorialInteriorCannonShoot'
        self._hitTaskString = 'TutorialInteriorCannonHit'
        if self._cannonDelay is None:
            self._shootTask()
        else:
            taskMgr.doMethodLater(self._cannonDelay, self._shootTask, uniqueName(self._shootTaskString))
        CameraShaker.setTutorialInteriorScale(0.2)
        return

    def stop(self):
        CameraShaker.clearTutorialInteriorScale()
        taskMgr.removeTasksMatching('*%s*' % self._shootTaskString)
        taskMgr.removeTasksMatching('*%s*' % self._hitTaskString)
        if hasattr(self, '_shootTaskName'):
            del self._shootTaskName

    def _shootTask(self, task=None):
        targetPos = self._target.getPos()
        flightTime = 4.0
        self.currSnd = distFireSfxNames[random.randint(0, len(distFireSfxNames) - 1)]
        self.currSnd.play()
        taskMgr.doMethodLater(flightTime, Functor(self._handleCannonballHit, targetPos), uniqueName(self._hitTaskString))
        taskMgr.doMethodLater(1.0 + random.random() * 15.0, self._shootTask, uniqueName(self._shootTaskString))

    def _handleCannonballHit(self, targetPos, task=None):
        _playHitEffect(targetPos, self._target, self._skillId)


class PhantomCannon(Cannon):

    def __init__(self, cr, parent, distance, height, targetNps, island):
        Cannon.__init__(self, cr)
        self.loadModel(None, InventoryType.CannonL1)
        self._started = False
        self._targetNps = targetNps
        self._skillId = 12906
        self._ammoSkillId = self._skillId
        self._pivotNode = parent.attachNewNode('phantomCannonPivot')
        self._island = island
        self.reparentTo(self._pivotNode)
        self._pivotNode.reparentTo(parent)
        self.setPos(0, distance, height)
        self.stash()
        return

    def destroy(self):
        self.stop()
        del self._island
        del self._targetNps
        self.unloadModel()
        self.delete()
        self._pivotNode.removeNode()
        del self._pivotNode

    def start(self):
        self._shootTaskString = 'PhantomCannonShoot'
        self._hitTaskString = 'PhantomCannonHit'
        self._shootTask(0, None)
        self._started = True
        return

    def isStarted(self):
        return self._started

    def stop(self):
        self._started = False
        taskMgr.removeTasksMatching('*%s*' % self._shootTaskString)
        taskMgr.removeTasksMatching('*%s*' % self._hitTaskString)
        if hasattr(self, '_shootTaskName'):
            del self._shootTaskName

    def _shootTask(self, time, task):
        maxDistance = time * 12.0
        self._pivotNode.setH(self._pivotNode.getH() + random.random() * maxDistance)
        target = random.choice(self._targetNps)
        targetPos = target.getPos(render)
        flightTime = 5.0
        self.playAttack(self._skillId, self._ammoSkillId, 'PhantomCannonballHit', targetPos=targetPos, flightTime=flightTime, preciseHit=True)
        taskMgr.doMethodLater(flightTime, Functor(_playHitEffect, targetPos, self._island, self._skillId), uniqueName(self._hitTaskString))
        delay = 1.0 + random.random() * 15.0
        taskMgr.doMethodLater(delay, Functor(self._shootTask, delay), uniqueName(self._shootTaskString))


class DistributedPiratesTutorial(DistributedObject.DistributedObject, FSM.FSM):
    notify = directNotify.newCategory('DistributedPiratesTutorial')
    PRELOADED_CUTSCENES = []

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        FSM.FSM.__init__(self, 'DistributedPiratesTutorial')
        self.active = 1
        self.JackSparrowPos = Point3(0, 0, 0)
        self.JackSparrowHpr = Point3(200, 0, 0)
        self.NPCDoIds = []
        self.ShipDoIds = []
        self.pendingJackRequest = None
        self.pendingNavyBoatRequest = None
        self.pendingDanRequest = None
        self.pendingStumpyRequest = None
        self.pendingIslandRequest = None
        self.BoatStumpyDoId = None
        self.island = None
        self.shipWreck = None
        self.loggingCannonDone = False
        self.debugTutorial = base.config.GetBool('debug-tutorial', 0)
        self.noJailLight = base.config.GetBool('no-jail-light', 0)
        self._leftJail = 0
        self.map = 0
        base.cr.tutorialObject = self
        self.enemyBoatHidden = True
        return

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        if localAvatar.style.getTutorial() == 0:
            self.map = MakeAPirate.MakeAPirate([base.localAvatar], 'makeAPirateComplete')
            self.map.load()
        localAvatar.b_setGameState('LandRoam')
        self.acceptOnce('localAvTeleportFinished', self.getStarted)
        base.setOverrideShipVisibility(True)
        self.acceptOnce('localPirateDisabled', self.localPlayerLeft)
        base.cr.timeOfDayManager.enableSync(False)

    def localPlayerLeft(self):
        self.cleanup()

    def getStarted(self, task=None):
        if self.state == 'Off':
            self.request('Act0Tutorial')

    def cleanup(self):
        if self.pendingJackRequest:
            base.cr.relatedObjectMgr.abortRequest(self.pendingJackRequest)
            self.pendingJackRequest = None
        if self.pendingNavyBoatRequest:
            base.cr.relatedObjectMgr.abortRequest(self.pendingNavyBoatRequest)
            self.pendingNavyBoatRequest = None
        if self.pendingDanRequest:
            base.cr.relatedObjectMgr.abortRequest(self.pendingDanRequest)
            self.pendingDanRequest = None
        if self.pendingStumpyRequest:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStumpyRequest)
            self.pendingStumpyRequest = None
        if self.pendingIslandRequest:
            base.cr.relatedObjectMgr.abortRequest(self.pendingIslandRequest)
            self.pendingIslandRequest = None
        taskMgr.remove(self.taskName('handleAct0Tutorial'))
        self._stopFog()
        self._stopInteriorCannonballHitEffects()
        self._stopTutorialInteriorEffects()
        if hasattr(self, '_phantomCannon'):
            self._phantomCannon.destroy()
            del self._phantomCannon
        for pcs in self.PRELOADED_CUTSCENES:
            for currCutscene in pcs:
                base.cr.cleanupPreloadedCutscene(currCutscene)

        self.PRELOADED_CUTSCENES = []
        if self.island is not None:
            self.island.stopCustomEffects()
            self.island = None
        self.ignoreAll()
        return

    def disable(self):
        self.cleanup()
        if base.cr and base.cr.timeOfDayManager:
            base.cr.timeOfDayManager.enableSync(True)
        DistributedObject.DistributedObject.disable(self)

    def preloadCutscene(self, pcs):
        if pcs in self.PRELOADED_CUTSCENES:
            return
        self.PRELOADED_CUTSCENES.append(pcs)
        for currCutscene in pcs:
            base.cr.preloadCutscene(currCutscene)

    def inventoryFailed(self):
        if localAvatar:
            localAvatar.b_setLocation(0, 0)
        if self.map:
            self.map.exit()
            self.map.unload()
            self.map = 0
        base.cr.gameFSM.request('closeShard', ['waitForAvatarList'])

    def enterAct0Tutorial(self):
        self.notify.debug('starting tutorial')
        QuestParser.init()
        if self.noJailLight:
            render.setLightOff()
        self.JackDoId = None
        self.DanDoId = None
        self.StumpyDoId = None
        self.IslandDoId = None

        def stumpyHere(stumpyId):
            self.StumpyDoId = stumpyId

        def stumpyBoatHere(stumpyBoatId):
            self.BoatStumpyDoId = stumpyBoatId
            self.pendingStumpyBoatRequest = base.cr.relatedObjectMgr.requestObjects([self.BoatStumpyDoId], eachCallback=self.doStumpyBoatIntro)

        def navyBoatHere(navyBoatId):
            self.BoatNavyDoId = navyBoatId
            self.pendingNavyBoatRequest = base.cr.relatedObjectMgr.requestObjects([self.BoatNavyDoId], eachCallback=self.setupNavyBoat)

        def islandHere(islandId):
            self.IslandDoId = islandId
            self.pendingIslandRequest = base.cr.relatedObjectMgr.requestObjects([self.IslandDoId], eachCallback=self.handleIslandGenerate)

        self.cr.uidMgr.addUidCallback(TutorialGlobals.STUMPY_UID, stumpyHere)
        self.cr.uidMgr.addUidCallback(TutorialGlobals.STUMPY_BOAT_UID, stumpyBoatHere, onlyOnce=False)
        self.cr.uidMgr.addUidCallback(TutorialGlobals.ENEMY_BOAT_UID, navyBoatHere, onlyOnce=False)
        self.cr.uidMgr.addUidCallback(LocationIds.RAMBLESHACK_ISLAND, islandHere)
        self.accept('doneJackIntro', self.doneJackIntro)
        self.accept('fadeInExteriorDoor', self.handleGoOutside)
        self.accept('fadeInInteriorDoor', self.handleGoInside)
        self.acceptOnce('beginSeachest', self.beginSeachest)
        if localAvatar.style.getTutorial() > 0:
            self.ignore('doneJackIntro')
            localAvatar.openJailDoor()
            localAvatar.style.setName(localAvatar.getName())
            localAvatar.guiMgr.showTrays()
            base.transitions.fadeIn()
        self.sendUpdate('clientEnterAct0Tutorial')
        return

    def _startTutorialInteriorEffects(self, startFire, cannonDelay=None):
        base.ambientMgr.requestFadeIn(SoundGlobals.AMBIENT_JAIL, finalVolume=PiratesGlobals.DEFAULT_AMBIENT_VOLUME)

    def _stopTutorialInteriorEffects(self):
        base.ambientMgr.requestFadeOut(SoundGlobals.AMBIENT_JAIL)

    def handleIslandGenerate(self, island):
        self.island = island

    def handleWalkedOutToIsland(self):
        if not self._leftJail:
            self._leftJail = 1
            base.cr.centralLogger.writeClientEvent('LEAVING_JAIL')
            UserFunnel.logSubmit(0, 'LEAVING_JAIL')
            UserFunnel.logSubmit(1, 'LEAVING_JAIL')
            self._stopTutorialInteriorEffects()
            self.island.setZoneLevel(0)
            localAvatar.bindAnim(['sword_draw', 'sword_idle', 'cutlass_combo', 'cutlass_sweep'])
            self._targetNps = self.island.findAllMatches('**/TorchFire')
            self._phantomCannon = PhantomCannon(self.cr, self.island, CannonDistance, 50, self._targetNps, self.island)
            self._phantomCannon.start()

    def generateShipWreck(self, island):
        objNP = island.find('**/=uid=%s' % TutorialGlobals.SHIP_WRECK_UID)
        self.shipWreck = ShipWreck.ShipWreck(objNP, TutorialGlobals.SHIP_WRECK_UID)
        self.shipWreck.tutorial = self
        self.shipWreck.makeTargetableCollision(island.doId)
        island.shipWreck = self.shipWreck

    def removeShipWreck(self):
        if self.shipWreck:
            self.shipWreck.delete()
            self.shipWreck.removeNode()

    def doStumpyBoatIntro(self, object):
        stumpyBoat = base.cr.doId2do[self.BoatStumpyDoId]

        def setupTalkToDan(talkToDan):
            stumpyBoat.setZoneLevel(0)
            if talkToDan == False:
                self.notify.debug('stumpyBoat: talkToDan is False')
                self.accept(stumpyBoat.proximityCollisionEnterEvent, self.triggerBoBeckCut)
                self.acceptOnce('sendToBoat', self.sendToBoat)
                self.notify.debug('stumpyBoat:waiting for stumpy %s' % self.StumpyDoId)
                self.pendingStumpyRequest = base.cr.relatedObjectMgr.requestObjects([self.StumpyDoId], eachCallback=self.doStumpyIntro)
            else:
                self.notify.debug('stumpyBoat:talkToDan is True')

        setupTalkToDan(False)
        stumpyBoat.hideName()

    def triggerBoBeckCut(self, collEntry):
        self.notify.debug('triggerBoBeckCut')
        stumpyBoat = base.cr.doId2do[self.BoatStumpyDoId]
        self.ignore(stumpyBoat.proximityCollisionEnterEvent)
        self.sendUpdate('autoVisit', [self.BoatStumpyDoId])
        base.avatarPhysicsMgr.removePhysicalNode(stumpyBoat.actorNode)

    def exitAct0Tutorial(self):
        pass

    def doneJackIntro(self):
        self.notify.debug('Done Introducing Jack Sparrow')
        localAvatar.unstash()
        self.request('Act1MakeAPirate')

    def enterAct1MakeAPirate(self):
        base.disableMouse()
        localAvatar.gameFSM.request('MakeAPirate')
        localAvatar.gameFSM.lockFSM = True
        localAvatar.guiMgr.hideTrays()
        self.avHpr = VBase3(180, 0, 0)
        ga = localAvatar.getParentObj()
        ga.builder.turnOffLights()
        self.jail = ga.find('**/*navy_jail_interior*')
        self.map.enter()
        self.accept('makeAPirateComplete', self.handleMakeAPirate)
        UserFunnel.logSubmit(1, 'CREATE_PIRATE_LOADS')
        UserFunnel.logSubmit(0, 'CREATE_PIRATE_LOADS')
        base.cr.centralLogger.writeClientEvent('CREATE_PIRATE_LOADS')

    def handleMakeAPirate(self, clothing=[]):
        self.notify.debug('done make-a-pirate')
        done = self.map.getDoneStatus()
        if done == 'cancel':
            localAvatar.b_setLocation(0, 0)
            self.map.exit()
            self.map.unload()
            self.map = 0
            base.cr.closeShard()
            base.cr.logout()
        else:
            if done == 'created':
                dna = self.map.pirate.style
                localAvatar.setDNA(dna)
                localAvatar.generateHuman(dna.gender, base.cr.humanHigh)
                localAvatar.motionFSM.off()
                localAvatar.motionFSM.on()
                if clothing:
                    clothes = []
                    for clothId in clothing:
                        clothType = None
                        if clothId == 'HAT':
                            clothType = ItemGlobals.HAT
                        elif clothId == 'SHIRT':
                            clothType = ItemGlobals.SHIRT
                        elif clothId == 'VEST':
                            clothType = ItemGlobals.VEST
                        elif clothId == 'COAT':
                            clothType = ItemGlobals.COAT
                        elif clothId == 'PANT':
                            clothType = ItemGlobals.PANT
                        elif clothId == 'BELT':
                            clothType = ItemGlobals.BELT
                        elif clothId == 'SHOE':
                            clothType = ItemGlobals.SHOE
                        if clothType and clothing[clothId][0]:
                            clothes.append([clothType, clothing[clothId][0], clothing[clothId][2]])

                    if clothes:
                        localAvatar.sendRequestMAPClothes(clothes)
                self.acceptOnce('avatarPopulated', self.avatarPopulated)
                if self.map.nameGui.customName:
                    localAvatar.setWishName()
                    base.cr.avatarManager.sendRequestPopulateAvatar(localAvatar.doId, localAvatar.style, 0, 0, 0, 0, 0)
                else:
                    name = self.map.nameGui.getNumericName()
                    base.cr.avatarManager.sendRequestPopulateAvatar(localAvatar.doId, localAvatar.style, 1, name[0], name[1], name[2], name[3])
                self.map.exit()
                self.map.unload()
                self.map = 0
            else:
                self.notify.error('Invalid doneStatus from MakeAPirate: ' + str(done))
            localAvatar.gameFSM.lockFSM = False
            ga = localAvatar.getParentObj()
            if ga is not None:
                ga.builder.turnOnLights()
        return

    def avatarPopulated(self):
        self.request('EscapeFromLA')
        localAvatar.b_setGameState('LandRoam')
        self.sendUpdate('makeAPirateComplete')

    def makeAPirateCompleteResp(self):
        base.transitions.fadeIn(1.0)

    def handleGoOutside(self, uid):
        base.loadingScreen.tick()
        if uid == LocationIds.RAMBLESHACK_INSIDE:
            self.preloadCutscene(CutsceneData.PRELOADED_CUTSCENE_STAGE4)
            base.loadingScreen.tick()
        self._stopTutorialInteriorEffects()
        base.loadingScreen.tick()
        if hasattr(self, '_phantomCannon'):
            self._phantomCannon.start()
        self.ignore(CannonballHitEvent)
        base.cr.timeOfDayManager.setEnvironment(TODGlobals.ENV_EVER_NIGHT, {})
        base.loadingScreen.tick()
        self._startFog()
        base.loadingScreen.tick()
        self.handleWalkedOutToIsland()
        base.loadingScreen.tick()

    def handleGoInside(self, uid):
        base.loadingScreen.tick()
        if uid == LocationIds.RAMBLESHACK_INSIDE:
            self.preloadCutscene(CutsceneData.PRELOADED_CUTSCENE_STAGE3)
            base.loadingScreen.tick()
        self._phantomCannon.stop()
        self._stopFog()
        isJail = False
        self.accept(CannonballHitEvent, Functor(self._handleInteriorCannonballHit, isJail))

    def _handleInteriorCannonballHit(self, isJail):
        return
        if isJail:
            offset = 0
        else:
            offset = 3
        self._dustEffect = CeilingDust.getEffect()
        if self._dustEffect:
            self._dustEffect.reparentTo(base.localAvatar)
            self._dustEffect.setPos(0, 0, 12 + offset)
            self._dustEffect.play()
        self._debrisEffect = CeilingDebris.getEffect()
        if self._debrisEffect:
            self._debrisEffect.reparentTo(base.localAvatar)
            self._debrisEffect.setPos(0, 0, 22 + offset)
            self._debrisEffect.play()

    def _stopInteriorCannonballHitEffects(self):
        self.ignore(CannonballHitEvent)
        if hasattr(self, '_dustEffect'):
            self._dustEffect.finish()
            del self._dustEffect
        if hasattr(self, '_debrisEffect'):
            self._debrisEffect.finish()
            del self._debrisEffect

    def _startFog(self):
        if not hasattr(self, '_fog'):
            self._fog = RingOfFog()
            self._fog.reparentTo(render)
            self._fog.setEffectColor(Vec4(0.2, 0.3, 0.5, 1))
            self._fog.startLoop()
            self._moveFogDownEvent = 'moveFogDown'
            taskMgr.add(self._fogPositionTask, self._moveFogDownEvent, priority=49)

    def _stopFog(self):
        if hasattr(self, '_fog'):
            taskMgr.remove(self._moveFogDownEvent)
            del self._moveFogDownEvent
            self._fog.stopLoop()
            self._fog.destroy()
            del self._fog

    def _tuneFog(self, alpha):
        if hasattr(self, '_fog'):
            self._fog.tuneFog(alpha)

    def _fogPositionTask(self, task):
        self._fog.setX(localAvatar, 0)
        self._fog.setY(localAvatar, 0)
        return task.cont

    def exitAct1MakeAPirate(self):
        base.enableMouse()
        base.localAvatar.setHpr(self.avHpr)
        localAvatar.b_setTutorial(PiratesGlobals.TUT_GOT_SEACHEST)

    def enterEscapeFromLA(self):
        UserFunnel.logSubmit(1, 'CUTSCENE_ONE_END')
        UserFunnel.logSubmit(0, 'CUTSCENE_ONE_END')
        base.cr.centralLogger.writeClientEvent('CUTSCENE_ONE_END')
        self.acceptOnce('startTutorialCannons', Functor(self._startTutorialInteriorEffects, False))

    def exitEscapeFromLA(self):
        pass

    def setupNavyBoat(self, object):
        if self.enemyBoatHidden:
            object.hideName()
            object.hide()

    def beginSeachest(self):
        self.notify.debug('beginSeachest')
        localAvatar.gameFSM.lockFSM = False
        localAvatar.b_setGameState('Dialog')
        localAvatar.gameFSM.lockFSM = True
        localAvatar.guiMgr.request('Interface', [False, True])
        localAvatar.guiMgr.chestTray.show()
        localAvatar.cameraFSM.request('Control')
        stage = localAvatar.getParent().getParent()
        base.camera.reparentTo(stage)
        base.camera.setPos(9.561, 26.215, 5.255)
        base.camera.setHpr(-2.999, 5.293, 2.296)
        localAvatar.setPos(stage, 9.561, 26.215, 1.0)
        self._seachest = localAvatar.tutObject
        localAvatar.tutObject = None
        t = Parallel(Sequence(LerpPosInterval(self._seachest, 10, VBase3(15, -10, 3.0)), Func(self._seachest.removeNode)), Sequence(LerpScaleInterval(self._seachest, 1, VBase3(0.1, 0.1, 0.1))))
        t.start()
        return

    def assignStumpyQuest(self):
        self.notify.debug('assignStumpyQuest')
        self.accept('removeDanAndNell', self.removeDanAndNell)

    def removeDanAndNell(self):
        UserFunnel.logSubmit(1, 'CUTSCENE_TWO_END')
        UserFunnel.logSubmit(0, 'CUTSCENE_TWO_END')
        base.cr.centralLogger.writeClientEvent('CUTSCENE_TWO_END')
        self.notify.debug('removeDanAndNell')
        localAvatar.setTutorial(PiratesGlobals.TUT_GOT_SEACHEST)
        localAvatar.gameFSM.lockFSM = False
        localAvatar.b_setGameState('LandRoam')
        localAvatar.guiMgr.chestTray.show()

    def stageStumpyPositionOnBoat(self):
        self.NPCStumpy.motionFSM.request('Off')
        self.NPCStumpy.loop('wheel_idle')

    def sendToBoat(self):
        if self.island is not None:
            self.island.stopCustomEffects()
        stumpyBoat = base.cr.getDo(self.BoatStumpyDoId)
        self.sendUpdate('teleportToShip')
        self.stageStumpyPositionOnBoat()
        self.acceptOnce('usedCannon', self.startShipMovement)
        stumpyBoat.cannons.values()[0][1].setIgnoreProximity(False)
        dialogue = loadSfx(SoundGlobals.BBD_TELL_SHOOT)
        localAvatar.guiMgr.subtitler.showText(PLocalizer.QuestScriptTutorialStumpy_1, sfx=dialogue, timeout=dialogue.length() + 1.0)
        localAvatar.guiMgr.subtitler.clearTextOverride = True
        return

    def doStumpyIntro(self, object):
        self.notify.debug('doStumpyIntro')
        self.NPCStumpy = object
        dnaDict = NPCList.NPC_LIST['1153439632.21darren']
        customDNA = HumanDNA.HumanDNA()
        customDNA.loadFromNPCDict(dnaDict)
        self.NPCStumpy.setDNA(customDNA)
        self.NPCStumpy.generateHuman('m', base.cr.humanHigh)
        self.NPCStumpy.setInteractOptions(allowInteract=False)
        self.NPCStumpy.setIgnoreProximity(True)
        self.NPCStumpy.disableBodyCollisions()
        self.NPCStumpy.setZ(9)
        self.notify.debug('collision event for Stumpy %s' % self.NPCStumpy.proximityCollisionEvent)
        stumpyBoat = base.cr.getDo(self.BoatStumpyDoId)
        self.acceptOnce(stumpyBoat.uniqueName('localAvBoardedShip'), self.doneStumpyIntro)

    def doneStumpyIntro(self, task=None):
        self.notify.debug('Done Introducing Stumpy McGee')
        self.enemyBoatHidden = False
        localAvatar.gameFSM.lockFSM = False
        localAvatar.b_setGameState('LandRoam')
        localAvatar.gameFSM.lockFSM = True
        self.sendUpdate('boardedTutorialShip')
        self.acceptOnce('showCannonExitPanel', self.showCannonExitPanel)
        self.accept('targetPracticeDone', self.targetPracticeDone)
        UserFunnel.logSubmit(1, 'CUTSCENE_THREE_START')
        UserFunnel.logSubmit(0, 'CUTSCENE_THREE_START')
        base.cr.centralLogger.writeClientEvent('CUTSCENE_THREE_START')
        if self.BoatStumpyDoId:
            stumpyBoat = base.cr.doId2do[self.BoatStumpyDoId]
            stumpyBoat.ignoreFloors()
            self.ignore(stumpyBoat.uniqueName('localAvBoardedShip'))
            navyBoat = base.cr.doId2do[self.BoatNavyDoId]
            navyBoat.show()
            navyBoat.hideName()
        base.cr.relatedObjectMgr.abortRequest(self.pendingStumpyRequest)

    def startShipMovement(self):
        if self.island is not None:
            self.island.stopCustomEffects()
        self._phantomCannon.stop()
        localAvatar.guiMgr.setIgnoreAllKeys(True)
        localAvatar.guiMgr.setIgnoreMainMenuHotKey(True)
        localAvatar.guiMgr.chestTray.hide()
        self.sendUpdate('startSailingStumpy')
        UserFunnel.logSubmit(1, 'CUTSCENE_THREE_END')
        UserFunnel.logSubmit(0, 'CUTSCENE_THREE_END')
        base.cr.centralLogger.writeClientEvent('CUTSCENE_THREE_END')
        return

    def targetPracticeDone(self):
        localAvatar.guiMgr.setIgnoreMainMenuHotKey(False)
        localAvatar.guiMgr.chestTray.show()

    def enemyShipSunk(self):
        localAvatar.gameFSM.lockFSM = False
        self.showCannonExitPanel()
        dialogue = loadSfx(SoundGlobals.BBD_GIVE_PRAISE)
        localAvatar.guiMgr.subtitler.showText(PLocalizer.QuestScriptTutorialStumpy_6, sfx=dialogue, timeout=dialogue.length() + 1.0)

    def showCannonExitPanel(self):
        self.notify.debug('showCannonExitPanel')
        localAvatar.cannon.showExitCannonPanel()
        localAvatar.cannon.setIgnoreProximity(True)
        self.acceptOnce('exitedCannon', self.cannonDoneShooting)

    def cannonDoneShooting(self):
        if not self.loggingCannonDone:
            UserFunnel.logSubmit(1, 'ACCESS_CANNON')
            UserFunnel.logSubmit(0, 'ACCESS_CANNON')
            base.cr.centralLogger.writeClientEvent('ACCESS_CANNON')
            self.loggingCannonDone = True
        self.sendUpdate('targetPracticeDone')
        self.request('Act2TargetSunk')

    def enterAct2TargetSunk(self):
        self.notify.debug('Sunk the target')
        self.accept('introduceJR', self.introduceJR)

    def exitAct2TargetSunk(self):
        pass

    def introduceJR(self):
        if localAvatar.cannon:
            localAvatar.cannon.handleEndInteractKey()
        if localAvatar.ship and localAvatar.ship.gameFSM:
            localAvatar.ship.gameFSM.stopCurrentMusic()
        localAvatar.setPos(0, 0, 0)
        localAvatar.nametag3d.hide()
        self.notify.debug('introduceJR')
        self.request('Act3IntroduceJR')
        self.removeShipWreck()
        if self.island is not None:
            self.island.stopCustomEffects()
            self.island.stash()
        return

    def enterAct3IntroduceJR(self):
        self.notify.debug('Here comes Jolly Roger')
        self.accept('JRAttackShip', self.JRAttackShip)
        UserFunnel.logSubmit(1, 'CUTSCENE_FOUR_START')
        UserFunnel.logSubmit(0, 'CUTSCENE_FOUR_START')
        base.cr.centralLogger.writeClientEvent('CUTSCENE_FOUR_START')

    def exitAct3IntroduceJR(self):
        pass

    def JRAttackShip(self):
        self.notify.debug('JR Attacking Ship')
        self.accept('JRDestroyShip', self.JRDestroyShip)

    def JRDestroyShip(self):
        self.notify.debug('JR Destroying Ship')
        self.request('Act4BackToMain')
        UserFunnel.logSubmit(1, 'CUTSCENE_FOUR_END')
        UserFunnel.logSubmit(0, 'CUTSCENE_FOUR_END')
        base.cr.centralLogger.writeClientEvent('CUTSCENE_FOUR_END')

    def enterAct4BackToMain(self):
        taskMgr.doMethodLater(0.0001, self.goBackToMain, self.taskName('goBackToMain'))

    def exitAct4BackToMain(self):
        pass

    def goBackToMain(self, task):
        self.request('Act4DoneTutorial')
        return Task.done

    def enterAct4DoneTutorial(self):
        base.transitions.fadeOut(1.0)
        base.cr.loadingScreen.showHint(LocationIds.PORT_ROYAL_ISLAND)
        base.cr.loadingScreen.showTarget(LocationIds.PORT_ROYAL_ISLAND)
        base.cr.loadingScreen.show()
        localAvatar.guiMgr.ignoreAllKeys = False
        localAvatar.guiMgr.showTrays()
        localAvatar.show()
        if base.downloadWatcher and hasattr(base.downloadWatcher, 'setStatusBarLocation'):
            base.downloadWatcher.setStatusBarLocation(2)
        if base.launcher.getPhaseComplete(4):
            self.leaveTutorial()
        else:
            base.cr.centralLogger.writeClientEvent('Player encountered phase 4 blocker after JR cutscene')
            base.downloadWatcher.foreground()
            self.acceptOnce('phaseComplete-4', self.leaveTutorial)

    def skipTutorial(self):

        def initDefQuest(inventory):
            self.pendingInitQuest = None
            if inventory:
                localAvatar.sendUpdate('giveDefaultQuest')
                localAvatar.b_setTutorial(PiratesGlobals.TUT_GOT_COMPASS)
                if base.launcher.getPhaseComplete(4):
                    self.leaveTutorial()
                else:
                    base.downloadWatcher.foreground()
                    self.acceptOnce('phaseComplete-4', self.leaveTutorial)
            return

        self.pendingInitQuest = DistributedInventoryBase.getInventory(localAvatar.getInventoryId(), initDefQuest)
        base.transitions.fadeOut(1.0)
        base.cr.loadingScreen.showHint(LocationIds.PORT_ROYAL_ISLAND)
        base.cr.loadingScreen.showTarget(LocationIds.PORT_ROYAL_ISLAND)
        base.cr.loadingScreen.show()
        localAvatar.guiMgr.ignoreAllKeys = False
        localAvatar.guiMgr.showTrays()
        localAvatar.show()
        if base.downloadWatcher and hasattr(base.downloadWatcher, 'setStatusBarLocation'):
            base.downloadWatcher.setStatusBarLocation(2)

    def leaveTutorial(self):
        if base.downloadWatcher and hasattr(base.downloadWatcher, 'background'):
            base.downloadWatcher.background()
        base.cr.tutorial = 0
        base.cr.tutorialObject = None
        base.setOverrideShipVisibility(False)
        localAvatar.clearTeleportFlag(PiratesGlobals.TFInTutorial)
        localAvatar.b_setLocation(self.cr.distributedDistrict.doId, PiratesGlobals.QuietZone)
        self.sendUpdate('tutorialComplete')
        UserFunnel.logSubmit(1, 'STARTGAME_DOCK')
        UserFunnel.logSubmit(0, 'STARTGAME_DOCK')
        base.cr.centralLogger.writeClientEvent('STARTGAME_DOCK')
        return