from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.movement.DistributedMovingObjectAI import DistributedMovingObjectAI
from pirates.quest.DistributedQuestGiverAI import DistributedQuestGiverAI

class DistributedReputationAvatarAI(DistributedMovingObjectAI, DistributedInteractiveAI, DistributedQuestGiverAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedReputationAvatarAI')

    def __init__(self, air):
        DistributedMovingObjectAI.__init__(self, air)
        DistributedInteractiveAI.__init__(self, air)
        DistributedQuestGiverAI.__init__(self, air)