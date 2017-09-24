from pirates.ai.PiratesAsyncRequest import PiratesAsyncRequest as AsyncRequest
from pirates.uberdog.UberDogGlobals import InventoryId, InventoryType, isLocatable, GiftOrigin
from pirates.uberdog.TradableInventoryBase import InvItem
import types
from direct.directnotify.DirectNotifyGlobal import directNotify
from pirates.inventory.InventoryGlobals import isStackableType

class AITradeException(Exception):
    pass


class AITradeBase(AsyncRequest):
    notify = directNotify.newCategory('AITradeBase')

    def __init__(self, distObj, avatarId=None, inventoryId=None, timeout=4.0):
        self.responseKey = 'tradeResponse'
        AsyncRequest.__init__(self, distObj.air, distObj.getDoId(), timeout)
        self.distObj = distObj
        self.avatarId = avatarId
        self.inventoryId = inventoryId
        self.failureCallback = []
        self.successCallback = []
        self.timeoutCallback = []
        self.nextNewDoIdKey = 0
        self.newDoId = {}
        self.readyToSend = False
        self.giving = []
        self.taking = []
        self.unequippables = []

    def setFailureCallback(self, function, extraArgs=[]):
        self.failureCallback.append((function, extraArgs))

    def setSuccessCallback(self, function, extraArgs=[]):
        self.successCallback.append((function, extraArgs))

    def setTimeoutCallback(self, function, extraArgs=[]):
        self.timeoutCallback.append((function, extraArgs))

    def giveCategoryLimit(self, category, addToLimit):
        limitChange = InventoryId.getLimitChange(category)
        self.giving.append([limitChange, addToLimit])

    def giveNewDistObj(self, category, dClassName, values=None):
        key = self.nextNewDoIdKey
        self.nextNewDoIdKey += 1
        self.newDoId[key] = category
        self.createObjectId('newDoId_%s' % (key,), dClassName, values=values)

    def _doCreateObject(self, *args, **kArgs):
        self.notify.warning('creating temporary copy of inventory object, second generate msg is on the way')
        AsyncRequest._doCreateObject(self, *args, **kArgs)

    def giveDoId(self, category, doId):
        self.giving.append([category, doId])

    def takeDoId(self, category, doId):
        self.taking.append([category, doId])

    def giveStackableTypeLimit(self, stackType, addToLimit):
        limitChange = InventoryId.getLimitChange(stackType)
        self.giving.append([limitChange, addToLimit])

    def giveStackableMinLimit(self, stackType, minLimit):
        limitMinimum = InventoryId.getLimitMinChange(stackType)
        self.giving.append([limitMinimum, minLimit])

    def giveStack(self, stackType, quantity):
        self.giving.append([stackType, quantity])

    def giveWeapon(self, weaponId, upgrades=[], location=0):
        self.giving.append([InventoryType.ItemTypeWeapon, weaponId, location, upgrades])

    def takeWeapon(self, weaponId, upgrades=[], location=0):
        self.taking.append([InventoryType.ItemTypeWeapon, weaponId, location, upgrades])

    def giveCharm(self, charmId, location=0):
        self.giving.append([InventoryType.ItemTypeCharm, charmId, location])

    def takeCharm(self, charmId, location=0):
        self.taking.append([InventoryType.ItemTypeCharm, charmId, location])

    def giveClothing(self, clothingId, colorId, location=0):
        self.giving.append([InventoryType.ItemTypeClothing, clothingId, location, colorId])

    def takeClothing(self, clothingId, colorId, location=0):
        self.taking.append([InventoryType.ItemTypeClothing, clothingId, location, colorId])

    def giveAccessory(self, accessoryType, accessoryId, location=0):
        self.giving.append([accessoryType, accessoryId, location])

    def takeAccessory(self, accessoryType, accessoryId, location=0):
        self.taking.append([accessoryType, accessoryId, location])

    def giveConsumable(self, consumableId, location=0, count=1):
        self.giving.append([InventoryType.ItemTypeConsumable, consumableId, location, count])

    def takeConsumable(self, consumableId, location=0, count=1):
        self.taking.append([InventoryType.ItemTypeConsumable, consumableId, location, count])

    def giveGoldInPocket(self, amount):
        self.giveBundle(InventoryType.ItemTypeMoney, amount)

    def takeGoldInPocket(self, amount):
        self.takeBundle(InventoryType.ItemTypeMoney, amount)

    def giveGoldWagered(self, amount):
        self.giveBundle(InventoryType.ItemTypeMoneyWagered, amount)

    def takeGoldWagered(self, amount):
        self.takeBundle(InventoryType.ItemTypeMoneyWagered, amount)

    def giveBundle(self, bundleId, count):
        self.giving.append([bundleId, count])

    def takeBundle(self, bundleId, count):
        self.taking.append([bundleId, count])

    def giveItem(self, item):
        self.giving.append(item)

    def takeItem(self, item):
        self.taking.append(item)

    def takeLocatable(self, item):
        if item[0] == InventoryType.ItemTypeClothing:
            self.notify.debug('takeLocatable: %s taking clothing %s' % (self.inventoryId, str(item)))
            self.takeClothing(item[1], item[3], item[2])
        elif item[0] == InventoryType.ItemTypeWeapon:
            self.notify.debug('takeLocatable: %s taking weapon %s' % (self.inventoryId, str(item)))
            self.takeWeapon(item[1], [], item[2])
        elif item[0] == InventoryType.ItemTypeConsumable:
            self.notify.debug('takeLocatable: %s taking tonic %s' % (self.inventoryId, str(item)))
            self.takeConsumable(item[1], item[2], item[3])
        elif item[0] == InventoryType.ItemTypeJewelry or item[0] == InventoryType.ItemTypeTattoo or item[0] == InventoryType.ItemTypeCharm:
            self.notify.debug('takeLocatable: %s taking accessory %s' % (self.inventoryId, str(item)))
            self.takeAccessory(item[0], item[1], item[2])
        elif item[0] == InventoryType.ItemTypeMoney:
            self.notify.debug('takeLocatable: %s taking gold %s' % (self.inventoryId, str(item)))
            self.takeGoldInPocket(item[1])

    def giveStackMax(self, stackType):
        percentChange = InventoryId.getStackPercentChange(stackType)
        self.giving.append([percentChange, 100])

    def takeStack(self, stackType, quantity):
        self.taking.append([stackType, quantity])

    def takeStackMax(self, stackType):
        percentChange = InventoryId.getStackPercentChange(stackType)
        self.taking.append([percentChange, 100])

    def giveAccumulatorAddition(self, accumulatorType, quantity):
        self.giving.append([accumulatorType, quantity])

    def finish(self):
        if self.inventoryId is None:
            inventoryId = self.neededObjects.get('setInventoryId')
            if inventoryId is not None:
                self.inventoryId = inventoryId[0]
            else:
                if not self.neededObjects.has_key('setInventoryId'):
                    self.askForObjectField('DistributedPlayerPirateAI', 'setInventoryId', self.avatarId)
                return
        for key, category in self.newDoId.items():
            doId = self.neededObjects.get('newDoId_%s' % (key,))
            if doId is not None:
                self.giveDoId(category, doId)
                del self.newDoId[key]

        if len(self.newDoId) or not self.readyToSend:
            return
        if not self.isTradeSent():
            self._sendTrade()
            return
        AsyncRequest.finish(self)

    def isTradeSent(self):
        return self.neededObjects.has_key(self.responseKey)

    def sendTrade(self):
        if not self.readyToSend:
            self.readyToSend = True
            self.finish()

    def rejectApprovedTrade(self, context, reasonId):
        if context != None:
            self.ignore(self.approvedTradeMsg(context))
        for failureInfo in self.failureCallback:
            apply(failureInfo[0], failureInfo[1] + [self] + [reasonId])

        AsyncRequest.finish(self)

    def approvedTradeResponse(self, context):
        self.ignore(self.rejectTradeMsg(context))
        for successInfo in self.successCallback:
            apply(successInfo[0], successInfo[1] + [self])

        self._checkCompletion(self.responseKey, None, True)
        return

    def timeout(self, task):
        for timeoutInfo in self.timeoutCallback:
            apply(timeoutInfo[0], timeoutInfo[1] + [self])

        AsyncRequest.timeout(self, task)

    def _normalizeTrade(self):
        TypeIndex = 0
        QuantityIndex = 1
        givingLimitChanges = {}
        takingLimitChanges = {}
        givingStacks = {}
        takingStacks = {}
        givingLocatable = []
        takingLocatable = []
        givingAccumulators = {}
        takingAccumulators = {}
        CategoryIndex = 0
        DoIdIndex = 1
        givingDoIds = {}
        takingDoIds = {}

        def check1(tradeItems, limitChanges, stacks, locatable, accumulators, doIds, giving):
            listType = type([])
            possibleTypes = (type(1), type(1L), listType)
            for i in tradeItems:
                for v in i:
                    itemType = type(v)
                    if itemType not in possibleTypes:
                        raise AITradeException, 'element is the wrong type'
                    if v > 4294967295L and itemType != listType:
                        raise AITradeException, 'element is larger than unsigned long'
                else:
                    t = i[TypeIndex]
                    if InventoryId.isLimitChange(t):
                        a = limitChanges.setdefault(t, [t, 0])
                        a[1] += i[QuantityIndex]
                        if a[1] > 65535L:
                            raise AITradeException, 'element is larger than unsigned short'
                    elif InventoryId.isStackable(t):
                        a = stacks.setdefault(t, [t, 0])
                        a[1] += i[QuantityIndex]
                        if a[1] > 65535L:
                            raise AITradeException, 'element is larger than unsigned short'
                    elif isLocatable(t):
                        inv = simbase.air.doId2do.get(self.inventoryId)
                        if inv:
                            theInvItem = InvItem(i)
                            theInvItemType = theInvItem.getType()
                            if giving:
                                equippableInfo = inv.getItemRequirements(theInvItemType, self.giving)
                                if (equippableInfo == None or filter(lambda x: equippableInfo[x][1] == False, equippableInfo)) and theInvItemType and theInvItemType not in self.unequippables:
                                    self.unequippables.append(theInvItemType)
                            if isStackableType(theInvItem.getCat()):
                                for currLocatable in locatable:
                                    prevInvItem = InvItem(currLocatable)
                                    if prevInvItem.compare(theInvItem, excludeLoc=True):
                                        adjustedInvItem = prevInvItem.adjustCount(theInvItem.getCount())
                                        locatable.remove(currLocatable)
                                        i = list(adjustedInvItem)
                                        break

                        else:
                            raise AITradeException, 'inventory not present'
                        locatable.append(i)
                    elif InventoryId.isAccumulator(t):
                        a = accumulators.setdefault(t, [t, 0])
                        a[1] += i[QuantityIndex]
                        if a[1] > 4294967295L:
                            raise AITradeException, 'element is larger than unsigned long'
                    elif InventoryId.isDoId(t):
                        doIds[i[DoIdIndex]] = i

            return

        check1(self.giving, givingLimitChanges, givingStacks, givingLocatable, givingAccumulators, givingDoIds, giving=True)
        check1(self.taking, takingLimitChanges, takingStacks, takingLocatable, takingAccumulators, takingDoIds, giving=False)

        def check2(s1, s2):
            for i in s1.keys():
                if s2.has_key(i):
                    q1 = s1[i][QuantityIndex]
                    q2 = s2[i][QuantityIndex]
                    if q1 == q2:
                        del s1[i]
                        del s2[i]
                    elif q1 > q2:
                        s1[i][QuantityIndex] -= q2
                        del s2[i]
                    else:
                        s2[i][QuantityIndex] -= q1
                        del s1[i]

        if givingLimitChanges or takingLimitChanges:
            check2(givingLimitChanges, takingLimitChanges)
            check2(takingLimitChanges, givingLimitChanges)
        if givingStacks or takingStacks:
            check2(givingStacks, takingStacks)
            check2(takingStacks, givingStacks)

        def check3(s1, s2):
            for i in s1.keys():
                if s2.has_key(i):
                    del s1[i]
                    del s2[i]

        if givingDoIds or takingDoIds:
            check3(givingDoIds, takingDoIds)
            check3(takingDoIds, givingDoIds)
        self._checkRules(givingLimitChanges, givingStacks, givingAccumulators, givingDoIds, givingLocatable, takingLimitChanges, takingStacks, takingAccumulators, takingDoIds, takingLocatable)
        self.giving = givingLimitChanges.values() + givingStacks.values() + givingLocatable + givingAccumulators.values() + givingDoIds.values()
        self.taking = takingLimitChanges.values() + takingStacks.values() + takingLocatable + takingAccumulators.values() + takingDoIds.values()
        self._sortOffer(self.giving)
        self._sortOffer(self.taking)

    def _checkRules(self, givingLimitChanges, givingStacks, givingAccumulators, givingDoIds, givingLocatable, takingLimitChanges, takingStacks, takingAccumulators, takingDoIds, takingLocatable):

        def isNotFreelyRemovable(stacks):
            for stackType, quantity in stacks.items():
                if not InventoryId.isFreeTakeStackType(stackType):
                    return True

            return False

        def isNotFreelyGivable(stacks):
            for stackType, quantity in stacks.items():
                if not InventoryId.isFreeGiveStackType(stackType):
                    return True

            return False

        if takingAccumulators:
            raise AITradeException, 'error: cannot take accumulators'
        elif not (givingStacks or givingDoIds or givingLimitChanges or givingLocatable):
            if not (takingStacks or takingDoIds or takingLocatable):
                raise AITradeException, 'error: nothing for nothing trade'
            elif takingDoIds or isNotFreelyRemovable(takingStacks):
                raise AITradeException, 'error: nothing for something trade'
        elif not (takingStacks or takingDoIds or givingLimitChanges or takingLocatable):
            if givingDoIds or isNotFreelyGivable(takingStacks):
                raise AITradeException, 'error: something for nothing trade'

    def _sortOffer(self, offer):
        categoryLimitChanges = []
        stackLimitChanges = []
        setAccumulators = []
        stackables = []
        locatable = []
        accumulators = []
        doIds = []
        for i in offer:
            a = i[0]
            if InventoryId.isLimitChange(a):
                changing = InventoryId.getChangeCategoryOrType(a)
                if InventoryId.isCategory(changing):
                    categoryLimitChanges.append(i)
                elif InventoryId.isStackable(changing):
                    stackLimitChanges.append(i)
                elif InventoryId.isAccumulator(changing):
                    setAccumulators.append(i)
                else:
                    print '=============EXCEPTION1 RAISED: %s' % a
                    raise Exception, 'undefined trade category'
            elif InventoryId.isStackable(a):
                stackables.append(i)
            elif isLocatable(a):
                locatable.append(i)
            elif InventoryId.isAccumulator(a):
                accumulators.append(i)
            elif InventoryId.isCategory(a):
                doIds.append(i)
            else:
                print '=============EXCEPTION2 RAISED: %s' % a
                raise Exception, 'undefined trade type'

        offer = categoryLimitChanges + stackLimitChanges + setAccumulators + stackables + locatable + accumulators + doIds

    def _sendTrade(self):
        context = self.air.allocateContext()
        try:
            self._normalizeTrade()
        except AITradeException, e:
            self.notify.warning('trade rejected by _normalizeTrade or _checkRules %s' % (e,))
            self.air.writeServerEvent('failedNormalizeTrade', self.inventoryId, '%s|%s|%s|%s' % (self.giving, self.taking, e, context))
            self.rejectApprovedTrade(None, 1)
            return

        if len(self.giving) or len(self.taking):
            self.neededObjects[self.responseKey] = None
            self.acceptOnce(self.rejectTradeMsg(context), Functor(self.rejectApprovedTrade, context), [])
            self.acceptOnce(self.approvedTradeMsg(context), Functor(self.approvedTradeResponse, context), [])
            origin = self.getOrigin()
            self.air.getInventoryMgr(self.avatarId).sendApprovedTrade(0, self.inventoryId, self.giving, self.taking, context, origin, self.unequippables)
        else:
            AsyncRequest.finish(self)

    def rejectTradeMsg(self, context):
        return 'rejectApprovedTrade-%s' % (context,)

    def approvedTradeMsg(self, context):
        return 'approvedTradeResponse-%s' % (context,)

    def isGift(self, inventoryType):
        for gift in self.giving:
            if gift[0] == inventoryType:
                return 1

        return 0

    def __repr__(self):
        return '%s: %s giving %s, taking %s' % (self.__class__.__name__, self.avatarId, self.giving, self.taking)

    def getOrigin(self):
        return 0