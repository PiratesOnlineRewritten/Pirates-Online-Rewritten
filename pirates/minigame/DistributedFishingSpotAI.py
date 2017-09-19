from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.inventory.LootableAI import LootableAI
from direct.directnotify import DirectNotifyGlobal
from pirates.ai import HolidayGlobals
import FishingGlobals

class DistributedFishingSpotAI(DistributedInteractiveAI, LootableAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedFishingSpotAI')

    def __init__(self, air):
        DistributedInteractiveAI.__init__(self, air)
        LootableAI.__init__(self, air)
        self.index = 0
        self.oceanOffset = 0
        self.onBoat = False

    def handleRequestInteraction(self, avatar, interactType, instant):

        self.d_spotFilledByAvId(self.air.getAvatarIdFromSender())

        return self.ACCEPT

    def setIndex(self, index):
        self.index = index

    def d_setIndex(self, index):
        self.sendUpdate('setIndex', [index])

    def b_setIndex(self, index):
        self.setIndex(index)
        self.d_setIndex(index)

    def getIndex(self):
        return self.index

    def setOceanOffset(self, offset):
        self.oceanOffset = offset

    def d_setOceanOffset(self, offset):
        self.sendUpdate('setOceanOffset', [offset])

    def b_setOceanOffset(self, offset):
        self.setOceanOffset(offset)
        self.d_setOceanOffset(offset)

    def getOceanOffset(self):
        return self.oceanOffset

    def setOnABoat(self, onBoat):
        self.onBoat = onBoat

    def d_setOnABoat(self, onBoat):
        self.sendUpdate('setOnABoat', [onBoat])

    def b_setOnABoat(self, onBoat):
        self.setOnABoat(onBoat)
        self.d_setOnABoat(onBoat)

    def getOnABoat(self):
        return self.onBoat

    def caughtFish(self, fishId, weight):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        fish = FishingGlobals.allFishData[fishId]
        minWeight, maxWeight = fish['weightRange']

        if not minWeight <= weight <= maxWeight:
            self.air.writeServerEvent('suspicious-event', 
                message='Received caughtFish update for invalid weight.',
                targetAvId=avatar.doId, 
                fishId=fishId,
                weight=weight)
            return

        reward = fish['gold']
        if self.air.holidayMgr.isHolidayActive(HolidayGlobals.DOUBLEGOLDHOLIDAY) or self.air.holidayMgr.isHolidayActive(HolidayGlobals.DOUBLEGOLDHOLIDAYPAID):
            reward = reward * 2

        experience = fish['experience']
        if self.air.holidayMgr.isHolidayActive(HolidayGlobals.DOUBLEXPHOLIDAY):        
            experience = experience * 2

        #TODO issue gold and experience

    def lostLure(self, lureId):
        pass

    def d_firstTimeFisher(self, avatarId):
        self.sendUpdateToAvaarId(avatarId, 'firstTimeFisher', [])

    def d_spotFilledByAvId(self, avId):
        self.sendUpdate('spotFilledByAvId', [avId])

    def d_setXpBonus(self, xpBonusAmount):
        self.sendUpdate('setXpBonus', [xpBonusAmount])

    def d_setGoldBonus(self, goldBonusAmount):
        self.sendUpdate('setGoldBonus', [goldBonusAmount])