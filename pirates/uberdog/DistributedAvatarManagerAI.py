from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedAvatarManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAvatarManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)