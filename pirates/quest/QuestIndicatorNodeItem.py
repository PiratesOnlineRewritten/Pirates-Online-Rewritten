from pirates.quest.QuestIndicatorNode import QuestIndicatorNode

class QuestIndicatorNodeItem(QuestIndicatorNode):

    def __init__(self, questStep):
        self.pendingStepObj = None
        QuestIndicatorNode.__init__(self, 'ItemIndicator', [], questStep)
        return

    def delete(self):
        if self.pendingStepObj:
            base.cr.relatedObjectMgr.abortRequest(self.pendingStepObj)
            self.pendingStepObj = None
        QuestIndicatorNode.delete(self)
        return