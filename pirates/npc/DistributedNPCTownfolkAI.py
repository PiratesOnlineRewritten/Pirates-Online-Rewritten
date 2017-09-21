from direct.directnotify import DirectNotifyGlobal
from pirates.battle.DistributedBattleNPCAI import DistributedBattleNPCAI
from pirates.economy.DistributedShopKeeperAI import DistributedShopKeeperAI
from pirates.piratesbase import PiratesGlobals
class DistributedNPCTownfolkAI(DistributedBattleNPCAI, DistributedShopKeeperAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedNPCTownfolkAI')

    def __init__(self, air):
        DistributedBattleNPCAI.__init__(self, air)
        DistributedShopKeeperAI.__init__(self, air)
        self.dnaId = ''
        self.shopId = 0
        self.helpId = 0

    def handleRequestInteraction(self, avatar, interactType, instant):
        if interactType == PiratesGlobals.INTERACT_TYPE_FRIENDLY:
            self.sendUpdateToAvatarId(avatar.doId, 'triggerInteractShow', [self.doId])

        return self.DENY

    def setDNAId(self, dnaId):
        self.dnaId = dnaId

    def d_setDNAId(self, dnaId):
        self.sendUpdate('setDNAId', [dnaId])

    def b_setDNAId(self, dnaId):
        self.setDNAId(dnaId)
        self.d_setDNAId(dnaId)

    def getDNAId(self):
        return self.dnaId

    def d_offerOptions(self, dialogFlag):
        self.sendUpdate('offerOptions', [dialogFlag])

    def d_startTutorial(self, todo):
        self.sendUpdate('startTutorial', [todo])

    def d_swordTutorialPt1(self, todo):
        self.sendUpdate('swordTutorialPt1', [todo])

    def pistolTutorialPt1(self, todo):
        self.sendUpdate('pistolTutorialPt1', [todo])
    
    def shipTutorialPt1(self, todo):
        self.sendUpdate('shipTutorialPt1', [todo])

    def setShopId(self, shopId):
        self.shopId = shopId

    def d_setShopId(self, shopId):
        self.sendUpdate('setShopId', [shopId])

    def b_setShopId(self, shopId):
        self.setShopId(shopId)
        self.d_setShopId(shopId)

    def getShopId(self):
        return self.shopId

    def setHelpId(self, helpId):
        self.helpId = helpId

    def d_setHelpId(self, helpId):
        self.sendUpdate('setHelpId', [helpId])

    def b_setHelpId(self, helpId):
        self.setHelpId(helpId)
        self.d_setHelpId(helpId)

    def getHelpId(self):
        return self.helpId

    def requestMusic(self, songId):
        pass

    def d_playMusic(self, songId):
        self.sendUpdate('playMusic', [songId])

    def levelUpCutlass(self, avId):
        pass

    def d_setQuestRewardsEarned(self, gold, reputation, items):
        self.sendUpdate('setQuestRewardsEarned', [gold, reputation, items])

    def setViewedPotionInstructions(self):
        pass

    def setZombie(self, zombie):
        self.zombie = zombie

    def d_setZombie(self, zombie):
        self.sendUpdate('setZombie', [zombie])
    
    def b_setZombie(self, zombie):
        self.setZombie(zombie)
        self.d_setZombie(zombie)