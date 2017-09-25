from pirates.distributed.DistributedInteractiveAI import DistributedInteractiveAI
from pirates.inventory.LootableAI import LootableAI
from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryType
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
        avatarId = self.air.getAvatarIdFromSender()
        self.d_spotFilledByAvId(avatarId)

        inventory = self.air.inventoryManager.getInventory(avatar.doId)

        if not inventory:
            self.notify.warning('Failed to get inventory for avatar %d!' % avatar.doId)
            return

        if not inventory.getStack(InventoryType.FishingTutorial):
            self.sendUpdateToAvatarId(avatarId, 'firstTimeFisher', [])

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

        fishData = FishingGlobals.getFishData(fishId)
        if not fishData:
            self.air.logPotentialHacker(
                message='Received caughtFish update for an invalid fish!',
                accountId=self.air.getAccountIdFromSender(),
                fishId=fishId,
                weight=weight)
            return

        minWeight, maxWeight = fishData['weightRange']
        
        if weight < minWeight or weight > maxWeight:
            self.air.logPotentialHacker(
                message='Received caughtFish update for invalid weight.',
                accountId=self.air.getAccountIdFromSender(),
                fishId=fishId,
                weight=weight)
            return

        reward = fishData['gold'] * weight
        bonusReward = 0
        if self.air.holidayMgr.isHolidayActive(HolidayGlobals.DOUBLEGOLDHOLIDAY) or self.air.holidayMgr.isHolidayActive(HolidayGlobals.DOUBLEGOLDHOLIDAYPAID):
            bonusReward = reward * 2

        if bonusReward:
            reward += bonusReward
            self.sendUpdateToAvatarId(avatar.doId, 'setGoldBonus', [bonusReward])

        experience = fishData['experience']
        bonusExperience = 0
        if self.air.holidayMgr.isHolidayActive(HolidayGlobals.DOUBLEXPHOLIDAY):
            bonusExperience = experience * 2

        if bonusExperience:
            experience += bonusExperience
            self.sendUpdateToAvatarId(avatar.doId, 'setXpBonus', [bonusExperience])

        inventory = self.air.inventoryManager.getInventory(avatar.doId)

        if not inventory:
            self.notify.warning('Failed to get inventory for avatar %d!' % avatar.doId)
            return

        inventory.setGoldInPocket(inventory.getGoldInPocket() + reward)
        inventory.setFishingRep(inventory.getFishingRep() + experience)

        # Clear Tutorial flags
        if not inventory.getStack(InventoryType.FishingTutorial):
            inventory.b_setStack(InventoryType.FishingTutorial, 1)

    def lostLure(self, lureId):
        avatar = self.air.doId2do.get(self.air.getAvatarIdFromSender())

        if not avatar:
            return

        if lureId not in [InventoryType.RegularLure, InventoryType.LegendaryLure]:
            self.air.logPotentialHacker(
                message='Received lostLure with an invalid lure Id!',
                accountId=self.aior.getAccountIdFromSender(),
                lureId=lureId)
            return

        inventory = self.air.inventoryManager.getInventory(avatar.doId)

        if not inventory:
            self.notify.warning('Failed to get inventory for avatar %d!' % avatar.doId)
            return

        lureCount = inventory.getStack(lureId)[1] if inventory.getStack(lureId) else 0
        lureCount = max(lureCount - 1, 0)
        inventory.b_setStack(lureId, lureCount)

    def d_spotFilledByAvId(self, avId):
        self.sendUpdate('spotFilledByAvId', [avId])
