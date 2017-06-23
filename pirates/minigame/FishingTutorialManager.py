

class FishingTutorialManager():

    def __init__(self):
        self.currentPriority = 0

    def showTutorial(self, contextId, priority=0):
        if not base.localAvatar.guiMgr.contextTutPanel.isFilled():
            self.currentPriority = 0
        if self.currentPriority > priority:
            return
        self.currentPriority = priority
        base.localAvatar.sendRequestContext(contextId)