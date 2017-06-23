from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui.BorderFrame import BorderFrame
from pirates.ship import ShipGlobals
from pirates.ship import ShipBlueprints
from pirates.piratesbase import Freebooter
from pandac.PandaModules import TextureStage
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesbase import PiratesGlobals
from pirates.ship import ShipUpgradeGlobals
from pirates.economy import EconomyGlobals
from pirates.battle import WeaponGlobals
from pirates.inventory import InventoryGlobals
from pirates.piratesgui import ShipUpgradeConfirm
from pandac.PandaModules import NodePath, TextureStage, ModelNode, SceneGraphReducer, TextureAttrib, CullFaceAttrib, GeomNode, TransparencyAttrib, CullBinAttrib

class ShipUpgradeInterface(DirectFrame):

    def __init__(self, parent, **kw):
        gui = loader.loadModel('models/gui/pir_m_gui_frm_shipUpgrade2')
        DirectFrame.__init__(self, parent=parent, relief=None, pos=(0, 0, 0.0), scale=1.0)
        self.initialiseoptions(ShipUpgradeInterface)
        self.interface = gui
        self.interface.reparentTo(self)
        self.interface.setScale(0.32)
        spotsLeft = [
         self.interface.find('**/icon_frames_down/icon_frame_down1'), self.interface.find('**/icon_frames_down/icon_frame_down2'), self.interface.find('**/icon_frames_down/icon_frame_down3')]
        spotsMiddle = [self.interface.find('**/icon_frames_down1/icon_frame_down4'), self.interface.find('**/icon_frames_down1/icon_frame_down2'), self.interface.find('**/icon_frames_down1/icon_frame_down5')]
        spotsRight = [self.interface.find('**/icon_frames_down2/icon_frame_down1'), self.interface.find('**/icon_frames_down2/icon_frame_down2'), self.interface.find('**/icon_frames_down2/icon_frame_down3')]
        self.spotMarkers = [
         spotsLeft, spotsMiddle, spotsRight]
        self.choiceButtons = []
        self.ship = None
        self.shipModel = None
        self.shipId = None
        self.previewValue = None
        self.previewCat = 0
        self.pageCount = 0
        self.maxPageCount = 0
        self.pageMode = ''
        self.waitingForUpgrade = False
        self.viewingCurrent = False
        self.viewingDowngrade = False
        self.viewingSidegrade = False
        self.tooExpensive = False
        left = -0.57
        top = -0.34
        midV = -0.625
        bottom = -0.895
        midH = -0.0085
        right = 0.56
        superRight = 0.56
        self.arrowDict = {(0, 0): self.interface.find('**/arrows/downgrade_upper_arrow'),(0, 1): self.interface.find('**/arrows/downgrade_mid_arrow'),(0, 2): self.interface.find('**/arrows/downgrade_lower_arrow'),(1, 0): self.interface.find('**/arrows/sidegrade_upper_arrow'),(1, 1): None,(1, 2): self.interface.find('**/arrows/sidegrade_lower_arrow'),(2, 0): self.interface.find('**/arrows/upgrade_upper_arrow'),(2, 1): self.interface.find('**/arrows/upgrade_mid_arrow'),(2, 2): self.interface.find('**/arrows/Upgrade_lower_arrow')}
        self.upgradeLine = self.interface.find('**/arrows/upgrade_line')
        self.downgradeLine = self.interface.find('**/arrows/downgrade_line')
        self.spotDict = {0: [],1: [1],2: [0, 2],3: [0, 1, 2]}
        self.buttonPostions = [
         [
          (
           left, 0, top), (left, 0, midV), (left, 0, bottom)], [(midH, 0, top), (midH, 0, midV), (midH, 0, bottom)], [(right, 0, top), (superRight, 0, midV), (right, 0, bottom)]]
        self.callback = None
        self.descriptionString = ''
        self.costString = ''
        self.attributeString = ''
        self.ownedString = ''
        self.currencyIconDict = None
        self.hullDetailIconDict = None
        self.broadsideIconDict = None
        self.sailSkillIconDict = None
        self.confirmPanel = None
        self.broadsideIdList = [
         InventoryType.CannonThunderbolt, InventoryType.CannonFury, InventoryType.CannonChainShot, InventoryType.CannonGrapeShot, InventoryType.CannonExplosive, InventoryType.CannonFirebrand]
        self.sailSkillList = [
         InventoryType.SailFullSail, InventoryType.SailTakeCover, InventoryType.SailOpenFire]
        self.setupGui()
        self.hide()
        base.sui = self
        return

    def destroy(self):
        self.choiceButtons = []
        self.currencyLabels = []
        self.upgradeLine = None
        self.downgradeLine = None
        self.currencyIconDict = None
        self.hullDetailIconDict = None
        self.broadsideIconDict = None
        self.sailSkillIconDict = None
        self.interface.removeNode()
        self.interface = None
        DirectFrame.destroy(self)
        return

    def setupGui(self):
        self.currencyIconDict = {}
        skillIcons = loader.loadModel('models/textureCards/skillIcons')
        MaterialIcons = loader.loadModel('models/textureCards/shipMaterialIcons')
        topGuiIcons = loader.loadModel('models/gui/toplevel_gui')
        tpMgr = TextPropertiesManager.getGlobalPtr()
        for currencyId in ShipUpgradeGlobals.COST_LIST:
            if currencyId == InventoryType.ItemTypeMoney:
                currencyIcon = topGuiIcons.find('**/treasure_w_coin*')
                currencyIcon.setScale(7.0)
            else:
                currencyIcon = MaterialIcons.find('**/%s' % EconomyGlobals.getItemIcons(currencyId))
                currencyIcon.setScale(1.8)
            iconKey = 'currency-%s' % currencyId
            self.currencyIconDict[currencyId] = currencyIcon
            tg = TextGraphic(currencyIcon, -0.25, 0.75, -0.31, 0.69)
            tpMgr.setGraphic(iconKey, tg)

        self.broadsideIconDict = {}
        for broadsideId in self.broadsideIdList:
            ammoIconName = WeaponGlobals.getSkillIcon(broadsideId)
            broadsideIcon = skillIcons.find('**/%s' % ammoIconName)
            iconKey = 'broadside-%s' % broadsideId
            self.broadsideIconDict[broadsideId] = broadsideIcon
            tg = TextGraphic(broadsideIcon, -0.25, 0.75, -0.31, 0.69)
            tpMgr.setGraphic(iconKey, tg)

        self.sailSkillIconDict = {}
        for sailSkillId in self.sailSkillList:
            ammoIconName = WeaponGlobals.getSkillIcon(sailSkillId)
            sailSkillIcon = skillIcons.find('**/%s' % ammoIconName)
            sailSkillIcon.setScale(2.0)
            iconKey = 'sailSkill-%s' % sailSkillId
            self.sailSkillIconDict[sailSkillId] = sailSkillIcon
            tg = TextGraphic(sailSkillIcon, -0.25, 0.75, -0.31, 0.69)
            tpMgr.setGraphic(iconKey, tg)

        self.hullDetailIconDict = {}
        buffCard = loader.loadModel('models/textureCards/buff_icons')
        inventoryGui = loader.loadModel('models/gui/gui_icons_inventory')
        armorIcon = buffCard.find('**/sail_take_cover')
        armorIcon.setScale(2.0)
        self.hullDetailIconDict['armor'] = armorIcon
        tg = TextGraphic(armorIcon, -0.25, 0.75, -0.31, 0.69)
        iconKey = 'dtl-armor'
        tpMgr.setGraphic(iconKey, tg)
        speedIcon = buffCard.find('**/sail_full_sail')
        speedIcon.setScale(2.0)
        self.hullDetailIconDict['speed'] = speedIcon
        tg = TextGraphic(speedIcon, -0.25, 0.75, -0.31, 0.69)
        iconKey = 'dtl-speed'
        tpMgr.setGraphic(iconKey, tg)
        turningIcon = buffCard.find('**/sail_come_about')
        turningIcon.setScale(2.0)
        self.hullDetailIconDict['speed'] = turningIcon
        tg = TextGraphic(turningIcon, -0.25, 0.75, -0.31, 0.69)
        iconKey = 'dtl-turning'
        tpMgr.setGraphic(iconKey, tg)
        cargoIcon = inventoryGui.find('**/pir_t_ico_trs_chest_01*')
        cargoIcon.setScale(2.0)
        self.hullDetailIconDict['cargo'] = cargoIcon
        tg = TextGraphic(cargoIcon, -0.25, 0.75, -0.31, 0.69)
        iconKey = 'dtl-cargo'
        tpMgr.setGraphic(iconKey, tg)
        self.logoLayerInv = TextureStage('logoInverse')
        self.logoLayerInv.setSort(1)
        self.logoLayerInv.setCombineRgb(TextureStage.CMReplace, TextureStage.CSTexture, TextureStage.COOneMinusSrcColor)
        self.logoLayerInv.setCombineAlpha(TextureStage.CMReplace, TextureStage.CSTexture, TextureStage.COSrcAlpha)
        Gui = loader.loadModel('models/gui/toplevel_gui')
        generic_x = Gui.find('**/generic_x')
        generic_box = Gui.find('**/generic_box')
        generic_box_over = Gui.find('**/generic_box_over')
        self.closeButton = DirectButton(parent=self, relief=None, pos=(1.28, 0, 0.67), scale=0.38, geom=generic_x, image=(generic_box, generic_box, generic_box_over, generic_box), image_scale=0.7, text='', textMayChange=1, command=self.close)
        buttonImage = (
         Gui.find('**/generic_button'), Gui.find('**/generic_button_down'), Gui.find('**/generic_button_over'), Gui.find('**/generic_button_disabled'))
        model = loader.loadModel('models/gui/avatar_chooser_rope')
        selectImage = (model.find('**/avatar_c_B_bottom'), model.find('**/avatar_c_B_bottom'), model.find('**/avatar_c_B_bottom_over'))
        self.confirmButton = DirectButton(parent=self, relief=None, image=selectImage, image_scale=(0.4,
                                                                                                    1.0,
                                                                                                    0.27), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text=PLocalizer.UpgradePurchaseConfirm, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(1.01, 0, -0.82), state=DGG.DISABLED, command=self.confirmPurchase)
        self.showNextButton = DirectButton(parent=self, relief=None, image=selectImage, image_scale=(0.15,
                                                                                                     1.0,
                                                                                                     0.25), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text=PLocalizer.UpgradeShowNext, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.5, 0, -0.95), state=DGG.NORMAL, command=self.showNext)
        self.showNextButton.hide()
        self.showPrevButton = DirectButton(parent=self, relief=None, image=selectImage, image_scale=(0.15,
                                                                                                     1.0,
                                                                                                     0.25), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text=PLocalizer.UpgradeShowPrev, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.275, 0, -0.95), state=DGG.NORMAL, command=self.showPrev)
        self.showPrevButton.hide()
        self.title = DirectLabel(parent=self, relief=None, text=PLocalizer.UpgradeTitle, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleTitleSmall, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.23,
                                                                                                                                                                                                                                                                                                               0,
                                                                                                                                                                                                                                                                                                               0.69), textMayChange=1)
        self.upgradeLineTitle = DirectLabel(parent=self.upgradeLine, relief=None, text=PLocalizer.UpgradeLineTitle, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.8,
                                                                                                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                                                                                                     -1.8), textMayChange=0, scale=3.5)
        self.downgradeLineTitle = DirectLabel(parent=self.downgradeLine, relief=None, text=PLocalizer.DowngradeLineTitle, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(-0.8, 0, -1.8), textMayChange=0, scale=3.5)
        self.previewTitle = DirectLabel(parent=self, relief=None, text='', text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.98,
                                                                                                                                                                                                                                                                                            0,
                                                                                                                                                                                                                                                                                            0.53), textMayChange=1)
        self.attributeList = DirectLabel(parent=self, relief=None, text='', text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=14, pos=(0.75,
                                                                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                                                                             0.45), textMayChange=1)
        self.ownedResourceList = DirectLabel(parent=self, relief=None, text='', text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ARight, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG1, text_shadow=PiratesGuiGlobals.TextShadow, pos=(1.27,
                                                                                                                                                                                                                                                                                                0,
                                                                                                                                                                                                                                                                                                0.45), textMayChange=1)
        self.selectHullButton = DirectButton(parent=self, relief=None, image=selectImage, image_scale=(0.22,
                                                                                                       1.0,
                                                                                                       0.22), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text=PLocalizer.UpgradeTypeHull, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(-0.457, 0, 0.51), state=DGG.NORMAL, command=self.layoutButtons, extraArgs=[0])
        self.selectRiggingButton = DirectButton(parent=self, relief=None, image=selectImage, image_scale=(0.22,
                                                                                                          1.0,
                                                                                                          0.22), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text=PLocalizer.UpgradeTypeRigging, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(-0.457, 0, 0.42), state=DGG.NORMAL, command=self.layoutButtons, extraArgs=[1])
        self.selectPatternButton = DirectButton(parent=self, relief=None, image=selectImage, image_scale=(0.22,
                                                                                                          1.0,
                                                                                                          0.22), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text=PLocalizer.UpgradeTypePattern, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(-0.457, 0, 0.332), state=DGG.NORMAL, command=self.layoutButtons, extraArgs=[2])
        self.selectLogoButton = DirectButton(parent=self, relief=None, image=selectImage, image_scale=(0.22,
                                                                                                       1.0,
                                                                                                       0.22), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text=PLocalizer.UpgradeTypeLogo, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(-0.457, 0, 0.245), state=DGG.NORMAL, command=self.layoutButtons, extraArgs=[3])
        self.selectExitButton = DirectButton(parent=self, relief=None, image=selectImage, image_scale=(0.22,
                                                                                                       1.0,
                                                                                                       0.22), image0_color=VBase4(0.65, 0.65, 0.65, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(0.9, 0.9, 0.9, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text=PLocalizer.UpgradeTypeExit, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.01), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(-0.457, 0, 0.155), state=DGG.NORMAL, command=self.close)
        self.currencyLabels = []
        ciXPos = -0.45
        ciZPos = -0.98
        ciXSpace = 0.17
        ciCount = 0
        shipIcons = loader.loadModel('models/gui/gui_icons_weapon')
        blankImage = shipIcons.find('**/pir_t_gui_frm_inventoryBox')
        return

    def updateCurrencyLabels(self, info=None):
        inv = localAvatar.getInventory()
        if inv:
            for currencyLabel in self.currencyLabels:
                currencyId = currencyLabel.currencyId
                if currencyId == InventoryType.ItemTypeMoney:
                    currencyName = PLocalizer.MoneyName
                    currencyAmount = inv.getGoldInPocket()
                else:
                    currencyName = PLocalizer.InventoryTypeNames.get(currencyId, 'Unknown Currency')
                    currencyAmount = inv.getStackQuantity(currencyId)
                currencyLabel['text'] = '%s\n%s' % (currencyName, currencyAmount)

            self.filloutOwned()
            self.filloutAttributeText()

    def layoutButtons(self, category=0):
        if self.confirmPanel:
            return
        self.costString = ''
        self.attributeString = ''
        self.filloutAttributeText()
        self.previewCat = category
        self.previewChange(self.shipId, changeCat=self.previewCat, changeValue=None)
        for column in self.spotMarkers:
            for marker in column:
                if marker:
                    marker.hide()

        for arrowKey in self.arrowDict:
            if self.arrowDict[arrowKey]:
                self.arrowDict[arrowKey].hide()

        self.showNextButton.hide()
        self.showPrevButton.hide()
        self.pageCount = 0
        self.maxPageCount = 0
        self.pageMode = ''
        self.upgradeLine.hide()
        self.downgradeLine.hide()
        if category == None:
            category = 0
        if category == 0:
            self.layOutHullButtons()
            self.title['text'] = PLocalizer.UpgradeTypeHull
        elif category == 1:
            self.layOutRiggingButtons()
            self.title['text'] = PLocalizer.UpgradeTypeRigging
        elif category == 2:
            self.layOutPatternButtons()
            self.title['text'] = PLocalizer.UpgradeTypePattern
        elif category == 3:
            self.layOutLogoButtons()
            self.title['text'] = PLocalizer.UpgradeTypeLogo
        return

    def layOutHullButtons(self):
        self.clearButtons()
        self.pageMode = 'Hulls'
        shipOV = base.cr.getOwnerView(self.shipId)
        shipHullType = shipOV.customHull
        if not shipHullType:
            shipHullType = 1
        shipHullInfo = ShipUpgradeGlobals.HULL_TYPES.get(shipHullType)
        currentShipButton = self.makeHullButton(shipHullType, isCurrentType=True)
        currentShipButton.reparentTo(self)
        spotPosition = self.buttonPostions[1][1]
        self.spotMarkers[1][1].show()
        currentShipButton.setPos(spotPosition)
        self.choiceButtons.append(currentShipButton)
        for downgradeOptionIndex in range(3):
            downgrade = shipHullInfo['Downgrades'][downgradeOptionIndex]
            if downgrade != None:
                downgradeInfo = ShipUpgradeGlobals.HULL_TYPES.get(downgrade)
                if downgradeInfo['Available']:
                    downgradeButton = self.makeHullButton(downgrade, current=0, downgrade=True)
                    spotIndex = downgradeOptionIndex
                    spotPosition = self.buttonPostions[0][spotIndex]
                    downgradeButton.reparentTo(self)
                    downgradeButton.setPos(spotPosition)
                    self.choiceButtons.append(downgradeButton)
                    self.spotMarkers[0][spotIndex].show()
                    self.arrowDict[0, spotIndex].show()
                    self.downgradeLine.show()

        for sidegradeOptionIndex in range(2):
            sidegrade = shipHullInfo['Sidegrades'][sidegradeOptionIndex]
            if sidegrade != None:
                sidegradeInfo = ShipUpgradeGlobals.HULL_TYPES.get(sidegrade)
                if sidegradeInfo['Available']:
                    sidegradeButton = self.makeHullButton(sidegrade, current=0, downgrade=False, sidegrade=True)
                    spotIndex = sidegradeOptionIndex
                    if spotIndex == 1:
                        spotIndex = 2
                    spotPosition = self.buttonPostions[1][spotIndex]
                    sidegradeButton.reparentTo(self)
                    sidegradeButton.setPos(spotPosition)
                    self.choiceButtons.append(sidegradeButton)
                    self.spotMarkers[1][spotIndex].show()
                    self.arrowDict[1, spotIndex].show()

        for upgradeOptionIndex in range(3):
            upgrade = shipHullInfo['Upgrades'][upgradeOptionIndex]
            if upgrade != None:
                upgradeInfo = ShipUpgradeGlobals.HULL_TYPES.get(upgrade)
                if upgradeInfo['Available']:
                    upgradeButton = self.makeHullButton(upgrade, current=0)
                    spotIndex = upgradeOptionIndex
                    spotPosition = self.buttonPostions[2][spotIndex]
                    upgradeButton.reparentTo(self)
                    upgradeButton.setPos(spotPosition)
                    self.choiceButtons.append(upgradeButton)
                    self.spotMarkers[2][spotIndex].show()
                    self.arrowDict[2, spotIndex].show()
                    self.upgradeLine.show()

        return

    def layOutRiggingButtons(self):
        self.clearButtons()
        self.pageMode = 'Rigging'
        shipOV = base.cr.getOwnerView(self.shipId)
        shipRiggingType = shipOV.customRigging
        if not shipRiggingType:
            shipRiggingType = ShipUpgradeGlobals.RIGGING_BASE
        shipRiggingInfo = ShipUpgradeGlobals.RIGGING_TYPES.get(shipRiggingType)
        currentShipButton = self.makeRiggingButton(shipRiggingType, isCurrentType=True)
        currentShipButton.reparentTo(self)
        spotPosition = self.buttonPostions[1][1]
        self.spotMarkers[1][1].show()
        currentShipButton.setPos(spotPosition)
        self.choiceButtons.append(currentShipButton)
        for downgradeOptionIndex in range(3):
            downgrade = shipRiggingInfo['Downgrades'][downgradeOptionIndex]
            if downgrade != None:
                downgradeInfo = ShipUpgradeGlobals.RIGGING_TYPES.get(downgrade)
                if downgradeInfo['Available']:
                    downgradeButton = self.makeRiggingButton(downgrade, current=0, downgrade=True)
                    spotIndex = downgradeOptionIndex
                    spotPosition = self.buttonPostions[0][spotIndex]
                    downgradeButton.reparentTo(self)
                    downgradeButton.setPos(spotPosition)
                    self.choiceButtons.append(downgradeButton)
                    self.spotMarkers[0][spotIndex].show()
                    self.arrowDict[0, spotIndex].show()
                    self.downgradeLine.show()

        for sidegradeOptionIndex in range(2):
            sidegrade = shipRiggingInfo['Sidegrades'][sidegradeOptionIndex]
            if sidegrade != None:
                sidegradeInfo = ShipUpgradeGlobals.RIGGING_TYPES.get(sidegrade)
                if sidegradeInfo['Available']:
                    sidegradeButton = self.makeRiggingButton(sidegrade, current=0, downgrade=False, sidegrade=True)
                    spotIndex = sidegradeOptionIndex
                    if spotIndex == 1:
                        spotIndex = 2
                    spotPosition = self.buttonPostions[1][spotIndex]
                    sidegradeButton.reparentTo(self)
                    sidegradeButton.setPos(spotPosition)
                    self.choiceButtons.append(sidegradeButton)
                    self.spotMarkers[1][spotIndex].show()
                    self.arrowDict[1, spotIndex].show()

        for upgradeOptionIndex in range(3):
            upgrade = shipRiggingInfo['Upgrades'][upgradeOptionIndex]
            if upgrade != None:
                upgradeInfo = ShipUpgradeGlobals.RIGGING_TYPES.get(upgrade)
                if upgradeInfo['Available']:
                    upgradeButton = self.makeRiggingButton(upgrade, current=0)
                    spotIndex = upgradeOptionIndex
                    spotPosition = self.buttonPostions[2][spotIndex]
                    upgradeButton.reparentTo(self)
                    upgradeButton.setPos(spotPosition)
                    self.choiceButtons.append(upgradeButton)
                    self.spotMarkers[2][spotIndex].show()
                    self.arrowDict[2, spotIndex].show()
                    self.upgradeLine.show()

        return

    def showNext(self):
        self.pageCount += 1
        if self.pageCount > self.maxPageCount:
            self.pageCount = 0
        if self.pageMode == 'Logo':
            self.layOutLogoButtons()
        elif self.pageMode == 'Sail':
            self.layOutPatternButtons()

    def showPrev(self):
        self.pageCount -= 1
        if self.pageCount < 0:
            self.pageCount = self.maxPageCount
        if self.pageMode == 'Logo':
            self.layOutLogoButtons()
        elif self.pageMode == 'Sail':
            self.layOutPatternButtons()

    def layOutPatternButtons(self):
        self.clearButtons()
        self.pageMode = 'Sail'
        shipOV = base.cr.getOwnerView(self.shipId)
        shipPatternType = shipOV.customSailPattern
        if not shipPatternType:
            shipPatternType = ShipUpgradeGlobals.SAILCOLOR_BASE
        shipPattenInfo = ShipUpgradeGlobals.SAILCOLOR_TYPES.get(shipPatternType)
        offX = 0.225
        offY = -0.21
        countX = 0
        countY = 0
        startX = -0.57
        startY = -0.35
        sailTypeList = ShipUpgradeGlobals.SAILCOLOR_TYPES.keys()
        sailTypeList.sort()
        for iconInfoKey in sailTypeList:
            if ShipUpgradeGlobals.SAILCOLOR_TYPES[iconInfoKey].get('Available', 0):
                patternButton = self.makePatternButton(iconInfoKey)
                patternButton.setPos(startX + countX * offX, 0, startY + countY * offY)
                self.choiceButtons.append(patternButton)
                countX += 1
                if countX >= 6:
                    countX = 0
                    countY += 1

    def layOutLogoButtons(self):
        self.clearButtons()
        self.pageMode = 'Logo'
        shipOV = base.cr.getOwnerView(self.shipId)
        shipLogoType = shipOV.customSailLogo
        if not shipLogoType:
            shipLogoType = ShipUpgradeGlobals.LOGO_BASE
        shipLogoInfo = ShipUpgradeGlobals.LOGO_TYPES.get(shipLogoType)
        offX = 0.225
        offY = -0.21
        countX = 0
        countY = 0
        startX = -0.57
        startY = -0.35
        logoTypeList = ShipUpgradeGlobals.LOGO_TYPES.keys()
        logoTypeList.sort()
        numIcons = len(logoTypeList)
        numIconsShown = 18
        startIndex = self.pageCount * numIconsShown
        self.maxPageCount = numIcons / numIconsShown
        if numIcons > numIconsShown:
            self.showNextButton.show()
            self.showPrevButton.show()
        countPlaced = 0
        countConsidered = startIndex
        considerIndex = 0
        placedIndex = 0
        for countLogos in range(0, numIcons):
            if considerIndex >= numIcons:
                print 'break'
                break
            iconInfoKey = logoTypeList[considerIndex]
            considerIndex += 1
            if ShipUpgradeGlobals.LOGO_TYPES[iconInfoKey].get('Available', 0):
                if placedIndex >= startIndex and placedIndex < startIndex + numIconsShown:
                    logoButton = self.makeLogoButton(iconInfoKey)
                    logoButton.setPos(startX + countX * offX, 0, startY + countY * offY)
                    self.choiceButtons.append(logoButton)
                    countX += 1
                    if countX >= 6:
                        countX = 0
                        countY += 1
                placedIndex += 1

    def makePatternButton(self, patternType, current=1):
        shipPatternInfo = ShipUpgradeGlobals.SAILCOLOR_TYPES.get(patternType)
        model = loader.loadModel('models/textureCards/sailColors.bam')
        patternName = ShipBlueprints.ColorDict.get(shipPatternInfo['StyleIndex'])
        if patternName == None:
            shipIcons = loader.loadModel('models/gui/gui_icons_weapon')
            buttonImage = shipIcons.find('**/pir_t_gui_frm_inventoryBox')
        else:
            buttonImage = model.find('**/%s' % patternName)
        command = self.previewChange
        extraArgs = [self.shipId, 2, patternType]
        patternButton = DirectButton(parent=self, relief=None, image=buttonImage, image_scale=(0.16,
                                                                                               1.0,
                                                                                               0.16), image0_color=VBase4(0.85, 0.85, 0.85, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(1.0, 1.0, 1.0, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text=shipPatternInfo['Name'], text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.11), text_scale=PiratesGuiGlobals.TextScaleMed, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        0.0), command=command, extraArgs=extraArgs)
        return patternButton

    def makeLogoButton(self, logoType, current=1):
        shipLogoInfo = ShipUpgradeGlobals.LOGO_TYPES.get(logoType)
        model = loader.loadModel('models/textureCards/sailLogo.bam')
        logoName = ShipBlueprints.LogoDict.get(shipLogoInfo['StyleIndex'])
        invert = shipLogoInfo['Invert']
        shipIcons = loader.loadModel('models/gui/gui_icons_weapon')
        blankImage = shipIcons.find('**/pir_t_gui_frm_inventoryBox')
        needInvert = 0
        logoNode = None
        if logoName == None:
            buttonImage = blankImage
            buttonGeom = None
        else:
            buttonImage = blankImage
            buttonGeom = model.find('**/%s' % logoName)
            logoTex = buttonGeom.findAllTextures('*')[0]
            if invert:
                needInvert = 1
        command = self.previewChange
        extraArgs = [self.shipId, 3, logoType]
        logoButton = DirectButton(parent=self, relief=None, image=buttonImage, image_scale=(0.16,
                                                                                            1.0,
                                                                                            0.16), image0_color=VBase4(0.85, 0.85, 0.85, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(1.0, 1.0, 1.0, 1), image3_color=VBase4(0.41, 0.4, 0.4, 1), text=shipLogoInfo['Name'], text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.11), text_scale=PiratesGuiGlobals.TextScaleMed, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  0.0), command=command, extraArgs=extraArgs)
        if buttonGeom:
            logoNode = logoButton.attachNewNode('Logo Display')
            buttonGeom.instanceTo(logoNode)
            buttonGeom.setScale(0.16)
        if needInvert:
            buttonGeom.setTextureOff(TextureStage.getDefault())
            buttonGeom.setTexture(self.logoLayerInv, logoTex)
            self.thing = buttonGeom
        return logoButton

    def makeHullButton(self, hullType, current=1, downgrade=False, sidegrade=False, isCurrentType=False):
        shipIcons = loader.loadModel('models/gui/gui_icons_weapon')
        buttonImage = shipIcons.find('**/pir_t_ico_knf_belt')
        UpgradeIcons = loader.loadModel('models/textureCards/shipUpgradeIcons')
        shipHullInfo = ShipUpgradeGlobals.HULL_TYPES.get(hullType)
        imageScale = 0.2
        if shipHullInfo.get('Icon', None):
            buttonImage = UpgradeIcons.find('**/%s' % shipHullInfo['Icon'])
            imageScale = 0.13
        command = self.previewChange
        extraArgs = [self.shipId, 0, hullType, downgrade, sidegrade]
        text = shipHullInfo['IconText']
        textColor = PiratesGuiGlobals.TextFG1
        textSize = PiratesGuiGlobals.TextScaleLarge
        shipButton = DirectButton(parent=self, relief=None, image=buttonImage, image_scale=imageScale, image0_color=VBase4(0.8, 0.8, 0.8, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(1.0, 1.0, 1.0, 1), image3_color=VBase4(0.4, 0.4, 0.4, 1), text=text, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0.055, -0.065), text_scale=textSize, text_fg=textColor, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 0.0), command=command, extraArgs=extraArgs)
        if isCurrentType:
            currentLabel = DirectLabel(parent=shipButton, relief=None, text=PLocalizer.YourCurrent, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0, -0.11), text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow)
        return shipButton

    def makeRiggingButton(self, riggingType, current=1, downgrade=False, sidegrade=False, isCurrentType=False):
        shipRiggingInfo = ShipUpgradeGlobals.RIGGING_TYPES.get(riggingType)
        if shipRiggingInfo.get('Icon', None):
            skillIcons = loader.loadModel('models/textureCards/skillIcons')
            buttonImage = skillIcons.find('**/%s' % shipRiggingInfo['Icon'])
            imageScale = 0.13
        else:
            UpgradeIcons = loader.loadModel('models/textureCards/shipUpgradeIcons')
            buttonImage = UpgradeIcons.find('**/pir_t_gui_shp_basic')
            imageScale = 0.13
        command = self.previewChange
        extraArgs = [self.shipId, 1, riggingType, downgrade, sidegrade]
        text = shipRiggingInfo.get('IconText', '-')
        textColor = PiratesGuiGlobals.TextFG1
        textSize = PiratesGuiGlobals.TextScaleMed
        if isCurrentType:
            text = PLocalizer.YourCurrent
            textColor = PiratesGuiGlobals.TextFG2
            textSize = PiratesGuiGlobals.TextScaleExtraLarge
        riggingButton = DirectButton(parent=self, relief=None, image=buttonImage, image_scale=imageScale, image0_color=VBase4(0.8, 0.8, 0.8, 1), image1_color=VBase4(0.4, 0.4, 0.4, 1), image2_color=VBase4(1.0, 1.0, 1.0, 1), image3_color=VBase4(0.4, 0.4, 0.4, 1), text=text, text_font=PiratesGlobals.getPirateBoldOutlineFont(), text_align=TextNode.ACenter, text_pos=(0.055, -0.065), text_scale=textSize, text_fg=textColor, text_shadow=PiratesGuiGlobals.TextShadow, pos=(0.0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    0.0), command=command, extraArgs=extraArgs)
        return riggingButton

    def filloutCosts(self, shipClass, costDict=None):
        downgrade = self.viewingDowngrade
        self.tooExpensive = False
        inv = localAvatar.getInventory()
        if downgrade:
            self.costString = ''
            self.ownedString = ''
        elif costDict == None or inv == None:
            self.costString = ''
            self.ownedString = ''
        else:
            costString = PLocalizer.ShipUgradeCosts + '\n' + PLocalizer.ShipUgradeCostsRequired + '\n\n'
            ownedString = '\n' + PLocalizer.ShipUgradeCostsOwned + '\n\n'
            for currency in ShipUpgradeGlobals.COST_LIST:
                fixedCost = 0
                relativeCost = 0
                if costDict.get('Fixed'):
                    if costDict['Fixed'].get(currency, 0):
                        fixedCost = costDict['Fixed'].get(currency, 0)
                if costDict.get('Relative'):
                    if costDict['Relative'].get(currency, 0):
                        relativeCost = ShipUpgradeGlobals.HULL_RELATIVE_COST_BASIS[shipClass] * costDict['Relative'].get(currency, 0)
                totalCost = int(fixedCost + relativeCost)
                if currency == InventoryType.ItemTypeMoney:
                    currencyName = PLocalizer.MoneyName
                    currencyAmount = inv.getGoldInPocket()
                else:
                    currencyName = PLocalizer.InventoryTypeNames.get(currency, 'Unknown Currency')
                    currencyAmount = inv.getStackQuantity(currency)
                if totalCost:
                    shortResouce = False
                    currencyString = '%s: %s' % (currencyName, totalCost)
                    if currencyAmount >= totalCost:
                        pass
                    else:
                        shortResouce = True
                        self.tooExpensive = True
                    costString += '\x05currency-%s\x05 ' % currency + currencyString + '\n\n'
                    if shortResouce:
                        ownedString += '\x01red\x01%s\x02\n\n' % currencyAmount
                    else:
                        ownedString += '%s\n\n' % currencyAmount

            self.costString = costString
        return

    def filloutOwned(self):
        downgrade = self.viewingDowngrade
        costDict = None
        inv = localAvatar.getInventory()
        if self.previewValue != None and self.previewCat != None and not self.viewingCurrent and not self.viewingDowngrade:
            typeDict = ShipUpgradeGlobals.UPGRADE_BY_CATINDEX.get(self.previewCat, {}).get(self.previewValue, {})
            if typeDict:
                costDict = typeDict.get('Cost', None)
        if costDict and self.ship and inv:
            ownedString = '\n' + PLocalizer.ShipUgradeCostsOwned + '\n\n'
            for currency in ShipUpgradeGlobals.COST_LIST:
                fixedCost = 0
                relativeCost = 0
                if costDict.get('Fixed'):
                    if costDict['Fixed'].get(currency, 0):
                        fixedCost = costDict['Fixed'].get(currency, 0)
                if costDict.get('Relative'):
                    if costDict['Relative'].get(currency, 0):
                        relativeCost = ShipUpgradeGlobals.HULL_RELATIVE_COST_BASIS[self.ship.shipClass] * costDict['Relative'].get(currency, 0)
                totalCost = int(fixedCost + relativeCost)
                if currency == InventoryType.ItemTypeMoney:
                    currencyName = PLocalizer.MoneyName
                    currencyAmount = inv.getGoldInPocket()
                else:
                    currencyAmount = inv.getStackQuantity(currency)
                if totalCost:
                    shortResouce = False
                    if currencyAmount >= totalCost:
                        pass
                    else:
                        shortResouce = True
                        self.tooExpensive = True
                    if shortResouce:
                        ownedString += '\x01red\x01%s\x02\n\n' % currencyAmount
                    else:
                        ownedString += '%s\n\n' % currencyAmount

        else:
            ownedString = ''
        self.ownedString = ownedString
        return

    def filloutPatternDetails(self, patternInfo=None, oldPatternInfo=None):
        showOld = 0
        self.attributeString = ''
        if oldPatternInfo != None and patternInfo == None:
            showOld = 1
            patternInfo = oldPatternInfo
        return

    def filloutRiggingDetails(self, riggingInfo=None, oldRiggingInfo=None):
        showOld = 0
        self.attributeString = ''
        boostString = ''
        if oldRiggingInfo != None and riggingInfo == None:
            showOld = 1
            riggingInfo = oldRiggingInfo
        boostInfo = riggingInfo['SkillBoosts']
        if boostInfo:
            self.attributeString = PLocalizer.ShipUpgradeSkillBoosts + '\n\n'
        for skillId in boostInfo.keys():
            skillLevel = boostInfo[skillId]
            skillName = PLocalizer.InventoryTypeNames[skillId]
            newAttributeLine = '\x05sailSkill-%s\x05 %s %s %s\n\n' % (skillId, skillName, PLocalizer.ShipUpgradeSkillBoostAdd, skillLevel)
            boostString += newAttributeLine

        self.attributeString += boostString
        return

    def filloutHullDetails(self, hullInfo=None, oldHullInfo=None):
        showOld = 0
        if oldHullInfo != None and hullInfo == None:
            showOld = 1
            hullInfo = oldHullInfo
        armorLine = ''
        speedLine = ''
        turningLine = ''
        cargoLine = ''
        broadsideLine = ''
        headingLine = ''
        if hullInfo and oldHullInfo:
            headingLine = hullInfo['Description']
            newArmor = hullInfo['Armor']
            oldArmor = oldHullInfo['Armor']
            diffArmor = int(newArmor * 100.0) - int(oldArmor * 100.0)
            newArmorP = int(newArmor * 100)
            armorText = ''
            if diffArmor == 0:
                armorText = ''
            else:
                if diffArmor >= 0:
                    armorText = '\x01green\x01+%s%%\x02' % diffArmor
                    signArmor = '+'
                else:
                    armorText = '\x01red\x01%s%%\x02' % diffArmor
                    signArmor = ''
                armorIconLine = '\x05dtl-armor\x05 '
                armorLine = armorIconLine + '%s: %s%% %s\n\n' % (PLocalizer.ShipUpgradeAttributeArmor, newArmorP, armorText)
                newSpeed = hullInfo['Speed']
                oldSpeed = oldHullInfo['Speed']
                diffSpeed = int(newSpeed * 100.0) - int(oldSpeed * 100.0)
                newSpeedP = int(newSpeed * 100)
                speedText = ''
                if diffSpeed == 0:
                    speedText = ''
                else:
                    if diffSpeed >= 0:
                        speedText = '\x01green\x01+%s%%\x02' % diffSpeed
                        signSpeed = '+'
                    else:
                        speedText = '\x01red\x01%s%%\x02' % diffSpeed
                        signSpeed = ''
                    speedIconLine = '\x05dtl-speed\x05 '
                    speedLine = speedIconLine + '%s: %s%% %s\n\n' % (PLocalizer.ShipUpgradeAttributeSpeed, newSpeedP, speedText)
                    newTurning = hullInfo['Turning']
                    oldTurning = oldHullInfo['Turning']
                    diffTurning = int(newTurning * 100.0) - int(oldTurning * 100.0)
                    newTurningP = int(newTurning * 100)
                    turningText = ''
                    if diffTurning == 0:
                        turningText = ''
                    elif diffTurning >= 0:
                        turningText = '\x01green\x01+%s%%\x02' % diffTurning
                        signTurning = '+'
                    else:
                        turningText = '\x01red\x01%s%%\x02' % diffTurning
                        signTurning = ''
                    turningIconLine = '\x05dtl-turning\x05 '
                    turningLine = turningIconLine + '%s: %s%% %s\n\n' % (PLocalizer.ShipUpgradeAttributeTurning, newTurningP, turningText)
                    newCargo = hullInfo['Cargo']
                    oldCargo = oldHullInfo['Cargo']
                    diffCargo = int(newCargo * 100.0) - int(oldCargo * 100.0)
                    newCargoP = int(newCargo * 100)
                    cargoText = ''
                    if diffCargo == 0:
                        cargoText = ''
                    if diffCargo >= 0:
                        cargoText = '\x01green\x01+%s%%\x02' % diffCargo
                        signCargo = '+'
                    cargoText = '\x01red\x01%s%%\x02' % diffCargo
                    signCargo = ''
            cargoIconLine = '\x05dtl-cargo\x05 '
            cargoLine = cargoIconLine + '%s: %s%% %s\n\n' % (PLocalizer.ShipUpgradeAttributeCargo, newCargoP, cargoText)
            if hullInfo.get('BroadsideType', 0):
                broadsideType = hullInfo.get('BroadsideType')
                broadsideAmount = int(hullInfo.get('BroadsideAmount') * 100)
                broadsideName = PLocalizer.InventoryTypeNames.get(broadsideType, 'Error')
                broadsideIconLine = '\x05broadside-%s\x05 ' % broadsideType
                broadsideLine = broadsideIconLine + PLocalizer.ShipBroadsideInfo % (broadsideAmount, broadsideName) + '\n'
        else:
            self.attributeString = 'No Attribute Data!'
        self.attributeString = headingLine + '\n\n' + armorLine + speedLine + turningLine + cargoLine + broadsideLine
        return

    def filloutAttributeText(self):
        self.attributeList['text'] = self.attributeString + ' '
        attribList = self.attributeList.component('text0').textNode.getWordwrappedText().split('\n')
        ownedText = ''
        for line in attribList:
            ownedText += '\n'

        self.attributeList['text'] = self.attributeString + '\n\n' + self.costString
        self.ownedResourceList['text'] = ownedText + '\n' + self.ownedString

    def previewChange(self, shipId, changeCat=None, changeValue=None, downgrade=False, sidegrade=False):
        if self.confirmPanel:
            return
        shipOV = base.cr.getOwnerView(self.shipId)
        hullMaterial = None
        sailMaterial = None
        sailPattern = None
        invertLogo = False
        logo = ShipGlobals.Logos.Undefined
        shipClass = shipOV.shipClass
        self.previewValue = changeValue
        self.previewCat = changeCat
        self.viewingDowngrade = downgrade
        self.viewingSidegrade = sidegrade
        hullType = max(shipOV.customHull, 1)
        oldHullType = hullType
        riggingType = max(shipOV.customRigging, 1)
        oldRiggingType = riggingType
        patternType = max(shipOV.customSailPattern, 1)
        oldPatternType = patternType
        logoType = max(shipOV.customSailLogo, 1)
        oldLogoType = logoType
        if changeCat == 0:
            if not changeValue:
                changeValue = oldHullType
            hullType = changeValue
            hullInfo = ShipUpgradeGlobals.HULL_TYPES.get(hullType)
            oldHullInfo = ShipUpgradeGlobals.HULL_TYPES.get(oldHullType)
            if oldHullType != hullType:
                self.viewingCurrent = False
                self.previewTitle['text'] = hullInfo.get('Name', 'No Name')
                self.filloutCosts(shipClass, hullInfo.get('Cost', None))
                self.filloutOwned()
                self.filloutHullDetails(hullInfo, oldHullInfo)
                self.filloutAttributeText()
            else:
                self.viewingCurrent = True
                self.previewTitle['text'] = hullInfo.get('Name', 'No Name')
                self.filloutCosts(shipClass)
                self.filloutOwned()
                self.filloutHullDetails(None, oldHullInfo)
                self.filloutAttributeText()
        else:
            if changeCat == 1:
                if not changeValue:
                    changeValue = oldRiggingType
                riggingType = changeValue
                riggingInfo = ShipUpgradeGlobals.RIGGING_TYPES.get(riggingType)
                oldRiggingInfo = ShipUpgradeGlobals.RIGGING_TYPES.get(oldRiggingType)
                if oldRiggingType != riggingType:
                    self.viewingCurrent = False
                    self.previewTitle['text'] = riggingInfo.get('Name', 'No Name')
                    self.filloutCosts(shipClass, riggingInfo.get('Cost', None))
                    self.filloutOwned()
                    self.filloutRiggingDetails(riggingInfo, oldRiggingInfo)
                    self.filloutAttributeText()
                else:
                    self.viewingCurrent = True
                    self.previewTitle['text'] = riggingInfo.get('Name', 'No Name')
                    self.filloutCosts(shipClass)
                    self.filloutOwned()
                    self.filloutRiggingDetails(None, oldRiggingInfo)
                    self.filloutAttributeText()
            else:
                if changeCat == 2:
                    if not changeValue:
                        changeValue = oldPatternType
                    patternType = changeValue
                    patternInfo = ShipUpgradeGlobals.SAILCOLOR_TYPES.get(patternType)
                    oldPatternInfo = ShipUpgradeGlobals.RIGGING_TYPES.get(oldPatternType)
                    if oldPatternType != patternType:
                        self.viewingCurrent = False
                        self.previewTitle['text'] = patternInfo.get('Name', 'No Name')
                        self.filloutCosts(shipClass, patternInfo.get('Cost', None))
                        self.filloutOwned()
                        self.filloutPatternDetails(patternInfo, oldPatternInfo)
                        self.filloutAttributeText()
                    else:
                        self.viewingCurrent = True
                        self.previewTitle['text'] = patternInfo.get('Name', 'No Name')
                        self.filloutCosts(shipClass)
                        self.filloutOwned()
                        self.filloutPatternDetails(None, oldPatternInfo)
                        self.filloutAttributeText()
                else:
                    if changeCat == 3:
                        if not changeValue:
                            changeValue = oldLogoType
                        logoType = changeValue
                        logoInfo = ShipUpgradeGlobals.LOGO_TYPES.get(logoType)
                        if oldLogoType != logoType:
                            self.viewingCurrent = False
                            self.previewTitle['text'] = logoInfo.get('Name', 'No Name')
                            self.filloutCosts(shipClass, logoInfo.get('Cost', None))
                            self.filloutOwned()
                            self.filloutAttributeText()
                        else:
                            self.viewingCurrent = True
                            self.previewTitle['text'] = logoInfo.get('Name', 'No Name')
                            self.filloutCosts(shipClass)
                            self.filloutOwned()
                            self.filloutAttributeText()
                    else:
                        self.viewingCurrent = False
                        self.previewTitle['text'] = ''
                    if downgrade:
                        self.tooExpensive = False
                    self.checkConfirmButtonState()
                    hullInfo = ShipUpgradeGlobals.HULL_TYPES.get(hullType)
                    if hullInfo:
                        hullMaterial = hullInfo['StyleIndex']
                    riggingInfo = ShipUpgradeGlobals.RIGGING_TYPES.get(riggingType)
                    if riggingInfo:
                        sailMaterial = riggingInfo['StyleIndex']
                patternInfo = ShipUpgradeGlobals.SAILCOLOR_TYPES.get(patternType)
                if patternInfo:
                    sailPattern = patternInfo['StyleIndex']
            logoInfo = ShipUpgradeGlobals.LOGO_TYPES.get(logoType)
            if logoInfo:
                logo = logoInfo['StyleIndex']
                invertLogo = logoInfo['Invert']
        self.previewShip(shipOV.shipClass, hullMaterial=hullMaterial, sailMaterial=sailMaterial, sailPattern=sailPattern, logo=logo, invertLogo=invertLogo)
        return

    def handleShipChanged(self):
        self.previewValue = None
        self.setShip(0, self.shipId, changed=1)
        return

    def previewShip(self, shipType, hullMaterial=None, sailMaterial=None, sailPattern=None, logo=None, invertLogo=False):
        self.clearShip()
        self.ship = base.shipFactory.getShip(shipType, hullMaterial=hullMaterial, sailMaterial=sailMaterial, sailPattern=sailPattern, logo=logo, invertLogo=invertLogo)
        self.shipModel = self.ship.modelRoot
        self.shipModel.setTransparency(TransparencyAttrib.MBinary, 1)
        self.ship.forceLOD(0)
        self.shipModel.setScale(0.0023)
        self.shipModel.setPos(0.15, 0.0, -0.15)
        self.shipModel.setH(110)
        self.shipModel.reparentTo(self)
        self.shipModel.setDepthTest(1)
        self.shipModel.setDepthWrite(1)
        self.ship.instantSailing()
        self.fixShipPR()
        self.stripShip()

    def setShip(self, shipIndex=0, shipId=None, changed=0):
        if shipId == None:
            shipIdList = localAvatar.getInventory().getShipDoIdList()
            shipId = shipIdList[shipIndex]
        if self.shipId != shipId or changed:
            if self.ship:
                self.ship.cleanup()
                self.ship = None
            self.ignore('ShipChanged-%s' % self.shipId)
            self.shipId = shipId
        if self.ship == None and self.shipId:
            shipOV = base.cr.getOwnerView(self.shipId)
            hullMaterial = None
            sailMaterial = None
            sailPattern = None
            invertLogo = False
            logo = ShipGlobals.Logos.Undefined
            if shipOV.customHull:
                hullType = ShipUpgradeGlobals.HULL_TYPES.get(shipOV.customHull)
                if hullType:
                    hullMaterial = hullType['StyleIndex']
            if shipOV.customRigging:
                riggingType = ShipUpgradeGlobals.RIGGING_TYPES.get(shipOV.customRigging)
                if riggingType:
                    sailMaterial = riggingType['StyleIndex']
            if shipOV.customSailPattern:
                patternType = ShipUpgradeGlobals.SAILCOLOR_TYPES.get(shipOV.customSailPattern)
                if patternType:
                    sailPattern = patternType['StyleIndex']
            if shipOV.customSailLogo:
                logoType = ShipUpgradeGlobals.LOGO_TYPES.get(shipOV.customSailLogo)
                if logoType:
                    logo = logoType['StyleIndex']
                    invertLogo = logoType['Invert']
            self.clearButtons()
            self.previewValue = None
            self.layoutButtons(self.previewCat)
            self.previewShip(shipOV.shipClass, hullMaterial=hullMaterial, sailMaterial=sailMaterial, sailPattern=sailPattern, logo=logo, invertLogo=invertLogo)
            self.previewChange(shipId, changeCat=self.previewCat, changeValue=self.previewValue)
            self.accept('ShipChanged-%s' % self.shipId, self.handleShipChanged)
        return

    def confirmPurchase(self):
        if self.confirmPanel:
            return
        if self.waitingForUpgrade:
            return
        if self.previewCat != None and self.previewValue != None:
            if not Freebooter.getPaidStatus(localAvatar.getDoId()):
                localAvatar.guiMgr.showNonPayer()
            else:
                if self.viewingDowngrade:
                    self.confirmPanel = ShipUpgradeConfirm.ShipUpgradeConfirm(PLocalizer.ShipUpgradeConfirmTitleDown, PLocalizer.ShipUpgradeConfirmAskDown, self.panelConfirmOkay, self.panelConfirmCancel)
                elif self.viewingSidegrade:
                    self.confirmPanel = ShipUpgradeConfirm.ShipUpgradeConfirm(PLocalizer.ShipUpgradeConfirmTitleSide, PLocalizer.ShipUpgradeConfirmAskSide, self.panelConfirmOkay, self.panelConfirmCancel)
                else:
                    self.confirmPanel = ShipUpgradeConfirm.ShipUpgradeConfirm(PLocalizer.ShipUpgradeConfirmTitle, PLocalizer.ShipUpgradeConfirmAsk, self.panelConfirmOkay, self.panelConfirmCancel)
                self.confirmPanel.reparentTo(self)
                self.confirmPanel.setPos(0, 0, -0.2)
        return

    def panelConfirmOkay(self):
        localAvatar.sendUpdate('requestShipUpgrade', [self.shipId, self.previewCat, self.previewValue])
        self.waitingForUpgrade = True
        self.checkConfirmButtonState()
        self.acceptOnce('ShipUpgraded', self.handleAckUpgrade)

    def panelConfirmCancel(self):
        pass

    def handleAckUpgrade(self, shipId=None, retCode=None):
        self.waitingForUpgrade = False
        self.checkConfirmButtonState()

    def checkConfirmButtonState(self):
        paidStatus = Freebooter.getPaidStatus(localAvatar.getDoId())
        self.confirmButton['text_scale'] = PiratesGuiGlobals.TextScaleLarge
        if self.waitingForUpgrade or self.viewingCurrent or self.tooExpensive:
            self.confirmButton['state'] = DGG.DISABLED
            if self.waitingForUpgrade:
                self.confirmButton['text'] = PLocalizer.UpgradePurchaseWait
                self.confirmButton['text_fg'] = PiratesGuiGlobals.TextFG3
            elif self.viewingCurrent:
                self.confirmButton['text'] = PLocalizer.UpgradePurchaseCurrent
                self.confirmButton['text_fg'] = PiratesGuiGlobals.TextFG3
            elif self.tooExpensive:
                self.confirmButton['text'] = PLocalizer.UpgradePurchasePoor
                self.confirmButton['text_fg'] = PiratesGuiGlobals.TextFG6
        else:
            self.confirmButton['state'] = DGG.NORMAL
            self.confirmButton['text_scale'] = PiratesGuiGlobals.TextScaleExtraLarge
            if not paidStatus:
                self.confirmButton['text'] = PLocalizer.UpgradePurchaseUnlimitedOnly
                self.confirmButton['text_fg'] = PiratesGuiGlobals.TextFG1
            elif self.viewingDowngrade:
                self.confirmButton['text'] = PLocalizer.UpgradePurchaseDowngrade
                self.confirmButton['text_fg'] = PiratesGuiGlobals.TextFG6
            elif self.viewingSidegrade:
                self.confirmButton['text_scale'] = PiratesGuiGlobals.TextScaleLarge
                self.confirmButton['text'] = PLocalizer.UpgradePurchaseSidegrade
                self.confirmButton['text_fg'] = PiratesGuiGlobals.TextFG1
            else:
                self.confirmButton['text'] = PLocalizer.UpgradePurchaseConfirm
                self.confirmButton['text_fg'] = PiratesGuiGlobals.TextFG1

    def onOpen(self, shipId=None, callback=None):
        self.setShip(shipId=shipId)
        self.updateCurrencyLabels()
        if callback:
            self.callback = callback
        self.accept('escape', self.close)
        for currencyId in ShipUpgradeGlobals.COST_LIST:
            if currencyId == InventoryType.ItemTypeMoney:
                self.accept(InventoryGlobals.getCategoryChangeMsg(localAvatar.getInventoryId(), InventoryType.ItemTypeMoney), self.updateCurrencyLabels)
            else:
                self.accept('inventoryQuantity-%s-%s' % (localAvatar.getInventoryId(), currencyId), self.updateCurrencyLabels)

        self.accept('mouse1', self.testStartDrag)
        self.accept('mouse1-up', self.endDrag)

    def testStartDrag(self, messageData=None):
        self.mouseXPos = None
        taskMgr.add(self.doShipDrag, 'shipUpgradeInterfaceDrag')
        return

    def doShipDrag(self, task=None):
        oldPos = self.mouseXPos
        self.mouseXPos = base.mouseWatcherNode.getMouseX()
        if oldPos != None:
            shipRot = (self.mouseXPos - oldPos) * 40.0
            if self.shipModel:
                oldH = self.shipModel.getH()
                newH = oldH + shipRot
                newH = max(min(newH, 150), 45)
                self.shipModel.setH(newH)
                self.fixShipPR()
        if task:
            return task.cont
        return

    def endDrag(self, messageData=None):
        taskMgr.remove('shipUpgradeInterfaceDrag')

    def fixShipPR(self):
        shipH = self.shipModel.getH()
        side = 90.0 - shipH
        self.shipModel.setP(-5.0)
        self.shipModel.setR(side * 0.25)

    def clearShip(self):
        if self.ship:
            self.ship.cleanup()
            self.ship = None
        return

    def clearButtons(self):
        for button in self.choiceButtons:
            button.remove()

        self.choiceButtons = []

    def close(self):
        self.onClose()
        self.hide()
        localAvatar.guiMgr.closeShipUpgrades()

    def onClose(self):
        self.endDrag()
        if self.confirmPanel:
            self.panelConfirmCancel()
            self.confirmPanel.destroy()
            self.confirmPanel = None
        self.clearShip()
        self.clearButtons()
        if self.callback:
            self.callback()
        self.ignore('escape')
        self.ignore('mouse1')
        self.ignore('mouse1-up')
        for currencyId in ShipUpgradeGlobals.COST_LIST:
            if currencyId == InventoryType.ItemTypeMoney:
                self.ignore(InventoryGlobals.getCategoryChangeMsg(localAvatar.getInventoryId(), InventoryType.ItemTypeMoney))
            else:
                self.ignore('inventoryQuantity-%s-%s' % (localAvatar.getInventoryId(), currencyId))

        return

    def stripShip(self):
        self.stripAttribs(self.shipModel, CullBinAttrib)

    def stripAttribs(self, geom, cls):
        ShipBlueprints.stripAttribs(geom, cls)