from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from pirates.piratesgui import GuiPanel, PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from otp.otpbase import OTPLocalizer
from pirates.inventory import InventoryUIContainer
from pirates.inventory.InventoryUIGlobals import *
from pirates.inventory.InventoryGlobals import Locations
from pirates.inventory import InventoryGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.inventory import ItemGlobals
from pirates.inventory import ItemConstants

class InventoryUIBeltGrid(InventoryUIContainer.InventoryUIContainer):

    def __init__(self, manager, sizeX=1.0, sizeZ=1.0, countX=1, countZ=1, hotkeyList=[]):
        InventoryUIContainer.InventoryUIContainer.__init__(self, manager, sizeX, sizeZ, countX, countZ, cellInfo=hotkeyList)
        self.containerType = CONTAINER_BELT
        gui = loader.loadModel('models/gui/gui_icons_weapon')
        self.cellImage = gui.find('**/pir_t_gui_frm_inventoryBox')
        self.initialiseoptions(InventoryUIBeltGrid)
        self.rightClickAction = {InventoryType.ItemTypeWeapon: (Locations.RANGE_WEAPONS, None, 0),InventoryType.ItemTypeCharm: (Locations.RANGE_WEAPONS, None, 1)}
        self.freeWeaponInfo = DirectLabel(parent=self, relief=None, textMayChange=0, text=PLocalizer.FreeWeaponFromBlackSmith, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_fg=PiratesGuiGlobals.TextFG2, text_scale=0.04, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0,
                                                                                                                                                                                                                                                                                                                         0))
        self.freeWeaponInfo.setPos(0.35, 0, -0.1)
        self.freeWeaponInfo.show()
        self.overflowInfo = DirectLabel(parent=self, relief=None, textMayChange=0, text=PLocalizer.OverflowHint, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_fg=PiratesGuiGlobals.TextFG2, text_scale=0.04, text_align=TextNode.ACenter, text_shadow=PiratesGuiGlobals.TextShadow, text_pos=(0,
                                                                                                                                                                                                                                                                                                           0))
        self.overflowInfo.setPos(0.35, 0, -0.1)
        self.overflowInfo.hide()
        self.accept('overflowChanged', self.handleOverflow)
        self.accept('newItemHeld', self.handleNewHeldItem)
        self.accept('checkForWeapons', self.checkforNoWeapons)
        return

    def canDrag(self):
        return 1

    def canReceive(self, myCell, fromSwap=0, itemInQuestion=None):
        if itemInQuestion:
            pass
        if itemInQuestion and not self.manager.canLocalUseItem(itemInQuestion.itemTuple)[0]:
            return 0
        else:
            return InventoryUIContainer.InventoryUIContainer.canReceive(self, myCell, fromSwap)

    def manageCells(self, hotkeyList):
        self.hotkeyList = hotkeyList
        for index in range(len(self.hotkeyList)):
            hotkey = self.hotkeyList[index]
            cell = self.cellList[index]
            cell.showLabel = 1
            cell.labelText = hotkey[0]
            cell.label['text'] = hotkey[0]
            cell.boundEvent = hotkey[1]
            self.accept(cell.boundEvent, self.useHotkey, extraArgs=[cell])
            cell.label.show()
            self.manager.assignCellSlot(cell, hotkey[2])
            cell.container.markCell(cell, MASK_EMPTYEQUIP)

    def useHotkey(self, cell):
        if cell.inventoryItem:
            messenger.send('Use_Weapon_Request', [cell.inventoryItem.getId(), cell.slotId])

    def handleNewHeldItem(self, itemTuple, canUse):
        if itemTuple != None:
            itemCat = itemTuple[0]
            itemId = itemTuple[1]
            itemRanges = InventoryGlobals.getEquipRanges(itemCat, itemId)
            if not itemRanges:
                return
            itemUseSlots = InventoryGlobals.expandRanges(itemRanges)
            for cell in self.cellList:
                if cell.slotId:
                    if cell.slotId in itemUseSlots:
                        cell.container.markCell(cell, MASK_ISDEST)
                        cell.container.unmarkCell(cell, MASK_NOTDEST)
                        canUse or cell.container.markCell(cell, MASK_NOTMEETREQUIREMENTS)
                else:
                    cell.container.markCell(cell, MASK_NOTDEST)
                    cell.container.unmarkCell(cell, MASK_ISDEST)

        else:
            for cell in self.cellList:
                cell.container.unmarkCell(cell, MASK_NOTDEST)
                cell.container.unmarkCell(cell, MASK_ISDEST)
                cell.container.unmarkCell(cell, MASK_NOTMEETREQUIREMENTS)
                self.checkReqsForCell(cell)

        return

    def postUpdate(self, cell):
        if cell:
            if cell.slotId:
                if cell in self.cellList:
                    self.checkReqsForCell(cell)
                gui = loader.loadModel('models/gui/gui_icons_weapon')
                if cell.inventoryItem or cell.slotId in Locations.RANGE_EQUIP_ITEMS:
                    localAvatar.d_requestCurrentCharm(0)
                cell.container.markCell(cell, MASK_EMPTYEQUIP)
                cell.container.unmarkCell(cell, MASK_FULLEQUIP)
            else:
                if cell.slotId in Locations.RANGE_EQUIP_ITEMS:
                    localAvatar.d_requestCurrentCharm(cell.inventoryItem.getId())
                cell.container.markCell(cell, MASK_FULLEQUIP)
                cell.container.unmarkCell(cell, MASK_EMPTYEQUIP)
            if cell.slotId in range(Locations.RANGE_EQUIP_WEAPONS[0], Locations.RANGE_EQUIP_WEAPONS[1] + 1):
                allWeaponDict = localAvatar.getInventory().getWeapons()
                allWeaponList = []
                for slotKey in allWeaponDict:
                    allWeaponList.append(allWeaponDict[slotKey][1])

                if localAvatar.isWeaponDrawn and not localAvatar.checkForWeaponInSlot(localAvatar.currentWeaponId, localAvatar.currentWeaponSlotId) and localAvatar.getGameState() == 'Battle':
                    localAvatar.b_setGameState('LandRoam')
        self.checkforNoWeapons()

    def checkforNoWeapons(self):
        if localAvatar.getInventory().getAllWeapons() == {}:
            self.freeWeaponInfo.show()
        else:
            self.freeWeaponInfo.hide()

    def testCellReqs(self, cell):
        if MASK_NOTMEETREQUIREMENTS in cell.statusMask:
            return 0
        else:
            return 1

    def handleOverflow(self, info=None):
        self.overflowInfo.hide()
        overflowItems = localAvatar.getInventory().getOverflowItems()
        for item in overflowItems:
            if item[0] in (InventoryType.ItemTypeWeapon, InventoryType.ItemTypeCharm):
                self.overflowInfo.show()
                return