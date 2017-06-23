from direct.gui.DirectGui import *
from direct.task import Task
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryPage
from pirates.piratesgui import WeaponPanel
from pirates.piratesgui.SkillButton import SkillButton
from pirates.piratesgui import InventoryItemGui
from pirates.piratesgui import InventoryItemList
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui.CombatTray import WeaponButton
from pirates.economy import EconomyGlobals
from pirates.economy.EconomyGlobals import *
from pirates.battle import WeaponGlobals
from pirates.reputation import ReputationGlobals
from pirates.inventory import InventoryUIManager
from pirates.inventory import InventoryUIBeltGrid
from pirates.inventory import InventoryUIBagbar
from pirates.inventory import InventoryUITrashContainer
from pirates.inventory import InventoryUIDrinker
from pirates.inventory import InventoryUIWeaponContainer
from pirates.inventory import InventoryUIClothingContainer
from pirates.inventory import InventoryUIJewelryContainer
from pirates.inventory import InventoryUIDressingContainer
from pirates.inventory import InventoryUIJewelryDressingContainer
from pirates.inventory import InventoryUITattooDressingContainer
from pirates.inventory import InventoryUIGoldContainer
from pirates.inventory import InventoryUIAmmoContainer
from pirates.inventory import InventoryUIMaterialContainer
from pirates.inventory import InventoryUIConsumableContainerLocatable
from pirates.inventory import InventoryUICardContainer
from pirates.piratesgui import RedeemCodeGUI
from pirates.uberdog import UberDogGlobals
from pirates.inventory.InventoryUIGlobals import *
from pirates.inventory.InventoryGlobals import Locations
from pirates.uberdog import DistributedInventoryBase

class InventoryBagPage(InventoryPage.InventoryPage):

    def __init__(self, inventoryUIManager):
        self.inventoryUIManager = inventoryUIManager
        InventoryPage.InventoryPage.__init__(self)
        self.initialiseoptions(InventoryBagPage)
        self.containerList = []
        self.containersToShowTrash = []
        self.treasureTab = None
        self.isReady = 0
        self.treasurePageReopen = 0
        self.openedContainer = None
        self.redeemCodeGUI = None
        self.buttonSize = self.inventoryUIManager.standardButtonSize
        self.weaponBag = self.addContainer(InventoryUIWeaponContainer.InventoryUIWeaponContainer(self.inventoryUIManager, self.buttonSize * 6.0, self.buttonSize * 5.0, 6, 5, slotList=range(Locations.RANGE_WEAPONS[0], Locations.RANGE_WEAPONS[0] + 30)))
        self.clothingBag = self.addContainer(InventoryUIClothingContainer.InventoryUIClothingContainer(self.inventoryUIManager, self.buttonSize * 5.0, self.buttonSize * 7.0, 5, 7, slotList=range(Locations.RANGE_CLOTHES[0], Locations.RANGE_CLOTHES[0] + 35)))
        self.jewelryBag = self.addContainer(InventoryUIJewelryContainer.InventoryUIJewelryContainer(self.inventoryUIManager, self.buttonSize * 4.0, self.buttonSize * 7.0, 4, 7, slotList=range(Locations.RANGE_JEWELERY_AND_TATTOO[0], Locations.RANGE_JEWELERY_AND_TATTOO[0] + 28)))
        cardRange = range(UberDogGlobals.InventoryType.begin_Cards, UberDogGlobals.InventoryType.end_Cards)
        cardRange.reverse()
        self.potionBag = self.addContainer(InventoryUIConsumableContainerLocatable.InventoryUIConsumableContainerLocatable(self.inventoryUIManager, self.buttonSize * 6.0, self.buttonSize * 7.0, 6, 7, slotList=range(Locations.RANGE_CONSUMABLE[0], Locations.RANGE_CONSUMABLE[0] + 42)))
        self.ammoBag = self.addContainer(InventoryUIAmmoContainer.InventoryUIAmmoContainer(self.inventoryUIManager, self.buttonSize * 7.0, self.buttonSize * 6.0, maxCountX=7, itemList=WeaponGlobals.getAllAmmoSkills()), showTrash=0)
        self.materialBag = self.addContainer(InventoryUIMaterialContainer.InventoryUIMaterialContainer(self.inventoryUIManager, self.buttonSize * 7.0, self.buttonSize * 6.0, maxCountX=7, itemList=WeaponGlobals.getAllAmmoSkills()), showTrash=0)
        self.cardBag = self.addContainer(InventoryUICardContainer.InventoryUICardContainer(self.inventoryUIManager, self.buttonSize * 4.0, self.buttonSize * 13.0, 4, 13, minCountZ=13, maxCountX=4, itemList=cardRange), showTrash=0)
        hotkeySlotStart = Locations.RANGE_EQUIP_WEAPONS[0]
        weaponKeySlotList = []
        for weaponIndex in range(Locations.RANGE_EQUIP_WEAPONS[0], Locations.RANGE_EQUIP_WEAPONS[1] + 1):
            weaponKeySlotList.append(('F%s' % weaponIndex, 'f%s' % weaponIndex, weaponIndex))

        weaponKeySlotList.append((PLocalizer.InventoryPageItemSlot, '', Locations.RANGE_EQUIP_ITEMS[0]))
        self.inventoryPanelHotkey = InventoryUIBeltGrid.InventoryUIBeltGrid(self.inventoryUIManager, self.buttonSize * float(len(weaponKeySlotList)), self.buttonSize, len(weaponKeySlotList), 1, weaponKeySlotList)
        self.inventoryPanelHotkey.setPos(0.425 - 0.5 * self.inventoryPanelHotkey.sizeX, 0.0, 0.895)
        self.inventoryPanelHotkey.reparentTo(self.weaponBag)
        self.inventoryPanelTrash = InventoryUITrashContainer.InventoryUITrashContainer(self.inventoryUIManager, self.buttonSize, self.buttonSize)
        self.inventoryPanelTrash.setup()
        self.inventoryPanelTrash.setPos(0.07, 0.0, -0.03)
        self.inventoryPanelTrash.reparentTo(self)
        self.inventoryPanelDrinker = InventoryUIDrinker.InventoryUIDrinker(self.inventoryUIManager, self.buttonSize, self.buttonSize)
        self.inventoryPanelDrinker.setup()
        self.inventoryPanelDrinker.setPos(0.3, 0.0, -0.03)
        self.inventoryPanelDrinker.reparentTo(self)
        self.inventoryPanelDressing = InventoryUIDressingContainer.InventoryUIDressingContainer(self.inventoryUIManager, self.buttonSize, self.buttonSize * 7.0, slotList=range(Locations.RANGE_EQUIP_CLOTHES[0], Locations.RANGE_EQUIP_CLOTHES[1] + 1))
        self.inventoryPanelDressing.setPos(-0.225, 0.0, -0.0)
        self.inventoryPanelDressing.reparentTo(self.clothingBag)
        self.inventoryPanelJewelryDressing = InventoryUIJewelryDressingContainer.InventoryUIJewelryDressingContainer(self.inventoryUIManager, self.buttonSize * 2.0, self.buttonSize * 4.0, slotList=range(Locations.RANGE_EQUIP_JEWELRY[0], Locations.RANGE_EQUIP_JEWELRY[1] + 1))
        self.inventoryPanelJewelryDressing.setPos(-0.37, 0.0, 0.41)
        self.inventoryPanelJewelryDressing.reparentTo(self.jewelryBag)
        self.inventoryPanelTattooDressing = InventoryUITattooDressingContainer.InventoryUITattooDressingContainer(self.inventoryUIManager, self.buttonSize * 2.0, self.buttonSize * 2.0, slotList=range(Locations.RANGE_EQUIP_TATTOO[0], Locations.RANGE_EQUIP_TATTOO[1] + 1))
        self.inventoryPanelTattooDressing.setPos(-0.37, 0.0, 0.0)
        self.inventoryPanelTattooDressing.reparentTo(self.jewelryBag)
        self.inventoryPanelGold = InventoryUIGoldContainer.InventoryUIGoldContainer(self.inventoryUIManager, self.buttonSize, self.buttonSize)
        self.inventoryPanelGold.setPos(0.85, 0.0, -0.03)
        self.inventoryPanelGold.reparentTo(self)
        self.backTabParent = self.attachNewNode('backTabs')
        self.frontTabParent = self.attachNewNode('frontTab', sort=2)
        self.tabBar = None
        self.tabCount = 0
        for container in self.containerList:
            container.setPos(0.14, 0.0, 0.44)
            container.setX(0.54 - 0.5 * container.sizeX)
            container.setZ(1.2 - container.getTotalHeight())
            container.reparentTo(self)

        self.weaponBag.setZ(0.2)
        self.clothingBag.setPos(self.buttonSize * 2.0 + 0.03, 0.0, 0.2)
        self.jewelryBag.setPos(self.buttonSize * 3.0 + 0.04, 0.0, 0.21)
        self.ammoBag.setPos(self.buttonSize * 0.5 - 0.03, 0.0, 0.248)
        self.cardBag.setPos(self.buttonSize * 1.5 - 0.02, 0.0, self.buttonSize * 2.0)
        Gui = loader.loadModel('models/gui/char_gui')
        buttonImage = (Gui.find('**/chargui_text_block_large'), Gui.find('**/chargui_text_block_large_down'), Gui.find('**/chargui_text_block_large_over'), Gui.find('**/chargui_text_block_large'))
        self.redeemCodeButton = DirectButton(parent=self, relief=None, image=buttonImage, image_scale=0.45, text=PLocalizer.InventoryRedeemCode, text_font=PiratesGlobals.getInterfaceOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.68,
                                                                                                                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                                                                                                                      0.04), command=self.showRedeemCodeGUI)
        self.redeemCodeButton.hide()
        self.faceCameraButton = DirectButton(parent=self, relief=None, image=buttonImage, image_scale=0.45, text=PLocalizer.InventoryFaceCamera, text_font=PiratesGlobals.getInterfaceOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.37,
                                                                                                                                                                                                                                                                                                                                                                                      0,
                                                                                                                                                                                                                                                                                                                                                                                      0.04), command=self.faceCamera)
        self.faceCameraButton.hide()
        self.notLoadedWarning = DirectLabel(parent=self, relief=DGG.SUNKEN, borderWidth=(0,
                                                                                         0), frameColor=(0.5,
                                                                                                         0.15,
                                                                                                         0.05,
                                                                                                         1), text=PLocalizer.InventoryNotLoaded, text_align=TextNode.ALeft, text_font=PiratesGlobals.getInterfaceOutlineFont(), text_scale=0.045, text_fg=(1,
                                                                                                                                                                                                                                                           1,
                                                                                                                                                                                                                                                           1,
                                                                                                                                                                                                                                                           1), text_wordwrap=20.0, state=DGG.DISABLED, pos=(0.1,
                                                                                                                                                                                                                                                                                                            0,
                                                                                                                                                                                                                                                                                                            0.75))
        self.accept('openingContainer', self.onOpen)
        self.acceptOnce('localPirate-created', self.askInventory)
        self.accept('pickedUpItem', self.onLocatable)
        self.invRequestId = None
        return

    def faceCamera(self):
        if localAvatar.getGameState() not in ('Cannon', 'Fishing', 'ParlorGame'):
            if localAvatar.cameraFSM.fpsCamera.isAvFacingScreen():
                self.checkAction()
            else:
                localAvatar.cameraFSM.fpsCamera.avFaceScreen()
                self.acceptOnce('action', self.checkAction)

    def checkAction(self):
        self.ignore('action')
        localAvatar.cameraFSM.fpsCamera.avFaceCamera()

    def onLocatable(self, type):
        if not self.isHidden():
            if type == InventoryType.ItemTypeWeapon:
                self.openContainer(self.weaponBag)
            elif type == InventoryType.ItemTypeClothing:
                self.openContainer(self.clothingBag)
            elif type in [InventoryType.ItemTypeJewelry, InventoryType.ItemTypeTattoo]:
                self.openContainer(self.jewelryBag)

    def askInventory(self, args=None):
        self.invRequestId = DistributedInventoryBase.DistributedInventoryBase.getInventory(base.localAvatar.inventoryId, self.inventoryArrived)

    def inventoryArrived(self, inventory):
        if inventory == None:
            self.askInventory()
        else:
            self.prepInventroy()
        return

    def onOpen(self, container):
        self.openedContainer = container
        self.controlTrash(container)

    def controlTrash(self, container, force=None):
        if container in self.containerList or force != None:
            if container in self.containersToShowTrash or force:
                self.inventoryPanelTrash.reparentTo(container)
                self.inventoryPanelTrash.setPos(self, 0.07, 0.0, -0.03)
                self.inventoryPanelTrash.show()
                self.redeemCodeButton.show()
                self.faceCameraButton.show()
            else:
                self.inventoryPanelTrash.hide()
                self.redeemCodeButton.hide()
                self.faceCameraButton.hide()
            if container == self.potionBag:
                self.inventoryPanelDrinker.reparentTo(container)
                self.inventoryPanelDrinker.setPos(self, 0.3, 0.0, -0.03)
                self.inventoryPanelDrinker.show()
                self.faceCameraButton.hide()
            else:
                self.inventoryPanelDrinker.hide()
        return

    def addContainer(self, container, showTrash=1):
        self.containerList.append(container)
        if showTrash:
            self.containersToShowTrash.append(container)
        if container.containerType == CONTAINER_NORMAL:
            self.inventoryUIManager.addLocalStoreContainer(container)
        return container

    def prepInventroy(self):
        if self.notLoadedWarning:
            self.notLoadedWarning.remove()
            self.notLoadedWarning = None
        if not self.inventoryUIManager.discoveredInventory:
            self.inventoryUIManager.discoverLocatableInventory(self.weaponBag, self.clothingBag)
        return

    def show(self):
        if not self.isReady:
            self.isReady = 1
            gui = loader.loadModel('models/gui/toplevel_gui')
            goldCoin = gui.find('**/treasure_w_coin*')
            self.openContainer(self.containerList[0])
            if self.tabBar == None:
                self.tabBar = localAvatar.guiMgr.chestPanel.makeTabBar()
            else:
                self.tabBar.unstash()
            for container in self.containerList:
                self.createContainerTab(container)

            gui = loader.loadModel('models/gui/toplevel_gui')
            treasureIcon = gui.find('**/topgui_icon_treasure')
            treasureIcon.setScale(0.2)
            tab = self.createTabExtended(PLocalizer.InventoryPageTreasure, treasureIcon, treasureIcon, self.openTreasures, [])
            self.treasureTab = tab
        InventoryPage.InventoryPage.show(self)
        for container in self.containerList:
            if not container.isHidden():
                container.show()

        if self.tabBar:
            self.tabBar.unstash()
        self.inventoryUIManager.setLocalInventoryOpen(1)
        if self.openedContainer:
            localAvatar.guiMgr.chestPanel.setTitleName(self.openedContainer.titleName)
        if self.treasurePageReopen:
            self.openTreasures()
        return

    def openTreasures(self):
        localAvatar.guiMgr.chestPanel.setTitleName(PLocalizer.Treasure)
        self.closeAll()
        self.openedContainer = None
        self.treasurePageReopen = 1
        localAvatar.guiMgr.collectionMain.show()
        self.tabBar.selectTab(self.treasureTab.getName())
        self.controlTrash(None, force=0)
        return

    def closeTreasures(self):
        if hasattr(base, 'localAvatar'):
            base.localAvatar.guiMgr.collectionMain.hide()

    def closeAll(self):
        self.closeContainers()
        self.closeTreasures()
        self.inventoryPanelGold.hide()
        self.inventoryPanelTrash.hide()

    def openContainer(self, openContainer):
        localAvatar.guiMgr.chestPanel.setTitleName(openContainer.titleName)
        self.closeAll()
        openContainer.takeOut()
        openContainer.show()
        self.inventoryPanelGold.reparentTo(openContainer)
        self.inventoryPanelGold.setPos(self, 0.85, 0.0, -0.03)
        self.inventoryPanelGold.show()
        self.treasurePageReopen = 0

    def closeContainers(self):
        for container in self.containerList:
            container.hide()

    def createTabExtended(self, name, iconClosed, iconOpen, command, extraArgList):
        newTab = self.tabBar.addTab('My Tab %s' % self.tabCount, frameSize=(-0.12, 0.12, -0.11, 0.11), focusSize=(-0.12, 0.12, -0.12, 0.12), heightFactor=0.6, command=command, extraArgs=extraArgList)
        self.tabCount += 1
        image = iconClosed
        newTab.imageTag = DirectLabel(parent=newTab, relief=None, state=DGG.DISABLED, image=image, image_scale=image.getScale(), image_color=Vec4(0.8, 0.8, 0.8, 1), pos=(0,
                                                                                                                                                                          0,
                                                                                                                                                                          0))
        newTab.nameTag = DirectLabel(parent=newTab, relief=None, state=DGG.DISABLED, text=name, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ALeft, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getInterfaceFont(), pos=(0,
                                                                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                                                                       0))
        newTab.nameTag.setBin('gui-fixed', 1)
        newTab.nameTag.hide()

        def mouseOver(tab=newTab):
            tab.imageTag.setScale(1.1)
            tab.imageTag['image_color'] = Vec4(1, 1, 1, 1)
            base.playSfx(PiratesGuiGlobals.getDefaultRolloverSound())
            newTab.nameTag.show()

        def mouseOff(tab=newTab):
            if not tab['selected']:
                tab.imageTag.setScale(1.0)
                tab.imageTag['image_color'] = Vec4(0.8, 0.8, 0.8, 1)
            else:
                mouseOver(tab)
            newTab.nameTag.hide()

        newTab['mouseEntered'] = mouseOver
        newTab['mouseLeft'] = mouseOff
        return newTab

    def createContainerTab(self, container):
        self.createTabExtended(container.titleName, container.titleImageClosed, container.titleImageOpen, self.openContainer, [container])

    def hide(self):
        self.closeTreasures()
        InventoryPage.InventoryPage.hide(self)
        for container in self.containerList:
            container.putAway()

        self.inventoryUIManager.setLocalInventoryOpen(0)
        if self.tabBar:
            self.tabBar.stash()

    def destroy(self):
        self.weaponBag = None
        self.clothingBag = None
        self.jewelryBag = None
        self.potionBag = None
        self.cardBag = None
        self.ammoBag = None
        self.treasureTab = None
        self.openedContainer = None
        self.ignoreAll()
        self.containersToShowHotTrash = []
        if self.invRequestId:
            DistributedInventoryBase.DistributedInventoryBase.cancelGetInventory(self.invRequestId)
            self.invRequestId = None
        InventoryPage.InventoryPage.destroy(self)
        return

    def showRedeemCodeGUI(self):
        if localAvatar.getTutorialState() < PiratesGlobals.TUT_MET_JOLLY_ROGER:
            localAvatar.guiMgr.createWarning(PLocalizer.CannotRedeemYet, PiratesGuiGlobals.TextFG6, duration=8.0)
            return
        if self.redeemCodeGUI:
            self.redeemCodeGUI.showCode()
        else:
            self.redeemCodeGUI = RedeemCodeGUI.RedeemCodeGUI(self)