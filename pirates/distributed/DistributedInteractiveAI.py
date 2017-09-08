from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.directnotify import DirectNotifyGlobal
from pirates.distributed.DistributedLocatableObjectAI import DistributedLocatableAI

class DistributedInteractiveAI(DistributedNodeAI, DistributedLocatableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteractiveAI')

    ACCEPT = 1
    DENY = 0

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)

        self.userId = 0
        self.uniqueId = ''

    def __getSender(self):
        avatarId = self.air.getAvatarIdFromSender()

        if avatarId not in self.air.doId2do:
            return None

        avatar = self.air.doId2do[avatarId]

        if not avatar:
            return None

        return avatar

    def requestInteraction(self, doId, interactType, instant):
        avatar = self.__getSender()

        if not avatar or self.userId:
            self.d_rejectInteraction(avatar)
            return

        handle = self.handleRequestInteraction(avatar, interactType, instant)

        if not handle:
            self.d_rejectInteraction(avatar)
            return

        self.b_setUserId(avatar.doId)
        self.sendUpdateToAvatarId(avatar.doId, 'acceptInteraction', [])

    def handleRequestInteraction(self, avatar, interactType, instant):
        return self.DENY

    def requestExit(self):
        avatar = self.__getSender()

        if not avatar or not self.userId:
            self.d_rejectExit(avatar)
            return

        handle = self.handleRequestExit(avatar)

        if not handle:
            self.d_rejectExit(avatar)
            return

        self.b_setUserId(0)

    def demandExit(self):

        avatar = self.__getSender()

        if not avatar or not self.userID:
            return

        self.b_setUserId(0)

    def handleRequestExit(self, avatar):
        return self.DENY

    def d_rejectInteraction(self, avatar):
        self.sendUpdateToAvatarId(avatar.doId, 'rejectInteraction', [])

    def d_rejectExit(self, avatar):
        self.sendUpdateToAvatarId(avatar.doId, 'rejectExit', [])

    def d_offerOptions(self, avatar, optionIds, statusCodes):
        self.sendUpdateToAvatarId(avatar, 'offerOptions', [optionIds, statusCodes])

    def selectOption(self, optionId):
        pass

    def setUserId(self, userId):
        self.userId = userId

    def d_setUserId(self, userId):
        self.sendUpdate('setUserId', [userId])

    def b_setUserId(self, userId):
        self.setUserId(userId)
        self.d_setUserId(userId)

    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def d_setUniqueId(self, uniqueId):
        self.sendUpdate('setUniqueId', [uniqueId])

    def b_setUniqueId(self, uniqueId):
        self.setUniqueId(uniqueId)
        self.d_setUniqueId(uniqueId)

    def getUniqueId(self):
        return self.uniqueId
