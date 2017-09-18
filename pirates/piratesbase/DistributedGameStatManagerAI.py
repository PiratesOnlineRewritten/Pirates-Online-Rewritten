from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal
from pirates.piratesbase.GameStatManagerBase import GameStatManagerBase

class DistributedGameStatManagerAI(DistributedObjectAI, GameStatManagerBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGameStatManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        GameStatManagerBase.__init__(self)
        self.aggroModelIndex = 0

    def getAggroModelIndex(self):
        return self.aggroModelIndex
