from direct.directnotify import DirectNotifyGlobal
from pirates.quest import QuestConstants, QuestAvatarBase, QuestHolder
from pirates.quest.QuestStepIndicator import QuestStepIndicator
from pirates.quest.QuestPath import QuestStep
from pirates.quest import QuestLadderDB
from direct.showbase.PythonUtil import report
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PDialog
from pirates.piratesgui import PiratesGuiGlobals
from otp.otpgui import OTPDialog

class DistributedQuestAvatar(QuestAvatarBase.QuestAvatarBase, QuestHolder.QuestHolder):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedQuestAvatar')

    def __init__(self):
        QuestAvatarBase.QuestAvatarBase.__init__(self)
        QuestHolder.QuestHolder.__init__(self)
        self.lastQuestStepRequest = None
        self.questStep = None
        self.oldQuestStep = None
        self.questIndicator = QuestStepIndicator()
        self.activeQuestId = ''
        self.activeQuestIdPending = ''
        self.popupDialog = None
        return

    def delete(self):
        self.activeQuestId = ''
        self.activeQuestIdPending = ''
        self.questIndicator.delete()
        self.questStep = None
        self.oldQuestStep = None
        self.lastQuestStepRequest = None
        return

    def setQuestHistory(self, history):
        self.questHistory = history

    def getQuestHistory(self):
        return self.questHistory

    def setQuestLadderHistory(self, history):
        self.questLadderHistory = history

    def getQuestLadderHistory(self):
        return self.questLadderHistory

    def setCurrentQuestChoiceContainers(self, containers):
        self.currentQuestChoiceContainers = containers

    def getCurrentQuestChoiceContainers(self):
        return self.currentQuestChoiceContainers

    def requestDropQuest(self, questId):
        DistributedQuestAvatar.notify.debug('requestDropQuest: %s (%s)' % (questId, self.doId))
        container = QuestLadderDB.getContainer(questId)
        parentContainer = QuestLadderDB.getParentContainer(container)
        if parentContainer and parentContainer.isChoice():
            for ctr in parentContainer.getContainers():
                self.sendUpdate('requestDropQuest', [ctr.getQuestId()])

        else:
            self.sendUpdate('requestDropQuest', [questId])

    def requestShareQuest(self, questId):
        DistributedQuestAvatar.notify.debug('requestShareQuest: %s (%s)' % (questId, self.doId))
        self.sendUpdate('requestShareQuest', [questId])

    def handleQuestDropped(self, droppedQuestId):
        self.questStatus.handleQuestDropped(droppedQuestId)

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def refreshActiveQuestStep(self, forceClear=False, forceRefresh=False):
        if self.activeQuestId:
            if forceRefresh or forceClear:
                self.lastQuestStepRequest = None
            if not forceClear:
                self.b_requestQuestStep(self.activeQuestId)
            else:
                self.b_requestQuestStep('')
        return

    def questStepAutoRefresh(self):
        return True

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def b_requestQuestStep(self, questId):
        if questId:
            stepRequest = (self.getLocation()[0], questId)
            if stepRequest[0]:
                if self.lastQuestStepRequest == stepRequest:
                    if self.questStep:
                        self.l_setQuestStep(self.questStep)
                    elif self.oldQuestStep:
                        self.l_setQuestStep(self.oldQuestStep)
                    else:
                        self.d_requestQuestStep(stepRequest)
                        self.l_requestQuestStep(stepRequest)
                else:
                    self.d_requestQuestStep(stepRequest)
                    self.l_requestQuestStep(stepRequest)
        else:
            self.l_requestQuestStep(None)
            self.l_setQuestStep(None)
        return

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def d_requestQuestStep(self, stepRequest):
        self.sendUpdate('requestQuestStep', [stepRequest[1]])

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def l_requestQuestStep(self, stepRequest):
        if stepRequest:
            self.lastQuestStepRequest = stepRequest
            self.oldQuestStep = None
        return

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def setQuestStep(self, questStepArgs):
        originDoId, stepDoId, typeData = questStepArgs
        if typeData[0] == 10:
            typeDict = dict(zip(('stepType', 'posH', 'islandUid', 'targetAreaUid',
                                 'nodeSizes', 'nearOffset', 'nearVis'), typeData))
            questStep = QuestStep(*(originDoId, stepDoId), **typeDict)
        else:
            questStep = QuestStep(*((originDoId, stepDoId) + typeData))
        self.l_setQuestStep(questStep)
        if questStep == QuestStep.getNullStep():
            localAvatar.guiMgr.mapPage.worldMap.mapBall.removeDart()
            return
        mapPage = localAvatar.guiMgr.mapPage
        doId = base.cr.uidMgr.uid2doId.get(questStep.getIsland())
        island = base.cr.doId2do.get(doId)
        if island:
            pos = island.getPos()
            if mapPage.worldMap.mapBall.questDartPlaced:
                localAvatar.guiMgr.mapPage.worldMap.mapBall.updateDart('questStep', pos)
            else:
                localAvatar.guiMgr.mapPage.addQuestDart('questStep', pos)
        else:
            localAvatar.guiMgr.mapPage.removeQuestDart('questStep')

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def l_setQuestStep(self, questStep):
        if questStep == QuestStep.getNullStep():
            self.oldQuestStep = None
            questStep = None
        elif not questStep and self.questStep:
            self.oldQuestStep = self.questStep
        self.questStep = questStep
        self.questIndicator.showQuestStep(self.questStep)
        return

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def b_requestActiveQuest(self, questId, localSet=False):
        if not questId == self.activeQuestId:
            self.d_requestActiveQuest(questId)
        if localSet:
            self.l_setActiveQuest(questId)
        self.l_requestActiveQuest(questId)

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def d_requestActiveQuest(self, questId):
        self.sendUpdate('requestActiveQuest', [questId])

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def l_requestActiveQuest(self, questId):
        self.b_requestQuestStep(questId)

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def setActiveQuest(self, questId):
        self.l_setActiveQuest(questId)

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def l_setActiveQuest(self, questId):
        if questId != self.activeQuestId:
            self.activeQuestId = questId
            messenger.send('localAvatarActiveQuestId', sentArgs=[self.activeQuestId])
            self.b_requestQuestStep(questId)
            if self.guiMgr and self.guiMgr.mapPage:
                questDartName = localAvatar.guiMgr.mapPage.worldMap.mapBall.questDartName
                if questDartName:
                    localAvatar.guiMgr.mapPage.worldMap.mapBall.updateDartText(questDartName, questId)
            if self.guiMgr.questPage:
                self.guiMgr.questPage.titleList.select(questId)

    def d_findNewActiveQuest(self, oldQuestId):
        self.sendUpdate('findNewActiveQuest', [oldQuestId])

    def popupProgressBlocker(self, questId):
        if questId == 'c3visitJoshamee':
            localAvatar.guiMgr.showNonPayer(quest=questId, focus=9)
            return
        elif questId == 'c4.1visitValentina':
            localAvatar.guiMgr.showStayTuned(quest=questId, focus=0)
            return
        popupDialogText = PLocalizer.ProgressBlockPopupDialog.get(questId)
        if popupDialogText:
            self.popupDialog = PDialog.PDialog(text=popupDialogText, style=OTPDialog.Acknowledge, command=self.__cleanupDialog)
        else:
            localAvatar.guiMgr.showNonPayer(quest=questId, focus=9)
            self.notify.warning('%s: No progressBlock dialog found!' % questId)

    def __cleanupDialog(self, value=None):
        if self.popupDialog:
            self.popupDialog.destroy()
            del self.popupDialog
            self.popupDialog = None
        return

    def d_useDowsingRod(self):
        self.sendUpdate('useDowsingRod', [])

    def dowsingRodResult(self, result):
        if self.isLocal():
            if result == QuestConstants.DowsingRodResults.DOWSING_ROD_NOT_AVAILABLE:
                localAvatar.guiMgr.createWarning(PLocalizer.DowsingRodNotAvailable, PiratesGuiGlobals.TextFG6)
            elif result == QuestConstants.DowsingRodResults.DOWSING_ROD_WARMER_FAR:
                localAvatar.guiMgr.createWarning(PLocalizer.DowsingRodWarmerFar, PiratesGuiGlobals.TextFG11)
            elif result == QuestConstants.DowsingRodResults.DOWSING_ROD_WARMER:
                localAvatar.guiMgr.createWarning(PLocalizer.DowsingRodWarmer, PiratesGuiGlobals.TextFG11)
            elif result == QuestConstants.DowsingRodResults.DOWSING_ROD_WARMER_CLOSE:
                localAvatar.guiMgr.createWarning(PLocalizer.DowsingRodWarmerClose, PiratesGuiGlobals.TextFG11)
            elif result == QuestConstants.DowsingRodResults.DOWSING_ROD_COLDER:
                localAvatar.guiMgr.createWarning(PLocalizer.DowsingRodColder, PiratesGuiGlobals.TextFG5)
            elif result == QuestConstants.DowsingRodResults.DOWSING_ROD_COLDER_CLOSE:
                localAvatar.guiMgr.createWarning(PLocalizer.DowsingRodColderClose, PiratesGuiGlobals.TextFG5)
            elif result == QuestConstants.DowsingRodResults.DOWSING_ROD_HOT:
                localAvatar.guiMgr.createWarning(PLocalizer.DowsingRodHot, PiratesGuiGlobals.TextLT11)
            elif result == QuestConstants.DowsingRodResults.DOWSING_ROD_SAME:
                localAvatar.guiMgr.createWarning(PLocalizer.DowsingRodSame, PiratesGuiGlobals.TextFG2)
            elif result == QuestConstants.DowsingRodResults.DOWSING_ROD_COMPLETE:
                localAvatar.guiMgr.createWarning(PLocalizer.DowsingRodNotAvailable, PiratesGuiGlobals.TextFG6)
            elif result == QuestConstants.DowsingRodResults.DOWSING_ROD_FIRST_TIME:
                localAvatar.guiMgr.createWarning(PLocalizer.DowsingRodFirstTime, PiratesGuiGlobals.TextFG2)