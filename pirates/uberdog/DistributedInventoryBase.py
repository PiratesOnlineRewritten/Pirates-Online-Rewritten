from direct.directnotify import DirectNotifyGlobal
from pirates.uberdog.UberDogGlobals import InventoryCategory, InventoryType, InventoryId, getSkillCategory, isLocatable, getWeaponCategory
from pirates.uberdog.InventoryInit import AccumulatorLimits
from pirates.battle import WeaponGlobals
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.inventory import InventoryGlobals

class DistributedInventoryBase():
    GetInvRequests = {}
    GetInvRequestId2InvId = {}
    InvRequestSerialGen = SerialNumGen()
    LastInventoryRequestId = None
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedInventoryBase')

    def __init__(self, distributedObjectCollectionManager):
        self.dcm = distributedObjectCollectionManager
        self.version = None
        self.ownerId = None
        self.categoryLimits = {}
        self.categoryCounts = {}
        self.stackLimits = {}
        self.stacks = {}
        self.stacksInCategory = {}
        self.accumulators = {}
        self.doIds = {}
        self.doIdsInCategory = {}
        self.doIdsReady = False
        self.stacksReady = False
        self.sentReadyMessage = False
        self.useTemporaryInventory = False
        self.temporaryInventory = {}

    def __str__(self):
        out = [
         'Inventory(%d)[owner = %s]' % (self.doId, self.ownerId)]
        out += ['Categories:']
        for categoryId, limit in sorted(self.categoryLimits.iteritems()):
            doIdsInCategory = self.doIdsInCategory.get(categoryId)
            if doIdsInCategory:
                out += ['  %4d: %7d/%-7d | doIds:  %s' % (categoryId, len(doIdsInCategory), limit, doIdsInCategory)]
            else:
                out += ['  %4d: %7d/%-7d | stacks: %s' % (categoryId, self.categoryCounts.get(categoryId, 0), limit, self.stacksInCategory.get(categoryId, {}).keys())]

        out += ['\nStacks:']
        for stackId, limit in sorted(self.stackLimits.iteritems()):
            out += ['  %4d: %7d / %-7d' % (stackId, self.stacks.get(stackId, 0), limit)]

        out += ['\nAccumulators:']
        for accumulatorId, limit in sorted(self.accumulators.iteritems()):
            out += ['  %4d: %7d / %-7d' % (accumulatorId, self.accumulators.get(accumulatorId, 0), limit)]

        return '\n'.join(out)

    if __dev__:

        def queryField(self, fieldName, callback=None):

            def response(context, value):
                print '%s: %s' % (fieldName, value)

            dclassName = 'DistributedInventoryAI'
            self.air.contextToClassName[1] = dclassName
            self.acceptOnce(simbase.air.queryObjectField(dclassName, fieldName, self.doId, 1), callback or response)

        def queryFieldToXML(self, fieldName):

            def response(context, value):
                print self.valueToXML(fieldName, value)

            self.queryField(fieldName, response)

        @classmethod
        def valueToXML(cls, fieldName, value):
            dclassName = 'DistributedInventoryAI'
            dclass = simbase.air.dclassesByName[dclassName]
            field = dclass.getFieldByName(fieldName)
            hex = field.parseString(str(value))
            return hex.encode('hex').upper()

        @classmethod
        def XMLToValue(cls, fieldName, xml):
            dclassName = 'DistributedInventoryAI'
            dclass = simbase.air.dclassesByName[dclassName]
            field = dclass.getFieldByName(fieldName)
            return field.formatData(xml.decode('hex'))

        def accumulatorSanityCheck(self, callback):

            def response(context, accumulators):
                accumulators = dict(accumulators[0])
                try:
                    overallRep = accumulators[InventoryType.OverallRep]
                    calculatedOverallRep = sum([ accumulators.get(category, 0) for category in xrange(InventoryType.GeneralRep, InventoryType.end_Accumulator) ])
                    if overallRep != calculatedOverallRep:
                        callback(False, 'OverallRep does not add up!')
                    if overallRep > AccumulatorLimits[InventoryType.OverallRep]:
                        callback(False, 'Overflow in overall rep category')
                    for category in xrange(InventoryType.GeneralRep, InventoryType.end_Accumulator):
                        if accumulators.get(category, 0) > AccumulatorLimits[category]:
                            callback(False, 'Overflow in rep category %s' % category)

                    callback(True)
                except Exception, e:
                    callback(False, 'Exception encountered: %s - %s' % (e.__class__.__name__, e))

            self.queryField('setAccumulators', response)

    def delete(self):
        self.ignoreAll()

    @classmethod
    def getInventoryOnlyStacks(cls, inventoryId):
        inv = getBase().getRepository().getDo(inventoryId)
        if inv is not None and inv.stacksReady:
            return inv
        else:
            return
        return

    @classmethod
    def getInventory(cls, inventoryId, callback, timeout=30):
        dcm = getBase().getRepository()
        if dcm is None:
            return
        inv = dcm.getDo(inventoryId)
        if inv is not None and inv.isReady():
            requestId = None
            cls.LastInventoryRequestId = requestId
            callback(inv)
        else:
            requestId = cls.InvRequestSerialGen.next()
            cls.GetInvRequests.setdefault(inventoryId, {})
            cls.GetInvRequests[inventoryId][requestId] = callback
            cls.GetInvRequestId2InvId[requestId] = inventoryId
            taskMgr.doMethodLater(timeout, cls.handleGetInventoryTimedOut, 'getInventoryTimedOut-' + str(requestId), extraArgs=[requestId, inventoryId, callback])
        return requestId

    @classmethod
    def getLastInventoryRequestId(cls):
        return cls.LastInventoryRequestId

    @classmethod
    def handleGetInventoryTimedOut(cls, requestId, inventoryId, callback):
        cls.notify.warning('inventory timed out.  requestId = %s, inventoryId = %s, callback = %s' % (requestId, inventoryId, callback))
        cls.cancelGetInventory(requestId)
        cls.LastInventoryRequestId = None
        callback(None)
        return

    @classmethod
    def cancelGetInventory(cls, requestId):
        if requestId in cls.GetInvRequestId2InvId:
            inventoryId = cls.GetInvRequestId2InvId.pop(requestId)
            cls.GetInvRequests[inventoryId].pop(requestId)
            if len(cls.GetInvRequests[inventoryId]) == 0:
                cls.GetInvRequests.pop(inventoryId)
            taskMgr.remove('getInventoryTimedOut-' + str(requestId))

    def getInventoryVersion(self):
        return self.version

    def setInventoryVersion(self, version):
        self.version = version

    def sendSetInventoryVersion(self, version):
        if self.version != version:
            self.version = version
            self.sendUpdate('setInventoryVersion', [version])

    def getOwnerId(self):
        return self.ownerId

    def setOwnerId(self, ownerId):
        self.ownerId = ownerId

    def sendSetOwnerId(self, ownerId):
        if self.ownerId != ownerId:
            self.ownerId = ownerId
            self.sendUpdate('setOwnerId', [ownerId])

    def setCategoryLimits(self, categoriesAndLimits):
        old = self.categoryLimits
        self.categoryLimits = dict(categoriesAndLimits)
        for category, limit in categoriesAndLimits:
            if old.get(category, 0) != limit:
                messenger.send('inventoryLimit-%s-%s' % (self.doId, category), [limit])

    def setStackLimits(self, stackTypesAndLimits):
        old = self.stackLimits
        self.stackLimits = dict(stackTypesAndLimits)
        for t, limit in stackTypesAndLimits:
            if old.get(t, 0) != limit:
                messenger.send('inventoryLimit-%s-%s' % (self.doId, t), [limit])

    def setStacks(self, stackTypesAndQuantities):
        old = self.stacks
        self.stacks = dict(stackTypesAndQuantities)
        stacksInCategory = {}
        for t, q in stackTypesAndQuantities:
            if old.get(t, 0) != q:
                messenger.send(InventoryGlobals.getCategoryQuantChangeMsg(self.doId, t), [q])
            categoryId = InventoryId.getCategory(t)
            categoryList = stacksInCategory.setdefault(categoryId, {})
            categoryList[t] = self.stacks[t]

        self.stacksInCategory = stacksInCategory

    def setDoIds(self, categoriesAndDoIds):
        old = self.doIds
        self.doIds = dict([ (doId, category) for category, doId in categoriesAndDoIds ])
        self.doIdsInCategory = {}
        for category, doId in categoriesAndDoIds:
            category = self.doIdsInCategory.setdefault(category, [])
            category.append(doId)

        for doId, category in old.items():
            if self.doIds.get(doId) is None:
                messenger.send('inventoryRemoveDoId-%s-%s' % (self.doId, category), [doId])
                if category == InventoryCategory.SHIPS:
                    self.removeShip(doId)
                    messenger.send('shipRemoved')

        mightBeComplete = True
        for doId, category in self.doIds.items():
            if category == InventoryCategory.WAGERS or category == InventoryCategory.SHIPS:
                continue
            if old.get(doId) is None:
                distObj = self.dcm.doId2do.get(doId)
                if distObj is not None:
                    messenger.send('inventoryAddDoId-%s-%s' % (self.doId, category), [
                     distObj])
                    if category == InventoryCategory.QUESTS:
                        messenger.send('QuestAddDoId-%s-%s' % (self.doId, InventoryCategory.QUESTS), [
                         distObj])
                else:
                    self.acceptOnce('generate-%s' % (doId,), self._objectGenerated, [category])
                    mightBeComplete = False

        self.sentReadyMessage = False
        if mightBeComplete:
            self._checkDoIdsCompletion()
        return

    def setAccumulators(self, accumulatorTypesAndQuantities):
        old = self.accumulators
        self.accumulators = dict(accumulatorTypesAndQuantities)
        for t, q in accumulatorTypesAndQuantities:
            if old.get(t, 0) != q:
                messenger.send('inventoryAccumulator-%s-%s' % (self.doId, t), [q])
                if t >= InventoryType.begin_Accumulator and t <= InventoryType.end_Accumulator:
                    messenger.send('repChange-%s' % self.doId)

    def isReady(self):
        return self.sentReadyMessage

    def getReadyMessage(self):
        return 'inventoryReady-%s' % self.doId

    def _checkDoIdsCompletion(self):
        for doId, category in self.doIds.items():
            if category == InventoryCategory.WAGERS or category == InventoryCategory.SHIPS:
                continue
            if self.dcm.doId2do.get(doId) is None:
                return

        self.doIdsReady = True
        self.checkIsReady()
        return

    def checkIsReady(self):
        if self.sentReadyMessage:
            return
        if self.doIdsReady and self.stacksReady:
            messenger.send(self.getReadyMessage(), [self])
            self.sentReadyMessage = True
            if self.doId in DistributedInventoryBase.GetInvRequests:
                reqId2callback = DistributedInventoryBase.GetInvRequests.pop(self.doId)
                for requestId in reqId2callback:
                    DistributedInventoryBase.GetInvRequestId2InvId.pop(requestId)

                reqIds = reqId2callback.keys()
                reqIds.sort()
                for reqId in reqIds:
                    callback = reqId2callback[reqId]
                    DistributedInventoryBase.LastInventoryRequestId = reqId
                    callback(self)
                    taskMgr.remove('getInventoryTimedOut-' + str(reqId))

    def _objectGenerated(self, category, distObj):
        messenger.send('inventoryAddDoId-%s-%s' % (self.doId, category), [
         distObj])
        self._checkDoIdsCompletion()

    def setTemporaryInventory(self, enabled):
        if enabled:
            self.addTemporaryInventory()
        else:
            self.removeTemporaryInventory()

    def setTemporaryStack(self, stackType, amount):
        self.temporaryInventory[stackType] = amount
        messenger.send('inventoryChanged-%s' % self.ownerId)

    def maxInventory(self, item, amount=None):
        if amount:
            self.temporaryInventory[item] = amount
        else:
            self.temporaryInventory[item] = self.getStackLimit(item)

    def addPVPInventory(self):
        self.maxInventory(InventoryType.AmmoLeadShot)
        self.maxInventory(InventoryType.AmmoBaneShot)
        self.maxInventory(InventoryType.AmmoVenomShot)
        self.maxInventory(InventoryType.AmmoHexEaterShot)
        self.maxInventory(InventoryType.AmmoSilverShot)
        self.maxInventory(InventoryType.AmmoSteelShot)
        self.maxInventory(InventoryType.AmmoGrenadeExplosion)
        self.maxInventory(InventoryType.AmmoGrenadeFlame)
        self.maxInventory(InventoryType.AmmoGrenadeShockBomb)
        self.maxInventory(InventoryType.AmmoGrenadeSmoke)
        self.maxInventory(InventoryType.AmmoGrenadeLandMine)
        self.maxInventory(InventoryType.AmmoGrenadeSiege)
        self.maxInventory(InventoryType.AmmoAsp)
        self.maxInventory(InventoryType.AmmoAdder)
        self.maxInventory(InventoryType.AmmoSidewinder)
        self.maxInventory(InventoryType.AmmoViperNest)
        self.maxInventory(InventoryType.AmmoRoundShot)
        self.maxInventory(InventoryType.AmmoChainShot)
        self.maxInventory(InventoryType.AmmoExplosive)
        self.maxInventory(InventoryType.AmmoBullet)
        self.maxInventory(InventoryType.AmmoGasCloud)
        self.maxInventory(InventoryType.AmmoGrapeShot)
        self.maxInventory(InventoryType.AmmoSkull)
        self.maxInventory(InventoryType.AmmoFirebrand)
        self.maxInventory(InventoryType.AmmoFlameCloud)
        self.maxInventory(InventoryType.AmmoFlamingSkull)
        self.maxInventory(InventoryType.AmmoBarShot)
        self.maxInventory(InventoryType.AmmoKnives)
        self.maxInventory(InventoryType.AmmoMine)
        self.maxInventory(InventoryType.AmmoBarnacles)
        self.maxInventory(InventoryType.AmmoThunderbolt)
        self.maxInventory(InventoryType.AmmoFury)
        self.maxInventory(InventoryType.AmmoComet)
        self.maxInventory(InventoryType.AmmoGrappleHook)
        self.temporaryInventory[InventoryType.Vitae_Level] = 0

    def addTemporaryInventory(self):
        self.addPVPInventory()
        self.useTemporaryInventory = True

    def removeTemporaryInventory(self):
        self.temporaryInventory.clear()
        self.useTemporaryInventory = False

    def computeCategoryCounts(self):
        counts = {}
        for category in self.doIds.values():
            counts[category] = counts.get(category, 0) + 1

        for stackType in self.stacks.keys():
            category = InventoryId.getCategory(stackType)
            if category:
                counts[category] = counts.get(category, 0) + 1

        self.categoryCounts = counts

    def getStacksInCategory(self, category):
        return self.stacksInCategory.get(category, {})

    def getDoList(self, category):
        dos = []
        for doId in self.doIdsInCategory.get(category, []):
            do = self.dcm.doId2do.get(doId)
            if do is not None:
                dos.append(do)

        return dos

    def getDoIdListCategory(self, category):
        return self.doIdsInCategory.get(category, [])

    def getCategoryLimit(self, category):
        return self.categoryLimits.get(category, 0)

    def getStackLimit(self, stackType):
        return self.stackLimits.get(stackType, 0)

    def getStackQuantity(self, stackType):
        if self.useTemporaryInventory:
            return self.temporaryInventory.get(stackType, self.stacks.get(stackType, 0))
        else:
            return self.stacks.get(stackType, 0)

    def useTemporaryStack(self, stackType, amount):
        current = self.temporaryInventory.get(stackType)
        if current:
            self.temporaryInventory[stackType] -= amount

    def getDoIdList(self):
        return self.doIds.keys()

    def getDoIdAndCategoryList(self):
        return self.doIds.items()

    def getAccumulator(self, accumulatorType):
        return self.accumulators.get(accumulatorType, 0)

    def getGoldInPocket(self):
        return self.getItemQuantity(InventoryType.ItemTypeMoney)

    def getGoldWagered(self):
        return self.getItemQuantity(InventoryType.ItemTypeMoneyWagered)

    def getMaterialInPocket(self, type):
        return self.getItemQuantity(type)

    def getNewPlayerToken(self):
        return self.getStackQuantity(InventoryType.NewPlayerToken)

    def getNewShipToken(self):
        return self.getStackQuantity(InventoryType.NewShipToken)

    def getNewWeaponToken(self):
        return self.getStackQuantity(InventoryType.NewWeaponToken)

    def getShipRepairToken(self):
        return self.getStackQuantity(InventoryType.ShipRepairToken)

    def getPlayerHealToken(self):
        return self.getStackQuantity(InventoryType.PlayerHealToken)

    def getPlayerMojoHealToken(self):
        return self.getStackQuantity(InventoryType.PlayerMojoHealToken)

    def getWeapons(self):
        return self.getItemsInCategory(getWeaponCategory())

    def getWeaponCounts(self, weaponIds=[]):
        if weaponIds:
            countsDict = {}
            for currWeapon in weaponIds:
                countsDict[currWeapon] = self.getItemQuantity(getWeaponCategory(), currWeapon)

            return countsDict
        else:
            return self.getItemQuantity(getWeaponCategory())

    def getConsumables(self):
        return self.getItemsInCategory(getConsumableCategory())

    def getSkills(self, weaponId):
        weaponSkillCategory = getSkillCategory(weaponId)
        return self.getStacksInCategory(weaponSkillCategory)

    def getCutlassWeapon(self):
        return self.getStackQuantity(InventoryType.CutlassWeaponL1)

    def getReputation(self, category):
        return self.accumulators.get(category, 0)

    def getDinghy(self):
        return self.getStackQuantity(InventoryType.Dinghy)

    def getTortugaTeleportToken(self):
        return self.getStackQuantity(InventoryType.TortugaTeleportToken)

    def getPortRoyalTeleportToken(self):
        return self.getStackQuantity(InventoryType.PortRoyalTeleportToken)

    def getKingsheadTeleportToken(self):
        return self.getStackQuantity(InventoryType.KingsheadTeleportToken)

    def getPadresDelFuegoTeleportToken(self):
        return self.getStackQuantity(InventoryType.PadresDelFuegoTeleportToken)

    def getCubaTeleportToken(self):
        return self.getStackQuantity(InventoryType.CubaTeleportToken)

    def getTonics(self):
        return dict(((tonicId, self.getStackQuantity(tonicId)) for tonicId in InventoryType.Potions))

    def getShipRepairKits(self):
        return self.getStackQuantity(InventoryType.ShipRepairKit)

    def getFriendsList(self):
        return self.getDoList(InventoryCategory.FRIENDS)

    def getPetsList(self):
        return self.getDoList(InventoryCategory.PETS)

    def getQuestList(self):
        return self.getDoList(InventoryCategory.QUESTS)

    def getShipList(self):
        return self.getDoList(InventoryCategory.SHIPS)

    def getShipDoIdList(self):
        shipIds = self.getDoIdListCategory(InventoryCategory.SHIPS)
        shipIds.sort(reverse=True)
        return shipIds

    def getShipMainpartsList(self):
        return self.getDoList(InventoryCategory.SHIP_MAINPARTS)

    def getShipMainpartsDoIdList(self):
        return self.getDoIdListCategory(InventoryCategory.SHIP_MAINPARTS)

    def getShipAccessoriesList(self):
        return self.getDoList(InventoryCategory.SHIP_ACCESSORIES)

    def getShipAccessoriesDoIdList(self):
        return self.getDoIdListCategory(InventoryCategory.SHIP_ACCESSORIES)

    def getTreasureMapsList(self):
        return self.getDoList(InventoryCategory.TREASURE_MAPS)

    def getWagerList(self):
        return self.getDoList(InventoryCategory.WAGERS)

    def getFlagList(self):
        return self.getDoList(InventoryCategory.FLAGS)

    def removeShip(self, shipId):
        pass
