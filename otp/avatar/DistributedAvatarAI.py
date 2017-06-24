from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class DistributedAvatarAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedAvatarAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)