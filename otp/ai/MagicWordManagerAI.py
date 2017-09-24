from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.directnotify import DirectNotifyGlobal

class MagicWordManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('MagicWordManagerAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        
    def setMagicWord(self, magicWord, avId, zoneId, userSignature): 
        if avId in simbase.air.doId2do:
            self.sendUpdateToAvatarId(avId, 'setMagicWordResponse', ["Default response message!"])