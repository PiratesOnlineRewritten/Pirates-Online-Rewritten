from direct.showbase.DirectObject import DirectObject
from pirates.quest.DialogTree import *
from pirates.quest.DialogProcess import *

class DialogProcessMaster(DirectObject):

    def __init__(self, npc, dialogIds):
        self.npc = npc
        self.npcId = npc.getUniqueId()
        self.dialogIds = dialogIds
        self.dialogs = {}
        self.currDialogId = None
        self.currStepId = None
        self.currProcess = None
        self.currProcessIndex = 0
        self.stepHistory = []
        self.delayedProcessCleanup = []
        return

    def start(self):
        for dialogId in self.dialogIds:
            self.dialogs[dialogId] = DialogDict.get(self.npcId).get(dialogId)

        if len(self.dialogs.keys()) > 1:
            self.presentAvailableDialogs()
        else:
            self.beginDialog(dialogId)

    def stop(self):
        if self.currDialogId:
            self.npc.endDialogInteraction(self.currDialogId)
            self.currDialogId = None
        self.ignore('SwitchStep')
        self.ignore('DialogProcessEnded')
        if self.currProcess:
            self.currProcess.end()
            self.currProcess.cleanup()
        for process in self.delayedProcessCleanup:
            process.cleanup()

        self.delayedProcess = []
        self.currProcess = None
        self.currStepId = None
        self.currProcessIndex = 0
        self.stepHistory = []
        self.dialogIds = None
        self.dialogs = {}
        return

    def presentAvailableDialogs(self):
        pass

    def beginDialog(self, dialogId):
        self.npc.requestDialogInteraction(dialogId)
        self.currDialogId = dialogId
        self.beginStep(0)

    def beginStep(self, stepId):
        self.ignore('SwitchStep')
        self.stepHistory.append(stepId)
        self.currStepId = stepId
        self.beginProcess(0)
        self.acceptOnce('SwitchStep', self.beginStep)

    def beginProcess(self, processIndex):
        if self.currProcess:
            self.ignore('DialogProcessEnded')
            self.currProcess.end()
            if self.currProcess.delayCleanup:
                self.delayedProcessCleanup.append(self.currProcess)
            else:
                self.currProcess.cleanup()
        self.currProcessIndex = processIndex
        self.currProcess = self.dialogs.get(self.currDialogId).get(self.currStepId)[processIndex]
        if self.currStepId == 0 and self.currProcessIndex == 0 or self.currProcess.avCanParticipate(localAvatar):
            self.accept('DialogProcessEnded', self.tryNextProcess)
            self.currProcess.begin(self.npc, self.currDialogId)
        else:
            self.currProcess = None
            self.tryNextProcess()
        return

    def tryNextProcess(self):
        if len(self.dialogs.get(self.currDialogId).get(self.currStepId)) > self.currProcessIndex + 1:
            self.beginProcess(self.currProcessIndex + 1)
        else:
            self.stop()