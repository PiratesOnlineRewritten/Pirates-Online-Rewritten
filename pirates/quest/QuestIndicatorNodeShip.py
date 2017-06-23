from pirates.effects.RayOfLight import RayOfLight
from pirates.quest.QuestIndicatorGridNode import QuestIndicatorGridNode

class QuestIndicatorNodeShip(QuestIndicatorGridNode):

    def __init__(self, questStep):
        self.nearEffect = None
        QuestIndicatorGridNode.__init__(self, 'ShipIndicator', [
         300, 1500], questStep)
        self._selfRefreshTask = None
        self._refreshTargetLoc = None
        return

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def delete(self):
        QuestIndicatorGridNode.delete(self)
        if self.nearEffect:
            self.nearEffect.cleanUpEffect()
        self.nearEffect = None
        self.stopTargetRefresh()
        return

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def enterOff(self):
        QuestIndicatorGridNode.enterOff(self)
        self.stopNearEffect()

    def enterFar(self):
        QuestIndicatorGridNode.enterFar(self)
        self.requestTargetRefresh()

    def exitFar(self):
        QuestIndicatorGridNode.exitFar(self)
        self.stopTargetRefresh()

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def enterNear(self):
        QuestIndicatorGridNode.enterNear(self)
        self.startNearEffect()

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def exitNear(self):
        self.stopNearEffect()
        QuestIndicatorGridNode.exitNear(self)

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def enterAt(self):
        QuestIndicatorGridNode.enterAt(self)

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def exitAt(self):
        QuestIndicatorGridNode.exitAt(self)

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def stepObjArrived(self, stepObj):
        QuestIndicatorGridNode.stepObjArrived(self, stepObj)
        if self.getCurrentOrNextState() in ('Near', ):
            self.startNearEffect()

    def stepObjLeft(self):
        self.stopNearEffect()
        QuestIndicatorGridNode.stepObjLeft(self)

    def showEffect(self):
        QuestIndicatorGridNode.showEffect(self)
        self.startNearEffect()

    def hideEffect(self):
        QuestIndicatorGridNode.hideEffect(self)
        self.stopNearEffect()

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def startNearEffect(self):
        if self.muted:
            return
        if not self.nearEffect:
            self.nearEffect = RayOfLight()
            self.nearEffect.setBottomRayEnabled(self.wantBottomEffect)
            self.nearEffect.startLoop()
        if self.stepObj:
            self.nearEffect.reparentTo(self.stepObj)

    @report(types=['frameCount', 'args'], dConfigParam='quest-indicator')
    def stopNearEffect(self):
        if self.nearEffect:
            self.nearEffect.stopLoop()
            self.nearEffect = None
        return