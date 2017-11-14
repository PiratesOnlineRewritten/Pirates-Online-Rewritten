import datetime
import time
import functools
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.directnotify.DirectNotifyGlobal import directNotify

class StatusDatabaseUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('StatusDatabaseUD')

    def __init__(self, air):
        DistributedObjectGlobalUD.__init__(self, air)
        
    def announceGenerate(self):
        self.notify.info('Starting Status Database!')
        DistributedObjectGlobalUD.announceGenerate(self)

    def requestOfflineAvatarStatus(self, avIds):
        sender = self.air.getAvatarIdFromSender()
        for i in avIds:
            self.air.dbInterface.queryObject(self.air.dbId, i, functools.partial(self.__handleToonInfo, avId=i, sender=sender))
            
    def __handleToonInfo(self, dclass, fields, avId, sender):
        if dclass != self.air.dclassesByName['DistributedPlayerPirateAI']:
            self.notify.warning('Avatar %d with non-Pirate dclass %d was detected!!' % (avId, dclass))
            return
        
        accountId = fields['setDISLid'][0]
        self.air.dbInterface.queryObject(self.air.dbId, accountId, functools.partial(self.__handleAccount, avId=avId, accountId=accountId, sender=sender))
        
    def __handleAccount(self, dclass, fields, avId, accountId, sender):
        if dclass != self.air.dclassesByName['AccountUD']:
            self.notify.warning('Account %d with non-Account dclass %d was detected!!' % (accountId, dclass))
            return    
        
        lastLogin = fields['LAST_LOGIN'][0]
        self.sendUpdateToAvatarId(sender, 'recvOfflineAvatarStatus', [avId, lastLogin])