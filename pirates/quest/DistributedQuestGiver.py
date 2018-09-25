from pandac.PandaModules import *
from direct.showbase.ShowBaseGlobal import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.ClockDelta import *
from direct.interval.IntervalGlobal import *
from direct.showbase.PythonUtil import getShortestRotation
from otp.avatar import Avatar
from otp.otpgui import OTPDialog
from pirates.quest import QuestMenuGUI, QuestConstants, QuestDB, QuestLadderDB
from pirates.quest import QuestParser
from pirates.distributed import InteractGlobals
from pirates.quest import QuestLadderDB
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import Freebooter
from pirates.piratesgui import PDialog
from pirates.quest.QuestDetailGUI import QuestDetailGUI
from pirates.quest.QuestRewardGUI import QuestRewardGUI
from pirates.quest import BranchMenuGUI
from pirates.quest import QuestTaskDNA
from pirates.quest import QuestOffer
from pirates.reputation.ReputationGlobals import getLevelFromTotalReputation
from pirates.quest.DialogTree import *
from pirates.quest.DialogProcessMaster import *
from otp.nametag.NametagConstants import CFSpeech, CFTimeout

class DistributedQuestGiver(Avatar.Avatar):
    notify = directNotify.newCategory('DistributedQuestGiver')
    NoOffer = 0
    LadderOffer = 1
    QuestOffer = 2
    InteractOffer = 3
    BranchOffer = 4
    QuestIconWorkTexture = None
    QuestIconStoryTexture = None
    QuestIconProgressTexture = None
    QuestIconCompleteTexture = None
    QuestIconDontCare = 1
    QuestIconStory = 2
    QuestIconWork = 3
    QuestIconNew = 1
    QuestIconProgress = 2
    QuestIconComplete = 3

    def __init__(self):
        self.playingQuestString = False
        self.dialogOpen = False
        self.newOffer = False
        self.offers = None
        self.offerType = self.NoOffer
        self.dialogFlag = 0
        self.firstDialog = True
        self.newDialog = False
        self.npcMoviePlayer = None
        self.quitButton = 0
        self.nametagIcon = None
        self.nametagIconGlow = None
        self.containerId = None
        self.dialogAnimSet = None
        self.animationIval = None
        self.resetQuest = None
        self.resetBranch = None
        self.selectedOffer = None
        self.dialogProcessMaster = None
        self.dialogQuestOffer = None
        return

    def generate(self):
        DistributedQuestGiver.notify.debug('generate(%s)' % self.doId)
        self.questMenuGUI = None
        self.questDetailGUI = None
        self.questRewardGUI = None
        self.branchMenuGUI = None
        self.questDetailCamera = None
        return

    def announceGenerate(self):
        DistributedQuestGiver.notify.debug('announceGenerate(%s)' % self.doId)

    def disable(self):
        DistributedQuestGiver.notify.debug('disable(%s)' % self.doId)
        if self.npcMoviePlayer:
            self.npcMoviePlayer.cleanup()
            self.npcMoviePlayer = None
        self.cleanUpQuestMenu()
        self.cleanUpQuestDetails()
        self.cleanUpBranchMenu()
        self.ignore('endDialogNPCInteract')
        self.ignore('lastSubtitlePage')
        return

    def cleanUpQuestMenu(self):
        if self.questMenuGUI:
            self.questMenuGUI.destroy()
            self.questMenuGUI = None
        return

    def cleanUpBranchMenu(self):
        self.resetBranch = None
        self.selectedOffer = None
        if self.branchMenuGUI:
            self.branchMenuGUI.destroy()
            self.branchMenuGUI = None
        return

    def cleanUpQuestDetails(self, hide=False):
        if self.questDetailGUI:
            if hide:
                self.questDetailGUI.hidePanelAndDestroy()
            else:
                self.questDetailGUI.destroy()
            self.questDetailGUI = None
        if self.questRewardGUI:
            if hide:
                self.questRewardGUI.hidePanelAndDestroy()
            else:
                self.questRewardGUI.destroy()
            self.questRewardGUI = None
        if not hide and self.questDetailCamera:
            self.questDetailCamera.finish()
            self.questDetailCamera = None
        return

    def delete(self):
        DistributedQuestGiver.notify.debug('delete(%s)' % self.doId)

    def offerOptions(self):
        self.notify.warning('offerOptions() needs override!')

    def cancelInteraction(self, av):
        self.notify.warning('cancelInteraction() needs override!')

    def hasOpenGUI(self):
        self.notify.warning('hasOpenGUI() needs override!')
        return False

    def hasQuestOffers(self):
        AvailableQuests = []
        inventory = localAvatar.getInventory()
        prereqExcludes = base.config.GetString('exclude-prereq-quests', '')
        for questId, questDNA in QuestDB.QuestDict.items():
            if len(prereqExcludes):
                if questId in prereqExcludes:
                    continue
            prereqs = questDNA.getPrereqs()
            passed = True
            for prereq in prereqs:
                if not prereq.giverCanGive(self.getUniqueId()):
                    passed = False
                    break
                if not prereq.avIsReady(localAvatar):
                    passed = False
                    break
                if questDNA.minLevel > localAvatar.level:
                    passed = False
                    break
                if not base.cr.questDependency.checkDependency(questId, localAvatar.getQuestLadderHistory(), 1):
                    passed = False
                    break
                boolWeapLvlCheck = (questDNA.weapLvlType != None) & (questDNA.minWeapLevel > 0)
                if boolWeapLvlCheck & (questDNA.minWeapLevel > getLevelFromTotalReputation(questDNA.weapLvlType, inventory.getReputation(questDNA.weapLvlType))[0]):
                    passed = False
                    break
                if questDNA.getVelvetRoped() and not Freebooter.getPaidStatus(localAvatar.getDoId()):
                    passed = False
                    break
                if questDNA.getAcquireOnce():
                    history = localAvatar.getQuestLadderHistory()
                    questLadderId = base.cr.questDynMap.findQuestLadderInt(questId)
                    containsLadderId = history.count(questLadderId)
                    if containsLadderId:
                        passed = False
                        break
                if questDNA.getHoliday() is not None:
                    holidayId = questDNA.getHoliday()
                    if base.cr.newsManager and not base.cr.newsManager.getHoliday(holidayId):
                        passed = False
                        break

            if prereqs and passed:
                AvailableQuests.append(questDNA)

        if len(AvailableQuests):
            inventory = localAvatar.getInventory()
            if inventory:
                toRemove = []
                questList = inventory.getQuestList()
                for questDNA in AvailableQuests:
                    questId = questDNA.getQuestId()
                    found = False
                    for quest in questList:
                        if questId == quest.getQuestId() or localAvatar.questStatus.hasLadderQuestId(questId):
                            found = True

                    if found:
                        toRemove.append(questDNA)

                for questDNA in toRemove:
                    AvailableQuests.remove(questDNA)

        for quest in localAvatar.getQuests():
            if quest and quest.getTimeLimit() and quest.canBeReturnedTo(self.getQuestGiverId()):
                return True

        return len(AvailableQuests) > 0

    def receiveOffer(self, offerType):
        self.newOffer = True
        self.offerType = offerType

    def clearOffer(self):
        self.newOffer = False
        self.offerType = self.NoOffer

    def displayNewQuests(self):
        self.cleanUpQuestDetails()
        while len(localAvatar.currentStoryQuests) and localAvatar.currentStoryQuests[0].getGiverId() != self.uniqueId:
            if localAvatar.currentStoryQuests[0].getGiverId() == '0':
                break
            localAvatar.currentStoryQuests.remove(localAvatar.currentStoryQuests[0])

        if len(localAvatar.currentStoryQuests):
            storyQuest = localAvatar.currentStoryQuests[0]
            self.presentQuestGiven(storyQuest)
            localAvatar.currentStoryQuests.remove(storyQuest)

    def presentOffer(self):
        if self.newOffer == False:
            while len(localAvatar.currentStoryQuests) and localAvatar.currentStoryQuests[0].getGiverId() != self.uniqueId:
                localAvatar.currentStoryQuests.remove(localAvatar.currentStoryQuests[0])

            if len(localAvatar.currentStoryQuests):
                storyQuest = localAvatar.currentStoryQuests[0]
                self.presentQuestGiven(storyQuest)
                localAvatar.currentStoryQuests.remove(storyQuest)
            return
        if self.offerType == self.QuestOffer:
            self.presentQuestOffer(self.offers)
        elif self.offerType == self.LadderOffer:
            self.presentQuestOffer(self.offers, ladder=True)
        elif self.offerType == self.InteractOffer:
            self.offerOptions(self.dialogFlag)
        elif self.offerType == self.NoOffer:
            self.notify.warning('offerType == No Offer')
        self.clearOffer()

    def setQuestOffer(self, offers):
        self.receiveOffer(self.QuestOffer)
        self.offers = offers
        for quest in localAvatar.getQuests():
            if quest.getTimeLimit() and quest.canBeReturnedTo(self.getQuestGiverId()):
                questOffer = QuestOffer.QuestTimerResetOffer.create(quest.getQuestId(), localAvatar, timerReset=True)
                offers.append(questOffer)
            branchParent = quest.getBranchParent(localAvatar)
            if branchParent and branchParent.getGiverId() == self.getQuestGiverId():
                questOffer = QuestOffer.QuestBranchResetOffer.create(quest.getQuestId(), localAvatar, branchReset=True)
                offers.append(questOffer)

        if not self.playingQuestString:
            self.presentQuestOffer(self.offers)

    def setQuestLadderOffer(self, offers, quitButton):
        self.receiveOffer(self.LadderOffer)
        self.offers = offers
        self.quitButton = quitButton
        if not self.playingQuestString:
            self.presentQuestOffer(self.offers, ladder=True)

    def presentQuestOffer(self, offers, ladder=False):
        if self.questMenuGUI:
            DistributedQuestGiver.notify.warning('setQuestOffer: old questMenu GUI still around')
            self.cleanUpQuestMenu()
        self.cleanUpQuestDetails()

        def handleSelection(offer, self=self, offers=offers):
            self.cleanUpQuestMenu()
            if offer == QuestConstants.CANCEL_QUEST:
                index = QuestConstants.CANCEL_QUEST
            else:
                index = offers.index(offer)
            self.sendOfferResponse(index, ladder)

        def handleOption(option, offer):
            base.test = self
            self.ignore('lastSubtitlePage')
            self.adjustNPCCamera('back')
            if option == PLocalizer.Accept:
                handleSelection(offer)
            elif self.questMenuGUI:
                self.questMenuGUI.show()
            self.cleanUpQuestDetails(hide=True)

        def displayQuestDetails(offer):
            self.questDetailGUI = QuestDetailGUI(offer, None)
            self.questDetailGUI.showPanel()
            base.questdet = self.questDetailGUI
            return

        def displayBranchDetails(offer):
            self.selectedOffer = offer
            self.cleanUpQuestDetails()
            self.questDetailGUI = QuestDetailGUI(offer, None)
            self.questDetailGUI.showPanel()
            base.questdet = self.questDetailGUI
            return

        def displayBranchOptions(offer, callback, descCallback):
            self.branchMenuGUI = BranchMenuGUI.BranchMenuGUI(offer, callback, descCallback)

        def handleBranchOption(option):
            if option == PLocalizer.Accept:
                if self.selectedOffer:
                    self.sendOfferResponse(0, ladder, self.selectedOffer)
            self.adjustNPCCamera('back')
            self.cleanUpQuestDetails(hide=True)
            self.cleanUpBranchMenu()
            if self.questMenuGUI:
                self.questMenuGUI.show()

        def describeQuest(offer):
            self.adjustNPCCamera('forward')
            questDNA = offer.getQuestDNA()
            if questDNA:
                if isinstance(offer, QuestOffer.QuestTimerResetOffer):
                    self.requestQuestReset(offer.getQuestId())
                    return
                elif isinstance(offer, QuestOffer.QuestBranchResetOffer):
                    self.requestBranchReset(offer.getQuestId())
                    return
                questStr = questDNA.getStringBefore()
                if questDNA.isBranch():
                    self.acceptOnce('lastSubtitlePage', displayBranchOptions, [offer, None, displayBranchDetails])
                    localAvatar.guiMgr.subtitler.setPageChat(questStr, options=[PLocalizer.Decline, PLocalizer.Accept], callback=handleBranchOption)
                else:
                    self.acceptOnce('lastSubtitlePage', displayQuestDetails, [offer])
                    localAvatar.guiMgr.subtitler.setPageChat(questStr, options=[PLocalizer.Decline, PLocalizer.Accept], callback=handleOption, extraArgs=[offer])
            return

        def questFull(arg):
            self.cleanUpQuestMenu()
            self.sendOfferResponse(QuestConstants.CANCEL_QUEST, ladder)

        inv = base.localAvatar.getInventory()
        numWorkQuests = 0
        if inv:
            questList = inv.getQuestList()
            for questId in questList:
                if not QuestLadderDB.getFamePath(questId):
                    numWorkQuests += 1

        hasStoryQuest = False
        for offer in offers:
            if QuestLadderDB.getFamePath(offer.getQuestId()):
                hasStoryQuest = True

        if not hasStoryQuest and numWorkQuests > QuestConstants.MAXIMUM_MERC_WORK:
            self.questMenuGUI = PDialog.PDialog(text=PLocalizer.QuestFull, style=OTPDialog.Acknowledge, command=questFull)
        else:
            self.questMenuGUI = QuestMenuGUI.QuestMenuGUI(offers, handleSelection, describeQuest)
        localAvatar.currentStoryQuests = []
        self.clearOffer()

    def presentBranchReset(self, declineOption=True):
        if not self.resetBranch:
            return

        def displayBranchOptions(offer, callback, descCallback):
            self.branchMenuGUI = BranchMenuGUI.BranchMenuGUI(offer, callback, descCallback)

        def displayBranchDetails(offer):
            self.selectedOffer = offer
            self.cleanUpQuestDetails()
            self.questDetailGUI = QuestDetailGUI(offer, None)
            self.questDetailGUI.showPanel()
            base.questdet = self.questDetailGUI
            subtitleOptions = [PLocalizer.Accept]
            if declineOption:
                subtitleOptions = [
                 PLocalizer.Decline, PLocalizer.Accept]
            localAvatar.guiMgr.subtitler.setPageChat('Is that your choice?', options=subtitleOptions, callback=handleBranchOption)
            return

        def handleBranchOption(option):
            if option == PLocalizer.Accept:
                if self.selectedOffer:
                    self.sendOfferResponse(0, offer=self.selectedOffer)
            else:
                self.offerOptions(False)
            self.adjustNPCCamera('back')
            self.cleanUpQuestDetails(hide=True)
            self.cleanUpBranchMenu()
            self.cleanUpQuestMenu()

        offer = QuestOffer.QuestOffer.create(self.resetBranch.getName(), localAvatar)
        if declineOption:
            subtitleOptions = [
             PLocalizer.Decline]
            self.acceptOnce('lastSubtitlePage', displayBranchOptions, [offer, None, displayBranchDetails])
            localAvatar.guiMgr.subtitler.setPageChat('', options=subtitleOptions, callback=handleBranchOption)
        else:
            subtitleOptions = []
            displayBranchOptions(offer, None, displayBranchDetails)
        self.ignore('doneChatPage')
        return

    def presentQuestReset(self):
        if not self.resetQuest:
            return

        def handleOption(option):
            if option == PLocalizer.Accept:
                self.resetQuest.startTimer()
            self.resetQuest = None
            self.__handleDoneChatPage(0)
            return

        self.questDetailGUI = QuestDetailGUI(None, None, self.resetQuest.questDNA)
        self.questDetailGUI.showPanel()
        localAvatar.guiMgr.subtitler.setPageChat('', options=[PLocalizer.Accept], callback=handleOption)
        return

    def presentQuestGiven(self, quest):
        self.resetBranch = None
        if self.resetBranch:
            container = localAvatar.questStatus.getContainer(quest.getQuestId())
            if container.parent and container.parent.getFirstQuestId() == quest.getQuestId():
                self.presentBranchReset(False)
                return
            else:
                self.resetBranch = None

        def handleOption(option):
            if len(localAvatar.currentStoryQuests):
                self.cleanUpQuestDetails(hide=True)
                while len(localAvatar.currentStoryQuests) and localAvatar.currentStoryQuests[0].getGiverId() != self.uniqueId:
                    localAvatar.currentStoryQuests.remove(localAvatar.currentStoryQuests[0])

            if len(localAvatar.currentStoryQuests):
                storyQuest = localAvatar.currentStoryQuests[0]
                self.presentQuestGiven(storyQuest)
                localAvatar.currentStoryQuests.remove(storyQuest)
            else:
                if hasattr(quest, 'questDNA') and quest.questDNA.getTimeLimit():
                    quest.startTimer()
                self.__handleDoneChatPage(0)

        self.questDetailGUI = QuestDetailGUI(None, None, quest)
        self.questDetailGUI.showPanel()
        localAvatar.guiMgr.subtitler.setPageChat('', options=[PLocalizer.Accept], callback=handleOption)
        base.questdet = self.questDetailGUI
        self.ignore('doneChatPage')
        return

    def adjustNPCCamera(self, direction):
        dummy = NodePath('dummy')
        dummy.reparentTo(camera)
        if direction == 'forward':
            dummy.setH(dummy, -15)
            dummy.setY(dummy, 0.75)
            duration = 0.7
        else:
            dummy.setY(dummy, -0.75)
            dummy.setH(dummy, 15)
            duration = 0.5
        dummy.wrtReparentTo(camera.getParent())
        camH, dummyH = getShortestRotation(camera.getH(), dummy.getH())
        self.questDetailCamera = Parallel(LerpFunc(camera.setH, duration=duration, fromData=camH, toData=dummyH, blendType='easeInOut'), LerpFunc(camera.setY, duration=duration, fromData=camera.getY(), toData=dummy.getY(), blendType='easeInOut'))
        dummy.removeNode()
        self.questDetailCamera.start()

    def getOfferedQuests(self):
        return list(self.offers)

    def sendOfferResponse(self, index, ladder=False, offer=None):
        if index == QuestConstants.CANCEL_QUEST:
            self.dialogOpen = False
        if offer:
            self.sendUpdate('assignBranchOffer', [offer])
        else:
            self.sendUpdate('setOfferResponse', [index, ladder])
        self.offers = None
        self.clearOffer()
        return

    def b_setPageNumber(self, paragraph, pageNumber):
        self.setPageNumber(paragraph, pageNumber)
        self.d_setPageNumber(paragraph, pageNumber)

    def d_setPageNumber(self, paragraph, pageNumber):
        pass

    def playQuestString(self, questStr, timeout=False, quitButton=1, useChatBubble=False, confirm=False, animSet=None):
        self.notify.debug('playQuestString %s, %s, %s, %s' % (timeout, quitButton, useChatBubble, confirm))
        if questStr.find('quest_') == 0:
            nmp = QuestParser.NPCMoviePlayer(questStr, localAvatar, self)
            nmp.play()
            self.npcMoviePlayer = nmp
        else:
            self.firstDialog = False
            self.dialogAnimSet = animSet
            if questStr:
                if timeout:
                    if useChatBubble:
                        self.setPageChat(localAvatar.doId, 0, questStr, 0, extraChatFlags=CFSpeech | CFTimeout, pageButton=False)
                    else:
                        base.localAvatar.guiMgr.subtitler.setPageChat(questStr, timeout=timeout)
                    return
                else:
                    self.playingQuestString = True
                    if self.newOffer == False:
                        questStr += '\x07'
                    base.localAvatar.guiMgr.subtitler.setPageChat(questStr, confirm=confirm)
                    self.dialogOpen = True
                self.playAnimation(0)
                if quitButton == 1 or confirm:
                    self.accept('doneChatPage', self.__handleDoneChatPage)
                if base.localAvatar.guiMgr.subtitler.getNumChatPages() == 1:
                    self.__handleNextChatPage(0, 0)
                else:
                    self.accept('nextChatPage', self.__handleNextChatPage)

    def __handleNextChatPage(self, pageNumber, elapsed):
        self.notify.debug('handleNextChatPage pageNumber = %s, elapsed = %s' % (pageNumber, elapsed))
        if pageNumber == base.localAvatar.guiMgr.subtitler.getNumChatPages() - 1:
            self.ignore('nextChatPage')
            self.playingQuestString = False
            self.presentBranchReset()
            self.presentQuestReset()
            self.presentOffer()
        self.playAnimation(pageNumber)

    def __handleDoneChatPage(self, elapsed):
        self.ignore('nextChatPage')
        self.ignore('doneChatPage')
        self.playingQuestString = False
        self.dialogOpen = False
        if self.newDialog:
            self.playDialog()
        if not self.hasOpenGUI():
            self.interactMode = 1
            self.cancelInteraction(base.localAvatar)
        self.cancelInteraction(base.localAvatar)

    def playAnimation(self, index):
        if self.animationIval:
            self.animationIval.finish()
            self.animationIval = None
        if self.dialogAnimSet:
            if len(self.dialogAnimSet) > index and self.dialogAnimSet[index]:
                self.animationIval = Sequence(Wait(0.5), Func(self.gameFSM.request, 'Emote'), Func(self.playEmote, self.dialogAnimSet[index]))
                self.animationIval.start()
        return

    def playDialog(self):
        self.notify.warning('playDialog() needs override!')

    def setQuestsCompleted(self, menuFlag, completedContainerIds, completedChainedQuestIds, completedQuestIds, completedQuestDoIds):
        questStr = ''
        self.cleanUpQuestDetails()

        def handleOption(option, questStr, menuFlag, confirm, animSet):
            self.cleanUpQuestDetails(hide=True)
            self.playQuestString(questStr, quitButton=menuFlag, confirm=True, animSet=animSet)

        if len(completedContainerIds):
            if completedContainerIds[0] in ['c3visitJack']:
                return
            if len(completedContainerIds) > 1:
                self.notify.warning('Multiple simultaneous completed quest containers for the same NPC: %s!' % completedContainerIds)
            containerId = completedContainerIds[0]
            self.containerId = containerId
            container = QuestLadderDB.getContainer(containerId)
            if container:
                dialogId = container.getDialogAfter()
                if dialogId:
                    self.requestDialog(dialogId)
                    return
                questStr = container.getStringAfter()
                animSet = container.getAnimSetAfter()
                localAvatar.b_setGameState('NPCInteract', localArgs=[self, False, False])
                if hasattr(self, '_questRewardsEarned'):
                    self.questRewardGUI = QuestRewardGUI(container, self._questRewardsEarned)
                    localAvatar.guiMgr.subtitler.setPageChat('', options=[PLocalizer.Continue], callback=handleOption, extraArgs=[questStr, menuFlag, True, animSet])
                else:
                    handleOption(questStr, menuFlag, True, animSet)
                return
            else:
                self.notify.warning('%s not in QuestLadderDB!' % containerId)
        if len(completedChainedQuestIds):
            pass
        if len(completedQuestIds):
            if len(completedContainerIds) == 0:
                questId = completedQuestIds[0]
                quest = QuestDB.QuestDict.get(questId)
                if quest:
                    questStr = quest.getStringAfter()
                    animSet = quest.getAnimSetAfter()
                    self.notify.debug('%s stringAfter: %s' % (questId, questStr))
                    if hasattr(self, '_questRewardsEarned'):
                        print 'GOT questRewardsEarned: %s' % self._questRewardsEarned
                        self.questRewardGUI = QuestRewardGUI(quest, self._questRewardsEarned)
                        localAvatar.guiMgr.subtitler.setPageChat('', options=[PLocalizer.Continue], callback=handleOption, extraArgs=[questStr, menuFlag, True, animSet])
                    else:
                        handleOption(questStr, menuFlag, True, animSet)
                else:
                    self.notify.warning('%s not in QuestDB!' % questId)
            localAvatar.b_setGameState('NPCInteract', localArgs=[self, True, False])
        if len(completedQuestIds) == 0 and len(completedChainedQuestIds) == 0 and len(completedContainerIds) == 0:
            if not self.hasOpenGUI():
                self.cancelInteraction(base.localAvatar)

    def requestQuestReset(self, questId):
        self.resetQuest = localAvatar.getQuestById(questId)
        if self.resetQuest:
            questStr = self.resetQuest.questDNA.getStringBefore()
            self.cleanUpQuestDetails(hide=True)
            self.playQuestString(questStr, quitButton=True, confirm=True)
            localAvatar.b_setGameState('NPCInteract', localArgs=[self, True, False])

    def requestBranchReset(self, questId):
        quest = localAvatar.getQuestById(questId)
        self.resetBranch = quest.getBranchParent(localAvatar)
        resetBranchDNA = QuestLadderDB.getContainer(self.resetBranch.getQuestId())
        questStr = resetBranchDNA.getStringBefore()
        self.cleanUpQuestDetails(hide=True)
        self.playQuestString(questStr, quitButton=False, confirm=True)
        localAvatar.b_setGameState('NPCInteract', localArgs=[self, True, False])

    def requestDialog(self, dialogId=None):
        self.endDialog()
        if not dialogId:
            availableDialogs = []
            npcDialogs = DialogDict.get(self.getUniqueId())
            if npcDialogs:
                for dialogId in npcDialogs:
                    firstDialogProcess = npcDialogs.get(dialogId).get(0)[0]
                    if firstDialogProcess.prereq and firstDialogProcess.avCanParticipate(localAvatar):
                        availableDialogs.append(dialogId)

        else:
            availableDialogs = [
             dialogId]
        localAvatar.b_setGameState('NPCInteract', localArgs=[self, True, True])
        self.accept('endDialogNPCInteract', self.endDialog)
        self.dialogProcessMaster = DialogProcessMaster(self, availableDialogs)
        taskMgr.doMethodLater(0.25, self.startDialog, 'startDialogProcessMaster')

    def startDialog(self, task=None):
        if self.dialogProcessMaster:
            self.dialogProcessMaster.start()

    def endDialog(self):
        taskMgr.remove('startDialogProcessMaster')
        self.ignore('endDialogNPCInteract')
        if self.dialogProcessMaster:
            self.dialogProcessMaster.stop()
            self.dialogProcessMaster = None
        return

    def requestDialogInteraction(self, dialogId):
        self.sendUpdate('requestDialogInteraction', [dialogId])

    def endDialogInteraction(self, dialogId):
        self.sendUpdate('endDialogInteraction', [dialogId])

    def requestDialogQuestAdvancement(self, questId, dialogId):
        self.sendUpdate('requestDialogQuestAdvancement', [questId, dialogId])

    def requestDialogQuestAssignment(self, questId, dialogId):
        self.sendUpdate('requestDialogQuestAssignment', [questId, dialogId])

    def requestDialogQuestOffer(self, questId, dialogId):
        self.sendUpdate('requestDialogQuestOffer', [questId, dialogId])

    def setDialogQuestOffer(self, questOffer):
        self.dialogQuestOffer = questOffer
        messenger.send('setDialogQuestOffer')

    def showDialogQuestOffer(self):
        if self.dialogQuestOffer:
            self.questDetailGUI = QuestDetailGUI(self.dialogQuestOffer, None)
            self.questDetailGUI.showPanel()
        return

    def assignDialogQuestOffer(self):
        if self.dialogQuestOffer:
            self.sendUpdate('assignDialogQuestOffer')

    def showQuestRewards(self):
        if hasattr(self, '_questRewardsEarned') and self.containerId:
            container = QuestLadderDB.getContainer(self.containerId)
            self.questRewardGUI = QuestRewardGUI(container, self._questRewardsEarned)

    def hideQuestRewards(self):
        if self.questRewardGUI:
            self.questRewardGUI.destroy()
            self.questRewardGUI = None
        return

    def requestNPCHostile(self, npcId, dialogId):
        self.sendUpdate('requestNPCHostile', [npcId, dialogId])

    def playDialogMovie(self, dialogId, doneCallback=None, oldLocalAvState=None):
        movieChoice = InteractGlobals.getNPCTutorial(dialogId)
        if movieChoice == None:
            movieChoice = dialogId
        globalClock.tick()
        self.currentDialogMovie = QuestParser.NPCMoviePlayer(movieChoice, localAvatar, self)
        self.currentDialogMovie.overrideOldAvState(oldLocalAvState)
        self.currentDialogMovie.play()
        self.acceptOnce('dialogFinish', self.stopDialogMovie, extraArgs=[doneCallback])
        return

    def stopDialogMovie(self, doneCallback):
        if hasattr(self, 'currentDialogMovie'):
            self.currentDialogMovie.npc.showName()
            self.currentDialogMovie.npc.nametag3d.setZ(0)
            self.currentDialogMovie.finishUpAll()
            del self.currentDialogMovie
            self.sendUpdate('dialogMovieComplete')
            if doneCallback:
                doneCallback()

    def swapCurrentDialogMovie(self, newDialogMovie):
        if hasattr(self, 'currentDialogMovie'):
            if newDialogMovie:
                oldAvState = self.currentDialogMovie.overrideOldAvState(None)
                newDialogMovie.overrideOldAvState(oldAvState)
            self.currentDialogMovie.finishUpAll()
        self.currentDialogMovie = newDialogMovie
        return

    def getQuestGiverId(self):
        return self.getUniqueId()

    def hasQuestOffersForLocalAvatar(self):
        av = localAvatar
        inventory = av.getInventory()
        selfId = self.getQuestGiverId()
        if inventory:
            numInProgress = 0
            for quest in inventory.getQuestList():
                questType = self.QuestIconDontCare
                if quest.tasks is None:
                    self.notify.warning('quest %s: does not contain a dna; potential for crash.' % quest.getQuestId())
                    return False
                for task, taskState in zip(quest.tasks, quest.taskStates):
                    if isinstance(task, QuestTaskDNA.VisitTaskDNA):
                        if task.npcId == selfId:
                            questStatus = self.QuestIconComplete
                            return (
                             questType, questStatus)

                if quest.canBeReturnedTo(selfId):
                    isComplete = False
                    if quest.isComplete():
                        container = localAvatar.questStatus.getContainer(quest.getQuestId())
                        if container and container.parent and container.parent.isChoice():
                            isComplete = True
                            for q in container.parent.getContainers():
                                if q.quest and not q.quest.isComplete():
                                    isComplete = False

                        else:
                            isComplete = True
                    if isComplete:
                        questStatus = self.QuestIconComplete
                        return (
                         questType, questStatus)
                    else:
                        numInProgress += 1

        else:
            self.notify.warning('avatar does not have inventory yet')
            return False
        offerDict = {}
        fromQuests = []
        prereqExcludes = base.config.GetString('exclude-prereq-quests', '')
        for questId, questDNA in QuestDB.QuestDict.items():
            if prereqExcludes and questId in prereqExcludes:
                continue
            passed = True
            for prereq in questDNA.prereqs:
                if not prereq.giverCanGive(selfId):
                    passed = False
                    break
                if not prereq.avIsReady(localAvatar):
                    passed = False
                    break
                if questDNA.minLevel > localAvatar.level:
                    passed = False
                    break
                if not base.cr.questDependency.checkDependency(questId, localAvatar.getQuestLadderHistory(), 1):
                    passed = False
                    break
                boolWeapLvlCheck = (questDNA.weapLvlType != None) & (questDNA.minWeapLevel > 0)
                if boolWeapLvlCheck & (questDNA.minWeapLevel > getLevelFromTotalReputation(questDNA.weapLvlType, inventory.getReputation(questDNA.weapLvlType))[0]):
                    passed = False
                    break
                if questDNA.getAcquireOnce():
                    history = localAvatar.getQuestLadderHistory()
                    questLadderId = base.cr.questDynMap.findQuestLadderInt(questId)
                    containsLadderId = history.count(questLadderId)
                    if containsLadderId:
                        passed = False
                        break
                if questDNA.getHoliday() is not None:
                    holidayId = questDNA.getHoliday()
                    if base.cr.newsManager and not base.cr.newsManager.getHoliday(holidayId):
                        passed = False
                        break

            if questDNA.prereqs and passed:
                fromQuests.append(questDNA)

        if len(fromQuests):
            inventory = av.getInventory()
            if inventory:
                questsLeft = []
                questList = inventory.getQuestList()
                for questDNA in fromQuests:
                    questId = questDNA.questId
                    if not av.questStatus.hasLadderQuestId(questId) and questId not in [ x.questId for x in questList ]:
                        questsLeft.append(questDNA)

                fromQuests = questsLeft
        if fromQuests:
            questType = self.QuestIconWork
            for quest in fromQuests:
                if QuestLadderDB.getFamePath(quest.questId):
                    questType = self.QuestIconStory
                    break

            questStatus = self.QuestIconNew
            return (
             questType, questStatus)
        if numInProgress:
            questStatus = self.QuestIconProgress
            return (
             questType, questStatus)
        return False

    def loadQuestIcons(self):
        if not DistributedQuestGiver.QuestIconWorkTexture:
            DistributedQuestGiver.QuestIconWorkTexture = loader.loadModel('models/gui/new_work_quest_icon')
            DistributedQuestGiver.QuestIconStoryTexture = loader.loadModel('models/gui/new_story_quest_icon')
            discardNP = DistributedQuestGiver.QuestIconStoryTexture.find('**/pPlane2')
            if not discardNP.isEmpty():
                discardNP.removeNode()
            gui = loader.loadModel('models/gui/toplevel_gui')
            DistributedQuestGiver.QuestIconProgressTexture = gui.find('**/quest_pending_icon')
            DistributedQuestGiver.QuestIconCompleteTexture = gui.find('**/reward_waiting_icon')

    def updateNametagQuestIcon(self, questId=None, item=None, note=None):
        offers = self.hasQuestOffersForLocalAvatar()
        if self.nametagIcon:
            self.nametagIcon.removeNode()
        if self.nametagIconGlow:
            self.nametagIconGlow.removeNode()
        self.loadQuestIcons()
        if offers:
            type, status = offers
            if status == DistributedQuestGiver.QuestIconNew:
                if type == DistributedQuestGiver.QuestIconStory:
                    self.nametagIcon = DistributedQuestGiver.QuestIconStoryTexture.copyTo(self.nametag3d)
                else:
                    self.nametagIcon = DistributedQuestGiver.QuestIconStoryTexture.copyTo(self.nametag3d)
                self.nametagIcon.setScale(3.5)
            elif status == DistributedQuestGiver.QuestIconComplete:
                self.nametagIcon = DistributedQuestGiver.QuestIconCompleteTexture.copyTo(self.nametag3d)
                self.nametagIcon.setScale(12)
            elif status == DistributedQuestGiver.QuestIconProgress:
                self.nametagIcon = DistributedQuestGiver.QuestIconProgressTexture.copyTo(self.nametag3d)
                self.nametagIcon.setScale(12)
            else:
                self.notify.error('invalid quest status: %s or type: %s' % (status, type))
        else:
            if self.nametagIcon:
                self.nametagIcon.detachNode()
            if self.nametagIconGlow:
                self.nametagIconGlow.detachNode()
        if self.nametagIcon:
            self.nametagIcon.setPos(0, 0, 3.5)
            if self.getNameText() is None:
                base.cr.centralLogger.writeClientEvent('NPC %s, %s: has no nameText, type = %s, status = %s!' % (self, self.getName(), type, status))
                if self.nametagIcon:
                    self.nametagIcon.detachNode()
                if self.nametagIconGlow:
                    self.nametagIconGlow.detachNode()
                return
            self.nametagIcon.reparentTo(self.getNameText())
            self.nametagIcon.setDepthWrite(0)
            if status == DistributedQuestGiver.QuestIconComplete or status == DistributedQuestGiver.QuestIconNew:
                self.nametagIconGlow = loader.loadModel('models/effects/lanternGlow')
                self.nametagIconGlow.reparentTo(self.nametag.getNameIcon())
                self.nametagIconGlow.setScale(20.0)
                self.nametagIconGlow.setColorScaleOff()
                self.nametagIconGlow.setFogOff()
                self.nametagIconGlow.setLightOff()
                self.nametagIconGlow.setPos(0, -0.05, 3.0)
                self.nametagIconGlow.setDepthWrite(0)
                self.nametagIconGlow.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
                self.nametagIconGlow.setColor(0.85, 0.85, 0.85, 0.85)
        self.loadShopCoin()
        return

    def forceDoneChatPage(self):
        self.__handleDoneChatPage(0)
