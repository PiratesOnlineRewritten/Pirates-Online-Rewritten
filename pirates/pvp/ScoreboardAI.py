from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class ScoreboardAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('ScoreboardAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)