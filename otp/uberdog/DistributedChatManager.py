from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from direct.directnotify import DirectNotifyGlobal

class DistributedChatManager(DistributedObjectGlobal):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedChatManagerAI')

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)

    def sendChatMessage(self, message, flags):
        self.sendUpdate('chatMessage', [message, flags])
