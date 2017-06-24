from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class OtpAvatarManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('OtpAvatarManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)