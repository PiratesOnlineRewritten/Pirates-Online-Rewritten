import random
import re
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from otp.otpbase import OTPGlobals
from otp.otpgui import OTPDialog
from otp.otpbase import OTPRender
from pirates.audio import SoundGlobals
from pirates.audio import MusicManager
from pirates.uberdog.UberDogGlobals import *
from pirates.piratesgui import InteractGUI, NamePanelGui
from otp.otpbase import OTPGlobals
from pirates.distributed import InteractGlobals
from pirates.battle import DistributedBattleNPC
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.leveleditor import NPCList
from pirates.quest import QuestParser
from pirates.quest import QuestTaskDNA
from pirates.quest.QuestReward import QuestReward
from pirates.pirate import HumanDNA, Biped
from pirates.piratesgui.NewTutorialPanel import NewTutorialPanel
from pirates.economy import DistributedShopKeeper
from pirates.economy import EconomyGlobals
from pirates.piratesgui import PDialog
import Townfolk
from pirates.interact import InteractiveBase
from pirates.leveleditor import CustomAnims
from direct.showbase.PythonUtil import report
from pirates.pirate import AvatarTypes
from pirates.pirate import TitleGlobals
from pirates.battle import DistributedBattleAvatar
from pirates.battle import EnemyGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.quest.QuestConstants import NPCIds
from pirates.battle import WeaponGlobals
import random
from direct.showbase import PythonUtil
from pirates.reputation import ReputationGlobals
from otp.nametag.NametagGlobals import CFSpeech, CFTimeout
import PotionInstructionPanel
from pirates.minigame.LegendaryTellGUI import LegendaryTellGUI
from pirates.piratesbase import Freebooter
from pirates.piratesbase import TeamUtils

class DistributedNPCTownfolk(DistributedBattleNPC.DistributedBattleNPC, DistributedShopKeeper.DistributedShopKeeper, Townfolk.Townfolk):
    DiskWaitingColor = (0, 0, 1, 0.5)
    DiskUseColor = None
    HelpTextIconTexture = None
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCTownfolk')

    def __init__(self, cr):
        DistributedBattleNPC.DistributedBattleNPC.__init__(self, cr)
        DistributedShopKeeper.DistributedShopKeeper.__init__(self)
        Townfolk.Townfolk.__init__(self)
        self.interactSphereNodePath = None
        self.interactMode = 0
        self.interactCamPosHpr = 0
        self.purgeInteractGui = 0
        self.beginFight = 0
        self.respecWeapon = 0
        self.pendingDoMovie = None
        self.hideHpMeterFlag = 1
        self.confirmDialog = None
        self.amUsingObj = None
        self.interactAnim = None
        self.animIval = None
        self.interactGUI = None
        self.questMenuGUI = None
        self.respecMenuGUI = None
        self.shipNamePanel = None
        self.classNameText = None
        self.shopId = PiratesGlobals.PORT_ROYAL_DEFAULTS
        self.helpId = 0
        self.noticeSpeed = 0.75
        self.shouldGreetOnNotice = 0
        self.preNoticeHeading = None
        self.noticeReactionList = []
        self.battleable = False
        self.prevAnimSet = None
        self.zombie = False
        self.efficiency = False
        return

    def makeMyAnimDict(self, gender, animNames):
        self.makeAnimDict(gender, animNames)

    def generateMyself(self):
        Townfolk.Townfolk.generateHuman(self, self.style.gender, base.cr.human, useFaceTex=config.GetBool('want-face-tex', 0))

    def announceGenerate(self):
        DistributedBattleNPC.DistributedBattleNPC.announceGenerate(self)
        yieldThread('battle gen')
        DistributedShopKeeper.DistributedShopKeeper.announceGenerate(self)
        yieldThread('shop gen')
        self.setName(self.name)
        self.setInteractOptions(proximityText=PLocalizer.InteractNamedTownfolk % self.name)
        localAvatar.checkForAutoTrigger(self.doId)
        yieldThread('auto trigger')
        if not self.canMove:
            self.motionFSM.off()
        self.updateNametagQuestIcon()
        self.accept('localAvatarQuestComplete', self.updateNametagQuestIcon)
        self.accept('localAvatarQuestUpdate', self.updateNametagQuestIcon)
        self.accept('localAvatarQuestItemUpdate', self.updateNametagQuestIcon)
        self.accept('inventoryAddDoId-%s-%s' % (localAvatar.getInventoryId(), InventoryCategory.QUESTS), self.updateNametagQuestIcon)
        self.accept('inventoryRemoveDoId-%s-%s' % (localAvatar.getInventoryId(), InventoryCategory.QUESTS), self.updateNametagQuestIcon)
        if self.getHelpId():
            if DistributedNPCTownfolk.HelpTextIconTexture is None:
                gui = loader.loadModel('models/gui/toplevel_gui')
                DistributedNPCTownfolk.HelpTextIconTexture = gui.find('**/generic_question*')
            self.nametagIcon = DistributedNPCTownfolk.HelpTextIconTexture.copyTo(self.nametag3d)
            self.nametagIcon.setScale(20)
            self.nametagIcon.setPos(0, 0, 3.5)
            self.nametagIcon.reparentTo(self.getNameText())
            self.nametagIcon.setDepthWrite(0)
            self.nametagIconGlow = loader.loadModel('models/effects/lanternGlow')
            self.nametagIconGlow.reparentTo(self.nametag.getNameIcon())
            self.nametagIconGlow.setScale(10.0)
            self.nametagIconGlow.setColorScaleOff()
            self.nametagIconGlow.setFogOff()
            self.nametagIconGlow.setLightOff()
            self.nametagIconGlow.setPos(0, -0.05, 3.2)
            self.nametagIconGlow.setDepthWrite(0)
            self.nametagIconGlow.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
            self.nametagIconGlow.setColor(0.85, 0.85, 0.85, 0.85)
        return

    def autoTriggerCheck(self, Task=None):
        localAvatar.checkForAutoTrigger(self.doId)
        if Task:
            return Task.done

    def generate(self):
        DistributedBattleNPC.DistributedBattleNPC.generate(self)
        DistributedShopKeeper.DistributedShopKeeper.generate(self)

    def setupAnimInfoState(self, state, info):
        if len(info) < len(self.FailsafeAnims):
            info += self.FailsafeAnims[len(info) - len(self.FailsafeAnims):]
        self.animInfo[state] = info

    def disable(self):
        self.stopInteract(localAvatar)
        DistributedBattleNPC.DistributedBattleNPC.disable(self)
        DistributedShopKeeper.DistributedShopKeeper.disable(self)
        self.stopBlink()
        if self.pendingDoMovie:
            base.cr.relatedObjectMgr.abortRequest(self.pendingDoMovie)
            self.pendingDoMovie = None
        self.ignore('doneChatPage')
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        if self.animIval:
            self.animIval.pause()
            self.animIval = None
        self.ignore('localAvatarQuestComplete')
        self.ignore('localAvatarQuestUpdate')
        self.ignore('localAvatarQuestItemUpdate')
        self.ignore('inventoryAddDoId-%s-%s' % (localAvatar.getInventoryId(), InventoryCategory.QUESTS))
        self.ignore('inventoryRemoveDoId-%s-%s' % (localAvatar.getInventoryId(), InventoryCategory.QUESTS))
        self.ignore('questInterestChange-%s' % self.getUniqueId())
        return

    def delete(self):
        DistributedBattleNPC.DistributedBattleNPC.delete(self)
        DistributedShopKeeper.DistributedShopKeeper.delete(self)
        self.ignoreAll()
        Townfolk.Townfolk.delete(self)

    def getNameText(self):
        return Townfolk.Townfolk.getNameText(self)

    def isBattleable(self):
        return self.battleable

    def startNoticeLoop(self):
        pass

    def endNoticeLoop(self):
        pass

    def startShuffle(self, turnAnim):
        if self.playNoticeAnims():
            self.loop(turnAnim, blendDelay=0.3)
            self.motionFSM.motionAnimFSM.interruptSplash()

    def playNoticeAnim(self):
        if not self.doneThreat:
            self.doneThreat = 1
            if self.preselectedReaction:
                reaction = self.preselectedReaction
                self.preselectedReaction = None
            else:
                reaction = self.getNoticeAnimation()
            if reaction:
                self.play(reaction, blendInT=0.3, blendOutT=0.3)
        return

    def presetNoticeAnimation(self):
        self.preselectedReaction = self.getNoticeAnimation()
        if not self.preselectedReaction:
            return None
        return self.getDuration(self.preselectedReaction)

    def getNoticeAnimation(self):
        if self.shouldGreetOnNotice:
            if self.greetingAnim != '':
                reaction = self.greetingAnim
            else:
                reaction = 'emote_wave'
        elif self.shouldTurnToNotice:
            choiceList = [
             'emote_yes']
            if not self.noticeReactionList:
                return None
            reaction = random.choice(self.noticeReactionList)
        return reaction

    def stateOkayForNotice(self):
        if self.getGameState() in ['LandRoam']:
            return 1
        return 0

    def firstNoticeLocalAvatar(self):
        if not self.playNoticeAnims():
            return
        if self.isInInvasion():
            return
        base.lastNotice = self
        self.localAvatarHasBeenNoticed = 1
        self.hasTurnedToNotice = 0
        if self.hasQuestOffersForLocalAvatar() and self.animSet not in ['tatoo_receive', 'sit', 'sit_sleep']:
            self.shouldGreetOnNotice = 1
        else:
            self.shouldGreetOnNotice = 0
        if self.animSet in ['default', 'idleB', 'idleC']:
            self.shouldTurnToNotice = 1
        else:
            if self.animSet in ['sow', 'primp', 'stir']:
                self.shouldTurnToNotice = 1
                if not self.shouldGreetOnNotice:
                    self.closeNoticeDistance = 15.0
            else:
                if self.noticeAnim1 != '' or self.noticeAnim2 != '':
                    self.shouldTurnToNotice = 1
                    if not self.shouldGreetOnNotice:
                        self.closeNoticeDistance = 20.0
                else:
                    self.shouldTurnToNotice = 0
                    if not self.shouldGreetOnNotice:
                        self.closeNoticeDistance = 20.0
                self.noticeReactionList = []
                if self.noticeAnim1 != '':
                    self.noticeReactionList.append(self.noticeAnim1)
            if self.noticeAnim2 != '':
                self.noticeReactionList.append(self.noticeAnim2)
        if self.noticeReactionList == [] and self.getAnimControlDict():
            self.noticeReactionList.append('emote_yes')
        self.preNoticeHeading = self.getHpr()

    def getAnimStyleExtras(self):
        extraList = [
         'walk', 'emote_yes', 'emote_wave', 'idle', 'idle_head_scratch_side', 'idle_head_scratch', 'idle_butt_scratch']
        if len(self.animInfo['LandRoam']) + 1 >= PiratesGlobals.SPIN_LEFT_INDEX:
            extraList.append(self.animInfo['LandRoam'][PiratesGlobals.SPIN_LEFT_INDEX][0])
        if len(self.animInfo['LandRoam']) + 1 >= PiratesGlobals.SPIN_RIGHT_INDEX:
            extraList.append(self.animInfo['LandRoam'][PiratesGlobals.SPIN_RIGHT_INDEX][0])
        return extraList

    def endNotice(self):
        heading = self.getHpr()
        if self.preNoticeHeading == None:
            self.preNoticeHeading = heading
        angle = PythonUtil.fitDestAngle2Src(heading[0], self.preNoticeHeading[0])
        newHpr = Vec3(angle, heading[1], heading[2])
        turnAnim = 'walk'
        noticeDif = abs(angle - heading[0])
        if self.usableAnimInfo():
            if noticeDif < 0:
                if len(self.animInfo['LandRoam']) + 1 >= PiratesGlobals.SPIN_LEFT_INDEX:
                    turnAnim = self.animInfo['LandRoam'][PiratesGlobals.SPIN_LEFT_INDEX][0]
            elif len(self.animInfo['LandRoam']) + 1 >= PiratesGlobals.SPIN_RIGHT_INDEX:
                turnAnim = self.animInfo['LandRoam'][PiratesGlobals.SPIN_RIGHT_INDEX][0]
        if turnAnim == 'idle':
            turnAnim = 'walk'
        if self.noticeIval:
            self.noticeIval.pause()
        self.noticeIval = Sequence(Func(self.startShuffle, turnAnim), LerpHprInterval(self, duration=self.noticeSpeed, hpr=newHpr), Func(self.setBackToIdle))
        self.noticeIval.start()
        self.doneThreat = 0
        self.localAvatarHasBeenNoticed = 0
        return

    def abortNotice(self):
        if self.noticeIval:
            self.noticeFlag = 1
            self.noticeIval.finish()
            self.noticeFlag = 0
            self.doneThreat = 0
        self.noticeIval = None
        self.localAvatarHasBeenNoticed = 0
        if self.preNoticeHeading:
            self.setHpr(self.preNoticeHeading)
        return

    def shouldNotice(self):
        if self.usingPropNoNotice:
            return 0
        if self.shouldTurnToNotice or self.shouldGreetOnNotice:
            return 1
        return 0

    def setBackToIdle(self):
        if self.playNoticeAnims():
            loop = 'idle'
            if self.usableAnimInfo():
                idleAnimInfo = self.animInfo['LandRoam'][PiratesGlobals.STAND_INDEX]
                self.loop(idleAnimInfo[0], blendDelay=0.3, rate=idleAnimInfo[1])
            else:
                self.loop('idle')

    def endShuffle(self):
        if self.playNoticeAnims():
            if self.noticeIdle and self.getCurrentAnim != self.noticeIdle:
                self.loop(self.noticeIdle, blendDelay=0.3)
            elif self.getCurrentAnim() != 'idle':
                self.loop('idle', blendDelay=0.3)

    def setDNAId(self, dnaId):
        if dnaId and NPCList.NPC_LIST.has_key(dnaId):
            dnaDict = NPCList.NPC_LIST[dnaId]
            customDNA = HumanDNA.HumanDNA()
            customDNA.loadFromNPCDict(dnaDict)
            self.setDNAString(customDNA)
        elif dnaId and re.search('/', dnaId):
            self.loadCast(dnaId)
        else:
            self.setDNAString(None)
            self.setDefaultDNA()
            self.style.makeNPCTownfolk()
        return

    def requestInteraction(self, avId, interactType=0):
        if localAvatar.zombie and avId == localAvatar.doId:
            localAvatar.guiMgr.createWarning(PLocalizer.ZombieNoPeople, PiratesGuiGlobals.TextFG6)
            return
        DistributedBattleNPC.DistributedBattleNPC.requestInteraction(self, avId, interactType)

    def rejectInteraction(self):
        if self.avatarType.isA(AvatarTypes.Cannonmaster):
            self.dialogFlag = 2
            self.playDialog()
        self.cancelInteraction(base.localAvatar)
        DistributedBattleNPC.DistributedBattleNPC.rejectInteraction(self)

    def requestStopInteract(self):
        messenger.send('stop interact', [])
        self.requestExit()

    def startInteract(self, av):
        if av == base.localAvatar and not self.interactMode:
            self.interactMode = 1
            self.setNameVisible(0)
            self.hideHpMeterFlag = 1
            self.playedFirstDialog = False
            self._questRewardsEarned = {}
            self.setChatAbsolute('', CFSpeech | CFTimeout)
            self.acceptInteraction()
            base.localAvatar.guiMgr.setIgnoreEscapeHotKey(True)
            if self.avatarType.isA(AvatarTypes.Tailor) or self.avatarType.isA(AvatarTypes.CatalogRep) or self.avatarType.isA(AvatarTypes.Tattoo) or self.avatarType.isA(AvatarTypes.Jeweler) or self.avatarType.isA(AvatarTypes.Barber):
                localAvatar.setSoloInteraction(True)

    def stopInteract(self, av, dialogStr=''):
        if av == base.localAvatar and self.interactMode and not self.isDeleted():
            localAvatar.setSoloInteraction(False)
            self.cleanUpQuestDetails()
            self.cleanUpQuestMenu()
            self.cleanUpBranchMenu()
            if self.interactGUI:
                self.notify.warning('stopInteract: old interact GUI still around')
                self.interactGUI.destroy()
                self.interactGUI = None
            if self.respecMenuGUI:
                self.respecMenuGUI.destroy()
                self.respecMenuGUI = None
            if self.confirmDialog:
                self.confirmDialog.destroy()
                self.confirmDialog = None
            self.finishShopping()
            self.playDialog(dialogStr=dialogStr)
            self.interactMode = 0
            self.setNameVisible(1)
            localAvatar.b_setGameState(localAvatar.gameFSM.defaultState)
            base.cr.interactionMgr.start()
            if self.amUsingObj:
                interactType = self.amUsingObj.interactType
            else:
                interactType = self.animSet
            self.endInteractMovie(interactType)
            if self.noticeReactionList:
                self.noticeLocalAvatar()
        return

    def playDialog(self, dialogStr='', timeout=5):
        activeHolidays = base.cr.newsManager.getHolidayIdList()
        emote = None
        if self.avatarType.isA(AvatarTypes.Fishmaster):
            inv = base.localAvatar.getInventory()
            if inv:
                if inv.getStackQuantity(InventoryType.FishingRod) <= 0:
                    self.playQuestString(PLocalizer.FishmasterFirstGreeting, timeout=10)
                    localAvatar.guiMgr.createLevelUpText()
                    localAvatar.guiMgr.levelUpLabel['text'] = PLocalizer.Minigame_Fishing_Tutorials['rodReceived']
                    localAvatar.guiMgr.levelUpCategoryLabel['text'] = ''
                    localAvatar.guiMgr.levelUpIval.pause()
                    localAvatar.guiMgr.levelUpIval.start()
                    base.talkAssistant.receiveGameMessage(PLocalizer.Minigame_Fishing_Tutorials['rodReceivedChatMessage'])
                    return
        if dialogStr:
            self.playQuestString(dialogStr, timeout=timeout)
        elif self.firstDialog == True and self.dialogFlag == 0:
            questStr, emote = InteractGlobals.getNPCGreeting(self)
            if self.avatarType.isA(AvatarTypes.Cannonmaster):
                self.playQuestString(questStr, timeout=120)
            else:
                self.playQuestString(questStr, timeout=timeout)
        elif self.dialogFlag == 0:
            questStr, emote = InteractGlobals.getNPCGoodbye(self)
            self.playQuestString(questStr, timeout=timeout, useChatBubble=True)
        elif self.dialogFlag == 1:
            questStr, emote = InteractGlobals.getNPCDuring(self)
            self.playQuestString(questStr, timeout=timeout, useChatBubble=True)
        elif self.dialogFlag == 2:
            questStr, emote = ('', None)
            if self.getHelpId():
                helpStrings = PLocalizer.townfolkHelpText.get(self.getHelpId())
                self.clearOffer()
                if len(helpStrings):
                    self.playQuestString(random.choice(helpStrings), timeout=False)
            else:
                questStr, emote = InteractGlobals.getNPCBrushoff(self)
                self.playQuestString(questStr, timeout=True, useChatBubble=True)
        else:
            self.notify.warning('Invalid dialogFlag: %d' % self.dialogFlag)
        if emote and self.shouldNotice():
            self.gameFSM.request('Emote')
            self.playEmote(emote)
        self.newDialog = False
        self.dialogFlag = 0
        return

    def hasOpenGUI(self):
        if self.interactGUI or self.questMenuGUI or self.shipNamePanel:
            return True
        return False

    def offerOptions(self, dialogFlag):
        self.dialogFlag = dialogFlag
        if self.interactGUI:
            self.notify.warning('offerOptions: old interact GUI still around')
            self.interactGUI.destroy()
            self.interactGUI = None
        if hasattr(self, 'currentDialogMovie') or self.purgeInteractGui or self.playingQuestString == True:
            self.receiveOffer(self.InteractOffer)
            self.genericDialog = False
            return
        if not self.interactMode:
            return
        if self.avatarType.isA(AvatarTypes.Musician):
            self.acceptOnce('stoppedShopping', self.cancelInteraction, [base.localAvatar])
            self.startShopping(InteractGlobals.MUSICIAN)
            if localAvatar.getGameState() != 'NPCInteract':
                localAvatar.b_setGameState('NPCInteract', localArgs=[self, True, False])
            self.clearOffer()
            return
        optionIds, stateCodes, bribeType = self.computeOptions()
        anyActive = False
        for i in range(len(optionIds)):
            if optionIds[i] != InteractGlobals.CANCEL and stateCodes[i] != InteractGlobals.DISABLED:
                anyActive = True
                break

        if anyActive:
            if self.localAvatarHasBeenNoticed:
                self.abortNotice()
            self.interactGUI = InteractGUI.InteractGUI()
            title = self.getMenuTitle()
            self.interactGUI.setOptions(title, optionIds, stateCodes, self.selectOptionConfirm, bribeType)
        elif self.dialogOpen == False:
            if self.firstDialog == True:
                self.dialogFlag = 2
            if not self.getHelpId():
                self.cancelInteraction(base.localAvatar)
                return
        if localAvatar.getGameState() != 'NPCInteract':
            localAvatar.b_setGameState('NPCInteract', localArgs=[self, True, False])
        if self.dialogOpen == False:
            if self.avatarType.isA(AvatarTypes.Stowaway):
                self.playDialog(timeout=15)
            else:
                self.playDialog()
        else:
            self.newDialog = True
            self.dialogFlag = dialogFlag
        self.clearOffer()
        return

    def selectOptionConfirm(self, optionId):
        if optionId == InteractGlobals.BRIBE:
            self.confirmBribe()
        elif optionId == InteractGlobals.HEAL_HP:
            self.confirmHealHp()
        elif optionId == InteractGlobals.HEAL_MOJO:
            self.confirmHealMojo()
        elif optionId == InteractGlobals.RESPEC:
            self.showRespecMenu()
        elif optionId == InteractGlobals.UPGRADE_ROD:
            self.showUpgradeRodDialog()
        elif optionId == InteractGlobals.LAUNCH_FISHING_BOAT:
            self.showLaunchFishingBoatDialog()
        elif optionId == InteractGlobals.LEGENDARY_FISH_STORY:
            self.confirmTellLegendaryFishStory()
        elif optionId == InteractGlobals.POTION_TUTORIAL:
            self.d_setViewedPotionInstructions()
        else:
            self.b_selectOption(optionId)

    def d_setViewedPotionInstructions(self):
        print 'viewing potion crafting tutorial'
        if self.interactGUI:
            self.interactGUI.hide()
        instructions = PotionInstructionPanel.PotionInstructionPanel()
        onInstructionsComplete = self.finishPotionInstructions
        instructions.show(onInstructionsComplete)
        self.sendUpdate('setViewedPotionInstructions')

    def finishPotionInstructions(self):
        if self.interactGUI:
            self.interactGUI.show()

    def setMovie(self, mode, avId):

        def doMovie(av):
            if mode == 'start':
                pass
            elif mode == 'stop':
                self.cancelInteraction(av)
            elif mode == 'clear':
                pass
            self.pendingDoMovie = None
            return

        av = base.cr.doId2do.get(avId)
        if avId != 0 and not av:
            self.notify.warning('setMovie: avId: %s not found' % avId)
            if self.pendingDoMovie:
                base.cr.relatedObjectMgr.abortRequest(self.pendingDoMovie)
                self.pendingDoMovie = None
            self.pendingDoMovie = base.cr.relatedObjectMgr.requestObjects([avId], eachCallback=doMovie, timeout=60)
        else:
            doMovie(av)
        return

    def getMenuTitle(self):
        return self.getName()

    def confirmHealHp(self):
        maxHp = localAvatar.getAdjMaxHp()
        hp = localAvatar.getHp()
        from pirates.economy import EconomyGlobals
        gold = EconomyGlobals.getAvatarHealHpCost(maxHp - hp)
        if self.confirmDialog:
            self.confirmDialog.destroy()
        self.confirmDialog = PDialog.PDialog(text=PLocalizer.HealHpConfirmDialog % {'gold': gold}, style=OTPDialog.YesNo, command=self.__handleHealHpConfirmation)

    def __handleHealHpConfirmation(self, value):
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        if value == 1:
            self.b_selectOption(InteractGlobals.HEAL_HP)
        return

    def confirmHealMojo(self):
        maxMojo = localAvatar.getMaxMojo()
        mojo = localAvatar.getMojo()
        gold = EconomyGlobals.getAvatarHealMojoCost(maxMojo - mojo)
        if self.confirmDialog:
            self.confirmDialog.destroy()
        self.confirmDialog = PDialog.PDialog(text=PLocalizer.HealMojoConfirmDialog % {'gold': gold}, style=OTPDialog.YesNo, command=self.__handleHealMojoConfirmation)

    def __handleHealMojoConfirmation(self, value):
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        if value == 1:
            self.b_selectOption(InteractGlobals.HEAL_MOJO)
        return

    def confirmTellLegendaryFishStory(self):
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        self.interactGUI.hide()
        uid = localAvatar.getParentObj().getUniqueId()
        self.confirmDialog = LegendaryTellGUI(1.24, 1.37, uid)
        self.confirmDialog.setCallBack(self.finishTellLegendaryFishStory)
        return

    def finishTellLegendaryFishStory(self):
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        self.interactGUI.show()
        return

    def launchFishingBoat(self):
        self.cr.loadingScreen.showTarget(ocean=True)
        self.cr.loadingScreen.showHint(ocean=True)
        self.cr.loadingScreen.show()
        self.cr.teleportMgr.requestTeleportToFishingShip()

    def confirmBribe(self):
        gold = 0
        for quest in localAvatar.getInventory().getQuestList():
            if quest.isComplete():
                continue
            for task in quest.questDNA.getTasks():
                if isinstance(task, QuestTaskDNA.BribeNPCTaskDNA) and task.getNpcId() == self.getUniqueId() and task.getGold() > gold:
                    gold = task.getGold()

        if self.confirmDialog:
            self.confirmDialog.destroy()
        avGold = localAvatar.getMoney()
        if avGold >= gold:
            self.confirmDialog = PDialog.PDialog(text=PLocalizer.BribeConfirmDialog % {'name': self.getName(),'gold': gold}, style=OTPDialog.YesNo, command=self.__handleBribeConfirmation)
        else:
            self.confirmDialog = PDialog.PDialog(text=PLocalizer.BribeNotEnoughGold % {'gold': gold}, style=OTPDialog.CancelOnly, command=self.__handleBribeConfirmation)
        gui = loader.loadModel('models/gui/toplevel_gui')
        goldCoin = gui.find('**/treasure_w_coin*')
        self.confirmDialog.goldLabel = DirectLabel(parent=self.confirmDialog, relief=0, text=PLocalizer.BribeConfirmYourGold % avGold, text_align=TextNode.ALeft, text_scale=0.035, text_pos=(0.0,
                                                                                                                                                                                              0.0), text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, image=goldCoin, image_scale=0.22, image_pos=(-0.04, 0, 0.01), pos=(-0.08, 0, -0.12))

    def __handleBribeConfirmation(self, value):
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        if value == 1:
            self.b_selectOption(InteractGlobals.BRIBE)
        return

    def computeOptions(self):
        questButtonState = InteractGlobals.NORMAL
        shipButtonState = InteractGlobals.NORMAL
        sellShipButtonState = InteractGlobals.NORMAL
        repairButtonState = InteractGlobals.DISABLED
        overhaulButtonState = InteractGlobals.DISABLED
        upgradeButtonState = InteractGlobals.NORMAL
        healButtonState = InteractGlobals.DISABLED
        healMojoButtonState = InteractGlobals.DISABLED
        storeButtonState = InteractGlobals.DISABLED
        sellItemButtonState = InteractGlobals.NORMAL
        sailButtonState = InteractGlobals.DISABLED
        sailTMButtonState = InteractGlobals.DISABLED
        bribeButtonState = InteractGlobals.DISABLED
        respecButtonState = InteractGlobals.NORMAL
        stowawayButtonState = InteractGlobals.NORMAL
        cannonDefenseButtonState = InteractGlobals.NORMAL
        potionTutorialButtonState = InteractGlobals.NORMAL
        launchFishingButtonState = InteractGlobals.NORMAL
        tellLegendaryFishStoryButtonState = InteractGlobals.NORMAL
        upgradeRodButtonState = InteractGlobals.DISABLED
        if not self.anyWeaponsRespecable():
            respecButtonState = InteractGlobals.DISABLED
        bribeType = 0
        inv = localAvatar.getInventory()
        if inv is None:
            self.notify.warning('computeOptions: inventory not present')
        else:
            if len(inv.getQuestList()) >= inv.getStackLimit(InventoryType.OpenQuestSlot) or not self.hasQuestOffers():
                questButtonState = InteractGlobals.DISABLED
            for quest in inv.getQuestList():
                foundBribe = 0
                if quest.isComplete():
                    continue
                if quest.questDNA is None:
                    self.notify.error('quest %s: does not contain a dna; is it a rogue quest, given in error?' % quest.getQuestId())
                for task in quest.questDNA.getTasks():
                    if isinstance(task, QuestTaskDNA.BribeNPCTaskDNA) and task.getNpcId() == self.getUniqueId():
                        bribeButtonState = InteractGlobals.NORMAL
                        foundBribe = 1
                        bribeType = task.bribeType
                        break

                if foundBribe:
                    break

            if len(inv.getShipDoIdList()) >= inv.getCategoryLimit(InventoryCategory.SHIPS) or localAvatar.style.getTutorial() < PiratesGlobals.TUT_GOT_SHIP:
                shipButtonState = InteractGlobals.DISABLED
            if len(inv.getShipDoIdList()) <= 0:
                sellShipButtonState = InteractGlobals.DISABLED
                upgradeButtonState = InteractGlobals.DISABLED
            for shipId in inv.getShipDoIdList():
                sailButtonState = InteractGlobals.NORMAL
                ship = base.cr.getOwnerView(shipId)
                if ship:
                    if ship.Hp < ship.maxHp:
                        repairButtonState = InteractGlobals.NORMAL

            if inv.getTreasureMapsList():
                if sailButtonState == InteractGlobals.NORMAL:
                    sailTMButtonState = InteractGlobals.NORMAL
        if base.localAvatar.hp < base.localAvatar.getAdjMaxHp():
            healButtonState = InteractGlobals.NORMAL
        if base.localAvatar.mojo < base.localAvatar.getAdjMaxMojo():
            healMojoButtonState = InteractGlobals.NORMAL
        if self.shopInventory:
            storeButtonState = InteractGlobals.NORMAL
        inv = localAvatar.getInventory()
        avFishingLevel = ReputationGlobals.getLevelFromTotalReputation(InventoryType.FishingRep, inv.getReputation(InventoryType.FishingRep))[0]
        rodLvl = inv.getStackQuantity(InventoryType.FishingRod)
        if avFishingLevel >= 5 and rodLvl < 2:
            upgradeRodButtonState = InteractGlobals.NORMAL
        elif avFishingLevel >= 15 and rodLvl < 3:
            upgradeRodButtonState = InteractGlobals.NORMAL
        if avFishingLevel < 10 or localAvatar.onWelcomeWorld or config.GetBool('disable-fishing-boats', 0):
            launchFishingButtonState = InteractGlobals.DISABLED
        if localAvatar.style.getTutorial() < PiratesGlobals.TUT_GOT_SHIP:
            stowawayButtonState = InteractGlobals.DISABLED
            cannonDefenseButtonState = InteractGlobals.DISABLED
        optionIds = InteractGlobals.getNPCInteractMenu(self.avatarType)[1]
        buttonStateDict = {InteractGlobals.QUEST: questButtonState,InteractGlobals.TALK: InteractGlobals.DISABLED,InteractGlobals.DUEL: InteractGlobals.DISABLED,InteractGlobals.STORE: storeButtonState,InteractGlobals.SELL_ITEMS: sellItemButtonState,InteractGlobals.SHIPS: shipButtonState,InteractGlobals.SELL_SHIPS: sellShipButtonState,InteractGlobals.TRAIN: InteractGlobals.DISABLED,InteractGlobals.REPAIR: repairButtonState,InteractGlobals.OVERHAUL: overhaulButtonState,InteractGlobals.UPGRADE: upgradeButtonState,InteractGlobals.TRADE: InteractGlobals.DISABLED,InteractGlobals.HEAL_HP: healButtonState,InteractGlobals.HEAL_MOJO: healMojoButtonState,InteractGlobals.CANCEL: InteractGlobals.NORMAL,InteractGlobals.SAIL: sailButtonState,InteractGlobals.SAILTM: sailTMButtonState,InteractGlobals.BRIBE: bribeButtonState,InteractGlobals.ACCESSORIES_STORE: InteractGlobals.NORMAL,InteractGlobals.TATTOO_STORE: InteractGlobals.NORMAL,InteractGlobals.JEWELRY_STORE: InteractGlobals.NORMAL,InteractGlobals.BARBER_STORE: InteractGlobals.NORMAL,InteractGlobals.RESPEC: respecButtonState,InteractGlobals.MUSICIAN: InteractGlobals.NORMAL,InteractGlobals.PVP_REWARDS_TATTOO: InteractGlobals.NORMAL,InteractGlobals.PVP_REWARDS_COATS: InteractGlobals.NORMAL,InteractGlobals.PVP_REWARDS_HATS: InteractGlobals.NORMAL,InteractGlobals.STOWAWAY: stowawayButtonState,InteractGlobals.PLAY_CANNON_DEFENSE: cannonDefenseButtonState,InteractGlobals.POTION_TUTORIAL: potionTutorialButtonState,InteractGlobals.LAUNCH_FISHING_BOAT: launchFishingButtonState,InteractGlobals.LEGENDARY_FISH_STORY: tellLegendaryFishStoryButtonState,InteractGlobals.UPGRADE_ROD: upgradeRodButtonState,InteractGlobals.CATALOG_STORE: InteractGlobals.NORMAL,InteractGlobals.PLAY_SCRIMMAGE: InteractGlobals.NORMAL}
        stateCodes = []
        for i in range(len(optionIds)):
            state = buttonStateDict.get(optionIds[i])
            if not state:
                state = InteractGlobals.DISABLED
            stateCodes.append(state)

        return (
         optionIds, stateCodes, bribeType)
        return None

    def d_selectOption(self, optionId):
        DistributedBattleNPC.DistributedBattleNPC.d_selectOption(self, optionId)

    def selectOption(self, optionId):
        if optionId in [InteractGlobals.STORE, InteractGlobals.TRAIN, InteractGlobals.SHIPS, InteractGlobals.ACCESSORIES_STORE, InteractGlobals.CATALOG_STORE, InteractGlobals.TATTOO_STORE, InteractGlobals.JEWELRY_STORE, InteractGlobals.BARBER_STORE, InteractGlobals.PVP_REWARDS_TATTOO, InteractGlobals.PVP_REWARDS_HATS, InteractGlobals.PVP_REWARDS_COATS, InteractGlobals.STOWAWAY]:
            if self.interactGUI:
                self.interactGUI.hide()
            self.startShopping(optionId)
        elif optionId == InteractGlobals.MUSICIAN:
            if self.interactGUI:
                self.interactGUI.hide()
            self.startShopping(optionId)
        elif optionId == InteractGlobals.REPAIR:
            if self.interactGUI:
                self.interactGUI.hide()
            self.startRepair(optionId)
        elif optionId == InteractGlobals.UPGRADE:
            if self.interactGUI:
                self.interactGUI.hide()
            self.startUpgrade(optionId)
        elif optionId == InteractGlobals.SELL_SHIPS:
            if self.interactGUI:
                self.interactGUI.hide()
            self.startSellShip(optionId)
        elif optionId == InteractGlobals.SELL_ITEMS:
            if self.interactGUI:
                self.interactGUI.hide()
            self.startSellItems(optionId)
        elif optionId == InteractGlobals.OVERHAUL:
            if self.interactGUI:
                self.interactGUI.hide()
            self.startOverhaul(optionId)
        elif optionId == InteractGlobals.QUEST:
            if self.interactGUI:
                self.interactGUI.hide()
        elif optionId == InteractGlobals.BRIBE:
            if self.interactGUI:
                self.interactGUI.destroy()
                self.interactGUI = None
        elif optionId == InteractGlobals.CANCEL:
            if self.interactGUI:
                self.interactGUI.hide()
            self.cancelInteraction(base.localAvatar)
        return

    @report(types=['frameCount', 'args'], dConfigParam='shipdeploy')
    def cancelInteraction(self, av, dialogStr=''):
        if av == localAvatar:
            self.requestStopInteract()
            self.stopInteract(av, dialogStr=dialogStr)
            self.firstDialog = True
            if av.playRewardAnimation:
                localAvatar.b_setGameState('OOBEmote', localArgs=[av.playRewardAnimation[0], av.playRewardAnimation[1]])
                av.playRewardAnimation = None
        return

    def handleEndInteractKey(self):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr and base.localAvatar.guiMgr.mainMenu and not base.localAvatar.guiMgr.mainMenu.isHidden():
            base.localAvatar.guiMgr.toggleMainMenu()
        else:
            cutscenePlaying = False
            if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr:
                base.localAvatar.guiMgr.setIgnoreEscapeHotKey(False)
            if base.cr.currentCutscene and not base.cr.currentCutscene.isEmpty():
                cutscenePlaying = True
            if not hasattr(self, 'currentDialogMovie') and not cutscenePlaying:
                if self.getHelpId():
                    self.playingQuestString = False
                    self.dialogOpen = False
                messenger.send('TownfolkEndingInteract')
                self.cancelInteraction(base.localAvatar)
            else:
                self.notify.warning('handleEndInteractKey failed')

    def finishShopping(self):
        if self.interactGUI:
            self.interactGUI.show()
        self.ignore('makeSale')
        DistributedShopKeeper.DistributedShopKeeper.finishShopping(self)

    def makeSaleResponse(self, result):
        DistributedShopKeeper.DistributedShopKeeper.makeSaleResponse(self, result)
        if result == EconomyGlobals.RESULT_SUCCESS_LAUNCH_FISHING_BOAT:
            self.launchFishingBoat()
        elif self.avatarType.isA(AvatarTypes.Shipwright):
            self.offerOptions(self.dialogFlag)

    def swordTutorialPt1(self):
        self.sendUpdate('swordTutorialPt1', [localAvatar.getDoId()])
        localAvatar.cameraFSM.request('FPS')

    def pistolTutorialPt1(self):
        self.sendUpdate('pistolTutorialPt1', [localAvatar.getDoId()])

    def setHp(self, hitPoints, quietly):
        DistributedBattleNPC.DistributedBattleNPC.setHp(self, hitPoints, quietly)

    def drawWeapon(self):
        print 'draw weapon'
        ival = self.pullOutCurrentWeapon()
        ival.start()

    def putAwayWeapon(self):
        self.beginFight = 0
        self.loop('idle')

    def drawSwordTutorial(self):
        self.drawSwordPanel = NewTutorialPanel(['drawSword'])
        taskMgr.doMethodLater(4.0, self.drawSwordPanel.activate, self.uniqueName('drawSwordPanelPause'), extraArgs=[])

    def attackSwordTutorial(self):
        if not self.beginFight:
            base.localAvatar.guiMgr.subtitler.confirmCallback()
            self.beginFight = 1
        taskMgr.remove(self.uniqueName('drawSwordPanelPause'))
        if hasattr(self, 'drawSwordPanel'):
            self.drawSwordPanel.hide()
        self.attackSwordPanel = NewTutorialPanel(['attackSword'])
        taskMgr.doMethodLater(4.0, self.attackSwordPanel.activate, self.uniqueName('attackSwordPanelPause'), extraArgs=[])

    def createHpMeter(self):
        pass

    def listenTime(self):
        self.accept('tooFast', self.tooFast)
        self.accept('tooSlow', self.tooSlow)

    def tooFast(self):
        pass

    def tooSlow(self):
        pass

    def ignoreTime(self):
        self.ignore('tooFast')
        self.ignore('tooSlow')

    def watchDistance(self):
        self.accept('tooFar', self.getCloser)

    def getCloser(self):
        pass

    def ignoreDistance(self):
        self.ignore('tooFar')

    def shipTutorialPt1(self):
        nameData = [
         PLocalizer.PirateShipPrefix.keys(), PLocalizer.PirateShipSuffix.keys()]
        self.shipNamePanel = NamePanelGui.NamePanelGui(PLocalizer.NamePanelTitle, nameData, showClose=False, allowEscape=False)
        self.shipNamePanel.setPos(-1, 0, 0)
        self.acceptOnce('nameChosen', self.handleShipNameChosen)

    def handleShipNameChosen(self, shipName):
        self.ignore('nameChosen')
        self.shipNamePanel.destroy()
        self.shipNamePanel = None
        avId = localAvatar.getDoId()
        self.sendUpdate('shipTutorialPt1', [avId, shipName])
        return

    def setQuestRewardsEarned(self, gold, reputation, items):
        if gold:
            self._questRewardsEarned['gold'] = gold
        if reputation:
            self._questRewardsEarned['reputation'] = reputation
        if items:
            self._questRewardsEarned['items'] = items
        self.notify.debug('questRewardsEarned: %s' % self._questRewardsEarned)

    def playDialogMovie(self, dialogId, doneCallback=None, oldLocalAvState=None):
        DistributedBattleNPC.DistributedBattleNPC.playDialogMovie(self, dialogId, doneCallback, oldLocalAvState)
        if self.interactGUI:
            self.interactGUI.destroy()
            self.interactGUI = None
        self.acceptOnce(InteractiveBase.END_INTERACT_EVENT, self.stopDialogMovieEvent)
        return

    def stopDialogMovieEvent(self):
        if hasattr(base, 'localAvatar') and base.localAvatar.guiMgr and base.localAvatar.guiMgr.mainMenu and not base.localAvatar.guiMgr.mainMenu.isHidden():
            base.localAvatar.guiMgr.toggleMainMenu()
        else:
            messenger.send('dialogFinish')

    def setPurgeInteractGui(self, val):
        self.purgeInteractGui = val

    def play(self, *args, **kwArgs):
        if self.altVisNode:
            self.altVisNode.play(*args, **kwArgs)
        else:
            Townfolk.Townfolk.play(self, *args, **kwArgs)

    def loop(self, *args, **kwArgs):
        if self.altVisNode:
            self.altVisNode.loop(*args, **kwArgs)
        else:
            Townfolk.Townfolk.loop(self, *args, **kwArgs)

    def pose(self, *args, **kwArgs):
        Townfolk.Townfolk.pose(self, *args, **kwArgs)

    def pingpong(self, *args, **kwArgs):
        Townfolk.Townfolk.pingpong(self, *args, **kwArgs)

    def stop(self, *args, **kwArgs):
        if self.altVisNode:
            self.altVisNode.stop(*args, **kwArgs)
        else:
            Townfolk.Townfolk.stop(self, *args, **kwArgs)

    def getDuration(self, *args, **kwArgs):
        if self.altVisNode:
            return self.altVisNode.getDuration(*args, **kwArgs)
        else:
            return DistributedBattleNPC.DistributedBattleNPC.getDuration(self, *args, **kwArgs)

    def getAnimInfo(self, *args, **kwArgs):
        if self.altVisNode:
            return self.altVisNode.getAnimInfo(*args, **kwArgs)
        else:
            return Townfolk.Townfolk.getAnimInfo(self, *args, **kwArgs)

    def triggerInteractShow(self, interactObj):
        self.amUsingObj = self.cr.doId2do.get(interactObj)
        self.startInteract(base.localAvatar)

    def playInteraction(self, hasMenu=True):
        if self.amUsingObj:
            interactType = self.amUsingObj.interactType
        else:
            interactType = self.animSet
        self.playInteractMovie(interactType, hasMenu)

    def playInteractMovie(self, interactType='default', hasMenu=True):
        self.setSkipLocalSmooth(True)
        allAnims = CustomAnims.INTERACT_ANIMS.get(interactType)
        if allAnims == None:
            self.notify.warning('undefined interaction type %s, not found in CustomAnims.INTERACT_ANIMS' % self.interactType)
        else:
            availAnims = allAnims.get('interact')
            availAnimsInto = allAnims.get('interactInto')
            if self.animIval:
                self.animIval.pause()
                self.animIval = None
            chosenAnim = random.choice(availAnims)
            self.interactCamPosHpr or self.pose(chosenAnim, 1, blendT=0)
            self.waitPending()
            if self.isInInvasion():
                np = self.attachNewNode('interactCamNode')
                np.setPos(self.headNode.getX(self) + 1, self.headNode.getY(self) + 6.5, self.headNode.getZ(self) + 1)
            else:
                if self.castDnaId:
                    if self.castDnaId in ['models/char/js_2000', 'models/char/td_2000', 'models/char/es_2000']:
                        np = self.attachNewNode('interactCamNode')
                        np.setPos(self.headNode.getX(self), self.headNode.getY(self) + 4.5, self.headNode.getZ(self) + 1)
                    else:
                        np = self.headNode.attachNewNode('interactCamNode')
                        np.setPos(1, 0, -4.5)
                    np.wrtReparentTo(render)
                    np.lookAt(self, self.headNode.getX(self), self.headNode.getY(self), self.headNode.getZ(self) * 0.95)
                    if hasMenu:
                        np.setH(np.getH() + 15)
                    self.interactCamPosHpr = [
                     np.getPos(render), np.getHpr(render)]
                    np.removeNode()
                if chosenAnim in self.getAnimNames():
                    chosenAnimInto = None
                    if availAnimsInto:
                        chosenAnimInto = random.choice(availAnimsInto)
                    if chosenAnimInto in self.getAnimNames():
                        duration = self.getDuration(chosenAnimInto)
                        self.lockFSM = True
                        if duration is None:
                            duration = 1.0
                        if self.localAvatarHasBeenNoticed:
                            self.abortNotice()
                        if self.isMixing():
                            if chosenAnimInto == chosenAnim:
                                self.animIval = Sequence(Wait(0.2), Func(self.loop, chosenAnim))
                            else:
                                self.animIval = Sequence(Wait(0.2), Func(self.play, chosenAnimInto), Func(self.loop, chosenAnim))
                        elif chosenAnimInto == chosenAnim:
                            self.animIval = Sequence(Func(self.loop, chosenAnim))
                        else:
                            self.animIval = Sequence(Func(self.play, chosenAnimInto), Wait(duration), Func(self.loop, chosenAnim))
                        self.animIval.start()
                    if self.animIval == None:
                        self.loop(chosenAnim)
                    self.interactAnim = chosenAnim
        return

    def endInteractMovie(self, interactType='default'):
        self.setSkipLocalSmooth(False)
        if self.interactAnim:
            if self.animIval:
                self.animIval.pause()
                self.animIval = None
            allAnims = CustomAnims.INTERACT_ANIMS.get(interactType)
            if allAnims == None:
                self.notify.warning('undefined interaction type %s, not found in CustomAnims.INTERACT_ANIMS' % self.interactType)
            else:
                availAnims = allAnims.get('idles')
                availAnimsOutof = allAnims.get('interactOutof')
                chosenAnim = random.choice(availAnims)
                if chosenAnim in self.getAnimNames():
                    self.interactAnim = chosenAnim
                    chosenAnimOutof = None
                    if availAnimsOutof:
                        chosenAnimOutof = random.choice(availAnimsOutof)
                    if chosenAnimOutof in self.getAnimNames():
                        duration = self.getDuration(chosenAnimOutof)
                        if duration is None:
                            duration = 1
                        self.lockFSM = True
                        if self.isMixing():
                            if chosenAnimOutof == self.interactAnim:
                                self.animIval = Sequence(Wait(0.2), Func(self.loop, self.interactAnim))
                            else:
                                self.animIval = Sequence(Wait(0.2), Func(self.play, chosenAnimOutof), Func(self.loop, self.interactAnim))
                        elif chosenAnimOutof == self.interactAnim:
                            self.animIval = Sequence(Func(self.loop, self.interactAnim))
                        else:
                            self.animIval = Sequence(Wait(0.2), Func(self.play, chosenAnimOutof), Wait(duration), Func(self.loop, self.interactAnim))
                        self.animIval.start()
            if self.animIval == None:
                self.loop(self.interactAnim)
            self.interactAnim = None
        return

    def levelUpCutlass(self):
        self.sendUpdate('levelUpCutlass', [localAvatar.getDoId()])

    def initializeNametag3d(self):
        Biped.Biped.initializeNametag3d(self)
        if not self.classNameText:
            self.classNameText = OnscreenText(parent=self.iconNodePath, pos=(0, -1.0), fg=(1,
                                                                                           1,
                                                                                           1,
                                                                                           1), bg=(0,
                                                                                                   0,
                                                                                                   0,
                                                                                                   0), scale=0.8, mayChange=1, font=PiratesGlobals.getPirateBoldOutlineFont())
            self.classNameText.setTransparency(TransparencyAttrib.MDual, 2)
            self.classNameText.setColorScaleOff(100)
            self.classNameText.setLightOff()
            self.classNameText.setFogOff()

    def setName(self, name):
        name = PLocalizer.NPCNames.get(self.uniqueId)
        DistributedBattleAvatar.DistributedBattleAvatar.setName(self, name)
        if self.classNameText:
            if self.avatarType.isA(AvatarTypes.Blacksmith):
                self.classNameText['text'] = PLocalizer.ShopBlacksmith
            elif self.avatarType.isA(AvatarTypes.Gunsmith):
                self.classNameText['text'] = PLocalizer.ShopGunsmith
            elif self.avatarType.isA(AvatarTypes.Shipwright):
                self.classNameText['text'] = PLocalizer.ShopShipwright
            elif self.avatarType.isA(AvatarTypes.Cannoneer):
                self.classNameText['text'] = PLocalizer.ShopCannoneer
            elif self.avatarType.isA(AvatarTypes.Gypsy):
                self.classNameText['text'] = PLocalizer.ShopGypsy
            elif self.avatarType.isA(AvatarTypes.MedicineMan):
                self.classNameText['text'] = PLocalizer.ShopMedicineMan
            elif self.avatarType.isA(AvatarTypes.Grenadier):
                self.classNameText['text'] = PLocalizer.ShopGrenadier
            elif self.avatarType.isA(AvatarTypes.Bartender):
                self.classNameText['text'] = PLocalizer.ShopBartender
            elif self.avatarType.isA(AvatarTypes.Merchant):
                self.classNameText['text'] = PLocalizer.ShopMerchant
            elif self.avatarType.isA(AvatarTypes.Tailor):
                self.classNameText['text'] = PLocalizer.ShopTailor
            elif self.avatarType.isA(AvatarTypes.Tattoo):
                self.classNameText['text'] = PLocalizer.ShopTattoo
            elif self.avatarType.isA(AvatarTypes.Jeweler):
                self.classNameText['text'] = PLocalizer.ShopJewelry
            elif self.avatarType.isA(AvatarTypes.Barber):
                self.classNameText['text'] = PLocalizer.ShopBarber
            elif self.avatarType.isA(AvatarTypes.Musician):
                self.classNameText['text'] = PLocalizer.ShopMusician
            elif self.avatarType.isA(AvatarTypes.Trainer):
                self.classNameText['text'] = PLocalizer.ShopTrainer
            elif self.avatarType.isA(AvatarTypes.PvPRewards):
                self.classNameText['text'] = PLocalizer.ShopPvP
            elif self.avatarType.isA(AvatarTypes.Stowaway):
                self.classNameText['text'] = PLocalizer.ShopStowaway
            elif self.avatarType.isA(AvatarTypes.Fishmaster):
                self.classNameText['text'] = PLocalizer.ShopFishmaster
            elif self.avatarType.isA(AvatarTypes.Cannonmaster):
                self.classNameText['text'] = PLocalizer.ShopCannonmaster
            elif self.avatarType.isA(AvatarTypes.CatalogRep):
                self.classNameText['text'] = PLocalizer.ShopCatalogRep
            elif self.avatarType.isA(AvatarTypes.ScrimmageMaster):
                self.classNameText['text'] = PLocalizer.ShopScrimmageMaster
            else:
                self.classNameText.hide()

    def setShopId(self, val):
        self.shopId = val

    def getShopId(self):
        return self.shopId

    def setHelpId(self, val):
        self.helpId = val

    def getHelpId(self):
        return self.helpId

    def showVoodooDollToAvatar(self):
        print 'triggering the interaction complete'

    def showUpgradeRodDialog(self):
        from pirates.minigame import FishingGlobals
        avGold = localAvatar.getMoney()
        inv = localAvatar.getInventory()
        avFishingLevel = ReputationGlobals.getLevelFromTotalReputation(InventoryType.FishingRep, inv.getReputation(InventoryType.FishingRep))[0]
        rodLvl = inv.getStackQuantity(InventoryType.FishingRod)
        if avFishingLevel >= 5 and rodLvl < 2:
            upgradeCost = FishingGlobals.ROD_JOURNEYMAN_COST
        else:
            if avFishingLevel >= 15 and rodLvl < 3:
                if Freebooter.getPaidStatus(localAvatar.doId) == False:
                    base.localAvatar.guiMgr.showNonPayer()
                    return
                upgradeCost = FishingGlobals.ROD_MASTER_COST
            else:
                return
            if avGold < upgradeCost:
                rodFailText = PLocalizer.UpgradeRodFail % {'gold': str(upgradeCost),'rod': PLocalizer.FishingRodNames[rodLvl + 1]}
                self.confirmDialog = PDialog.PDialog(text=rodFailText, style=OTPDialog.Acknowledge, command=self.notEnoughMoney)
            upgradeRodText = PLocalizer.UpgradeRodConfirmDialog % {'gold': str(upgradeCost),'rod': PLocalizer.FishingRodNames[rodLvl + 1]}
            self.confirmDialog = PDialog.PDialog(text=upgradeRodText, style=OTPDialog.YesNo, command=self.__handleUpgradeRodConfirmation)

    def showLaunchFishingBoatDialog(self):
        avGold = localAvatar.getMoney()
        launchCost = EconomyGlobals.LAUNCH_FISHING_BOAT_COST
        if Freebooter.getPaidStatus(localAvatar.doId) == False:
            base.localAvatar.guiMgr.showNonPayer()
        elif avGold < launchCost:
            launchFailText = PLocalizer.LaunchFishingBoatFail % {'gold': str(launchCost),'have': str(avGold)}
            self.confirmDialog = PDialog.PDialog(text=launchFailText, style=OTPDialog.Acknowledge, command=self.notEnoughMoney)
        else:
            launchBoatText = PLocalizer.LaunchFishingBoatConfirmDialog % {'gold': str(launchCost)}
            self.confirmDialog = PDialog.PDialog(text=launchBoatText, style=OTPDialog.YesNo, command=self.__handleLaunchFishingBoatConfirmation)

    def showRespecMenu(self):
        if self.interactGUI:
            self.interactGUI.hide()
        if self.respecMenuGUI:
            self.respecMenuGUI.destroy()
        optionIds = [
         InteractGlobals.RESPEC_CUTLASS, InteractGlobals.RESPEC_PISTOL, InteractGlobals.RESPEC_DAGGER, InteractGlobals.RESPEC_DOLL, InteractGlobals.RESPEC_GRENADE, InteractGlobals.RESPEC_STAFF, InteractGlobals.RESPEC_SAILING, InteractGlobals.RESPEC_CANNON, InteractGlobals.BACK]
        stateCodes = []
        for opt in optionIds:
            stateCodes.append(self.isRespecAvailable(opt))

        self.respecMenuGUI = InteractGUI.InteractGUI()
        title = self.getMenuTitle()
        self.respecMenuGUI.setOptions(title, optionIds, stateCodes, self.selectRespecOptionConfirm, 0)

    def isRespecAvailable(self, igOption):
        if igOption == InteractGlobals.CANCEL or igOption == InteractGlobals.BACK:
            return InteractGlobals.NORMAL
        else:
            basicSkills = WeaponGlobals.StartingSkills
            begin = -1
            end = -1
            weaponRep = self.getIGToITMap()[igOption]
            if weaponRep == InventoryType.CutlassRep:
                begin = InventoryType.begin_WeaponSkillCutlass
                end = InventoryType.end_WeaponSkillCutlass
            else:
                if weaponRep == InventoryType.PistolRep:
                    begin = InventoryType.begin_WeaponSkillPistol
                    end = InventoryType.end_WeaponSkillPistol
                elif weaponRep == InventoryType.DaggerRep:
                    begin = InventoryType.begin_WeaponSkillDagger
                    end = InventoryType.end_WeaponSkillDagger
                elif weaponRep == InventoryType.GrenadeRep:
                    begin = InventoryType.begin_WeaponSkillGrenade
                    end = InventoryType.end_WeaponSkillGrenade
                elif weaponRep == InventoryType.DollRep:
                    begin = InventoryType.begin_WeaponSkillDoll
                    end = InventoryType.end_WeaponSkillDoll
                elif weaponRep == InventoryType.WandRep:
                    begin = InventoryType.begin_WeaponSkillWand
                    end = InventoryType.end_WeaponSkillWand
                elif weaponRep == InventoryType.SailingRep:
                    begin = InventoryType.begin_SkillSailing
                    end = InventoryType.end_SkillSailing
                elif weaponRep == InventoryType.CannonRep:
                    begin = InventoryType.begin_WeaponSkillCannon
                    end = InventoryType.end_WeaponSkillCannon
                else:
                    return InteractGlobals.DISABLED
                for skillId in range(begin, end):
                    if skillId in WeaponGlobals.DontResetSkills:
                        continue
                    skillPts = localAvatar.getInventory().getStackQuantity(skillId)
                    if skillId in basicSkills:
                        if skillPts > 2:
                            return InteractGlobals.NORMAL
                    elif skillPts > 1:
                        return InteractGlobals.NORMAL

            return InteractGlobals.DISABLED

    def anyWeaponsRespecable(self):
        list = [InteractGlobals.RESPEC_CUTLASS, InteractGlobals.RESPEC_PISTOL, InteractGlobals.RESPEC_DAGGER, InteractGlobals.RESPEC_DOLL, InteractGlobals.RESPEC_GRENADE, InteractGlobals.RESPEC_STAFF, InteractGlobals.RESPEC_SAILING, InteractGlobals.RESPEC_CANNON]
        for optionId in list:
            if self.isRespecAvailable(optionId) == InteractGlobals.NORMAL:
                return 1

        return 0

    def selectRespecOptionConfirm(self, optionId):
        if optionId == InteractGlobals.CANCEL or optionId == InteractGlobals.BACK:
            self.respecMenuGUI.destroy()
            self.respecMenuGUI = None
            self.interactGUI.show()
            return
        weaponRep = self.getIGToITMap()[optionId]
        self.respecWeapon = optionId
        if self.confirmDialog:
            self.confirmDialog.destroy()
        self.respecMenuGUI.hide()
        numRespecs = localAvatar.getInventory().getStackQuantity(getNumRespecType(weaponRep))
        goldCost = EconomyGlobals.getRespecCost(numRespecs)
        respecText = PLocalizer.RespecConfirmDialog % {'gold': str(goldCost),'weapon': PLocalizer.InventoryTypeNames[weaponRep]}
        if numRespecs < 2:
            respecText += PLocalizer.RespecPriceIncreaseDialog
        self.confirmDialog = PDialog.PDialog(text=respecText, style=OTPDialog.YesNo, command=self.__handleRespecConfirmation)
        return

    def __handleRespecConfirmation(self, value):
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        if value == 1:
            if self.hasEnoughRespecMoney(self.respecWeapon):
                self.respecTransaction(self.respecWeapon)
                self.respecMenuGUI.destroy()
                self.respecMenuGUI = None
                self.offerOptions(self.dialogFlag)
            else:
                self.confirmDialog = PDialog.PDialog(text=PLocalizer.NotEnoughMoneyWarning, style=OTPDialog.Acknowledge, command=self.notEnoughMoney)
        else:
            self.respecMenuGUI.show()
        return

    def __handleUpgradeRodConfirmation(self, value):
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        if value == 1:
            self.b_selectOption(InteractGlobals.UPGRADE_ROD)
        return

    def __handleLaunchFishingBoatConfirmation(self, value):
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        if value == 1:
            self.b_selectOption(InteractGlobals.LAUNCH_FISHING_BOAT)
        return

    def notEnoughMoney(self, value=0):
        if self.respecMenuGUI:
            self.respecMenuGUI.destroy()
            self.respecMenuGUI = None
        if self.confirmDialog:
            self.confirmDialog.destroy()
            self.confirmDialog = None
        self.offerOptions(self.dialogFlag)
        return

    def getIGToITMap(self):
        return {InteractGlobals.RESPEC_CUTLASS: InventoryType.CutlassRep,InteractGlobals.RESPEC_PISTOL: InventoryType.PistolRep,InteractGlobals.RESPEC_DAGGER: InventoryType.DaggerRep,InteractGlobals.RESPEC_DOLL: InventoryType.DollRep,InteractGlobals.RESPEC_GRENADE: InventoryType.GrenadeRep,InteractGlobals.RESPEC_STAFF: InventoryType.WandRep,InteractGlobals.RESPEC_SAILING: InventoryType.SailingRep,InteractGlobals.RESPEC_CANNON: InventoryType.CannonRep}

    def respecTransaction(self, weaponOpt):
        weaponRep = self.getIGToITMap()[weaponOpt]
        if self.hasEnoughRespecMoney(self.respecWeapon):
            localAvatar.guiMgr.skillPage.respec(weaponRep)
            self.b_selectOption(weaponOpt)

    def hasEnoughRespecMoney(self, weaponOpt):
        weaponRep = self.getIGToITMap()[weaponOpt]
        curGold = localAvatar.getInventory().getGoldInPocket()
        numRespecs = localAvatar.getInventory().getStackQuantity(getNumRespecType(weaponRep))
        goldCost = EconomyGlobals.getRespecCost(numRespecs)
        if curGold >= goldCost:
            return 1
        else:
            return 0

    def getShipRank(self):
        inv = localAvatar.getInventory()
        if not inv:
            return 0
        return TitleGlobals.getRank(TitleGlobals.ShipPVPTitle, inv.getStackQuantity(InventoryType.PVPTotalInfamySea))

    def getLandRank(self):
        inv = localAvatar.getInventory()
        if not inv:
            return 0
        return TitleGlobals.getRank(TitleGlobals.LandPVPTitle, inv.getStackQuantity(InventoryType.PVPTotalInfamyLand))

    def playMusic(self, songId):
        songName = SoundGlobals.getMusicFromSongId(songId)
        base.musicMgr.request(name=songName, priority=5, looping=False)
        base.localAvatar.guiMgr.messageStack.addTextMessage(PLocalizer.SongPlayingAnnouncement % PLocalizer.InventoryTypeNames[songId], seconds=10, priority=0, color=(0,
                                                                                                                                                                       0,
                                                                                                                                                                       0,
                                                                                                                                                                       1))

    def setInInvasion(self, value):
        self.inInvasion = value
        if value:
            if self.battleTubeNodePaths:
                for np in self.battleTubeNodePaths:
                    np.node().setIntoCollideMask(np.node().getIntoCollideMask() & ~PiratesGlobals.WallBitmask)

        elif self.battleTubeNodePaths:
            for np in self.battleTubeNodePaths:
                np.node().setIntoCollideMask(np.node().getIntoCollideMask() | PiratesGlobals.WallBitmask)

    def getMinimapObject(self):
        if not self.minimapObj and not self.isDisabled():
            self.minimapObj = MinimapTownfolk(self)
        return self.minimapObj

    def setEfficiency(self, efficiency):
        if self.efficiency != efficiency:
            self.efficiency = efficiency
            if efficiency:
                self.enableReducedMixing()
            else:
                self.enableMixing()

    def setIsTracked(self, questId):
        self.isTracked = False
        if self.minimapObj:
            self.minimapObj.setIsTracked(self.isTracked)

    def checkWeaponSwitch(self, currentWeaponId, isWeaponDrawn):
        DistributedBattleNPC.DistributedBattleNPC.checkWeaponSwitch(self, currentWeaponId, isWeaponDrawn)
        self.resetAnimProp()

    def handleTeamSwitch(self):
        if TeamUtils.damageAllowed(localAvatar, self):
            self.setInteractOptions(isTarget=False, allowInteract=False)
            self.battleable = True
            if self.animSet != 'default':
                self.prevAnimSet = self.animSet
                self.animSet = 'default'
                self.animSetSetup = False
                self.reducedAnimList = None
                self.createAnimDict()
                self.unloadAnims()
                self.loadAnimsOnAllLODs(self.animDict, 'modelRoot')
                self.animInfo = Biped.Biped.animInfo
        else:
            self.setInteractOptions(proximityText=PLocalizer.InteractNamedTownfolk % self.name)
            self.battleable = False
            if self.prevAnimSet:
                self.animSet = self.prevAnimSet
                self.prevAnimSet = None
                self.animSetSetup = False
                self.setupCustomAnims()
                self.setupActorAnims()
        self.deleteBattleCollisions()
        self.initializeBattleCollisions()
        return

    def setTeam(self, team):
        prevTeam = self.getTeam()
        DistributedBattleNPC.DistributedBattleNPC.setTeam(self, team)
        if team == prevTeam:
            return
        if team != prevTeam:
            self.handleTeamSwitch()

    def setZombie(self, value, cursed=False):
        needToHide = self.isHidden()
        if self.zombie == value:
            return
        self.zombie = value
        self.cursed = cursed
        self.changeBodyType()
        if needToHide:
            self.hide()

    def changeBodyType(self):
        self.generateHuman(self.style.gender, base.cr.human)
        if self.motionFSM.state != 'Off':
            self.motionFSM.off()
            self.motionFSM.on()

    def canIdleSplashEver(self):
        return True

    def canIdleSplash(self):
        return self.getCurrentAnim() == 'idle' and self.animProp == None


class MinimapTownfolk(DistributedBattleAvatar.MinimapBattleAvatar):
    DEFAULT_COLOR = VBase4(0.1, 1.0, 0.1, 0.7)
