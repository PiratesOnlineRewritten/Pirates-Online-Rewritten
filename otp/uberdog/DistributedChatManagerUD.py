from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify import DirectNotifyGlobal

class DistributedChatManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedChatManagerUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)

    def chatMessage(self, message, flags):
        avatarId = self.air.getAvatarIdFromSender()

        if not avatarId:
            return

        def queryAvatar(dclass, fields):
            if not dclass or not fields:
                self.notify.warning('Failed to query avatar %d!' % avatarId)
                return

            dg = dclass.aiFormatUpdate('setTalk', avatarId, avatarId, self.air.ourChannel, [avatarId, fields.get('setDISLid', (0,))[0],
                fields.get('setName', ('',))[0], message, [], flags])

            self.air.send(dg)

        self.air.dbInterface.queryObject(self.air.dbId, avatarId, queryAvatar, dclass=self.air.dclassesByName[
            'DistributedAvatarUD'])
