from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from pirates.quest import QuestDB, Quest, QuestBase, QuestTaskDNA, QuestConstants
from pirates.cutscene import Cutscene, CutsceneData
from pirates.piratesgui import NewTutorialPanel
from pirates.piratesbase import PLocalizer, PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.cutscene import CutsceneActor
QuestPopupDict = {'c2_visit_will_turner': ['leaveJail'],'c2.2defeatSkeletons': ['showSkeleton', 'closeShowSkeleton'],'c2_visit_tia_dalma': ['showJungleTia', 'closeShowJungleTia'],'c2.4recoverOrders': ['showNavy', 'closeShowNavy'],'c2.5deliverOrders': ['showGovMansion', 'closeShowGovMansion'],'c2.9visitDarby': ['showDarby', 'closeShowDarby'],'c2.10visitDockworker': ['showDinghy', 'closeShowDinghy'],'c2.11visitBarbossa': ['showBarbossa', 'closeShowbarbossa'],'c3visitJack': ['showTortugaJack', 'closeShowTortugaJack']}
QUEST_TYPE_AVATAR = 0
QUEST_TYPE_TM = 1

class DistributedQuest(DistributedObject.DistributedObject, QuestBase.QuestBase, Quest.Quest):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedQuest')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        QuestBase.QuestBase.__init__(self)
        Quest.Quest.__init__(self)
        self.type = QUEST_TYPE_AVATAR
        self.sceneObj = None
        self.targetObjIds = []
        self.setAsActive = False
        self.endEvent = ''
        self.popupDialog = None
        self.preloadedCutscenes = []
        self.prevLocalAvState = None
        self.viewedInGUI = True
        self.setOwningAv(localAvatar.doId)
        return

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        QuestBase.QuestBase.announceGenerate(self)
        self.setActive()
        messenger.send('localAvatarQuestAdded', [self])
        popupDialogText = QuestPopupDict.get(self.getQuestId())
        if popupDialogText:
            if base.localAvatar.showQuest:
                base.localAvatar.resetQuestShow()
                self.popupDialog = NewTutorialPanel.NewTutorialPanel(popupDialogText)
                self.popupDialog.activate()

                def closeTutorialWindow():
                    messenger.send(self.popupDialog.closeMessage)

                if self.getQuestId() == 'c2_visit_will_turner':
                    if localAvatar.style.getTutorial() != PiratesGlobals.TUT_GOT_SEACHEST:
                        self.removePopup()
                    self.accept('InputState-forward', self.removePopup)
                    self.accept('InputState-reverse', self.removePopup)
                    self.accept('InputState-turnLeft', self.removePopup)
                    self.accept('InputState-turnRight', self.removePopup)
                else:
                    self.popupDialog.setYesCommand(closeTutorialWindow)
        self.cr.uidMgr.addUid(self.questId, self.doId)

    def delete(self):
        self.cr.uidMgr.removeUid(self.questId)
        messenger.send('localAvatarQuestDeleted', [self])
        DistributedObject.DistributedObject.delete(self)
        QuestBase.QuestBase.delete(self)
        Quest.Quest.destroy(self)
        self.stopTimer()
        self.setInactive()
        self.__cleanupDialog()
        for currPreload in self.preloadedCutscenes:
            base.cr.cleanupPreloadedCutscene(currPreload)

        self.preloadedCutscenes = []

    def __cleanupDialog(self, value=None):
        if self.popupDialog:
            self.popupDialog.destroy()
            del self.popupDialog
            self.popupDialog = None
        taskMgr.remove('destroyPopup')
        self.ignore('InputState-forward')
        self.ignore('InputState-reverse')
        self.ignore('InputState-turnLeft')
        self.ignore('InputState-turnRight')
        return

    def setTaskStates(self, taskStates):
        oldTaskStates = getattr(self, 'taskStates', None)
        lookingForItems = {}
        if self.isGenerated():
            for task, taskState in zip(self.questDNA.tasks, oldTaskStates):
                if task.__class__ in QuestTaskDNA.RecoverItemClasses:
                    lookingForItems[task.item] = (
                     taskState.getAttempts(), taskState.getProgress(), taskState.getGoal())

        Quest.Quest.setTaskStates(self, taskStates)
        if self.isGenerated():
            for task, taskState in zip(self.questDNA.tasks, self.taskStates):
                if task.__class__ in QuestTaskDNA.RecoverItemClasses:
                    oldAttempts, oldProgress, oldGoal = lookingForItems[task.item]
                    newProgress = taskState.getProgress()
                    newAttempts = taskState.getAttempts()
                    newGoal = taskState.getGoal()
                    if oldProgress >= oldGoal:
                        note = QuestConstants.QuestItemNotification.AlreadyFound
                    elif newProgress > oldProgress:
                        if newProgress >= newGoal:
                            note = QuestConstants.QuestItemNotification.ProgressMadeGoalMet
                        else:
                            note = QuestConstants.QuestItemNotification.ProgressMadeGoalUnmet
                    elif newAttempts > oldAttempts:
                        note = QuestConstants.QuestItemNotification.ValidAttempt
                    else:
                        note = QuestConstants.QuestItemNotification.InvalidAttempt
                    messenger.send('localAvatarQuestItemUpdate', [self, task.item, note])
                    return

        if self.isGenerated():
            if self.isComplete():
                messenger.send('localAvatarQuestComplete', [self])
                if self.getQuestId() == 'c2_visit_will_turner':
                    messenger.send('closeTutorialWindow')
                self.__cleanupDialog()
            else:
                messenger.send('localAvatarQuestUpdate', [self])
        return

    def announceNewQuest(self):
        base.localAvatar.guiMgr.showQuestAddedText(self)

    def getProgressMsg(self):
        if self.taskStates:
            questTaskDNA = self.questDNA.getTaskDNAs()[0]
            taskState = self.taskStates[0]
            return questTaskDNA.getProgressMessage(taskState)
        else:
            return (None, None)
        return None

    def getCompleteText(self):
        if self.type == QUEST_TYPE_AVATAR:
            return 'QUEST COMPLETE!'
        else:
            return 'OBJECTIVE COMPLETE!'

    def startFinalizeScene(self, idx, giverId, endEvent=None):
        sceneInfo = self.questDNA.getFinalizeInfo()
        sceneToPlay = sceneInfo[idx]
        self.endEvent = endEvent
        if sceneToPlay.get('type') == 'dialog':
            npc = base.cr.doId2do.get(giverId)
            if npc == None:
                self.doneFinalizeScene()
                self.notify.warning('no npc %s found for %s' % (giverId, self))
                return
            dialogId = sceneToPlay.get('sceneId')
            npc.playDialogMovie(dialogId, self.doneFinalizeScene, self.prevLocalAvState)
            if not self.prevLocalAvState:
                self.prevLocalAvState = npc.currentDialogMovie.oldGameState
        elif sceneToPlay.get('type') == 'cutscene':
            name = sceneToPlay.get('sceneId')
            preloadInfo = sceneToPlay.get('preloadInfo', [])
            for currPreload in preloadInfo:
                base.cr.preloadCutscene(currPreload)
                self.preloadedCutscenes.append(currPreload)

            plCutscene = base.cr.getPreloadedCutsceneInfo(name)
            if plCutscene == None or plCutscene.isEmpty():
                self.sceneObj = Cutscene.Cutscene(self.cr, name, self.doneFinalizeScene, giverId)
                self.sceneObj.play()
            else:
                self.sceneObj = plCutscene
                plCutscene.initialize(self.doneFinalizeScene, giverId, True)
                plCutscene.play()
            if not self.prevLocalAvState:

                def cutsceneStarted():
                    localCutActor = self.sceneObj.getActor(CutsceneActor.CutLocalPirate.getActorKey())
                    self.prevLocalAvState = localCutActor.oldParams.gameState

                self.sceneObj.setStartCallback(cutsceneStarted)
            else:
                self.sceneObj.overrideOldAvState(self.prevLocalAvState)
        return

    def doneFinalizeScene(self):
        if self.sceneObj:
            self.sceneObj.destroy()
            self.sceneObj = None
        if self.cr:
            self.sendUpdate('doneFinalizeScene')
        if self.endEvent != '':
            messenger.send(self.endEvent)
        return

    def setActive(self):
        self.sendUpdate('setActive')
        self.setAsActive = True

    def setInactive(self):
        if self.setAsActive == True:
            if not hasattr(base, 'localAvatar'):
                self.notify.warning('Uh oh, tried to delete active questdoId %s when localAvatar was not present' % self.doId)
                return
            self.targetObjIds = []
            self.setAsActive = False

    def updateTargetLoc(self, pos, worldZone, targetObjId):
        self.targetObjIds.append(targetObjId)

    def amFinalized(self):
        messenger.send('localAvatarQuestFinalized', [self.doId])
        Quest.Quest.setFinalized(self, True)
        base.localAvatar.resetStoryQuest()
        if localAvatar.playRewardAnimation and localAvatar.getGameState() not in ['NPCInteract']:
            localAvatar.b_setGameState('OOBEmote', localArgs=[localAvatar.playRewardAnimation[0], localAvatar.playRewardAnimation[1]])
            localAvatar.playRewardAnimation = None
        return

    def removePopup(self, msg=None):
        if msg:
            taskMgr.remove('showLaterPopup')
            self.ignore('InputState-forward')
            self.ignore('InputState-reverse')
            self.ignore('InputState-turnLeft')
            self.ignore('InputState-turnRight')
            if self.popupDialog:
                taskMgr.doMethodLater(1, self.destroyPopup, 'destroyPopup', extraArgs=[])

    def destroyPopup(self):
        if self.popupDialog:
            self.popupDialog.destroy()
            self.popupDialog = None
        return

    def resetQuest(self):
        self.setFinished(False)
        self.setFinalized(False)
        localAvatar.guiMgr.questPage.updateQuestDetails(self)

    def updateTimer(self, task=None):
        self.setTimeRemaining(self.getTimeRemaining() - 1)
        if localAvatar.activeQuestId == self.questId:
            localAvatar.guiMgr.setQuestTimerText(self.getTimerText())
        if self.getTimeRemaining() <= 0:
            self.setTimedOut(True)
            self.sendUpdate('resetProgress', [localAvatar.getDoId(), True])
        else:
            taskMgr.doMethodLater(1.0, self.updateTimer, 'questTimerTask')

    def startTimer(self):
        timeLimit = self.questDNA.getTimeLimit() + 1
        taskMgr.remove('questTimerTask')
        self.setTimedOut(False)
        self.setTimeRemaining(timeLimit)
        self.sendUpdate('resetProgress', [localAvatar.getDoId(), False])
        if localAvatar.activeQuestId == self.questId:
            localAvatar.guiMgr.updateQuestStatusText(self.getQuestId())
        localAvatar.guiMgr.questPage.updateQuestIdDetails(self.getQuestId())
        taskMgr.doMethodLater(1.0, self.updateTimer, 'questTimerTask')

    def stopTimer(self):
        localAvatar.guiMgr.setQuestTimerText('')
        taskMgr.remove('questTimerTask')

    def getTimerText(self):
        if self.getTimeRemaining() > 0:
            minutes = str(self.getTimeRemaining() / 60)
            seconds = self.getTimeRemaining() % 60
            if seconds < 10:
                seconds = '0' + str(seconds)
            else:
                seconds = str(seconds)
            timeLeft = minutes + ':' + seconds
            return PLocalizer.TimerStatus % {'remainingTime': timeLeft}
        else:
            return PLocalizer.TimedOutStatus