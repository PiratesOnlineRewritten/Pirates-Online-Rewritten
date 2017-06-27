from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory import InventoryUIItem
from pirates.inventory import InventoryUINoTradeItem
from pirates.inventory import InventoryUIStackItem
from pirates.inventory import InventoryUICardItem
from pirates.inventory import InventoryUIWeaponItem
from pirates.inventory import InventoryUICharmItem
from pirates.inventory import InventoryUIConsumableItem
from pirates.inventory import InventoryUIAmmoItem
from pirates.inventory import InventoryUIMaterialItem
from pirates.inventory import InventoryUIFishingItem
from pirates.inventory import InventoryUIGoldItem
from pirates.inventory import InventoryUITreasureItem
from pirates.inventory import InventoryUIClothingItem
from pirates.inventory import InventoryUIJewelryItem
from pirates.inventory import InventoryUITattooItem
from pirates.inventory import InventoryUIPouchItem
from pirates.inventory import InventoryStackSplitter
from pirates.inventory import InventoryRemoveConfirm
from pirates.inventory import InventoryPlunderPanel
from pirates.inventory import ItemGlobals
from pirates.inventory import InventoryExchange
from pirates.inventory.InventoryUIGlobals import *
from pirates.inventory.InventoryGlobals import Locations
from pirates.uberdog.UberDogGlobals import InventoryType, InventoryCategory
from pirates.economy import EconomyGlobals
from pirates.battle import WeaponGlobals
from pirates.uberdog import UberDogGlobals
from pirates.piratesgui import HighSeasScoreboard
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx
from pirates.pirate import MasterHuman
from pirates.pirate import Human
from pirates.pirate import HumanDNA
from pirates.uberdog.TradableInventoryBase import InvItem
from pirates.inventory import ItemGlobals
from pirates.inventory import ItemConstants
from pirates.inventory import InventoryGlobals
from direct.distributed.ClockDelta import globalClockDelta
from pirates.piratesbase import Freebooter
import time

class InventoryUIManager(DirectFrame):
    testItemCount = 0
    clothingEquipDelay = 5.0
    notify = directNotify.newCategory('InventoryUIManager')

    def __init__(self):
        DirectFrame.__init__(self, parent=aspect2d)
        self.containerList = []
        self.HeldNode = DirectFrame(parent=self, sortOrder=1, relief=None, frameSize=(0.0,
                                                                                      0.0,
                                                                                      0.0,
                                                                                      0.0))
        self.HeldNode.setBin('gui-popup', 1)
        self.screenSizeMult = 0.5
        self.screenSizeX = (base.a2dRight - base.a2dLeft) * self.screenSizeMult
        self.screenSizeZ = (base.a2dTop - base.a2dBottom) * self.screenSizeMult
        self.heldItem = None
        self.heldFromCell = None
        self.withInCell = None
        self.withInBag = None
        self.itemPickup = PICKUP_EMPTY
        self.pickupTimedOut = 0
        self.start()
        self.stackSplitter = None
        self.removeConfirm = None
        self.removeContainer = None
        self.plunderPanel = None
        self.showingItem = None
        self.locked = 0
        self.localInventoryOpen = 0
        self.standardButtonSize = 0.14
        self.pickUpTime = 0.3
        self.localStoreContainers = []
        base.im = self
        self.scoreboard = None
        self.lootContainer = None
        self.containerIsGeneric = False
        self.tradeContainer = None
        self.discoveredInventory = 0
        self.trashItem = None
        self.reasonNoUse = None
        self.hasShownVelvet = 0
        if config.GetBool('trash-invalid-loot', 0):
            self.trashInvalidItems = 1
        else:
            self.trashInvalidItems = 0
        self.slotToCellMap = {}
        for index in xrange(Locations.TOTAL_NUM_LOCATIONS - 1):
            self.slotToCellMap[index] = None

        self.slotPendingActionList = []
        self.associatedSlotDict = {}
        self.takeAllSound = loadSfx(SoundGlobals.SFX_GUI_TAKE_ALL)
        self.takeGoldSound = loadSfx(SoundGlobals.SFX_GUI_TAKE_GOLD)
        self.takeNonGoldSound = loadSfx(SoundGlobals.SFX_GUI_TAKE_NONGOLD)
        self.trashSound = loadSfx(SoundGlobals.SFX_FX_CHEST_APPEAR_02)
        self.takeAllSound.setVolume(0.4)
        self.takeGoldSound.setVolume(0.4)
        self.takeNonGoldSound.setVolume(0.4)
        self.displayHuman = Human.Human()
        self.displayHuman.ignoreAll()
        self.displayHuman.mixingEnabled = False
        self.localDrinkingPotion = 0
        base.iEx = InventoryExchange

    def destroy(self):
        self.heldItem = None
        self.heldFromCell = None
        self.withInCell = None
        self.withInBag = None
        taskMgr.remove('stuckPendingTask')
        taskMgr.remove('InventoryUIManagerTrack')
        self.ignore('mouse1-up')
        for container in self.containerList:
            container.destroy()

        self.containerList = []
        if self.displayHuman:
            self.displayHuman.delete()
            self.displayHuman.remove()
            self.displayHuman.removeNode()
            self.displayHuman = None

        self.takeAllSound.stop()
        loader.unloadSfx(self.takeAllSound)
        self.takeGoldSound.stop()
        loader.unloadSfx(self.takeGoldSound)
        self.takeNonGoldSound.stop()
        loader.unloadSfx(self.takeNonGoldSound)
        self.trashSound.stop()
        loader.unloadSfx(self.trashSound)
        DirectFrame.destroy(self)

    def start(self):
        taskMgr.add(self.trackMouse, 'InventoryUIManagerTrack')
        self.accept('mouse1-up', self.checkForDrop)
        self.accept('drinkingStarted', self.lockDrinking)
        self.accept('drinkingFinished', self.unlockDrinking)

    def lockDrinking(self):
        self.localDrinkingPotion = 1

    def unlockDrinking(self):
        self.localDrinkingPotion = 0

    def setLocalInventoryOpen(self, open):
        self.localInventoryOpen = open

    def trackMouse(self, task):
        if base.mouseWatcherNode.hasMouse():
            self.screenSizeX = (base.a2dRight - base.a2dLeft) * self.screenSizeMult
            self.screenSizeZ = (base.a2dTop - base.a2dBottom) * self.screenSizeMult
            offX = 0.0
            offZ = 0.0
            if self.heldItem and self.heldItem.cell and self.heldItem.cell.container:
                offX = self.heldItem.cell.container.cellSizeX
                offZ = self.heldItem.cell.container.cellSizeZ
            mpos = base.mouseWatcherNode.getMouse()
            newX = mpos.getX() * self.screenSizeX + offX * 0.0
            newZ = mpos.getY() * self.screenSizeZ + offZ * 0.0
            self.HeldNode.setX(newX)
            self.HeldNode.setZ(newZ)
        return task.cont

    def setWithin(self, cell, shouldClear=0, task=None):
        if cell == self.withInCell and shouldClear:
            self.withInCell = None
        else:
            self.withInCell = cell
            if cell.container.containerType == CONTAINER_TRASH or cell.container.containerType == CONTAINER_SELL:
                pass
        if cell and cell.container:
            cell.container.handleWithIn(cell, shouldClear)
        return

    def setWithinBag(self, bag, clear=0, task=None):
        if bag == self.withInBag and clear:
            self.withInBag = None
            taskMgr.remove('InventoryUIManagerOpenBag')
        else:
            self.withInBag = bag
            if self.itemPickup == PICKUP_DRAG:
                taskMgr.doMethodLater(0.3, bag.bar.openBag, 'InventoryUIManagerOpenBag', [bag])
        return

    def withinDrag(self, task=None):
        if self.withInCell:
            self.withInCell.container.cellClick(self.withInCell, MOUSE_PRESS)

    def rightPress(self, task=None):
        if localAvatar.getGameState() in ('Fishing', 'ParlorGame'):
            return
        if self.withInCell:
            if self.withInCell.slotId and self.isSlotPending(self.withInCell.slotId):
                return
            self.withInCell.container.cellRightClick(self.withInCell, MOUSE_PRESS)

    def startPickupWithTimer(self):
        self.pickupTimedOut = 0
        taskMgr.doMethodLater(self.pickUpTime, self.lockoutPickup, 'InventoryUIManagerLockoutPickup')

    def lockoutPickup(self, task=None):
        self.pickupTimedOut = 1
        if self.heldItem:
            if self.heldItem.cell:
                self.heldItem.cell.container.postPickupLockout()

    def checkForDrop(self, caller=None):
        if self.heldItem and not self.withInCell:
            self.releaseHeld()
        if self.itemPickup == PICKUP_DRAG and self.heldItem:
            if self.withInCell:
                self.withInCell.container.cellClick(self.withInCell, MOUSE_RELEASE)
            else:
                self.releaseHeld()

    def hasContainerBeenAdded(self, container):
        return container in self.containerList

    def addContainer(self, container):
        if container not in self.containerList:
            self.containerList.append(container)
            container.reparentTo(self)
            container.show()
            container.manager = self
        else:
            import pdb
            pdb.set_trace()

    def makeItem(self, item):
        testItem = InventoryUIItem.InventoryUIItem(self, item)
        InventoryUIManager.testItemCount += 1
        return testItem

    def makeNoTradeItem(self, item):
        testItem = InventoryUINoTradeItem.InventoryUINoTradeItem(self, item)
        InventoryUIManager.testItemCount += 1
        return testItem

    def makeStackItem(self, itemTuple, showMax=1):
        itemCategory = itemTuple[0]
        itemId = itemTuple[1]
        if itemCategory == InventoryType.ItemTypeMoney:
            item = self.makeGoldItem(itemTuple)
        elif itemCategory == InventoryType.TreasureCollection:
            item = self.makeTreasureItem(itemTuple)
        elif itemCategory == InventoryCategory.CARDS:
            cardId = itemId
            itemTuple[1] -= InventoryType.begin_Cards
            item = self.makeCardItem(cardId, itemTuple, imageScaleFactor=1.9)
        elif itemCategory == InventoryCategory.WEAPON_PISTOL_AMMO:
            itemTuple[1] = WeaponGlobals.getSkillAmmoInventoryId(itemId)
            item = self.makeAmmoItem(itemId, itemTuple, showMax=0)
        else:
            item = InventoryUIStackItem.InventoryUIStackItem(self, itemTuple, showMax=showMax)
            InventoryUIManager.testItemCount += 1
        return item

    def makeCardItem(self, cardId, itemTuple, showMax=0, imageScaleFactor=0.05):
        return InventoryUICardItem.InventoryUICardItem(self, cardId, itemTuple, imageScaleFactor=imageScaleFactor, showMax=showMax)

    def makeWeaponItem(self, itemTuple):
        return InventoryUIWeaponItem.InventoryUIWeaponItem(self, itemTuple)

    def makeCharmItem(self, itemTuple):
        return InventoryUICharmItem.InventoryUICharmItem(self, itemTuple)

    def makeConsumableItem(self, itemTuple, showMax=1):
        return InventoryUIConsumableItem.InventoryUIConsumableItem(self, itemTuple, showMax=showMax)

    def makeAmmoItem(self, skillId, itemTuple, showMax=1, update=False):
        return InventoryUIAmmoItem.InventoryUIAmmoItem(self, skillId, itemTuple, showMax=showMax, update=update)

    def makeMaterialItem(self, materialId, itemTuple, showMax=1, update=False):
        return InventoryUIMaterialItem.InventoryUIMaterialItem(self, materialId, itemTuple, showMax=showMax, update=update)

    def makeFishingItem(self, skillId, itemTuple, showMax=1, update=False):
        return InventoryUIFishingItem.InventoryUIFishingItem(self, skillId, itemTuple, showMax=showMax, update=update)

    def makePouchItem(self, itemTuple):
        return InventoryUIPouchItem.InventoryUIPouchItem(self, itemTuple)

    def makeGoldItem(self, itemTuple, update=False):
        return InventoryUIGoldItem.InventoryUIGoldItem(self, itemTuple, update=update)

    def makeTreasureItem(self, itemTuple):
        return InventoryUITreasureItem.InventoryUITreasureItem(self, itemTuple)

    def makeClothingItem(self, itemTuple):
        return InventoryUIClothingItem.InventoryUIClothingItem(self, itemTuple)

    def makeJewelryItem(self, itemTuple):
        return InventoryUIJewelryItem.InventoryUIJewelryItem(self, itemTuple)

    def makeTattooItem(self, itemTuple):
        return InventoryUITattooItem.InventoryUITattooItem(self, itemTuple)

    def makeLocatableItem(self, itemTuple):
        itemCategory = itemTuple[0]
        if itemCategory == InventoryType.ItemTypeWeapon:
            return self.makeWeaponItem(itemTuple)
        if itemCategory == InventoryType.ItemTypeCharm:
            return self.makeCharmItem(itemTuple)
        elif itemCategory == InventoryType.ItemTypeClothing:
            return self.makeClothingItem(itemTuple)
        elif itemCategory == InventoryType.ItemTypeTattoo:
            return self.makeTattooItem(itemTuple)
        elif itemCategory == InventoryType.ItemTypeJewelry:
            return self.makeJewelryItem(itemTuple)
        elif itemCategory == InventoryType.ItemTypeConsumable:
            return self.makeConsumableItem(itemTuple)

    def wearItem(self, itemToWear, equipLocation, remove=None):
        localAvatar.wearItem(itemToWear, equipLocation, remove)

    def wearJewelry(self, itemToWear, equipLocation, removeType=None):
        localAvatar.wearJewelry(itemToWear, equipLocation, removeType)

    def wearTattoo(self, itemToWear, equipLocation, remove=None):
        localAvatar.wearTattoo(itemToWear, equipLocation, remove)

    def deleteItem(self, itemToTrash):
        if itemToTrash.cell:
            itemToTrash = itemToTrash.cell.container.grabCellItem(itemToTrash.cell)
            itemToTrash.cell.container.unHotlinkItem(itemToTrash)
            itemToTrash.cell.inventoryItem = None
        itemToTrash.destroy()
        return

    def discoverLocatableInventory(self, weaponBag, clothingBag=None, consumableBag=None):
        locatableItems = localAvatar.getInventory().getLocatables()
        misplacedSlots = []
        itemsToTrash = []
        base.localAvatar.lockRegen()
        for itemKey in locatableItems:
            if self.slotToCellMap.has_key(itemKey) and self.slotToCellMap[itemKey]:
                itemTuple = locatableItems[itemKey]
                itemId = itemTuple[1]
                itemCategory = itemTuple[0]
                slotCell = self.slotToCellMap[itemKey]
                uiItem = self.makeLocatableItem(itemTuple)
                if uiItem:
                    self.putIntoCellSlot(itemKey, uiItem)
                    slotCell.container.postUpdate(slotCell)
                    uiItem.refreshImageColor()
                elif self.trashInvalidItems:
                    itemsToTrash.append(itemTuple)
            else:
                misplacedSlots.append(itemKey)

        if len(itemsToTrash) > 0:
            print 'trashing invalid items %s' % itemsToTrash
            import pdb
            pdb.set_trace()
            localAvatar.getInventory().trashItems(itemsToTrash)
        base.localAvatar.unlockAndRegen()
        self.discoveredInventory = 1
        messenger.send('Inventory_Discovered', [self])
        self.accept('inventoryLocation-%s' % localAvatar.getInventory().doId, self.handleSlotUpdate)
        self.accept(InventoryGlobals.getOverflowChangeMsg(localAvatar.getInventory().doId), self.handleOverflow)
        if misplacedSlots:
            messenger.send('overflowChanged', [])
            runningList = []
            for slot in misplacedSlots:
                misplacedItemType = locatableItems[slot][0]
                newSlot = self.findOpenSlotForItemType(misplacedItemType, runningList)
                if newSlot:
                    localAvatar.getInventory().swapItems(slot, newSlot)

    def findOpenSlotForItemType(self, type, runningList=[]):
        slotRange = Locations.LOCATION_RANGES.get(type)
        if slotRange:
            if type not in (InventoryType.ItemTypeWeapon, InventoryType.ItemTypeClothing):
                return
            for rangeIndex in range(len(slotRange) - 1, -1, -1):
                atomicRange = slotRange[rangeIndex]
                for slotIndex in range(atomicRange[0], atomicRange[1]):
                    if self.slotToCellMap.has_key(slotIndex) and self.slotToCellMap[slotIndex] != None and self.slotToCellMap[slotIndex].inventoryItem == None and slotIndex not in runningList:
                        runningList.append(slotIndex)
                        return slotIndex

        return

    def markHeld(self):
        if self.heldFromCell:
            self.heldFromCell.container.markCell(self.heldFromCell, MASK_HELD)

    def releaseHeld(self):
        if not self.heldFromCell:
            self.heldItem = None
        if not self.heldItem:
            return
        self.heldItem.reparentTo(self.heldFromCell)
        self.heldItem.show()
        self.heldFromCell.container.resizeItem(self.heldItem)
        self.heldFromCell.container.unmarkCell(self.heldFromCell, MASK_HELD)
        self.heldFromCell.container.onRelease(self.heldFromCell)
        if self.heldFromCell.showLabel:
            self.heldFromCell.label.show()
            self.heldFromCell.label.reparentTo(self.heldItem)
        self.heldItem = None
        exHeldCell = self.heldFromCell
        self.heldFromCell = None
        exHeldCell.container.checkReqsForCell(exHeldCell)
        messenger.send('newItemHeld', [None, 1])
        self.markHeld()
        messenger.send('releaseHeld')
        return

    def testFullSlot(self):
        if self.heldFromCell and self.heldFromCell.slotId == None:
            self.reasonNoUse = ItemConstants.REASON_CANTPLACE
            self.displayReasonNoUse()
        return

    def getLocatableFromItem(self, item):
        inv = localAvatar.getInventory()
        if not inv:
            return None
        if item.cell and item.cell.slotId:
            return inv.getLocatables().get(item.cell.slotId)
        return None

    def removeFromHeld(self):
        item = self.heldItem
        self.heldItem.reparentTo(hidden)
        self.heldItem = None
        self.heldFromCell.container.unmarkCell(self.heldFromCell, MASK_HELD)
        self.heldFromCell = None
        self.markHeld()
        return item

    def canUseHeldItem(self):
        if self.heldItem and self.canLocalUseItem(self.heldItem.itemTuple)[0]:
            return 1
        else:
            return 0

    def canLocalUseItem(self, itemTuple):
        canUse = 1
        reason = ItemConstants.REASON_NONE
        itemCat = itemTuple[0]
        itemId = itemTuple[1]
        rarity = ItemGlobals.getRarity(itemId)
        if rarity != ItemConstants.CRUDE and not Freebooter.getPaidStatus(base.localAvatar.getDoId()):
            canUse = 0
            reason = ItemConstants.REASON_VELVETROPE
            return (
             canUse, reason)
        elif itemCat == InventoryType.ItemTypeClothing:
            gender = localAvatar.style.getGender()
            if gender == 'm' and ItemGlobals.getMaleModelId(itemId) == -1:
                canUse = 0
                reason = ItemConstants.REASON_GENDER
                return (
                 canUse, reason)
            elif gender == 'f' and ItemGlobals.getFemaleModelId(itemId) == -1:
                canUse = 0
                reason = ItemConstants.REASON_GENDER
                return (
                 canUse, reason)
        elif itemCat in [InventoryType.ItemTypeWeapon, InventoryType.ItemTypeCharm]:
            inv = localAvatar.getInventory()
            if not inv:
                canUse = 0
                reason = ItemConstants.REASON_INVENTORY
                return (
                 canUse, reason)
            reqs = localAvatar.getInventory().getItemRequirements(itemId)
            if reqs == None or filter(lambda x: reqs[x][1] == False, reqs):
                canUse = 0
                reason = ItemConstants.REASON_LEVEL
                return (
                 canUse, reason)
        return (canUse, reason)

    def testCanUse(self, locatable):
        canUse, reason = self.canLocalUseItem(locatable)
        if not canUse:
            self.reasonNoUse = reason
        else:
            self.reasonNoUse = None
        return canUse

    def putIntoHeld(self, item, cell):
        if item and cell and not (self.heldItem or self.heldFromCell):
            self.switchContainersForItem(item)
            self.heldItem = item
            self.heldItem.reparentTo(self.HeldNode)
            item.setScale(base.a2dTopCenter.getScale())
            self.heldFromCell = cell
            self.heldItem.cell = cell
            self.heldFromCell.label.reparentTo(self.heldFromCell)
            self.markHeld()
            if self.heldFromCell.inventoryItem:
                heldItem = self.heldFromCell.inventoryItem
                locatable = heldItem.itemTuple
                type = locatable[0]
                canUse = self.testCanUse(locatable)
                self.heldFromCell.container.checkReqsForCell(self.heldFromCell)
                messenger.send('newItemHeld', [locatable, canUse])

    def displayReasonNoUse(self, popUp=1):
        if not self.reasonNoUse:
            return
        elif self.reasonNoUse == ItemConstants.REASON_CANTPLACE:
            displayText = PLocalizer.EquipReasonFullSlot
        elif self.reasonNoUse == ItemConstants.REASON_VELVETROPE:
            displayText = PLocalizer.EquipReasonVelvet
            if popUp:
                localAvatar.guiMgr.showNonPayer()
                self.hasShownVelvet = 1
        elif self.reasonNoUse == ItemConstants.REASON_GENDER:
            if localAvatar.style.getGender() == 'm':
                displayText = PLocalizer.EquipReasonGenderFemale
            elif localAvatar.style.getGender() == 'f':
                displayText = PLocalizer.EquipReasonGenderMale
        elif self.reasonNoUse == ItemConstants.REASON_LEVEL:
            displayText = PLocalizer.EquipReasonLevel
        elif self.reasonNoUse == ItemConstants.REASON_INVENTORY:
            displayText = PLocalizer.EquipReasonInventory
        localAvatar.guiMgr.createWarning(displayText, PiratesGuiGlobals.TextFG6)
        self.reasonNoUse = None
        return

    def displaySlotFullReason(self):
        localAvatar.guiMgr.createWarning(PLocalizer.EquipReasonFull, PiratesGuiGlobals.TextFG6)

    def switchContainersForItem(self, item):
        locatable = self.getLocatableFromItem(item)
        if locatable:
            messenger.send('pickedUpItem', [locatable[0]])
        elif item.getCategory():
            messenger.send('pickedUpItem', [item.getCategory()])

    def placeHeldIntoCell(self, cell):
        cellHeld = self.heldFromCell
        cellDest = cell
        success = True
        if cellHeld.container and cellHeld.container.containerType == CONTAINER_PLUNDER:
            success = self.takePlunderItemFromCell(cellHeld, toCell=cellDest, playSound=False)
        if not cellHeld.isEmpty() and success:
            droppedItem = cellHeld.container.grabCellItem(cellHeld)
            heldId = self.heldFromCell.slotId
            self.releaseHeld()
            self.putIntoCellSlot(cellDest.slotId, droppedItem, 1, oldSlotId=heldId)
            if cellHeld.container and not cellHeld.container.isEmpty() and cellHeld.container.containerType != CONTAINER_PLUNDER:
                localAvatar.getInventory().swapItems(cellHeld.slotId, cellDest.slotId)
        if cellHeld and cellHeld.container:
            cellHeld.container.checkReqsForCell(cellHeld)
        if cellDest and cellDest.container:
            cellDest.container.checkReqsForCell(cellDest)

    def swapHeldWithCell(self, cell):
        if self.heldFromCell.container.containerType == CONTAINER_PLUNDER:
            self.releaseHeld()
            return
        cellA = self.heldFromCell
        cellB = cell
        droppedItem = self.removeFromHeld()
        grabbedItem = cell.container.grabCellItem(cellB)
        if droppedItem.cell and droppedItem.cell.container:
            droppedItem.cell.container.unHotlinkItem(droppedItem)
        if grabbedItem.cell and grabbedItem.cell.container:
            grabbedItem.cell.container.unHotlinkItem(grabbedItem)
        droppedItem.cell = None
        grabbedItem.cell = None
        cellA.inventoryItem = None
        cellB.inventoryItem = None
        self.putIntoCellSlot(cellB.slotId, droppedItem, 1)
        self.putIntoCellSlot(cellA.slotId, grabbedItem, 1)
        self.putIntoHeld(grabbedItem, cellA)
        localAvatar.getInventory().swapItems(cellA.slotId, cellB.slotId)
        cell.container.onRelease(cell)
        self.markHeld()
        cellA.container.checkReqsForCell(cellA)
        cellB.container.checkReqsForCell(cellB)
        return

    def assignCellSlot(self, cell, slot):
        if slot == None:
            cell.slotId = None
        elif self.slotToCellMap[slot] == None:
            self.slotToCellMap[slot] = cell
            cell.container.assignSlot(cell, slot)
        else:
            print 'SLOT COLLISION ERROR! FIX ME!'
            import pdb
            pdb.set_trace()
        return

    def markSlotPending(self, slot):
        self.slotPendingActionList.append(slot)
        cell = self.slotToCellMap.get(slot)
        if cell and cell.container:
            cell.container.markCell(cell, MASK_PENDING)
        taskMgr.remove('stuckPendingTask')
        taskMgr.doMethodLater(20.0, self.fixStuckPending, 'stuckPendingTask')

    def unmarkSlotPending(self, slot):
        if slot in self.slotPendingActionList:
            self.slotPendingActionList.remove(slot)
        cell = None
        if self.slotToCellMap.has_key(slot):
            cell = self.slotToCellMap[slot]
        if cell and cell.container:
            cell.container.unmarkCell(cell, MASK_PENDING)
        if self.associatedSlotDict.has_key(slot):
            assocSlot = self.associatedSlotDict[slot]
            self.unmarkSlotPending(assocSlot)
            del self.associatedSlotDict[slot]
        return

    def isSlotPending(self, slot):
        if slot in self.slotPendingActionList and slot != None:
            return 1
        else:
            return 0
        return

    def fixStuckPending(self, task=None):
        holdList = []
        for stuckSlot in self.slotPendingActionList:
            holdList.append(stuckSlot)

        for stuckSlot in holdList:
            self.handleSlotUpdate(stuckSlot)

        self.associatedSlotDict = {}
        if task:
            return task.done

    def putIntoCellSlot(self, slot, item, localChange=0, oldSlotId=None):
        if self.slotToCellMap.get(slot):
            slotCell = self.slotToCellMap[slot]
            if localChange:
                if self.isSlotPending(slot):
                    raise "you need to test that this slot isn't buffering a local change"
                elif slotCell == self.heldFromCell:
                    pass
                if not self.isSlotPending(slot):
                    self.markSlotPending(slot)
                    if oldSlotId:
                        self.markSlotPending(oldSlotId)
                        self.associatedSlotDict[slot] = oldSlotId
            elif self.isSlotPending(slot):
                self.unmarkSlotPending(slot)
            if slotCell and not slotCell.inventoryItem:
                slotCell.container.putIntoCell(item, slotCell)
                return slotCell
            if slotCell and slotCell == self.heldFromCell:
                heldCell = self.heldFromCell
                self.releaseHeld()
                self.putIntoHeld(item, heldCell)
        return None

    def deleteFromCellSlot(self, slot):
        if self.slotToCellMap.has_key(slot):
            slotCell = self.slotToCellMap[slot]
            if slotCell == self.heldFromCell:
                self.releaseHeld()
            if slotCell.inventoryItem:
                item = slotCell.container.grabCellItem(slotCell)
                self.deleteItem(item)

    def swapCellSlot(self, fromSlot, toSlot):
        if self.slotToCellMap.has_key(fromSlot) and self.slotToCellMap.has_key(toSlot):
            fromCell = self.slotToCellMap[fromSlot]
            toCell = self.slotToCellMap[toSlot]
            if fromCell == self.heldFromCell or toCell == self.heldFromCell:
                self.releaseHeld()
            fromItem = fromCell.container.grabCellItem(fromCell)
            toItem = toCell.container.grabCellItem(toCell)
            fromCell.inventoryItem = None
            toCell.inventoryItem = None
            fromCell.container.putIntoCell(toItem, fromCell)
            toCell.container.putIntoCell(fromItem, toCell)
        return

    def handleSlotUpdate(self, slot):
        if self.slotToCellMap.has_key(slot):
            slotCell = self.slotToCellMap[slot]
            locatableItems = localAvatar.getInventory().getLocatables()
            item = locatableItems.get(slot)
            if not slotCell:
                if slot >= Locations.RANGE_OVERFLOW[0]:
                    if slot <= Locations.RANGE_OVERFLOW[1]:
                        messenger.send('overflowChanged', [])
                if slotCell:
                    if not item:
                        if slotCell.inventoryItem:
                            if slotCell.inventoryItem.getCategory() == InventoryType.ItemTypeConsumable and slotCell.inventoryItem.hasDrunk:
                                removedText = PLocalizer.ItemDrank % slotCell.inventoryItem.getName()
                            else:
                                removedText = PLocalizer.ItemRemoved % slotCell.inventoryItem.getName()
                            localAvatar.guiMgr.createWarning(removedText, PiratesGuiGlobals.TextFG6)
                            self.deleteFromCellSlot(slot)
                            if self.isSlotPending(slot):
                                self.unmarkSlotPending(slot)
                        slotCell.container.postUpdate(slotCell)
                        return
                    else:
                        itemId = item[1]
                        itemCategory = item[0]
                    uiItem = slotCell.inventoryItem or self.makeLocatableItem(item)
                    self.putIntoCellSlot(slot, uiItem)
                    slotCell.container.postUpdate(slotCell)
                elif slotCell.inventoryItem.getId() == itemId:
                    if self.isSlotPending(slot):
                        self.unmarkSlotPending(slot)
                else:
                    placeInHeld = 0
                    if slotCell == self.heldFromCell:
                        placeInHeld = 1
                    oldName = slotCell.inventoryItem.getName()
                    self.deleteFromCellSlot(slot)
                    uiItem = self.makeLocatableItem(item)
                    self.putIntoCellSlot(slot, uiItem)
                    if placeInHeld:
                        self.putIntoHeld(uiItem, slotCell)
                slotCell.container.postUpdate(slotCell)

    def handleOverflow(self, slot):
        slotCell = self.slotToCellMap.get(slot)
        if slotCell:
            displayText = PLocalizer.EquipItemInFromOverflow % slotCell.inventoryItem.getName()
            localAvatar.guiMgr.createWarning(displayText, PiratesGuiGlobals.TextFG6, duration=4.0)

    def addLocalStoreContainer(self, container):
        self.localStoreContainers.append(container)

    def takePlunderItemFromCell(self, cell, toCell=None, playSound=True):
        if toCell != None:
            pass
        location = 0
        if toCell and toCell.slotId:
            location = toCell.slotId
        if not cell.inventoryItem:
            return False
        inventory = base.localAvatar.getInventory()
        if not inventory:
            return False
        if location and not inventory.locationAvailable(location) or location in Locations.RANGE_EQUIP_SLOTS:
            location = 0
        if cell.inventoryItem.getCategory() in (InventoryType.ItemTypeWeapon, InventoryType.ItemTypeCharm, InventoryType.ItemTypeClothing, InventoryType.ItemTypeConsumable):
            locatables = [
             InvItem([cell.inventoryItem.getCategory(), cell.inventoryItem.getId(), 0, 0])]
            locationIds = inventory.canAddLocatables(locatables)
            for locationId in locationIds:
                if locationId in (Locations.INVALID_LOCATION, Locations.NON_LOCATION):
                    base.localAvatar.guiMgr.createWarning(PLocalizer.InventoryFullWarning, PiratesGuiGlobals.TextFG6)
                    return False

        item = cell.container.grabCellItem(cell)
        fromContainer = cell.container
        cell.stash()
        cell.inventoryItem = None
        category = item.getCategory()
        if category == InventoryCategory.WEAPON_PISTOL_AMMO:
            id = item.getSkillId()
            extraArg = item.amount
        elif category == InventoryCategory.CARDS:
            id = item.getCardId()
            extraArg = 1
        else:
            if category == InventoryType.ItemTypeClothing:
                id = item.getId()
                extraArg = item.getColorId()
            elif category == InventoryType.ItemTypeMoney:
                id = item.getId()
                extraArg = item.amount
            elif category == InventoryCategory.MONEY:
                id = item.getId()
                extraArg = item.amount
            elif category == InventoryType.TreasureCollection:
                id = item.getId()
                extraArg = item.itemTuple[3]
            else:
                id = item.getId()
                extraArg = 1
            if self.scoreboard:
                if playSound:
                    if id == UberDogGlobals.InventoryType.ItemTypeMoney:
                        self.takeGoldSound.play()
                    else:
                        self.takeNonGoldSound.play()
                self.scoreboard.requestItem([category, id, extraArg, location])
            if self.lootContainer:
                if playSound:
                    if id == UberDogGlobals.InventoryType.ItemTypeMoney:
                        self.takeGoldSound.play()
                    else:
                        self.takeNonGoldSound.play()
                self.lootContainer.d_requestItem([category, id, extraArg, location])
        messenger.send('lootsystem-plunderContainer-Empty', [])
        return True

    def takeAllLoot(self, grids, playSound=True):
        if self.heldItem:
            self.releaseHeld()
        items = []
        cells = {}
        for grid in grids:
            for cell in grid.cellList:
                if cell.inventoryItem and not cell.inventoryItem.isHidden():
                    category = cell.inventoryItem.getCategory()
                    if category == InventoryCategory.WEAPON_PISTOL_AMMO:
                        id = cell.inventoryItem.getSkillId()
                        extraArg = cell.inventoryItem.amount
                    elif category == InventoryCategory.CARDS:
                        id = cell.inventoryItem.getCardId()
                        extraArg = 1
                    elif category == InventoryType.ItemTypeClothing:
                        id = cell.inventoryItem.getId()
                        extraArg = cell.inventoryItem.getColorId()
                    elif category == InventoryType.ItemTypeMoney:
                        id = cell.inventoryItem.getId()
                        extraArg = cell.inventoryItem.amount
                    elif category == InventoryCategory.MONEY:
                        id = cell.inventoryItem.getId()
                        extraArg = cell.inventoryItem.amount
                    elif category == InventoryType.TreasureCollection:
                        id = cell.inventoryItem.getId()
                        extraArg = cell.inventoryItem.itemTuple[3]
                    else:
                        id = cell.inventoryItem.getId()
                        extraArg = 1
                    info = (
                     category, id, extraArg)
                    items.append(info)
                    cells[cell] = info

        if items:
            if self.lootContainer and self.lootContainer.getItemsToTake():
                if len(items) > self.lootContainer.getItemsToTake():
                    return
                else:
                    self.lootContainer.subtractItemsToTake(len(items))
                    if not self.lootContainer.getItemsToTake():
                        closeWindow = True
                    else:
                        closeWindow = False
            else:
                closeWindow = False
            givingItems, extraItems = self.getGivingItems(items)
            if givingItems:
                if playSound:
                    self.playTakeAllSound()
                if self.scoreboard:
                    self.scoreboard.requestItems(givingItems)
                elif self.lootContainer:
                    self.lootContainer.d_requestItems(givingItems)
            if extraItems:
                for cell in cells:
                    if cells[cell] in givingItems:
                        cell.hide()

                base.localAvatar.guiMgr.createWarning(PLocalizer.PlunderItemsLeftWarning, PiratesGuiGlobals.TextFG6)
            else:
                self.closePlunder()
            if closeWindow:
                self.closePlunder()

    def getGivingItems(self, items):
        weapons = []
        clothes = []
        consumables = []
        givingItems = []
        extraItems = []
        inventory = base.localAvatar.getInventory()
        if inventory:
            for item in items:
                if item[0] in (InventoryType.ItemTypeWeapon, InventoryType.ItemTypeCharm):
                    weapons.append([ItemGlobals.getGoldCost(item[0]), item])
                elif item[0] == InventoryType.ItemTypeClothing:
                    clothes.append([ItemGlobals.getGoldCost(item[0]), item])
                elif item[0] == InventoryType.ItemTypeConsumable:
                    consumables.append([ItemGlobals.getGoldCost(item[0]), item])
                else:
                    givingItems.append(item)

            weapons.sort()
            clothes.sort()
            consumables.sort()
            locatables = []
            for weapon in weapons:
                locatables.append(InvItem([weapon[1][0], weapon[1][1], 0]))

            invalidLocations = 0
            locationIds = inventory.canAddLocatables(locatables)
            for locationId in locationIds:
                if locationId in (Locations.INVALID_LOCATION, Locations.NON_LOCATION):
                    invalidLocations += 1

            for i in range(0, invalidLocations):
                extraItems.append(weapons[i][1])

            for i in range(invalidLocations, len(weapons)):
                givingItems.append(weapons[i][1])

            locatables = []
            for cloth in clothes:
                locatables.append(InvItem([cloth[1][0], cloth[1][1], 0, 0]))

            invalidLocations = 0
            locationIds = inventory.canAddLocatables(locatables)
            for locationId in locationIds:
                if locationId in (Locations.INVALID_LOCATION, Locations.NON_LOCATION):
                    invalidLocations += 1

            for i in range(0, invalidLocations):
                extraItems.append(clothes[i][1])

            for i in range(invalidLocations, len(clothes)):
                givingItems.append(clothes[i][1])

            locatables = []
            for consumable in consumables:
                locatables.append(InvItem([consumable[1][0], consumable[1][1], 0, 0]))

            invalidLocations = 0
            locationIds = inventory.canAddLocatables(locatables)
            for locationId in locationIds:
                if locationId in (Locations.INVALID_LOCATION, Locations.NON_LOCATION):
                    invalidLocations += 1

            for i in range(0, invalidLocations):
                extraItems.append(consumables[i][1])

            for i in range(invalidLocations, len(consumables)):
                givingItems.append(consumables[i][1])

        return (
         givingItems, extraItems)

    def testPlunder(self):
        plunderList = [
         (
          UberDogGlobals.InventoryType.CutlassWeaponL1, 0), (UberDogGlobals.InventoryType.PistolWeaponL3, 0), (UberDogGlobals.InventoryType.ItemTypeMoney, 32), (UberDogGlobals.InventoryType.Collection_Set2_Part9, 0), (UberDogGlobals.InventoryType.begin_Cards, 0)]
        self.openPlunder(plunderList)

    def openPlunder(self, plunderList, lootContainer=None, customName=None, timer=0, autoShow=True):
        if not self.plunderPanel:
            if self.lootContainer:
                self.closePlunder()
            rating = 0
            typeName = ''
            if lootContainer:
                self.lootContainer = lootContainer
                rating = lootContainer.getRating()
                typeName = lootContainer.getTypeName()
                numItems = lootContainer.getItemsToTake()
            else:
                numItems = 0
            self.plunderPanel = InventoryPlunderPanel.InventoryPlunderPanel(self, plunderList, rating, typeName, numItems, customName, timer=timer, autoShow=autoShow)
            self.plunderPanel.reparentTo(self)
            self.plunderPanel.setPos(-1.1, 0.0, -0.2)

    def closePlunder(self, closeContainer=True):
        if self.lootContainer:
            if closeContainer:
                self.lootContainer.doneTaking()
            self.lootContainer = None
        if self.plunderPanel:
            self.plunderPanel.destroy()
        self.plunderPanel = None
        if self.scoreboard:
            self.scoreboard.closePanel()
        self.scoreboard = None
        messenger.send('plunderClosed')
        return

    def showPlunder(self):
        if self.plunderPanel:
            self.plunderPanel.show()

    def hidePlunder(self):
        if self.plunderPanel:
            self.plunderPanel.hide()

    def hasPlunder(self):
        return self.plunderPanel

    def addScoreboard(self, scoreboard):
        self.scoreboard = scoreboard

    def removeScoreboard(self):
        self.scoreboard = None
        return

    def selectStack(self, cell):
        if self.tradeContainer:
            self.splitStack(cell)
        else:
            return

    def splitStack(self, cell):
        if not self.stackSplitter:
            if cell.inventoryItem.getAmount() == 0:
                return
            self.stackSplitter = InventoryStackSplitter.InventoryStackSplitter(cell, self)
            self.stackSplitter.reparentTo(self)
            self.cancelCellItemDetails()
            self.locked = 1

    def closeSplitter(self):
        if self.stackSplitter:
            self.stackSplitter.destroy()
            self.stackSplitter = None
            self.locked = 0
        return

    def holdForSale(self, cell):
        if cell.inventoryItem:
            self.trashItem = cell.inventoryItem
            self.trashItem.cell.container.markCell(self.trashItem.cell, MASK_TRASH)
            self.releaseHeld()
            self.cancelCellItemDetails()
            self.locked = 1

    def releaseFromSale(self):
        if self.trashItem:
            self.trashItem.show()
            self.trashItem.cell.container.unmarkCell(self.trashItem.cell, MASK_TRASH)
        self.trashItem = None
        self.removeContainer = None
        self.locked = 0
        return

    def makeSale(self, amount):
        if self.trashItem:
            self.markSlotPending(self.trashItem.cell.slotId)
            itemToTrash = localAvatar.getInventory().getLocatables().get(self.trashItem.cell.slotId)
            if itemToTrash:
                messenger.send('sellItem', [itemToTrash, amount])
        self.releaseFromSale()

    def openRemover(self, cell):
        if cell.slotId == None:
            displayText = PLocalizer.CantTrashThat
            localAvatar.guiMgr.createWarning(displayText, PiratesGuiGlobals.TextFG6)
            return
        if not self.removeConfirm and cell.inventoryItem:
            self.removeConfirm = InventoryRemoveConfirm.InventoryRemoveConfirm(cell, self)
            self.trashItem = cell.inventoryItem
            self.trashItem.cell.container.markCell(self.trashItem.cell, MASK_TRASH)
            self.removeConfirm.reparentTo(self)
            self.releaseHeld()
            self.cancelCellItemDetails()
            self.locked = 1
        return

    def closeRemover(self):
        if self.removeConfirm:
            self.trashItem.show()
            self.trashItem.cell.container.unmarkCell(self.trashItem.cell, MASK_TRASH)
            self.trashItem = None
            self.removeConfirm.destroy()
            self.removeConfirm = None
            self.removeContainer = None
            self.locked = 0
        return

    def discardFromRemover(self):
        if self.trashItem.cell == None:
            pass
        else:
            self.markSlotPending(self.trashItem.cell.slotId)
            itemToTrash = localAvatar.getInventory().getLocatables().get(self.trashItem.cell.slotId)
            if itemToTrash:
                localAvatar.getInventory().trashItems([itemToTrash])
                self.trashSound.play()
        self.closeRemover()
        return

    def startCellItemDetails(self, cell, detailsPos, detailsHeight, detailsDelay, event=None):
        while taskMgr.hasTaskNamed('inventoryUIDetailTask'):
            taskMgr.remove('inventoryUIDetailTask')

        if cell.inventoryItem:
            taskMgr.doMethodLater(detailsDelay, self.showDetails, 'inventoryUIDetailTask', extraArgs=[cell.inventoryItem, cell, detailsPos, detailsHeight])
        elif cell.hotlink:
            taskMgr.doMethodLater(detailsDelay, self.showDetails, 'inventoryUIDetailTask', extraArgs=[cell.hotlink, cell, detailsPos, detailsHeight])
        elif self.showingItem:
            taskMgr.doMethodLater(detailsDelay, self.hideDetails, 'inventoryUIHideDetailTask')

    def hideDetails(self, task=None):
        if self.showingItem:
            self.showingItem.hideDetails()
            self.showingItem = None
        return

    def showDetails(self, item, cell, detailsPos, detailsHeight, task=None):
        self.hideDetails()
        self.showingItem = item
        item.showDetails(cell, detailsPos, detailsHeight)

    def cancelCellItemDetails(self, event=None):
        self.hideDetails()
        while taskMgr.hasTaskNamed('inventoryUIDetailTask'):
            taskMgr.remove('inventoryUIDetailTask')

    def playTakeAllSound(self):
        self.takeAllSound.play()

    def getDisplayHuman(self):
        return self.displayHuman

    def getMasterHuman(self):
        return base.cr.humanHigh
