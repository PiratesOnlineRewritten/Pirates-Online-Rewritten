from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class SpeedchatRelayUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('SpeedchatRelayUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

    def forwardSpeedchat(self, receiverId, speedchatType, parameters, senderAccountId, senderPlayerName, todo):
        pass