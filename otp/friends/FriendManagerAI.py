from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class FriendManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('FriendManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)