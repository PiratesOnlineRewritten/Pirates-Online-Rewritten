from direct.showbase.PythonUtil import POD, makeTuple
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import ItemGlobals

class QuestPrereq(POD):

    def avIsReady(self, av):
        return True

    def avIsReadyAI(self, av):
        return self.avIsReady(av)

    def giverCanGive(self, giver):
        return True


class HpAtLeast(QuestPrereq):
    DataSet = {'minHp': None}

    def __init__(self, minHp):
        QuestPrereq.__init__(self, minHp=minHp)

    def avIsReady(self, av):
        return av.getMaxHp() >= self.minHp


class SwiftnessAtLeast(QuestPrereq):
    DataSet = {'minSwiftness': None}

    def __init__(self, minSwiftness):
        QuestPrereq.__init__(self, minSwiftness=minSwiftness)

    def avIsReady(self, av):
        return av.getMaxSwiftness() >= self.minSwiftness


class LuckAtLeast(QuestPrereq):
    DataSet = {'minLuck': None}

    def __init__(self, minLuck):
        QuestPrereq.__init__(self, minLuck=minLuck)

    def avIsReady(self, av):
        return av.getMaxLuck() >= self.minLuck


class MojoAtLeast(QuestPrereq):
    DataSet = {'minMojo': None}

    def __init__(self, minMojo):
        QuestPrereq.__init__(self, minMojo=minMojo)

    def avIsReady(self, av):
        return av.getMaxMojo() >= self.minMojo


class DidQuest(QuestPrereq):
    DataSet = {'questIds': None}

    def __init__(self, questIds):
        QuestPrereq.__init__(self, questIds=questIds)

    def setQuestIds(self, questIds):
        self.questIds = makeTuple(questIds)

    def avIsReady(self, av):
        from pirates.quest import QuestLadderDB
        questHistory = av.getQuestLadderHistory()
        for questId in self.questIds:
            container = QuestLadderDB.getContainer(questId)
            questInts = QuestLadderDB.getAllParentQuestInts(container)
            thisQuestInHistory = False
            for qInt in questInts:
                if qInt in questHistory:
                    thisQuestInHistory = True
                    break

            if not thisQuestInHistory:
                return False

        return True

    def giverCanGive(self, avId):
        return False


class GetFrom(QuestPrereq):
    DataSet = {'questGivers': None}

    def __init__(self, questGivers):
        QuestPrereq.__init__(self, questGivers=questGivers)

    def setQuestGivers(self, questGivers):
        self.questGivers = makeTuple(questGivers)

    def giverCanGive(self, giver):
        return giver in self.questGivers


class HasQuest(QuestPrereq):
    DataSet = {'questIds': None}

    def __init__(self, questIds):
        QuestPrereq.__init__(self, questIds=questIds)

    def setQuestIds(self, questIds):
        self.questIds = makeTuple(questIds)

    def avIsReady(self, av):
        quests = []
        for q in av.getQuests():
            quests.append(q.getQuestId())

        for questId in self.questIds:
            if questId not in quests:
                return False

        return True


class NotCompleted(QuestPrereq):
    DataSet = {'questIds': None}

    def __init__(self, questIds):
        QuestPrereq.__init__(self, questIds=questIds)

    def setQuestIds(self, questIds):
        self.questIds = makeTuple(questIds)

    def avIsReady(self, av):
        from pirates.quest import QuestLadderDB
        questHistory = av.getQuestLadderHistory()
        for questId in self.questIds:
            container = QuestLadderDB.getContainer(questId)
            questInts = QuestLadderDB.getAllParentQuestInts(container)
            thisQuestInHistory = False
            for qInt in questInts:
                if qInt in questHistory:
                    thisQuestInHistory = True
                    break

            if thisQuestInHistory:
                return False
            currentQuests = av.getQuests()
            for quest in currentQuests:
                if questId == quest.getQuestId() or container.hasQuest(quest.getQuestId()):
                    return False

        return True


class WithinTimeOfDay(QuestPrereq):
    DataSet = {'timeFrom': 0,'timeTo': 0}

    def __init__(self, timeFrom, timeTo):
        QuestPrereq.__init__(self, timeFrom=timeFrom, timeTo=timeTo)
        self.timeFrom2 = None
        self.timeTo2 = None
        return

    def avIsReady(self, av):
        currTime = base.cr.timeOfDayManager.getCurrentIngameTime()
        if self.timeFrom > self.timeTo:
            self.timeTo2 = 25
            self.timeFrom2 = 0
            return currTime >= self.timeFrom and currTime < self.timeTo2 or currTime >= self.timeFrom2 and currTime < self.timeTo
        else:
            return currTime >= self.timeFrom and currTime < self.timeTo

    def avIsReadyAI(self, av):
        currTime = simbase.air.timeOfDayManager.getCurrentIngameTime()
        if self.timeFrom > self.timeTo:
            self.timeTo2 = 25
            self.timeFrom2 = 0
            return currTime >= self.timeFrom and currTime < self.timeTo2 or currTime >= self.timeFrom2 and currTime < self.timeTo
        else:
            return currTime >= self.timeFrom and currTime < self.timeTo


class RequiresItemEquipped(QuestPrereq):
    DataSet = {'itemId': None}

    def __init__(self, itemId):
        QuestPrereq.__init__(self, itemId=itemId)

    def avIsReady(self, av):
        from pirates.inventory.InventoryGlobals import Locations
        inv = av.getInventory()
        if not inv:
            return False
        categoryId = ItemGlobals.getClass(self.itemId)
        if inv.getItemQuantity(categoryId, self.itemId) > 0:
            if categoryId == InventoryType.ItemTypeWeapon:
                if av.currentWeaponId == itemId:
                    return True
                else:
                    return False
            elif categoryId == InventoryType.ItemTypeCharm:
                if av.getCurrentCharm() == self.itemId:
                    return True
                else:
                    return False
            elif categoryId == InventoryType.ItemTypeClothing:
                locationRange = Locations.RANGE_EQUIP_CLOTHES
            elif categoryId == InventoryType.ItemTypeJewelry:
                locationRange = Locations.RANGE_EQUIP_JEWELRY
            elif categoryId == InventoryType.ItemTypeTattoo:
                locationRange = Locations.RANGE_EQUIP_TATTOO
            else:
                locationRange = (0, 0)
            for location in range(locationRange[0], locationRange[1] + 1):
                locatable = inv.getLocatables().get(location)
                if locatable and locatable[1] == self.itemId:
                    return True

        return False


class RequiresItemUnequipped(QuestPrereq):
    DataSet = {'itemId': None}

    def __init__(self, itemId):
        QuestPrereq.__init__(self, itemId=itemId)

    def avIsReady(self, av):
        from pirates.inventory.InventoryGlobals import Locations
        inv = av.getInventory()
        if not inv:
            return False
        categoryId = ItemGlobals.getClass(self.itemId)
        if inv.getItemQuantity(categoryId, self.itemId) > 0:
            if categoryId == InventoryType.ItemTypeWeapon:
                if av.currentWeaponId == self.itemId:
                    return False
                else:
                    return True
            else:
                if categoryId == InventoryType.ItemTypeCharm:
                    if av.getCurrentCharm() == self.itemId:
                        return False
                    else:
                        return True
                else:
                    if categoryId == InventoryType.ItemTypeClothing:
                        locationRange = Locations.RANGE_EQUIP_CLOTHES
                    elif categoryId == InventoryType.ItemTypeJewelry:
                        locationRange = Locations.RANGE_EQUIP_JEWELRY
                    elif categoryId == InventoryType.ItemTypeTattoo:
                        locationRange = Locations.RANGE_EQUIP_TATTOO
                    else:
                        locationRange = (0, 0)
                    equippedItem = False
                    for location in range(locationRange[0], locationRange[1] + 1):
                        locatable = inv.getLocatables().get(location)
                        if locatable and locatable[1] == self.itemId:
                            equippedItem = True

                if not equippedItem:
                    return True
            return False
        return True


class RequiresItem(QuestPrereq):
    DataSet = {'itemId': None}

    def __init__(self, itemId):
        QuestPrereq.__init__(self, itemId=itemId)

    def avIsReady(self, av):
        inv = av.getInventory()
        if not inv:
            return False
        categoryId = ItemGlobals.getClass(self.itemId)
        if inv.getItemQuantity(categoryId, self.itemId) > 0:
            return True
        else:
            return False


class IsGender(QuestPrereq):
    DataSet = {'gender': 'm'}

    def __init__(self, gender):
        QuestPrereq.__init__(self, gender=gender)

    def avIsReady(self, av):
        return av.style.getGender() == self.gender

    def avIsReadyAI(self, av):
        return av.dna.getGender() == self.gender


class IsHoliday(QuestPrereq):
    DataSet = {'holidayId': None}

    def __init__(self, holidayId):
        QuestPrereq.__init__(self, holidayId=holidayId)

    def avIsReady(self, av):
        return base.cr.newsManager and self.holidayId in base.cr.newsManager.getHolidayIdList()

    def avIsReadyAI(self, av):
        return simbase.air.holidayMgr.isHolidayActive(self.holidayId)