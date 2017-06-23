import math
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from direct.actor import Actor
from direct.task import Task
from direct.showbase.PythonUtil import quickProfile
from pirates.pirate import AvatarType
from otp.otpbase import OTPRender
from pirates.battle import DistributedBattleable
from pirates.inventory import Lootable
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.pirate import BattleNPCGameFSM
from pirates.treasuremap import TreasureMapRulesPanel
from pirates.battle.EnemySkills import EnemySkills
from pirates.effects.SmokeWisps import SmokeWisps
from pirates.effects.Flame import Flame
from pirates.effects.FuseSparks import FuseSparks
from pirates.effects.SimpleSmokeCloud import SimpleSmokeCloud
from pirates.effects.ExplosionFlip import ExplosionFlip
from pirates.effects.CameraShaker import CameraShaker
from pirates.effects.ShipSplintersA import ShipSplintersA
from pirates.effects.DustRing import DustRing
from pirates.effects.ShockwaveRing import ShockwaveRing
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.quest import QuestLadderDB
from pirates.uberdog.UberDogGlobals import *
from pirates.quest.QuestConstants import PropIds
propCache = {}
SoundFiles = {'1274477304.85akelts': [SoundGlobals.SFX_MONSTER_EP_BEWARE],'1274137485.25akelts': [SoundGlobals.SFX_FX_ELEVATOR],'1274997857.99akelts': [SoundGlobals.SFX_FX_ELEVATOR]}
UninteractableProps = [
 '1274477304.85akelts']

class DistributedQuestProp(DistributedBattleable.DistributedBattleable, Lootable.Lootable):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedQuestProp')
    deferrable = True
    DiskWaitingEnemyColor = (1, 0, 0, 1)
    UpdateDelay = 2.0

    def __init__(self, cr):
        NodePath.__init__(self, 'DistributedQuestProp')
        DistributedBattleable.DistributedBattleable.__init__(self, cr)
        Lootable.Lootable.__init__(self)
        self.anims = None
        self.type = None
        self.battleTube = None
        self.name = ''
        self.isNpc = 1
        self.prop = None
        self.propColorR = 1.0
        self.propColorG = 1.0
        self.propColorB = 1.0
        self.propColorA = 1.0
        self.sphereScale = 10
        self.cTrav = None
        self.cProx = None
        self.cProxNode = None
        self.cProxNodePath = None
        self.isSearching = False
        self.belongsToTeam = PiratesGlobals.PROP_TEAM
        self.avatarType = AvatarType.AvatarType()
        self.interactAble = None
        self.interactType = None
        self.avId = None
        self.pendingMovie = None
        self.currentTarget = None
        self.skillEffects = {}
        self.level = 1
        self.hp = 0
        self.maxHp = 0
        self.lootType = None
        self.showTreasureIval = None
        self.raiseTreasureIval = None
        self.currentDepth = 0.0
        self.startingDepth = 0.0
        self.orientation = 0.0
        self.chestRoot = None
        self.chest = None
        self.spotRoot = None
        self.spot = None
        self.fireEffect = None
        self.smokeWispEffect = None
        self.sparks = None
        self.smokeVfx = None
        self.explosionVfx = None
        self.dustRingVfx = None
        self.splintersVfx = None
        self.explosionSfx = loadSfx(SoundGlobals.SFX_WEAPON_GRENADE_IMPACT)
        self.noIntervals = True
        self.questIds = []
        self.completedQuestIds = []
        self.notCompletedQuestIds = []
        self.questInteractionAllowed = False
        self.isActor = False
        self.openAnim = None
        self.openSound = None
        self.updatePanel = None
        self.messageHolder = None
        self.sounds = []
        self.playedSounds = []
        return

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def setSphereScale(self, sphereScale):
        self.sphereScale = sphereScale

    def getSphereScale(self):
        return self.sphereScale

    def generate(self):
        DistributedBattleable.DistributedBattleable.generate(self)
        self.battleTubeRadius = 2.0
        self.battleTubeHeight = 5.0
        self.battleCollisionBitmask = PiratesGlobals.WallBitmask | PiratesGlobals.TargetBitmask | PiratesGlobals.RadarAvatarBitmask
        self.aimTubeNodePaths = []
        self.battleTubeNodePaths = []

    def setVisZone(self, zone):
        self.visZone = zone

    def getVisZone(self):
        return self.visZone

    def setHp(self, hp, quietly=0):
        self.hp = hp
        if self.hp == self.maxHp and self.prop and 'break' in self.prop.getAnimNames():
            self.prop.pose('break', 0)
        self.refreshStatusTray()
        localAvatar.guiMgr.attuneSelection.update()

    def getHp(self):
        return self.hp

    def setMaxHp(self, maxHp):
        self.maxHp = maxHp

    def getMaxHp(self):
        return self.maxHp

    def announceGenerate(self):
        self.setInteractOptions(proximityText=self.getInteractText(), sphereScale=self.getSphereScale(), diskRadius=self.getSphereScale() * 2.0, exclusive=0)
        self.setAllowInteract(False)
        DistributedBattleable.DistributedBattleable.announceGenerate(self)
        self.loadProp()
        if self.prop:
            self.getParentObj().builder.addSectionObj(self.prop, self.visZone)
        self.gameFSM = BattleNPCGameFSM.BattleNPCGameFSM(self)
        if not self.sounds:
            sounds = SoundFiles.get(self.uniqueId, [])
            self.playedSounds = []
            for i in range(0, len(sounds)):
                self.sounds.append(loadSfx(sounds[i]))
                self.playedSounds.append(False)

        self.checkQuestInteractions()
        self.accept('inventoryAddDoId-%s-%s' % (localAvatar.getInventoryId(), InventoryCategory.QUESTS), self.checkQuestInteractions)
        self.accept('inventoryRemoveDoId-%s-%s' % (localAvatar.getInventoryId(), InventoryCategory.QUESTS), self.checkQuestInteractions)

    def disable(self):
        DistributedBattleable.DistributedBattleable.disable(self)
        self.deleteBattleCollisions()
        self.deleteProximityCollisions()
        taskMgr.remove(self.taskName('removeOnFireEffect'))
        self._removeOnFireEffect()
        if self.prop:
            self.getParentObj().builder.removeSectionObj(self.prop, self.visZone)
            if self.isActor:
                self.prop.delete()
            else:
                self.prop.removeNode()
            self.prop = None
        if self.sparks:
            self.sparks.stopLoop()
            self.sparks = None
        if self.smokeVfx:
            self.smokeVfx.cleanUpEffect()
            self.smokeVfx = None
        if self.explosionVfx:
            self.explosionVfx.cleanUpEffect()
            self.explosionVfx = None
        if self.dustRingVfx:
            self.dustRingVfx.cleanUpEffect()
            self.dustRingVfx = None
        if self.splintersVfx:
            self.splintersVfx.cleanUpEffect()
            self.splintersVfx = None
        if self.chest:
            self.chest.removeNode()
            self.chest = None
        if self.chestRoot:
            self.chestRoot.removeNode()
            self.chestRoot = None
        if self.showTreasureIval:
            self.showTreasureIval.pause()
            self.showTreasureIval = None
        if self.raiseTreasureIval:
            self.raiseTreasureIval.pause()
            self.raiseTreasureIval = None
        if self.spot:
            self.spot.removeNode()
            self.spot = None
        if self.spotRoot:
            self.spotRoot.removeNode()
            self.spotRoot = None
        self.openAnim = None
        if self.openSound:
            self.openSound.stop()
            loader.unloadSfx(self.openSound)
            self.openSound = None
        if self.updatePanel:
            self.updatePanel.destroy()
            self.updatePanel = None
        if self.messageHolder:
            self.messageHolder.removeNode()
            self.messageHolder = None
        for sound in self.sounds:
            sound.stop()
            loader.unloadSfx(sound)

        self.sounds = []
        self.playedSounds = []
        self.gameFSM.cleanup()
        return

    def delete(self):
        DistributedBattleable.DistributedBattleable.delete(self)

    def loadProp(self):
        if self.prop:
            return
        if self.type != PiratesGlobals.QUEST_PROP_DIG_SPOT:
            modelPath = PiratesGlobals.QUEST_PROP_MODELS.get(self.type, 'models/props/crate_04')
            anims = PiratesGlobals.QUEST_PROP_ANIMS.get(self.type, {})
            if anims:
                self.isActor = True
                self.prop = Actor.Actor(modelPath)
                anims = PiratesGlobals.QUEST_PROP_ANIMS.get(self.type, {})
                self.prop.loadAnims(anims)
            else:
                self.isActor = False
                self.prop = self.getPropModel(modelPath)
            propColor = self.getPropColor()
            self.prop.setColorScale(propColor[0], propColor[1], propColor[2], propColor[3])
            self.prop.reparentTo(self)
        if self.type == PiratesGlobals.QUEST_PROP_POWDER_KEG:
            self.lightUp()
        if self.type == PiratesGlobals.QUEST_PROP_TRS_CHEST_02:
            cb = self.prop.find('**/+Character').node().getBundle(0)
            ab = self.prop.find('**/+AnimBundleNode').node().getBundle()
            self.openAnim = cb.bindAnim(ab, -1)
            self.openAnim.pose(0)
            self.openSound = loadSfx(SoundGlobals.SFX_FX_OPEN_CHEST_02)
            self.openSound.setVolume(0.8)

    def getInteractText(self):
        interactText = PLocalizer.CustomQuestPropInteractStrings.get(self.uniqueId)
        if interactText:
            return interactText
        else:
            return PLocalizer.QuestPropInteractStrings.get(self.type, PLocalizer.InteractGeneral)

    def lightUp(self):
        self.sparks = FuseSparks.getEffect(unlimited=True)
        self.sparks.setPos(0.5, 0, 1.2)
        self.sparks.reparentTo(self.prop)
        self.sparks.startLoop()

    def explode(self):
        base.playSfx(self.explosionSfx, node=self, cutoff=200)
        if self.sparks:
            self.sparks.stopLoop()
            self.sparks = None
        self.prop.stash()
        self.explosionVfx = ExplosionFlip.getEffect(unlimited=True)
        if self.explosionVfx:
            self.explosionVfx.reparentTo(self)
            self.explosionVfx.setScale(1.5)
            self.explosionVfx.play()
        self.smokeVfx = SimpleSmokeCloud.getEffect(unlimited=True)
        if self.smokeVfx:
            self.smokeVfx.reparentTo(self)
            self.smokeVfx.setPos(0, 0, 1)
            self.smokeVfx.setEffectScale(1.0)
            self.smokeVfx.play()
        self.dustRingVfx = DustRing.getEffect(unlimited=True)
        if self.dustRingVfx:
            self.dustRingVfx.reparentTo(self)
            self.dustRingVfx.setPos(0, 0, -2)
            self.dustRingVfx.play()
        cameraShakerEffect = CameraShaker()
        cameraShakerEffect.reparentTo(self)
        cameraShakerEffect.shakeSpeed = 0.06
        cameraShakerEffect.shakePower = 4.0
        cameraShakerEffect.scalePower = True
        cameraShakerEffect.numShakes = 2
        cameraShakerEffect.scalePower = 1.0
        cameraShakerEffect.play(120.0)
        self.splintersVfx = ShipSplintersA.getEffect(unlimited=True)
        if self.splintersVfx:
            self.splintersVfx.reparentTo(self)
            self.splintersVfx.setPos(0, 0, -2)
            self.splintersVfx.play()
        shockwaveRingEffect = ShockwaveRing.getEffect(unlimited=True)
        if shockwaveRingEffect:
            shockwaveRingEffect.reparentTo(self)
            shockwaveRingEffect.setPos(0, 0, -2)
            shockwaveRingEffect.size = 80
            shockwaveRingEffect.play()
        return

    def loadChest(self):
        if self.chest:
            return
        self.chestRoot = self.attachNewNode('chestRoot')
        self.chest = loader.loadModel('models/props/treasureChest')
        self.chest.findAllMatches('**/pile_group').stash()
        self.chest.setH(self.orientation)
        self.chest.reparentTo(self.chestRoot)
        self.chest.setScale(0.8)
        self.dirt = loader.loadModel('models/props/dirt_pile')
        self.dirt.setH(self.orientation)
        self.dirt.reparentTo(self.chestRoot)
        self.dirt.flattenStrong()

    def requestInteraction(self, avId, interactType=0):
        if interactType == PiratesGlobals.INTERACT_TYPE_HOSTILE:
            base.localAvatar.setCurrentTarget(self.doId)
        else:
            localAvatar.motionFSM.off()
        DistributedBattleable.DistributedBattleable.requestInteraction(self, avId, interactType)

    def rejectInteraction(self, wantMessage=True):
        if wantMessage:
            message = PLocalizer.CustomQuestPropWarningStrings.get(self.uniqueId)
            if not message:
                message = PLocalizer.QuestPropWarningStrings.get(self.type, PLocalizer.AlreadySearched)
            localAvatar.guiMgr.createWarning(message)
        localAvatar.motionFSM.on()
        DistributedBattleable.DistributedBattleable.rejectInteraction(self)

    def setPropColor(self, r, g, b, a):
        self.propColorR = r
        self.propColorG = g
        self.propColorB = b
        self.propColorA = a

    def getPropColor(self):
        return (
         self.propColorR, self.propColorG, self.propColorB, self.propColorA)

    def getPropModel(self, name):
        model = propCache.get(name)
        if model:
            return model.copyTo(NodePath())
        else:
            model = loader.loadModel(name)
            model.flattenStrong()
            propCache[name] = model
            return model.copyTo(NodePath())

    def stashModel(self):
        if self.prop:
            self.prop.stash()

    def unstashModel(self):
        if self.prop:
            self.prop.unstash()

    def stashProp(self):
        self.stash()

    def unstashProp(self):
        self.unstash()

    def breakProp(self):
        if self.prop and 'break' in self.prop.getAnimNames():
            self.prop.play('break')

    def setProximitySphere(self, distance):
        self.cTrav = base.localAvatar.cTrav
        if self.cProx == None and distance > 0:
            self.cProx = CollisionSphere(0, 0, 0, distance)
            self.cProx.setTangible(0)
            self.cProxNode = CollisionNode(self.uniqueName('ProxSphere'))
            self.cProxNode.setFromCollideMask(BitMask32.allOff())
            self.cProxNode.setIntoCollideMask(PiratesGlobals.WallBitmask)
            self.cProxNode.addSolid(self.cProx)
            self.cProxNodePath = self.attachNewNode(self.cProxNode)
            if base.config.GetBool('show-prox-radius', 0):
                self.cProxNodePath.show()
            enterCollEvent = self.uniqueName('enter' + 'ProxSphere')
            exitCollEvent = self.uniqueName('exit' + 'ProxSphere')
            self.accept(enterCollEvent, self._handleEnterProxSphere)
            self.accept(exitCollEvent, self._handleExitProxSphere)
        return

    def _handleEnterProxSphere(self, collEntry):
        self.sendRequestClientProximity()

    def _handleExitProxSphere(self, collEntry):
        self.sendRequestClientExitProximity()

    def sendRequestClientProximity(self):
        self.sendUpdate('requestClientProximity', [])

    def sendRequestClientExitProximity(self):
        self.sendUpdate('requestClientExitProximity', [])

    def deleteProximityCollisions(self):
        if self.cProxNodePath:
            self.cTrav.removeCollider(self.cProxNodePath)
            self.cProxNodePath.removeNode()
            self.cProxNodePath = None
        if self.cProxNode:
            self.cProxNode = None
        if self.cProx:
            self.cProx = None
        return

    def startSearching(self, searchTime):
        self.isSearching = True
        self.acceptInteraction()
        localAvatar.guiMgr.workMeter.updateText(PLocalizer.InteractSearching)
        localAvatar.guiMgr.workMeter.startTimer(searchTime)
        localAvatar.b_setGameState('Searching')
        pos = localAvatar.getPos(self)
        angle = math.atan2(pos[0], pos[1])
        radius = 4
        localAvatar.setPos(self, math.sin(angle) * radius, math.cos(angle) * radius, 0)
        localAvatar.headsUp(self)
        localAvatar.setH(localAvatar, 0)

    def stopSearching(self, questProgress):
        if self.isSearching:
            self.isSearching = False
            localAvatar.guiMgr.workMeter.stopTimer()
            localAvatar.guiMgr.showQuestProgress(questProgress)
            if localAvatar.getGameState() == 'Searching':
                localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)
            self.refreshState()

    def createDigSpot(self):
        if not self.spot:
            self.spot = loader.loadModel('models/effects/pir_m_efx_msc_digSpot')
            self.spot.hide(OTPRender.MainCameraBitmask)
            self.spot.showThrough(OTPRender.EnviroCameraBitmask)
            self.spot.setTransparency(TransparencyAttrib.MAlpha)
            self.spot.setColorScale(0.8, 0.9, 0.8, 0.35)
            self.spot.setBin('shadow', -10)
            self.spot.setDepthTest(0)
            self.spot.setScale(50)
            self.spotRoot = self.attachNewNode('geomRoot')
            lod = LODNode('treeLOD')
            lodNP = self.spotRoot.attachNewNode(lod)
            self.spot.reparentTo(lodNP)
            lod.addSwitch(100, 0)

    def startDigging(self):
        if self.currentDepth == self.startingDepth:
            self.orientation = localAvatar.getH()
        self.acceptInteraction()
        localAvatar.b_setGameState('Digging')
        localAvatar.guiMgr.workMeter.updateText(PLocalizer.InteractDigging)
        localAvatar.guiMgr.workMeter.startTimer(self.startingDepth, self.currentDepth)
        pos = localAvatar.getPos(self)
        angle = math.atan2(pos[0], pos[1])
        radius = 5
        localAvatar.setPos(self, math.sin(angle) * radius, math.cos(angle) * radius, 0)
        localAvatar.headsUp(self)
        localAvatar.setH(localAvatar, -90)

    def stopDigging(self, questProgress):
        localAvatar.guiMgr.workMeter.stopTimer()
        if localAvatar.gameFSM.state == 'Digging':
            if localAvatar.getPlundering() != self.getDoId():
                localAvatar.guiMgr.showQuestProgress(questProgress)
            if localAvatar.lootCarried > 0:
                localAvatar.b_setGameState('LandTreasureRoam')
            else:
                localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)
                if localAvatar.getPlundering() == self.getDoId():
                    localAvatar.motionFSM.off()

    def setStartingDepth(self, depth):
        self.startingDepth = depth

    def setCurrentDepth(self, depth):
        oldZ = self.currentDepth / float(self.startingDepth) * -2.6
        self.currentDepth = depth
        z = self.currentDepth / float(self.startingDepth) * -2.6
        dirtZ = min(z + 0.5, -1.5)
        dirtOldZ = min(oldZ + 0.5, -1.5)
        if self.currentDepth == self.startingDepth:
            if self.chest:
                self.chest.stash()
                self.dirt.stash()
                self.chest.setZ(z)
                self.dirt.setZ(z * 1.5)
        else:
            self.loadChest()
            self.chest.unstash()
            self.dirt.unstash()
            self.chestRoot.setColorScale(1, 1, 1, 1)
            if self.raiseTreasureIval:
                self.raiseTreasureIval.pause()
            self.chest.setPos(Vec3(0, 0, oldZ))
            self.dirt.setPos(Vec3(0, 0, dirtOldZ))
            self.raiseTreasureIval = Sequence(Wait(0.5), Parallel(LerpPosInterval(self.chest, self.UpdateDelay, Vec3(0, 0, z)), LerpPosInterval(self.dirt, self.UpdateDelay, Vec3(0, 0, dirtZ))))
            self.raiseTreasureIval.start()
            if self.state == 'Use':
                localAvatar.guiMgr.workMeter.startTimer(self.startingDepth, self.currentDepth)

    def showTreasure(self, gold):
        self.loadChest()
        self.showTreasureIval = Sequence(Wait(4.0), Func(self.chestRoot.setTransparency, 1), LerpColorScaleInterval(self.chestRoot, 0.5, Vec4(1, 1, 1, 0)), Func(self.chest.stash))
        self.showTreasureIval.start()

    def aiRequestsExit(self):
        self.requestExit()

    def requestExit(self):
        DistributedBattleable.DistributedBattleable.requestExit(self)
        self.stopSearching(0)
        self.stopDigging(0)

    def createBattleCollisions(self):
        if self.battleTubeNodePaths:
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
        self.cr.targetMgr.addTarget(aimTubeNodePath.id(), self)
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
                self.cr.targetMgr.removeTarget(np.id())
            np.removeNode()

        self.aimTubeNodePaths = []
        return

    def showWaitingInfo(self):
        DistributedBattleable.DistributedBattleable.showWaitingInfo(self)
        if self.disk and localAvatar.currentWeaponId and localAvatar.isWeaponDrawn:
            self.disk.setColorScale(*self.DiskWaitingEnemyColor)

    def startLooting(self, plunderList, itemsToTake=0, timer=0, autoShow=False, customName=None):
        self.acceptInteraction()
        customName = PLocalizer.CustomQuestPropNames.get(self.uniqueId, None)
        Lootable.Lootable.startLooting(self, plunderList, itemsToTake=itemsToTake, timer=timer, autoShow=autoShow, customName=customName)
        if self.openAnim:
            self.openAnim.setPlayRate(1.0)
            self.openAnim.play()
        if self.openSound:
            self.openSound.play()
        return

    def stopLooting(self):
        if localAvatar.getPlundering() == self.getDoId():
            self.rejectInteraction(wantMessage=False)
            Lootable.Lootable.stopLooting(self)
            if self.openAnim:
                self.openAnim.setPlayRate(-1.0)
                self.openAnim.play()

    def doneTaking(self):
        Lootable.Lootable.doneTaking(self)
        self.requestExit()
        localAvatar.motionFSM.on()
        self.cr.interactionMgr.start()

    def setOnFire(self, duration):
        if self.fireEffect:
            return
        effectScale = self.getSphereScale()
        self.fireEffect = Flame.getEffect()
        if self.fireEffect:
            self.fireEffect.reparentTo(self)
            self.fireEffect.setPos(0, 0, self.height * 0.8)
            self.fireEffect.effectScale = 0.1 * effectScale
            self.fireEffect.duration = 4.0
            self.fireEffect.startLoop()
            self.fireEffect.setDefaultColor()
        self.smokeWispEffect = SmokeWisps.getEffect()
        if self.smokeWispEffect:
            self.smokeWispEffect.reparentTo(self)
            self.smokeWispEffect.setPos(0, 0, self.height)
            self.smokeWispEffect.startLoop()
        taskMgr.doMethodLater(duration, self._removeOnFireEffect, self.taskName('removeOnFireEffect'))

    def _removeOnFireEffect(self, task=None):
        if self.fireEffect:
            self.fireEffect.stopLoop()
            self.fireEffect = None
        if self.smokeWispEffect:
            self.smokeWispEffect.stopLoop()
            self.smokeWispEffect = None
        return

    def showHpMeter(self):
        DistributedBattleable.DistributedBattleable.showHpMeter(self)
        statusTray = localAvatar.guiMgr.targetStatusTray
        statusTray.updateName(self.getShortName(), self.level, self.doId)
        statusTray.updateHp(self.hp, self.maxHp, self.doId)
        statusTray.voodooMeter.hide()
        statusTray.targetFrame2.hide()
        statusTray.updateStatusEffects(self.skillEffects)
        statusTray.updateIcon(self.doId)
        sticky = localAvatar.currentTarget == self and localAvatar.hasStickyTargets()
        statusTray.updateSticky(sticky)
        statusTray.show()

    def hideHpMeter(self, delay=0.0):
        DistributedBattleable.DistributedBattleable.hideHpMeter(self, delay=delay)
        if base.localAvatar.guiMgr.targetStatusTray.doId == self.getDoId():
            if self.hp <= 0:
                localAvatar.guiMgr.targetStatusTray.updateHp(0, self.maxHp)
            localAvatar.guiMgr.targetStatusTray.fadeOut(delay=delay)

    def refreshStatusTray(self):
        statusTray = localAvatar.guiMgr.targetStatusTray
        if localAvatar.currentTarget == self or statusTray.doId == self.doId:
            statusTray.updateHp(self.hp, self.maxHp, self.doId)
            statusTray.updateStatusEffects(self.skillEffects)
            sticky = localAvatar.currentTarget == self and localAvatar.hasStickyTargets()
            statusTray.updateSticky(sticky)
            if self.hp > 0:
                statusTray.show()
            else:
                self.hideHpMeter(1.0)

    def clearInteract(self):
        self.requestExit()
        localAvatar.b_setGameState('Off')
        localAvatar.b_setGameState('LandRoam')

    def disableTeleportEffect(self):
        base.cr.teleportMgr.doEffect = False

    def requestGotSpecialReward(self, itemId):
        if hasattr(base, 'localAvatar'):
            base.localAvatar.gotSpecialReward(itemId)

    def requestCurrentWeapon(self, weaponId):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            self.rejectInteraction(wantMessage=False)
            base.localAvatar.guiMgr.combatTray.toggleWeapon(weaponId, -1)

    def putAwayCurrentWeapon(self):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
            self.rejectInteraction(wantMessage=False)
            if base.localAvatar.isWeaponDrawn:
                base.localAvatar.guiMgr.combatTray.toggleWeapon(localAvatar.currentWeaponId, localAvatar.currentWeaponSlotId)

    def freePlayer(self):
        self.rejectInteraction(wantMessage=False)

    def throwWarning(self):
        self.rejectInteraction()

    def requestSpawnFriendly(self, npcId):
        pass

    def setLootType(self, lootType):
        self.lootType = lootType

    def getLootType(self):
        return self.lootType

    def getName(self):
        return PLocalizer.QuestPropNames[self.getType()][0]

    def getTypeName(self):
        return self.getName()

    def getRating(self):
        return self.lootType + 1

    def d_requestItem(self, itemInfo):
        self.sendUpdate('requestItem', [itemInfo])

    def d_requestItems(self, items):
        self.sendUpdate('requestItems', [items])

    def getTeam(self):
        return self.belongsToTeam

    def getPVPTeam(self):
        return 0

    def getSiegeTeam(self):
        return 0

    def getLevel(self):
        return self.level

    def getSkillEffects(self):
        return []

    def setInteractMode(self, mode):
        pass

    def getShortName(self):
        return self.getName()

    def isBoss(self):
        return False

    def isInInvasion(self):
        return False

    def getArmorScale(self):
        return 1.0

    def isInvisible(self):
        return 0

    def getMinimapObject(self):
        return None

    def destroyMinimapObject(self):
        pass

    def getAvatarType(self):
        return self.avatarType

    def setQuestIds(self, questIds):
        self.questIds = questIds

    def getQuestIds(self):
        return self.questIds

    def setCompletedQuestIds(self, questIds):
        self.completedQuestIds = questIds

    def getCompletedQuestIds(self):
        return self.completedQuestIds

    def setNotCompletedQuestIds(self, questIds):
        self.notCompletedQuestIds = questIds

    def getNotCompletedQuestIds(self):
        return self.notCompletedQuestIds

    def setAllowInteract(self, allowInteract):
        if allowInteract:
            if self.questInteractionAllowed:
                DistributedBattleable.DistributedBattleable.setAllowInteract(self, allowInteract)
        else:
            DistributedBattleable.DistributedBattleable.setAllowInteract(self, allowInteract)

    def checkQuestInteractions(self, caller=None):
        self.questInteractionAlowed = False
        if self.uniqueId in UninteractableProps:
            return
        if not (self.questIds or self.completedQuestIds):
            self.questInteractionAllowed = True
            self.setAllowInteract(True)
            return
        currentQuests = localAvatar.getQuests()
        for questId in self.questIds:
            container = QuestLadderDB.getContainer(questId)
            for quest in currentQuests:
                if container.getQuestId() == quest.getQuestId() or container.hasQuest(quest.getQuestId()):
                    self.questInteractionAllowed = True
                    self.setAllowInteract(True)
                    return

        questHistory = localAvatar.getQuestLadderHistory()
        for questId in self.completedQuestIds:
            qInt = QuestLadderDB.getContainer(questId).getQuestInt()
            if qInt in questHistory:
                self.questInteractionAllowed = True
                self.setAllowInteract(True)
                return

        for questId in self.notCompletedQuestIds:
            qInt = QuestLadderDB.getContainer(questId).getQuestInt()
            if qInt not in questHistory:
                self.questInteractionAllowed = True
                self.setAllowInteract(True)
                return

    def sendUpdateMessage(self, stage):
        if not self.messageHolder:
            self.messageHolder = aspect2d.attachNewNode('message')
            self.updatePanel = TreasureMapRulesPanel.TreasureMapRulesPanel(PLocalizer.QuestPropUpdateTitles.get(self.uniqueId), '', self.messageHolder)
        self.messageHolder.setPos(Vec3(0, 0, 0.85))
        instructions = PLocalizer.QuestPropUpdateMessages.get(self.uniqueId)[stage]
        self.updatePanel.setInstructions(instructions)
        self.updatePanel.show()

    def sendLocalSound(self, num, alwaysPlay):
        if len(self.sounds) > num and (not self.playedSounds[num] or alwaysPlay):
            base.playSfx(self.sounds[num], node=self)
            self.playedSounds[num] = True