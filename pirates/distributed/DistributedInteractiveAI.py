from direct.distributed.DistributedNodeAI import DistributedNodeAI
from direct.directnotify import DirectNotifyGlobal

class DistributedInteractiveAI(DistributedNodeAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInteractiveAI')

    ACCEPT = 1
    DENY = 0
    MULTIUSE = False

    def __init__(self, air):
        DistributedNodeAI.__init__(self, air)

        self.uniqueId = ''

    def requestInteraction(self, doId, interactType, instant):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.notify.warning('Failed to request interact for non-existant avatar!')

            self.air.logPotentialHacker( 
                message='Received requestInteraction from non-existant avatar',
                targetAvId=avatar.doId, 
                doId=doId,
                interactType=interactType,
                instant=instant)            
            return

        handle = self.handleRequestInteraction(avatar, interactType, instant)

        if not handle:
            self.d_rejectInteraction(avatar.doId)
            return

        if not self.MULTIUSE:
            self.d_setUserId(avatar.doId)
        else:
            self.sendUpdateToAvatarId(avatar.doId, 'setUserId', [avatar.doId])

        self.sendUpdateToAvatarId(avatar.doId, 'acceptInteraction', [])

    def handleRequestInteraction(self, avatar, interactType, instant):
        self.notify.warning('handleRequestInteraction not overriden by %s; Defaulting to DENY' % self.__class__.__name__)
        return self.DENY

    def requestExit(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.notify.warning('Failed to request exit for non-existant avatar!')

            self.air.logPotentialHacker(
                message='Received requestExit from non-existant avatar',
                targetAvId=avatar.doId, 
                doId=doId,
                interactType=interactType,
                instant=instant)   
            return

        handle = self.handleRequestExit(avatar)

        if not handle:
            self.d_rejectExit(avatar.doId)
            return

        if not self.MULTIUSE:
            self.d_setUserId(0)
        else:
            self.sendUpdateToAvatarId(avatar.doId, 'setUserId', [0])

    def demandExit(self):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            self.notify.warning('Failed to demand exit for non-existant avatar!')
            return

        self.d_setUserId(0)

    def handleRequestExit(self, avatar):
        return self.DENY

    def d_rejectInteraction(self, doId):
        self.sendUpdateToAvatarId(doId, 'rejectInteraction', [])

    def d_rejectExit(self, doId):
        self.sendUpdateToAvatarId(doId, 'rejectExit', [])

    def d_offerOptions(self, doId, optionIds, statusCodes):
        self.sendUpdateToAvatarId(doId, 'offerOptions', [optionIds, statusCodes])

    def selectOption(self, optionId):
        pass

    def d_setUserId(self, userId):
        self.sendUpdate('setUserId', [userId])

    def setUniqueId(self, uniqueId):
        self.uniqueId = uniqueId

    def d_setUniqueId(self, uniqueId):
        self.sendUpdate('setUniqueId', [uniqueId])

    def b_setUniqueId(self, uniqueId):
        self.setUniqueId(uniqueId)
        self.d_setUniqueId(uniqueId)

    def getUniqueId(self):
        return self.uniqueId
