from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task.Task import Task
from direct.interval.IntervalGlobal import *
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesgui import InventoryPage
from pirates.pirate import TitleGlobals
from pirates.uberdog.DistributedInventoryBase import DistributedInventoryBase
from pirates.ship import ShipGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesgui import GuiTray
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import GuiButton
from direct.gui import DirectButton
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.piratesgui import BorderFrame
from pirates.piratesbase import Freebooter
from pirates.inventory import InventoryGlobals

class TitlePanel(DirectFrame):

    def __init__(self, parent, titleId, position, panelIndex, titlesPage, defaultOnLand=0, defaultOnSea=0):
        DirectFrame.__init__(self, parent, pos=position)
        self.iconModel = loader.loadModel(TitleGlobals.getModelPath(titleId))
        tempModel = loader.loadModel('models/textureCards/skillIcons')
        self.titleId = titleId
        self.rank = 1
        self.maxRank = 1
        self.expPoints = 241
        self.expBase = 150
        self.expTarget = 400
        self.landActive = defaultOnLand
        self.seaActive = defaultOnSea
        self.panelIndex = panelIndex
        self.titlesPage = titlesPage
        self.booleanTitle = TitleGlobals.isBooleanTitle(self.titleId)
        topgui = loader.loadModel('models/gui/toplevel_gui')
        self.titleNameFrame = BorderFrame.BorderFrame(parent=self, relief=None, pos=(0.12,
                                                                                     0,
                                                                                     0.01), frameSize=(-0.15, 0.5, -0.15, 0.03), modelName='pir_m_gui_frm_subframe', imageColorScale=VBase4(0.75, 0.75, 0.9, 0.75), text=TitleGlobals.getTitleRankName(self.titleId, self.expPoints), text_align=TextNode.ALeft, text_scale=0.035, text_pos=(0, -0.02), text_fg=PiratesGuiGlobals.TextFG1, text_wordwrap=15, text_shadow=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                                                                                                                                                                          1), textMayChange=1, text_font=PiratesGlobals.getInterfaceFont())
        self.titleDescFrame = DirectFrame(parent=self, relief=None, pos=(0.125, 0, -0.095), text=TitleGlobals.getTitleDesc(self.titleId), text_align=TextNode.ALeft, text_scale=0.03, text_pos=(0, -0.01), text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=15, text_shadow=(0,
                                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                                             0,
                                                                                                                                                                                                                                                                             1), textMayChange=0, text_font=PiratesGlobals.getInterfaceFont())
        shipcard = loader.loadModel('models/gui/ship_battle')
        tex = shipcard.find('**/ship_battle_speed_bar*')
        self.expFrame = DirectFrame(parent=self, pos=(0.36, 0, -0.05), relief=None, image=tex, image_scale=(0.23,
                                                                                                            1,
                                                                                                            0.5), scale=(1.48,
                                                                                                                         1,
                                                                                                                         1.2))
        self.expMeter = DirectWaitBar(parent=self.expFrame, relief=DGG.RAISED, borderWidth=(0.004,
                                                                                            0.004), range=100, value=50, frameColor=(0,
                                                                                                                                     0,
                                                                                                                                     0,
                                                                                                                                     0), barColor=(223 / 255.0, 137 / 255.0, 28 / 255.0, 1), frameSize=(-0.222, 0.084, -0.012, 0.012), pos=(0.069,
                                                                                                                                                                                                                                            0,
                                                                                                                                                                                                                                            0.0))
        self.expMeterText = DirectFrame(parent=self, relief=None, pos=(0.6, 0, 0.0), text='%s / %s' % (self.expBase, self.expTarget), text_align=TextNode.ARight, text_scale=0.03, text_pos=(0, -0.01), text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=15, text_shadow=(0,
                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                                                          1), textMayChange=1, text_font=PiratesGlobals.getInterfaceFont())
        if self.booleanTitle:
            self.expFrame.hide()
            self.expMeterText.hide()
        imgScale = TitleGlobals.getScale(self.titleId)
        self.iconFrame = GuiButton.GuiButton(parent=self, pos=(0.04, 0, -0.05), helpText=TitleGlobals.getTitleName(self.titleId), helpPos=(-0.26, 0, 0.08), relief=None, image=self.iconModel.find('**/' + TitleGlobals.getIconName(self.titleId, 1)), image_scale=(0.15 * imgScale, 1, 0.15 * imgScale))
        self.landButton = DirectButton.DirectButton(parent=self, pos=(0.71, 0, -0.05), relief=None, scale=0.22, image_color=VBase4(0.75, 0.85, 1.0, 1.0), image=(topgui.find('**/pir_t_gui_frm_base_circle_over'), topgui.find('**/pir_t_gui_frm_base_circle'), topgui.find('**/pir_t_gui_frm_base_circle_over'), topgui.find('**/pir_t_gui_frm_base_circle')), command=self.selectLandBadge, extraArgs=[self.panelIndex])
        self.titlesPage.landButtons.append(self.landButton)
        self.seaButton = DirectButton.DirectButton(parent=self, pos=(0.87, 0, -0.05), relief=None, scale=0.22, image_color=VBase4(0.75, 0.85, 1.0, 1.0), image=(topgui.find('**/pir_t_gui_frm_base_circle_over'), topgui.find('**/pir_t_gui_frm_base_circle'), topgui.find('**/pir_t_gui_frm_base_circle_over'), topgui.find('**/pir_t_gui_frm_base_circle')), command=self.selectSeaBadge, extraArgs=[self.panelIndex])
        self.titlesPage.seaButtons.append(self.seaButton)
        return

    def refresh(self):
        inv = localAvatar.getInventory()
        origRank = self.rank
        if inv:
            invType = TitleGlobals.getInventoryType(self.titleId)
            if self.titleId == TitleGlobals.ShipPVPTitle:
                self.expPoints = localAvatar.getInventory().getStackQuantity(InventoryType.PVPTotalInfamySea)
            elif self.titleId == TitleGlobals.LandPVPTitle:
                self.expPoints = localAvatar.getInventory().getStackQuantity(InventoryType.PVPTotalInfamyLand)
            elif invType:
                self.expPoints = inv.getStackQuantity(invType)
            else:
                self.expPoints = 0
                if self.titleId == TitleGlobals.FounderTitle and localAvatar.getFounder():
                    self.expPoints = 1
            self.rank = TitleGlobals.getRank(self.titleId, self.expPoints)
            self.maxRank = TitleGlobals.getMaxRank(self.titleId)
            self.expTarget = TitleGlobals.getBreakpoints(self.titleId)[min(self.rank + 1, self.maxRank)]
            self.expBase = TitleGlobals.getBreakpoints(self.titleId)[self.rank]
        if self.titleNameFrame:
            self.titleNameFrame['text'] = TitleGlobals.getTitleRankName(self.titleId, self.expPoints)
        if self.expMeter:
            value = 0
            if self.rank < self.maxRank and self.expTarget - self.expBase > 0:
                value = int((self.expPoints - self.expBase) * 100 / (self.expTarget - self.expBase))
            self.expMeter['value'] = value
        if self.expMeterText:
            if self.rank >= self.maxRank:
                self.expBase = 0
                self.expTarget = 0
            text = '0 / 0'
            if self.rank < self.maxRank and self.expTarget - self.expBase > 0:
                text = '%s / %s' % (self.expPoints - self.expBase, self.expTarget - self.expBase)
            self.expMeterText['text'] = text
        if self.iconFrame:
            icName = TitleGlobals.getIconName(self.titleId, self.rank)
            if icName:
                img = self.iconModel.find('**/' + icName)
            else:
                img = None
            self.iconFrame['image'] = img
            imgScale = TitleGlobals.getScale(self.titleId)
            self.iconFrame['image_scale'] = (0.065 * imgScale, 1, 0.065 * imgScale)
        titleOnOff = [
         PLocalizer.TitleOff, PLocalizer.TitleOn]
        if self.rank != origRank:
            if self.landActive:
                self.titlesPage.setLandActive(self.panelIndex, self.landActive)
            if self.seaActive:
                self.titlesPage.setSeaActive(self.panelIndex, self.seaActive)
        if self.rank == 0 or not Freebooter.getPaidStatus(localAvatar.doId):
            self.landButton.hide()
            self.seaButton.hide()
        else:
            self.landButton.show()
            self.seaButton.show()
        return

    def destroy(self):
        self.buttonImageBack = None
        self.buttonImageCoin = None
        if self.titleNameFrame:
            self.titleNameFrame.destroy()
            self.titleNameFrame = None
        if self.expFrame:
            self.expFrame.destroy()
            self.expFrame = None
        if self.expMeterText:
            self.expMeterText.destroy()
            self.expMeterText = None
        if self.iconFrame:
            self.iconFrame.destroy()
            self.iconFrame = None
        if self.titleDescFrame:
            self.titleDescFrame.destroy()
            self.titleDescFrame = None
        DirectFrame.destroy(self)
        return

    def selectLandBadge(self, badgeIndex):
        self.landButton['state'] = DGG.DISABLED
        self.titlesPage.setLandBadge(badgeIndex)

    def selectSeaBadge(self, badgeIndex):
        self.seaButton['state'] = DGG.DISABLED
        self.titlesPage.setSeaBadge(badgeIndex)


class TitlesPage(InventoryPage.InventoryPage):

    def __init__(self):
        InventoryPage.InventoryPage.__init__(self)
        self.initialiseoptions(TitlesPage)
        self.titles = []
        self.selectedLandIndex = -1
        self.selectedSeaIndex = -1
        self.landButtons = []
        self.seaButtons = []
        self.forceInitLand = -1
        self.forceInitSea = -1
        self.loaded = 0
        self.opened = 0
        gui = loader.loadModel('models/gui/gui_main')
        scale = 0.335
        self.background = self.attachNewNode('background')
        self.background.setScale(scale)
        self.background.setPos(0.53, 0, 0.74)
        gui.find('**/gui_inv_red_general1').copyTo(self.background)
        PiratesGlobals.flattenOrdered(self.background)
        self.displayTitleFrame = DirectFrame(parent=self, relief=None, pos=(0.55, 0,
                                                                            1.175), text=PLocalizer.DisplayTitle, text_align=TextNode.ALeft, text_scale=0.045, text_pos=(-0.45, 0.05), text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=20, text_shadow=(0,
                                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                                         0,
                                                                                                                                                                                                                                                         1), textMayChange=1, text_font=PiratesGlobals.getInterfaceFont())
        self.displayTitleLandFrame = BorderFrame.BorderFrame(parent=self, relief=None, pos=(0.81,
                                                                                            0,
                                                                                            1.02), frameSize=(-0.05, 0.05, -0.26, -0.08), modelName='pir_m_gui_frm_subframe', imageColorScale=VBase4(0.75, 0.75, 0.9, 0.75), text=PLocalizer.DisplayTitleLand, text_align=TextNode.ACenter, text_scale=0.032, text_pos=(0, -0.01), text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=15, text_shadow=(0,
                                                                                                                                                                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                                                                                                                                                                     0,
                                                                                                                                                                                                                                                                                                                                                                                                     1), textMayChange=0, text_font=PiratesGlobals.getInterfaceFont())
        self.displayTitleSeaFrame = BorderFrame.BorderFrame(parent=self, relief=None, pos=(0.97,
                                                                                           0,
                                                                                           1.02), frameSize=(-0.05, 0.05, -0.26, -0.08), modelName='pir_m_gui_frm_subframe', imageColorScale=VBase4(0.75, 0.75, 0.9, 0.75), text=PLocalizer.DisplayTitleSea, text_align=TextNode.ACenter, text_scale=0.032, text_pos=(0, -0.01), text_fg=PiratesGuiGlobals.TextFG2, text_wordwrap=15, text_shadow=(0,
                                                                                                                                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                                                                                                                                   1), textMayChange=0, text_font=PiratesGlobals.getInterfaceFont())
        self.dummyFrame = DirectFrame(parent=self, relief=None, pos=(0.1, 0, 0.89))
        self.accept('LocalAvatarInfamyUpdated', self.refresh)
        self.accept('landBadgeSet', self.updateLandBadge)
        self.accept('seaBadgeSet', self.updateSeaBadge)
        return

    def destroy(self):
        self.ignoreAll()
        if self.displayTitleFrame:
            self.displayTitleFrame.destroy()
            self.displayTitleFrame = None
        if self.displayTitleLandFrame:
            self.displayTitleLandFrame.destroy()
            self.displayTitleLandFrame = None
        if self.displayTitleSeaFrame:
            self.displayTitleSeaFrame.destroy()
            self.displayTitleSeaFrame = None
        if self.background:
            self.background.removeNode()
            self.background = None
        for button in self.landButtons:
            button.destroy()

        self.landButtons = []
        for button in self.seaButtons:
            button.destroy()

        self.seaButtons = []
        if self.titles:
            for panel in self.titles:
                panel.destroy()

        self.titles = None
        self.loaded = 0
        InventoryPage.InventoryPage.destroy(self)
        return

    def show(self):
        self.refresh()
        InventoryPage.InventoryPage.show(self)
        self.updateChecks()

    def updateLandBadge(self, titleId, rank):
        self.updateChecks()

    def updateSeaBadge(self, titleId, rank):
        self.updateChecks()

    def updateChecks(self):
        for landButton in self.landButtons:
            landButton['state'] = DGG.NORMAL
            landButton['geom'] = None

        for seaButton in self.seaButtons:
            seaButton['state'] = DGG.NORMAL
            seaButton['geom'] = None

        landIndex = -1
        seaIndex = -1
        if localAvatar.badge:
            landIndex = localAvatar.badge[0] - 1
        if localAvatar.shipBadge:
            seaIndex = localAvatar.shipBadge[0] - 1
        if landIndex >= 0 and landIndex < len(self.landButtons):
            self.landButtons[landIndex]['geom'] = loader.loadModel('models/gui/toplevel_gui').find('**/treasure_w_coin*')
            self.landButtons[landIndex]['geom_scale'] = 0.8
        if seaIndex >= 0 and seaIndex < len(self.seaButtons):
            self.seaButtons[seaIndex]['geom'] = loader.loadModel('models/gui/toplevel_gui').find('**/treasure_w_coin*')
            self.seaButtons[seaIndex]['geom_scale'] = 0.8
        return

    def updateText(self):
        tText = PLocalizer.DisplayTitle
        if not Freebooter.getPaidStatus(localAvatar.doId):
            tText = PLocalizer.DisplayTitleFree
        self.displayTitleFrame['text'] = tText

    def refresh(self, amount=0):
        if not self.loaded:
            self.loadGui()
        for panel in self.titles:
            panel.refresh()

        self.updateText()
        self.updateChecks()
        self.accept('LocalBadgeChanged', self.infamyUpdate)

    def infamyUpdate(self, task=None):
        self.refresh()

    def hide(self):
        InventoryPage.InventoryPage.hide(self)

    def loadGui(self):
        count = 0
        for key in TitleGlobals.TitlesDict.keys():
            if not self.shouldShowTitle(key):
                continue
            yPos = 0.01 - count * 0.2
            forceLandOn = 0
            forceSeaOn = 0
            panel = TitlePanel(self.dummyFrame, key, (0, 0, yPos), count, self, forceLandOn, forceSeaOn)
            self.titles.append(panel)
            count += 1

        self.displayTitleLandFrame['frameSize'] = self.displayTitleSeaFrame['frameSize'] = (
         -0.05, 0.05, -0.26 - 0.2 * (count - 1), -0.08)
        self.loaded = 1

    def shouldShowTitle(self, titleId):
        if titleId == TitleGlobals.FounderTitle and not localAvatar.getFounder():
            return 0
        elif titleId == TitleGlobals.ShipPVPTitle and not base.config.GetBool('want-sea-infamy', 0):
            return 0
        elif titleId == TitleGlobals.LandPVPTitle and not base.config.GetBool('want-land-infamy', 0):
            return 0
        return 1

    def setLandBadge(self, badgeIndex):
        landIndex = 0
        if localAvatar.badge:
            landIndex = localAvatar.badge[0]
        titlePanel = self.titles[badgeIndex]
        if landIndex == titlePanel.titleId:
            localAvatar.sendRequestSetBadgeIcon(-1, -1)
        else:
            localAvatar.sendRequestSetBadgeIcon(titlePanel.titleId, titlePanel.rank)

    def setSeaBadge(self, badgeIndex):
        seaIndex = 0
        if localAvatar.shipBadge:
            seaIndex = localAvatar.shipBadge[0]
        titlePanel = self.titles[badgeIndex]
        if seaIndex == titlePanel.titleId:
            localAvatar.sendRequestSetShipBadgeIcon(-1, -1)
        else:
            localAvatar.sendRequestSetShipBadgeIcon(titlePanel.titleId, titlePanel.rank)